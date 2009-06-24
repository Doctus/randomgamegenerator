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



nConnectionManager::nConnectionManager(QWidget *parent, cGame *mGame) : QObject(parent)
{
    connected = Connection::NONE;

    tcpServer = new QTcpServer(this);
    this->mGame = mGame;

    connect(&pingTimer, SIGNAL(timeout()), this, SLOT(ping()));
    pingTimer.setInterval(5000);
}

/*
 * Can't be hosting a server and connect to somewhere at the same time. So it checks for connected to not equal 2(server)
 * and if not, it sets connected to 1(client)
 */
void nConnectionManager::connectTo(QString host, uint port, QString handle){
    if(connected == Connection::SERVER)
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
    else if(connected == Connection::CLIENT)
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

    ourHandle = handle;

    QTcpSocket *sock = new QTcpSocket(this);

    connect(sock, SIGNAL(error(QAbstractSocket::SocketError)), this, SLOT(failedConnectionSlot(QAbstractSocket::SocketError)));
    connect(sock, SIGNAL(connected()), this, SLOT(succeededConnectionSlot()));

    nConnection *conn = new nConnection(sock);
    connect(conn, SIGNAL(newData(QByteArray, nConnection*)), this, SLOT(newData(QByteArray,nConnection*)));
    connect(conn, SIGNAL(disconnected(nConnection*)), this, SLOT(disconnectedSlot(nConnection*)));

    mConnections.append(conn);

    sock->connectToHost(host, port);
}

/*
 * Can't be hosting a server and connect to somewhere at the same time. So it checks for connected to not equal 1(client)
 * and if not, it sets connected to 2(server)
 */
void nConnectionManager::startServer(uint port, QString handle)
{
    if(connected == Connection::CLIENT)
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
    else if(connected == Connection::SERVER)
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

    ourHandle = handle;

    pingTimer.start();
    connected = Connection::SERVER;

    connect(tcpServer, SIGNAL(newConnection()), this, SLOT(newConnection()));

    QMessageBox infoDialog((QWidget*)parent());
    infoDialog.setText("The server has been started.");
    infoDialog.exec();
}

//private
void nConnectionManager::sendMessageToAll(QString message)
{
    QByteArray out(message.toUtf8());
    foreach(nConnection *conn, mConnections)
    {
        conn->sendData(out);
    }
}

void nConnectionManager::sendNetMessageToAllButOne(QString message, QString handle)
{
    QByteArray out(message.toUtf8());
    foreach(nConnection *conn, mConnections)
    {
        if(conn->getHandle() != handle)
            conn->sendData(out);
    }
}

bool nConnectionManager::sendMessageToHandle(QString message, QString handle)
{
    QByteArray out(message.toUtf8());

    cout << "Sending \"" << message.toStdString() << "\" to \"" << handle.toStdString() << "\"" << endl;

    foreach(nConnection *conn, mConnections)
    {
        if(conn->getHandle() == handle)
        {
            conn->sendData(out);
            return true;
        }
    }

    return false;
}

QString nConnectionManager::getLocalUserList()
{
    QString str = "";
    foreach(nConnection *conn, mConnections)
    {
        str.append(conn->getHandle() + " ");
    }

    return str;
}

QString nConnectionManager::getLocalHandle()
{
    return ourHandle;
}

bool nConnectionManager::isConnectionType(Connection::conn type)
{
    if(type == connected)
        return true;
    return false;
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
    connected = Connection::NONE;
}


void nConnectionManager::newConnection()
{
    QTcpSocket *sock = tcpServer->nextPendingConnection();

    nConnection *conn = new nConnection(sock);

    connect(conn, SIGNAL(newData(QByteArray, nConnection*)), this, SLOT(newData(QByteArray, nConnection*)));
    connect(conn, SIGNAL(disconnected(nConnection*)), this, SLOT(disconnectedSlot(nConnection*)));

    conn->sendData(ourHandle.toUtf8());

    mConnections.append(conn);
}

void nConnectionManager::newData(QByteArray in, nConnection *mConnection)
{
    if(mConnection->getProperlyConnected())
        emit newNetMessage(QString::fromUtf8(in), mConnection->getHandle());
    else
    {
        QString handle = QString::fromUtf8(in);
        mConnection->setHandle(handle);
        mConnection->setProperlyConnected(true);
        emit connectedSignal(handle);
    }
}

void nConnectionManager::ping()
{

}


//Note that this is only used when initiating a connection to a server, not when hosting one.
void nConnectionManager::failedConnectionSlot(QAbstractSocket::SocketError error)
{
    QMessageBox errorDialog((QWidget*)parent());
    errorDialog.setText("Could not connect to host: " + QString::number(error) + "/" + mConnections.at(0)->tcpSocket->errorString());
    errorDialog.exec();

    mConnections.clear();
}

//Note that this is only used when initiating a connection to a server, not when hosting one.
void nConnectionManager::succeededConnectionSlot()
{
    /*QMessageBox infoDialog((QWidget*)parent());
    infoDialog.setText("Connected to host!");
    infoDialog.exec();*/

    connected = Connection::CLIENT;

    nConnection *conn = mConnections.at(0);

    conn->sendData(ourHandle.toUtf8());
}

void nConnectionManager::disconnectedSlot(nConnection *conn)
{
    if(connected == Connection::CLIENT)
    {
        /*QMessageBox errorDialog((QWidget*)parent());
        errorDialog.setText("Got disconnected from host: " + conn->tcpSocket->errorString());
        errorDialog.show();*/

        connected = 0;
    }
    /*else if(connected == Connection::SERVER)
    {
        QMessageBox errorDialog((QWidget*)parent());
        errorDialog.setText("\"" + conn->getHandle() + "\" has disconnected");
        errorDialog.show();
    }*/

    emit disconnectedSignal(conn->getHandle());

    mConnections.removeOne(conn);
}

void nConnectionManager::stateChangedSlot(QAbstractSocket::SocketState state)
{

}
