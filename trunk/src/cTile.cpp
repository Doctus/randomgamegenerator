#include "cTile.h"

cTile::cTile(int id, int tile, int layer, int mapId, QPoint pos, cTileset *tileset)
{
    this->id = id;
    this->tile = tile;
    this->layer = layer;
    this->mapId = mapId;
    this->pos = pos;
    this->mTileset = tileset;
}


int cTile::getId()
{
    return id;
}

int cTile::getTilesetId()
{
    return mTileset->getId();
}

int cTile::getTile()
{
    return tile;
}

int cTile::getLayer()
{
    return layer;
}

int cTile::getMapId()
{
    return mapId;
}

QPoint cTile::getPos()
{
    return pos;
}

cTileset* cTile::getTileset()
{
    return mTileset;
}

