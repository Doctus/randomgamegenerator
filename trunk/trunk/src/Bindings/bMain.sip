%Module bmainmod

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip
%Import QtOpenGL/QtOpenGLmod.sip
%Import QtNetwork/QtNetworkmod.sip

class bMain : QObject {

%TypeHeaderCode
#include <bMain.h>
%End


public:
    bMain();
    void start();
    void insertChatMessage(QString str);
    void sendNetMessageToAll(QString msg);
    void sendNetMessageToHandle(QString msg, QString handle);

    QString getLocalUserList();
    QString getLocalHandle();
    bool isClient();
    bool isServer();

signals:
    void newNetMessageSignal(QString str, QString handle);
    void newChatInputSignal(QString str);
    void connectedSignal(QString handle);
};
