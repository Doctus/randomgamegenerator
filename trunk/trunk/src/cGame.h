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

class cGame;

#include "cMap.h"
#include "cTileManager.h"
#include "cTilesetManager.h"
#include "Widgets/wMenuBar.h"
#include "Widgets/wDockWidgets.h"

using namespace std;

class cGame : public QObject
{
    Q_OBJECT;

    private:
    cMap *mCurrentMap;
    cTileManager *mTileManager;
    cTilesetManager *mTilesetManager;
    wMenuBar *mMenuBar;
    wGLWidget *mGLWidget;
    wDockWidgets *mDockWidgets;

    friend class wMenuBar;

    public:
    cGame(QWidget *parent);
    ~cGame();

    private slots:
    void draw();
    void displayFPS();

    public:
    void loadMap(string fileName);
    void saveMap(string fileName);
    void showTextDockWidget();
};

#endif
