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


#ifndef NCONNECTION_H
#define NCONNECTION_H

class nConnection;

#include <QtNetwork/QTcpSocket>
#include <QtCore/QObject>
#include <QtCore/QByteArray>
#include <iostream>

#include "nConnectionManager.h"

using namespace std;

class nConnection : public QObject
{
    Q_OBJECT;

    private:
    QTcpSocket *tcpSocket;
    QString handle;

    friend class nConnectionManager;

    public:
    nConnection(QTcpSocket *tcpSocket);

    void sendData(QByteArray out);
    void setHandle(QString handle);
    QString getHandle();
    void disconnectConnections();

    private slots:
    void readData();
    void disconnectedSlot();

    signals:
    void newData(QByteArray in, nConnection *mConnection); //not implented in nConnection.cpp, but in the auto-generated moc
    void disconnected(nConnection *conn);
};


#endif // NCONNECTION_H
