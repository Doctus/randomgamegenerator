#ifndef CTILESETMANAGER_GUARD
#define CTILESETMANAGER_GUARD

#include <vector>
#include <string>

#include "cTileset.h"
#include "Widgets/GLWidget.h"

using namespace std;

class cTilesetManager
{
    private:
    vector<cTileset*> tilesets;
    int id;

    public:
    cTilesetManager();

    int loadTileset(GLWidget *mGLWidget, int tileWidth, int tileHeight, string filename);
    void removeTileset(cTileset *tileset);
    void removeTileset(int id);

    cTileset* findTileset(int id);
    cTileset* findTileset(string filename);

    private:
    int getPosition(int id);
};

#endif

