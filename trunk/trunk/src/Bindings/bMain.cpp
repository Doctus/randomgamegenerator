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

void bMain::sendChatMessageToAll(QString msg)
{
    mGame->mConnectionManager->sendMessageToAll(msg);
}

void bMain::sendChatMessageToHandle(QString msg, QString handle)
{
    mGame->mConnectionManager->sendMessageToHandle(msg, handle);
}

void bMain::chatInputTrigger(QString msg)
{
    emit newChatInput(msg);
}

void bMain::netMessageTrigger(QString msg, QString handle)
{
    emit newNetMessageSignal(msg, handle);
}
