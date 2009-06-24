#include "bMain.h"

#include "../cGame.h"
#include "../Widgets/wDockWidgets.h"
#include "../Network/nConnectionManager.h"

//#include <string.h>

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
}

void bMain::start()
{
    /*int argc = 1;
    char argv[0][30];

    strcpy(argv[0], "Random Game Generator");*/

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

void bMain::sendNetMessageToHandle(QString msg, QString handle)
{
    mGame->mConnectionManager->sendMessageToHandle(msg, handle);
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
