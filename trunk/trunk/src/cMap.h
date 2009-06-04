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


#ifndef MAP_H
#define MAP_H

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <confuse.h>

class cMap;

#include "cTilesetManager.h"
#include "cTileManager.h"
#include "cEventManager.h"
#include "cCamera.h"
#include "Widgets/wGLWidget.h"

using namespace libconfig;
using namespace std;

class cMap
{
    private:
    cTilesetManager *mTilesetManager;
    cTileManager *mTileManager;
    cEventManager *mEventManager;
    vector<int> tilesetIds;
    vector<int> layers;
    int id;
    cCamera *mCamera;
    int tileWidth, tileHeight;
    wGLWidget *mGLWidget;

    public:
    cMap(int id, wGLWidget *mGLWidget, cTileManager *tileManager, cTilesetManager *tilesetManager);
    ~cMap();

    bool loadMap(string filename);
    void draw();
};

#endif

