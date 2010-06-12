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

#ifndef BMAIN_H
#define BMAIN_H

#include <QtGui/QApplication>
#include <QtGui/QMainWindow>
#include <QtCore/QObject>
#include <QtGui/QToolTip>

#include <vector>

#include "../cGame.h"
#include "../Widgets/wAction.h"
#include "../cTileset.h"
#include "../cShapeManager.h"


class bMain : public QObject
{
    Q_OBJECT;

    private:
    static cGame *mainGame;
    QVector<QToolTip*> tooltips;

    public:
    bMain();
    //virtual ~bMain() {}

    void start();
    static cGame* getGameInstance();
	
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

    private slots:
    void mouseMoveTrigger(int x, int y);
    void mousePressTrigger(int x, int y, int type);
    void mouseReleaseTrigger(int x, int y, int type);

    void leaveEventTrigger();
    void enterEventTrigger();

    signals:
    void mouseMoveSignal(int x, int y);
    void mousePressSignal(int x, int y, int type);
    void mouseReleaseSignal(int x, int y, int type);

    void leaveEventSignal();
    void enterEventSignal();
};

#endif // BMAIN_H
