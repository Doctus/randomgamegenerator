#ifndef CTILE_GUARD
#define CTILE_GUARD

class cTile;

#include <QtCore/QPoint>

#include "cTileManager.h"
#include "cTileset.h"

class cTile
{
    private:
    int id;
    int tile;
    int layer;
    int mapId;
    QPoint pos;
    cTileset *mTileset;

    friend class cTileManager;

    cTile(int id, int tile, int layer, int mapId, QPoint pos, cTileset *tileset);

    public:
    int getId();
    int getTilesetId();
    int getTile();
    int getLayer();
    int getMapId();
    QPoint getPos();
    cTileset* getTileset();
};

#endif
