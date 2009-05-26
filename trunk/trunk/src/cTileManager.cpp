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


#include "cTileManager.h"

cTileManager::cTileManager()
{
    id = 0;
}

int cTileManager::addTile(int tile, int layer, int mapId, QPoint pos, cTileset *tileset)
{
    id++;
    tiles.push_back(new cTile(id, tile, layer, mapId, pos, tileset));
    return id;
}

void cTileManager::removeTile(cTile *tile)
{
    removeTile(tile->getId());
}

void cTileManager::removeTile(int id)
{
    int pos = getPos(id);

    if(pos != -1)
        tiles.erase(tiles.begin() + pos);
}


cTile* cTileManager::findTile(int id)
{
    int pos = getPos(id);

    if(pos == -1)
        return NULL;

    return tiles[pos];
}

vector<cTile*> cTileManager::getTilesByTilesetId(int id)
{
    vector<cTile*> ret;

    for(unsigned int i = 0; i < tiles.size(); i++)
    {
        if(tiles[i]->getTilesetId() == id)
            ret.push_back(tiles[i]);
    }

    return ret;
}

vector<cTile*> cTileManager::getTilesByMapId(int id)
{
    vector<cTile*> ret;

    for(unsigned int i = 0; i < tiles.size(); i++)
    {
        if(tiles[i]->getMapId() == id)
            ret.push_back(tiles[i]);
    }

    return ret;
}

int cTileManager::getPos(int id)
{
    for(unsigned int i = 0; i < tiles.size(); i++)
    {
        if(tiles[i]->getId() == id)
            return i;
    }

    return -1;
}

