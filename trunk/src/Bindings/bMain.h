#ifndef BMAIN_H
#define BMAIN_H

#include <QtGui/QApplication>
#include <QtGui/QMainWindow>
#include <QtCore/QObject>


class bMain : public QObject
{
    Q_OBJECT;

    public:
    bMain();
    //virtual ~bMain() {}

    void start();
    void insertChatMessage(QString str);
    void sendChatMessageToAll(QString msg);
    void sendChatMessageToHandle(QString msg, QString handle);

    private slots:
    void chatInputTrigger(QString msg);
    void netMessageTrigger(QString msg, QString handle);

    signals:
    void newNetMessageSignal(QString str, QString handle);
    void newChatInput(QString str);
};

#endif // BMAIN_H
