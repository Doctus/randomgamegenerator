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

#include "cTilesetManager.h"
#include "cShapeManager.h"
#include "Widgets/wGLWidget.h"
#include "Bindings/bMain.h"
#include "Bindings/bImage.h"

using namespace std;

class cGame : public QObject
{
    Q_OBJECT;

    private:
    cTilesetManager *mTilesetManager;
    wGLWidget *mGLWidget;
    cShapeManager *mShapeManager;

    QString title;

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
    QString getTitle();
};

#endif
