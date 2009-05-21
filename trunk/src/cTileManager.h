#ifndef CTILEMANAGER_GUARD
#define CTILEMANAGER_GUARD

#include <vector>
#include <QtCore/QPoint>

#include "cTile.h"
#include "cTileset.h"

using namespace std;

class cTileManager
{
    private:
    vector<cTile*> tiles;
    int id;

    public:
    cTileManager();

    int addTile(int tile, int layer, int mapId, QPoint pos, cTileset *tileset);
    void removeTile(cTile *tile);
    void removeTile(int id);

    cTile* findTile(int id);
    vector<cTile*> getTilesByTilesetId(int id);
    vector<cTile*> getTilesByMapId(int id);

    private:
    int getPos(int id);
};

#endif

