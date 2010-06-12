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


#ifndef CTILESET_H
#define CTILESET_H

#include <string>
#include <iostream>

#include <QtGui/QImage>
#include <QtCore/QPoint>

class cTileset;

#include "cTilesetManager.h"
#include "Widgets/wGLWidget.h"

using namespace std;

class cTileset
{
    private:
    int id;
    int tileWidth;
    int tileHeight;
    string filename;
    QImage *image;
    wGLWidget *mGLWidget;
    map<unsigned int, GLuint> textureIds;

    friend class cTilesetManager;

    cTileset(int id, wGLWidget *mGLWidget, int tileWidth, int tileHeight, string filename);
    ~cTileset();

    public:
    int getId();
    int getTileWidth();
    int getTileHeight();
    int getHighestTile();
    GLuint getTextureId(int tile);
    GLuint getTextureId(int x, int y);

    string getFilename();
    int getW();
    int getH();

    map<unsigned int, GLuint> reload();

    private:
    void loadImage();
};

#endif

