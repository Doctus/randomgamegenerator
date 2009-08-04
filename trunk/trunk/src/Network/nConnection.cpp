/*
Random Game Generator - The generation of time transcending tabletop games!
Copyright (C) 2009 Michael de Lang

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/


#include "nConnection.h"

nConnection::nConnection(QTcpSocket *tcpSocket)
{
    this->tcpSocket = tcpSocket;
    handle = "";
    properlyConnected = false;

    connect(tcpSocket, SIGNAL(readyRead()), this, SLOT(readData()));
    connect(tcpSocket, SIGNAL(disconnected()), this, SLOT(disconnectedSlot()));
}


void nConnection::sendData(QString data)
{
     QByteArray block;
     qint64 bytesSent = 0;
     QDataStream out(&block, QIODevice::ReadWrite);
     out.setVersion(QDataStream::Qt_4_5);
     out << (quint16)0;
     //out << qCompress(data.toUtf8(), 9);
     out << data;
     out.device()->seek(0);
     out << (quint16)(block.size() - sizeof(quint16));
    if((bytesSent = tcpSocket->write(block)) != block.length())
        cout << "not all bytes were sent, " << bytesSent << " opposed to " << data.length() + sizeof(quint16) << endl;

    //cout << "Sending \"" << QString::fromUtf8(block).toStdString() << "\"" << endl;
}

void nConnection::setHandle(QString handle)
{
    this->handle = handle;
}

QString nConnection::getHandle()
{
    return handle;
}

bool nConnection::getProperlyConnected()
{
    return properlyConnected;
}

void nConnection::setProperlyConnected(bool pc)
{
    properlyConnected = pc;
}

void nConnection::disconnectConnections()
{
    tcpSocket->disconnectFromHost();
}

void nConnection::readData()
{
    /*while(tcpSocket->canReadLine())
    {
        QByteArray data = tcpSocket->readLine(tcpSocket->bytesAvailable());
        emit newData(data, this);
    }*/

    QDataStream in(tcpSocket);
    static quint16 blockSize;
    in.setVersion(QDataStream::Qt_4_5);

    while(!in.atEnd())
    {
        if (blockSize == 0 && tcpSocket->bytesAvailable() < (int)sizeof(quint16))
        {
            //cout << "No size sent?" << endl;
            return;
        }

        if(blockSize == 0)
            in >> blockSize;

        if (tcpSocket->bytesAvailable() < blockSize)
        {
            //cout << "Blocksize not met" << endl;
            return;
        }

        /*QByteArray message; //message length is done by QDataStream automatically. Serializing ftw?
        in >> message;
        message = qUncompress(message);*/

        QString message;
        in >> message;

        //cout << "Received \"" << message.toStdString() << "\"" << endl;

        if(!message.isEmpty() && !message.isNull())
            emit newData(message.toUtf8(), this);
        blockSize = 0;
    }

}

void nConnection::disconnectedSlot()
{
    emit disconnected(this);
}
