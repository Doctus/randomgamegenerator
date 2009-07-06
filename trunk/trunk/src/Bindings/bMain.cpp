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
cGame* bMain::mainGame;

bMain::bMain()
{


    widget = new QMainWindow(); //parent widget
    widget->resize(640, 480);

    QIcon *icon = new QIcon("../data/FAD-icon.png");

    widget->setWindowIcon(*icon);

    mainGame = new cGame(widget);

    cout << "mainGame initialised" << endl;

    connect(mainGame->mDockWidgets, SIGNAL(newChatInputSignal(QString)), this, SLOT(chatInputTrigger(QString)));
    connect(mainGame->mConnectionManager, SIGNAL(newNetMessage(QString,QString)), this, SLOT(netMessageTrigger(QString, QString)));
    connect(mainGame->mConnectionManager, SIGNAL(connectedSignal(QString)), this, SLOT(connectedTrigger(QString)));
    connect(mainGame->mConnectionManager, SIGNAL(disconnectedSignal(QString)), this, SLOT(disconnectedTrigger(QString)));
    connect(mainGame->mMenuBar, SIGNAL(loadMapSignal(QString)), this, SLOT(loadMapTrigger(QString)));
    connect(mainGame->mGLWidget, SIGNAL(mouseClickSignal(int,int)), this, SLOT(mouseClickTrigger(int,int)));
    connect(mainGame->mGLWidget, SIGNAL(mouseMoveSignal(int,int)), this, SLOT(mouseMoveTrigger(int,int)));
}

void bMain::start()
{
    widget->show();

    app.exec();

    return;
}

cGame* bMain::getGameInstance()
{
    return mainGame;
}

void bMain::insertChatMessage(QString str)
{
    mainGame->mDockWidgets->insertMessage(str);
}

void bMain::sendNetMessageToAll(QString msg)
{
    mainGame->mConnectionManager->sendMessageToAll(msg);
}

bool bMain::sendNetMessageToHandle(QString msg, QString handle)
{
    return mainGame->mConnectionManager->sendMessageToHandle(msg, handle);
}

void bMain::sendNetMessageToAllButOne(QString msg, QString handle)
{
    mainGame->mConnectionManager->sendNetMessageToAllButOne(msg, handle);
}


QString bMain::getLocalUserList()
{
    return mainGame->mConnectionManager->getLocalUserList();
}

QString bMain::getLocalHandle()
{
    return mainGame->mConnectionManager->getLocalHandle();
}

bool bMain::isClient()
{
    return mainGame->mConnectionManager->isConnectionType(Connection::CLIENT);
}

bool bMain::isServer()
{
    return mainGame->mConnectionManager->isConnectionType(Connection::SERVER);
}


int bMain::displayUserDialogChoice(QString text, QVector<QString> buttonTexts, int defaultButton)
{
    if(buttonTexts.size() == 0)
        return -1;

    QVector<QPushButton*> buttons;

    QMessageBox questionDialog(widget);
    questionDialog.setText(text);

    for(int j = buttonTexts.size() - 1; j >= 0; j--)
    {
        QPushButton *newButton = questionDialog.addButton(buttonTexts[j], QMessageBox::AcceptRole);
        buttons.push_front(newButton);
        if(j == defaultButton)
            questionDialog.setDefaultButton(newButton);
    }

    questionDialog.exec();

    int i= 0;

    foreach(QPushButton *button, buttons)
    {
        if(questionDialog.clickedButton() == button)
            return i;
        i++;
    }

    return -1;
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

void bMain::loadMapTrigger(QString filename)
{
    emit loadMapSignal(filename);
}

void bMain::mouseMoveTrigger(int x, int y)
{
    emit mouseMoveSignal(x, y);
}

void bMain::mouseClickTrigger(int x, int y)
{
    emit mouseClickSignal(x, y);
}
