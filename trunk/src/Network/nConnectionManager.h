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


#ifndef NCONNECTIONMANAGER_H
#define NCONNECTIONMANAGER_H

#include <QtCore/QList>
#include <QtCore/QObject>
#include <QtCore/QByteArray>
#include <QtCore/QTimer>
#include <QtNetwork/QTcpServer>
#include <QtNetwork/QTcpSocket>
#include <QtGui/QMessageBox>

#include <iostream>

#include "nConnection.h"

using namespace std;

class nConnectionManager : public QObject
{
    Q_OBJECT;

    private:
    QList<nConnection*> mConnections;
    QTcpServer *tcpServer;
    QTimer pingTimer;
    int connected;

    public:
    nConnectionManager(QWidget *parent);

    void connectTo(QString host, uint port);
    void startServer(uint port);
    void disconnectConnections();

    private slots:

    //server slots
    void newConnection();
    void newData(QByteArray in, nConnection *mConnection); //server AND client slot
    void ping();

    //client slots
    void failedConnectionSlot(QAbstractSocket::SocketError error);
    void succeededConnectionSlot();
    void disconnectedSlot();
};

#endif // NCONNECTIONMANAGER_H
