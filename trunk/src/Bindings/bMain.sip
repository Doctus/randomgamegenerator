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

%Module _bmainmod

%Import QtCore/QtCoremod.sip
//%Import QtGui/QtGuimod.sip
//%Import QtOpenGL/QtOpenGLmod.sip
//%Import QtNetwork/QtNetworkmod.sip

class bMain : QObject {

%TypeHeaderCode
#include <bMain.h>
%End


public:
    bMain();
    void start();
    void insertChatMessage(QString str);
    void sendNetMessageToAll(QString msg);
    bool sendNetMessageToHandle(QString msg, QString handle);
    void sendNetMessageToAllButOne(QString msg, QString handle);

    QString getLocalUserList();
    QString getLocalHandle();
    bool isClient();
    bool isServer();

    int displayUserDialogChoice(QString text, QVector<QString> buttonTexts, int defaultButton = 0);
    int showPopupMenuAt(int x, int y, QVector<QString> actionTexts);
    QString getUserTextInput(QString question);

    int getCamX();
    int getCamY();
    int getCamW();
    int getCamH();

    void changeImage(QString oldFilename, QString newFilename);

signals:
    void newNetMessageSignal(QString str, QString handle);
    void newChatInputSignal(QString str);

    void connectedSignal(QString handle);
    void disconnectedSignal(QString handle);

    void loadMapSignal(QString filename);
    void saveMapSignal(QString filename);

    void mouseMoveSignal(int x, int y);
    void mousePressSignal(int x, int y, int type);
    void mouseReleaseSignal(int x, int y, int type);
};

class bImage
{

%TypeHeaderCode
#include <bImage.h>
%End

    public:
    bImage(int x, int y, int w, int h, int tile, int layer, QString filename);
    ~bImage();

    int getId();
    int getX();
    int getY();
    int getW();
    int getH();
    int getTile();
    int getLayer();
    QString getFilename();

    void setX(int x);
    void setY(int y);
    void setW(int w);
    void setH(int h);
    void setTile(int tile);
    void setLayer(int layer);
};
