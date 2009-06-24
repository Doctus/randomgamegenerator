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
    void sendChatMessageToAll(QString msg);
    void sendChatMessageToHandle(QString msg, QString handle);

signals:
    void newNetMessageSignal(QString str, QString handle);
    void newChatInput(QString str);
};
