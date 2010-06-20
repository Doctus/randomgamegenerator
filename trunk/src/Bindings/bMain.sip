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
%Import QtGui/QtGuimod.sip
//%Import stdvector.sip
//%Import QtOpenGL/QtOpenGLmod.sip
//%Import QtNetwork/QtNetworkmod.sip

class bMain : QObject {

%TypeHeaderCode
#include "bMain.h"
%End


public:
    bMain();
    void start();
   
    int displayUserDialogChoice(QString text, QVector<QString> buttonTexts, int defaultButton = 0);
    int showPopupMenuAt(int x, int y, QVector<QString> actionTexts);
    int showPopupMenuAtAbs(int x, int y, QVector<QString> actionTexts);
    void displayTooltip(QString text, int x, int y);
    //void removeTooltip(int id);
    QString getUserTextInput(QString question);

    QMainWindow* getMainWindow();

    int getCamX();
    int getCamY();
    int getCamW();
    int getCamH();

    void setCam(int x, int y);
    void adjustCam(int x, int y);

    void setZoom(float zoom);
    float getZoom();

    void changeImage(QString oldFilename, QString newFilename, int tileWidth, int tileHeight);
    int getTileCountOfImage(QString filename, int tileWidth, int tileHeight);

    void addLine(int x, int y, int w, int h, int thickness);
    void deleteLine(int x, int y, int w, int h, int thickness = -1);
    void clearLines();
    QVector<QRect> getLineOfThickness(int thickness);

    /*void addTranslationFile(QString filename);
    void removeTranslationFile(QString filename);*/

signals:
    void mouseMoveSignal(int x, int y);
    void mousePressSignal(int x, int y, int type);
    void mouseReleaseSignal(int x, int y, int type);

    void leaveEventSignal();
    void enterEventSignal();
};

class bImage
{

%TypeHeaderCode
#include "bImage.h"
%End

    public:
    bImage(int x, int y, int w, int h, int drawW, int drawH, int tile, int layer, QString filename);
    ~bImage();

    int getId();
    int getX();
    int getY();
    int getW();
    int getH();
    int getDrawW();
    int getDrawH();
    int getTile();
    int getLayer();
    bool getHidden();
    QString getFilename();
    int getTilesetId();

    int getTilesetW();
    int getTilesetH();

    void setX(int x);
    void setY(int y);
    void setW(int w);
    void setH(int h);
    void setDrawW(int w);
    void setDrawH(int h);
    void setTile(int tile);
    void setLayer(int layer);
    void setHidden(bool hidden);

    void DELETEME();
};
