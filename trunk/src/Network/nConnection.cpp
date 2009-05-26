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

    connect(tcpSocket, SIGNAL(readyRead()), this, SLOT(readData()));
}


void nConnection::sendData(QByteArray out)
{
    if(tcpSocket->write(out) != out.length())
        cout << "not all bytes were sent" << endl;
}

void nConnection::setHandle(QString handle)
{
    this->handle = handle;
}

QString nConnection::getHandle()
{
    return handle;
}

void nConnection::disconnectConnections()
{
    tcpSocket->disconnectFromHost();
}

void nConnection::readData()
{
    QByteArray data = tcpSocket->readAll();
    emit newData(data, this);
}
