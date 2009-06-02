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


#include "nConnectionManager.h"

nConnectionManager::nConnectionManager(QWidget *parent) : QObject(parent)
{
    connected = 0;

    tcpServer = new QTcpServer(this);

    connect(&pingTimer , SIGNAL(timeout()), this, SLOT(ping()));
    pingTimer.setInterval(5000);
}

/*
 * Can't be hosting a server and connect to somewhere at the same time. So it checks for connected to not equal 2(server)
 * and if not, it sets connected to 1(client)
 */
void nConnectionManager::connectTo(QString host, uint port)
{
    if(connected == 2)
    {
        QMessageBox warningDialog((QWidget*)parent());
        warningDialog.setText("You can't be hosting and being connected to a host at the same time. Continueing will disconnect your current connection.");
        warningDialog.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
        warningDialog.setDefaultButton(QMessageBox::Cancel);
        int ret = warningDialog.exec();

        if(ret == QMessageBox::Cancel)
            return;

        disconnectConnections();
    }
    else if(connected == 1)
    {
        QMessageBox warningDialog((QWidget*)parent());
        warningDialog.setText("You're already connected. Continueing will disconnect your current connection.");
        warningDialog.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
        warningDialog.setDefaultButton(QMessageBox::Cancel);
        int ret = warningDialog.exec();

        if(ret == QMessageBox::Cancel)
            return;

        disconnectConnections();
    }

    QTcpSocket *sock = new QTcpSocket(this);

    connect(sock, SIGNAL(error(QAbstractSocket::SocketError)), this, SLOT(failedConnectionSlot(QAbstractSocket::SocketError)));
    connect(sock, SIGNAL(connected()), this, SLOT(succeededConnectionSlot()));
    connect(sock, SIGNAL(disconnected()), this, SLOT(disconnectedSlot()));

    mConnections.append(new nConnection(sock));

    sock->connectToHost(host, port);
}

/*
 * Can't be hosting a server and connect to somewhere at the same time. So it checks for connected to not equal 1(client)
 * and if not, it sets connected to 2(server)
 */
void nConnectionManager::startServer(uint port)
{
    if(connected == 1)
    {
        QMessageBox warningDialog((QWidget*)parent());
        warningDialog.setText("You can't be hosting and being connected to a host at the same time. Continueing will disconnect your current connection.");
        warningDialog.setStandardButtons(QMessageBox::Ok | QMessageBox::Cancel);
        warningDialog.setDefaultButton(QMessageBox::Cancel);
        int ret = warningDialog.exec();

        if(ret == QMessageBox::Cancel)
            return;

        disconnectConnections();
    }
    else if(connected == 2)
    {
        QMessageBox errorDialog((QWidget*)parent());
        errorDialog.setText("You are already hosting!");
        errorDialog.exec();
        return;
    }

    if(!tcpServer->listen(QHostAddress::Any, port))
    {
        QMessageBox errorDialog((QWidget*)parent());
        errorDialog.setText("The server could not be started on port ");
        errorDialog.exec();
        return;
    }

    pingTimer.start();
    connected = 2;

    connect(tcpServer, SIGNAL(newConnection()), this, SLOT(newConnection()));

    QMessageBox infoDialog((QWidget*)parent());
    infoDialog.setText("The server has been started.");
    infoDialog.exec();
}

void nConnectionManager::disconnectConnections()
{
    if(pingTimer.isActive())
        pingTimer.stop();

    if(tcpServer->isListening())
    {
        tcpServer->close();
        disconnect(tcpServer, SIGNAL(newConnection()), this, SLOT(newConnection()));
    }

    foreach(nConnection *conn, mConnections)
    {
        conn->disconnectConnections();
    }

    mConnections.clear();
}


void nConnectionManager::newConnection()
{
    QTcpSocket *sock = tcpServer->nextPendingConnection();

    QByteArray block;
    QDataStream out(&block, QIODevice::WriteOnly);
    out.setVersion(QDataStream::Qt_4_0);
    out << QString("Hello from server!");

    sock->write(block);

    nConnection *conn = new nConnection(sock);
    connect(conn, SIGNAL(newData(QByteArray, nConnection*)), this, SLOT(newData(QByteArray, nConnection*)));
    mConnections.append(conn);

    QMessageBox infoDialog((QWidget*)parent());
    infoDialog.setText("Got new connection.");
    infoDialog.exec();
}

void nConnectionManager::newData(QByteArray in, nConnection *mConnection)
{
    QString str = mConnection->getHandle() + ": \"" + QString(in);
    cout << "new data arrived from: " << str.toStdString() << endl;
}

void nConnectionManager::ping()
{
    cout << "something" << endl;
}



void nConnectionManager::failedConnectionSlot(QAbstractSocket::SocketError error)
{
    QMessageBox errorDialog((QWidget*)parent());
    errorDialog.setText("Could not connect to host: " + QString(error) + "/" + mConnections.at(0)->tcpSocket->errorString());
    errorDialog.show();

    mConnections.clear();
}

void nConnectionManager::succeededConnectionSlot()
{
    QMessageBox infoDialog((QWidget*)parent());
    infoDialog.setText("Connected to host!");
    infoDialog.show();

    connected = 1;

    if(mConnections.size() > 0)
        mConnections.at(0)->sendData(QByteArray("Hello!"));
    else
    {
        QMessageBox errorDialog((QWidget*)parent());
        errorDialog.setText("Something wrong with mConnections.");
        errorDialog.show();
        connected = 0;
    }
}

void nConnectionManager::disconnectedSlot()
{
    QMessageBox errorDialog((QWidget*)parent());
    errorDialog.setText("Got disconnected from host: " + mConnections.at(0)->tcpSocket->errorString());
    errorDialog.show();

    mConnections.clear();
    connected = 0;
}

void nConnectionManager::stateChangedSlot(QAbstractSocket::SocketState state)
{
    /*QMessageBox errorDialog((QWidget*)parent());
    switch (state)
    {
        case QAbstractSocket::UnconnectedState:
            errorDialog.setText("State changed: UnconnectedState");
            break;
        case QAbstractSocket::HostLookupState:
            errorDialog.setText("State changed: HostLookupState");
            break;
        case QAbstractSocket::ConnectedState:
            errorDialog.setText("State changed: ConnectedState");
            break;
        case QAbstractSocket::ConnectingState:
            errorDialog.setText("State changed: ConnectingState");
            break;
        case QAbstractSocket::BoundState:
            errorDialog.setText("State changed: BoundState");
            break;
        case QAbstractSocket::ClosingState:
            errorDialog.setText("State changed: ClosingState");
            break;
        case QAbstractSocket::ListeningState:
            errorDialog.setText("State changed: ListeningState");
            break;
        default:
            errorDialog.setText("State changed: ERROR, DEFAULT!?");
            break;
    }

    errorDialog.exec();*/
}
