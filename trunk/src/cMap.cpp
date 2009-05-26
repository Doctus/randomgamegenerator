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


#include "cMap.h"

struct tilesetConverter
{
    int requestedId, actualId;

    tilesetConverter(int x, int y) {requestedId = x; actualId = y;}
};

vector<int> addItemIfNotExist(vector<int> v, int x)
{
    for(unsigned int i = 0; i < v.size(); i++)
    {
        if(v[i] == x)
            return v;
    }

    v.push_back(x);
    return v;
}

int findActualId(vector<tilesetConverter> v, int requestedId)
{
    for(unsigned int i = 0; i < v.size(); i++)
    {
        if(v[i].requestedId == requestedId)
            return v[i].actualId;
    }

    return -1;
}

cMap::cMap(int id, wGLWidget *mGLWidget, cTileManager *tileManager, cTilesetManager *tilesetManager)
{
    this->id = id;
    this->mGLWidget = mGLWidget;
    tileWidth = 0;
    tileHeight = 0;
    mTileManager = tileManager;
    mTilesetManager = tilesetManager;
    mEventManager = cEventManager::getInstance();
    mCamera = new cCamera(0, 0, 640, 480);
}

cMap::~cMap()
{
    //mTileManager->unregisterMap(this);
    //mTilesetManager->unregisterMap(this);
    delete mCamera;
}


bool cMap::loadMap(string filename)
{
    Config conf;

    try
    {
        conf.readFile(filename.c_str());
    }
    catch(ParseException pe)
    {
        cout << "ParseException: " << pe.what() << endl;
        return false;
    }
    catch(FileIOException fioe)
    {
        cout << "FileIOException" << endl; //file did not exist. Har har
        return false;
    }

    int mapx = 0;
    int mapy = 0;
    vector<tilesetConverter> mTilesetConverter;

    if(!(conf.lookupValue("map.tilewidth", tileWidth) && conf.lookupValue("map.tileheight", tileHeight)
    && conf.lookupValue("map.mapx", mapx) && conf.lookupValue("map.mapy", mapy)))
        return false;

    Setting &sett = conf.lookup("map.tilesets");
    for(int i = 0; i < sett.getLength(); i++)
    {
        stringstream ss;
        string lookup;
        ss << i;
        lookup = "map.tilesets.[" + ss.str() + "]";
        Setting &tempSett = conf.lookup(lookup.c_str());
        std::string tilesetFilename;
        int requestId = 0;
        int actualId = 0;

        if(!tempSett.lookupValue("id", requestId))
            return false;

        if(!tempSett.lookupValue("file", tilesetFilename))
            return false;

        cout << "id + file: " << requestId << " - " << tilesetFilename << endl;

        actualId = mTilesetManager->loadTileset(mGLWidget, tileWidth, tileHeight, tilesetFilename);

        if(actualId != -1)
            mTilesetConverter.push_back(tilesetConverter(requestId, actualId));
    }

    int currx = 0, curry = 0, prevlayer = 0;

    Setting &sett2 = conf.lookup("map.tiles");
    for(int i = 0; i < sett2.getLength(); i++)
    {
        stringstream ss;
        string lookup;
        ss << i;
        lookup = "map.tiles.[" + ss.str() + "]";
        Setting &tempSett = conf.lookup(lookup.c_str());

        int layer, tilesetId, tile = -1;

        if(!tempSett.lookupValue("layer", layer))
            return false;

        if(!tempSett.lookupValue("tileset", tilesetId))
            return false;

        if(!tempSett.lookupValue("tile", tile))
            return false;

        if(curry >= mapy)
        {
            if(layer == prevlayer)
                continue;
        }

        if(layer != prevlayer)
        {
            currx = 0;
            curry = 0;
        }

        layers = addItemIfNotExist(layers, layer);

        //cout << "tile: " << tile << " - " << id << " - " << currx << " - " << curry << " - " << tilesetId << " - " << tileWidth << " - " << tileHeight << endl;

        cTileset *tempTileset = mTilesetManager->findTileset(findActualId(mTilesetConverter, tilesetId));

        if(tile != -1 && tempTileset != NULL)
        {
            mTileManager->addTile(tile, layer, id, QPoint(currx*tileWidth, curry*tileHeight), tempTileset);
        }

        if(++currx >= mapx)
        {
            currx = 0;
            curry++;
        }

        prevlayer = layer;
    }

    return true;
}

void cMap::draw()
{
    vector<cTile*> tiles = mTileManager->getTilesByMapId(id);
    
    QPoint cam = mCamera->getCam();

    int lx = cam.x() - tileWidth;
    int rx = cam.x() + mCamera->getBounds().x() + tileWidth;

    int ty = cam.y() - tileHeight;
    int by = cam.y() + mCamera->getBounds().y() + tileHeight;
    for(unsigned int j = 0; j < tiles.size(); j++)
    {
        QPoint pos = tiles[j]->getPos();

        if(pos.x() >= lx && pos.x() <= rx &&
           pos.y() >= ty && pos.y() <= by)
        {
            mGLWidget->drawImage(tiles[j]->getTileset()->getTextureId(tiles[j]->getTile()), pos.x() - cam.x(), pos.y() - cam.y(), tileWidth, tileHeight);
        }
    }
}

void cMap::logic()
{
    if(mEventManager->isKeyPressed(Qt::Key_Right))
        mCamera->adjustCam(QPoint(1, 0));

    if(mEventManager->isKeyPressed(Qt::Key_Left))
        mCamera->adjustCam(QPoint(-1, 0));

    if(mEventManager->isKeyPressed(Qt::Key_Up))
        mCamera->adjustCam(QPoint(0, -1));

    if(mEventManager->isKeyPressed(Qt::Key_Down))
        mCamera->adjustCam(QPoint(0, 1));
}
