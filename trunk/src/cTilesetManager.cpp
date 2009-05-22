#include "cTilesetManager.h"

cTilesetManager::cTilesetManager()
{
    id = 0;
}

int cTilesetManager::loadTileset(GLWidget *mGLWidget, int tileWidth, int tileHeight, string filename)
{
    id++;
    try
    {
        tilesets.push_back(new cTileset(id, mGLWidget, tileWidth, tileHeight, filename));
    }
    catch (...) //this needs to be handled better than just catching any and all exception...although it works <_<
    {
        return -1;
    }
    return id;
}

void cTilesetManager::removeTileset(cTileset *tileset)
{
    removeTileset(tileset->getId());
}

void cTilesetManager::removeTileset(int id)
{
    int pos = getPosition(id);

    if(pos != -1)
        tilesets.erase(tilesets.begin() + pos);
    //else exception?
}


cTileset* cTilesetManager::findTileset(int id)
{
    int pos = getPosition(id);

    if(pos == -1)
        return NULL;

    return tilesets[pos]; //exception?
}

cTileset* cTilesetManager::findTileset(string filename)
{
    for(unsigned int i = 0; i < tilesets.size(); i++)
    {
        if(tilesets[i]->getFilename() == filename)
            return tilesets[i];
    }

    return NULL; //exception?
}

int cTilesetManager::getPosition(int id)
{
    for(unsigned int i = 0; i < tilesets.size(); i++)
    {
        if(tilesets[i]->getId() == id)
            return i;
    }

    return -1; //exception?
}



