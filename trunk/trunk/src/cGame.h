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


#ifndef CGAME_H
#define CGAME_H

#include <QtGui/QWidget>
#include <QtGui/QScrollArea>

class cGame;

#include "cTilesetManager.h"
#include "Widgets/wMenuBar.h"
#include "Widgets/wGLWidget.h"
#include "Widgets/wDockWidgets.h"
#include "Network/nConnectionManager.h"
#include "Bindings/bMain.h"
#include "Bindings/bImage.h"

using namespace std;

class cGame : public QObject
{
    Q_OBJECT;

    private:
    cTilesetManager *mTilesetManager;
    wMenuBar *mMenuBar;
    wGLWidget *mGLWidget;
    wDockWidgets *mDockWidgets;
    nConnectionManager *mConnectionManager;

    QString title;

    friend class wMenuBar;
    friend class wGLWidget;
    friend class bMain;
    friend class bImage;

    public:
    cGame(QWidget *parent);
    ~cGame();

    private slots:
    void draw();
    void displayFPS();

    public:
    void showTextDockWidget();
    QString getTitle();
};

#endif
