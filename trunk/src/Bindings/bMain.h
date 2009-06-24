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
    void sendNetMessageToAll(QString msg);
    void sendNetMessageToHandle(QString msg, QString handle);

    QString getLocalUserList();
    QString getLocalHandle();
    bool isClient();
    bool isServer();

    private slots:
    void chatInputTrigger(QString msg);
    void netMessageTrigger(QString msg, QString handle);
    void connectedTrigger(QString handle);

    signals:
    void newNetMessageSignal(QString str, QString handle);
    void newChatInputSignal(QString str);
    void connectedSignal(QString handle);
};

#endif // BMAIN_H
