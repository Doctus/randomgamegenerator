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


#ifndef CTILESETMANAGER_H
#define CTILESETMANAGER_H

#include <vector>
#include <string>

#include "cTileset.h"
#include "Widgets/wGLWidget.h"

using namespace std;

class cTilesetManager
{
    private:
    vector<cTileset*> tilesets;
    int id;

    public:
    cTilesetManager();

    int loadTileset(wGLWidget *mGLWidget, int tileWidth, int tileHeight, string filename);
    void removeTileset(cTileset *tileset);
    void removeTileset(int id);

    cTileset* findTileset(int id);
    cTileset* findTileset(string filename);

    private:
    int getPosition(int id);
};

#endif

