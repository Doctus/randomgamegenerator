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

