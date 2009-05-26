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


#include "cGame.h"

unsigned int FPScounter = 0;

cGame::cGame(QWidget *parent) : QObject(parent)
{
    mGLWidget = new wGLWidget(parent);
    ((QMainWindow*)parent)->setCentralWidget(mGLWidget);

    mMenuBar = new wMenuBar(parent, this);

    mDockWidgets = new wDockWidgets((QMainWindow*)parent);

    mTileManager = new cTileManager();
    mTilesetManager = new cTilesetManager();
    mCurrentMap = new cMap(0, mGLWidget, mTileManager, mTilesetManager);

    QTimer *timer = new QTimer(this);
    QTimer *timer2 = new QTimer(this);
    QTimer *timer3 = new QTimer(this);
    connect(timer , SIGNAL(timeout()), this, SLOT(draw()));
    connect(timer2, SIGNAL(timeout()), this, SLOT(logic()));
    connect(timer3, SIGNAL(timeout()), this, SLOT(displayFPS()));
    timer ->start(40);
    timer2->start(20);
    timer3->start(5000);
}

cGame::~cGame()
{
    delete mTileManager;
    delete mTilesetManager;
}

void cGame::draw()
{
    if(mCurrentMap != NULL)
        mCurrentMap->draw();

    mGLWidget->updateGL();

    FPScounter++;
}

void cGame::logic()
{
    if(mCurrentMap != NULL)
        mCurrentMap->logic();
}

void cGame::displayFPS()
{
    cout << FPScounter << " frames per 5 seconds" << endl;
    FPScounter = 0;
}


void cGame::loadMap(string fileName)
{
    if(mCurrentMap != NULL)
        mCurrentMap->loadMap(fileName);
}

void cGame::saveMap(string fileName)
{
}

void cGame::showTextDockWidget()
{
    this->mDockWidgets->showTextDockWidgets();
}

