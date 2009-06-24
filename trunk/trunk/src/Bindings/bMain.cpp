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

#include "bMain.h"

#include "../cGame.h"
#include "../Widgets/wDockWidgets.h"
#include "../Network/nConnectionManager.h"

QApplication app(NULL, NULL);
QMainWindow *widget;
cGame *mGame;

bMain::bMain()
{


    widget = new QMainWindow(); //parent widget
    widget->resize(640, 480);

    mGame = new cGame(widget);

    connect(mGame->mDockWidgets, SIGNAL(newChatInputSignal(QString)), this, SLOT(chatInputTrigger(QString)));
    connect(mGame->mConnectionManager, SIGNAL(newNetMessage(QString,QString)), this, SLOT(netMessageTrigger(QString, QString)));
    connect(mGame->mConnectionManager, SIGNAL(connectedSignal(QString)), this, SLOT(connectedTrigger(QString)));
    connect(mGame->mConnectionManager, SIGNAL(disconnectedSignal(QString)), this, SLOT(disconnectedTrigger(QString)));
}

void bMain::start()
{
    widget->show();

    app.exec();

    return;
}

void bMain::insertChatMessage(QString str)
{
    mGame->mDockWidgets->insertMessage(str);
}

void bMain::sendNetMessageToAll(QString msg)
{
    mGame->mConnectionManager->sendMessageToAll(msg);
}

bool bMain::sendNetMessageToHandle(QString msg, QString handle)
{
    return mGame->mConnectionManager->sendMessageToHandle(msg, handle);
}

void bMain::sendNetMessageToAllButOne(QString msg, QString handle)
{
    mGame->mConnectionManager->sendNetMessageToAllButOne(msg, handle);
}

QString bMain::getLocalUserList()
{
    return mGame->mConnectionManager->getLocalUserList();
}

QString bMain::getLocalHandle()
{
    return mGame->mConnectionManager->getLocalHandle();
}

bool bMain::isClient()
{
    return mGame->mConnectionManager->isConnectionType(Connection::CLIENT);
}

bool bMain::isServer()
{
    return mGame->mConnectionManager->isConnectionType(Connection::SERVER);
}

void bMain::chatInputTrigger(QString msg)
{
    emit newChatInputSignal(msg);
}

void bMain::netMessageTrigger(QString msg, QString handle)
{
    emit newNetMessageSignal(msg, handle);
}

void bMain::connectedTrigger(QString handle)
{
    emit connectedSignal(handle);
}

void bMain::disconnectedTrigger(QString handle)
{
    emit disconnectedSignal(handle);
}
