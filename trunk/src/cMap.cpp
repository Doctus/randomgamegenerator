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
    mCamera = new cCamera(0, 0, 640, 480);
}

cMap::~cMap()
{
    //mTileManager->unregisterMap(this);
    //mTilesetManager->unregisterMap(this);
    delete mCamera;
}


/*bool cMap::loadMap(string filename)
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
}*/

bool cMap::loadMap(string filename)
{
    cfg_opt_t tileset_opts[] =
    {
        CFG_INT("id", -1, CFGF_NONE),
        CFG_STR("file", "", CFGF_NONE),
        CFG_END()
    };

    cfg_opt_t tile_opts[] =
    {
        CFG_INT("tileid", -1, CFGF_NONE),
        CFG_INT("tilesetid", -1, CFGF_NONE),
        CFG_END()
    };

    cfg_opt_t layer_opts[] =
    {
        CFG_INT("height", -1, CFGF_NONE),
        CFG_SEC("tile", tile_opts, CFGF_TITLE | CFGF_MULTI),
        CFG_END()
    };

    cfg_opt_t map_opts[] =
    {
        CFG_STR("name", "", CFGF_NONE),
        CFG_STR("author", "", CFGF_NONE),
        CFG_STR("comments", "", CFGF_NONE),
        CFG_INT("tilewidth", -1, CFGF_NONE),
        CFG_INT("tileheight", -1, CFGF_NONE),
        CFG_INT("mapx", -1, CFGF_NONE),
        CFG_INT("mapy", -1, CFGF_NONE),
        CFG_SEC("layer", layer_opts, CFGF_TITLE | CFGF_MULTI),
        CFG_SEC("tileset", tileset_opts, CFGF_TITLE | CFGF_MULTI),
        CFG_END()
    };

    cfg_opt_t opts[] =
    {
        CFG_SEC("map", map_opts, CFGF_TITLE | CFGF_MULTI),
        CFG_END()
    };

    cfg_t *cfg = cfg_init(opts, CFGF_NONE);

    if(cfg_parse(cfg, filename.c_str()) == CFG_PARSE_ERROR)
    {
        cout << "couldn't parse file" << endl;
        return false;
    }

    if(cfg_size(cfg, "map") == 0)
        return false;

    cfg_t *cfg_map, *cfg_tileset, *cfg_layer, *cfg_tile;

    std::string mapName, mapAuthor, mapComments;
    int mapx, mapy;
    unsigned int i, j;
    vector<tilesetConverter> mTilesetConverter;

    cfg_map = cfg_getnsec(cfg, "map", 0);

    if( (mapName = cfg_getstr(cfg_map, "name")).length() == 0 || (mapAuthor = cfg_getstr(cfg_map, "author")).length() == 0 || (mapComments = cfg_getstr(cfg_map, "comments")).length() == 0 )
        return false;

    if( (mapx = cfg_getint(cfg_map, "mapx")) == -1 || (mapy = cfg_getint(cfg_map, "mapy")) == -1 || (tileWidth = cfg_getint(cfg_map, "tilewidth")) == -1 || (tileHeight = cfg_getint(cfg_map, "tileheight")) == -1 )
        return false;

    for(i = 0; i < cfg_size(cfg_map, "tileset"); i++)
    {
        cfg_tileset = cfg_getnsec(cfg_map, "tileset", i);
        int requestId = cfg_getint(cfg_tileset, "id");
        string tilesetFilename = cfg_getstr(cfg_tileset, "file");

        if(requestId == -1 || tilesetFilename.length() == 0)
            return false;

        cout << "id + file: " << requestId << " - " << tilesetFilename << endl;
        int actualId = mTilesetManager->loadTileset(mGLWidget, tileWidth, tileHeight, tilesetFilename);

        if(actualId != -1)
            mTilesetConverter.push_back(tilesetConverter(requestId, actualId));
    }

    for(i = 0; i < cfg_size(cfg_map, "layer"); i++)
    {
        cfg_layer = cfg_getnsec(cfg_map, "layer", i);
        int height = cfg_getint(cfg_layer, "height");
        int currx = 0, curry = 0;

        if(height == -1)
            return false;

        for(j = 0; j < cfg_size(cfg_layer, "tile"); j++)
        {
            cfg_tile = cfg_getnsec(cfg_layer, "tile", j);
            int tilesetId = cfg_getint(cfg_tile, "tilesetid");
            int tile = cfg_getint(cfg_tile, "tileid");

            if(tilesetId == -1)
                continue;

            cTileset *tempTileset = mTilesetManager->findTileset(findActualId(mTilesetConverter, tilesetId));

            if(tempTileset == NULL)
                continue;

            cout << "tile: " << tile << " - " << id << " - " << currx << " - " << curry << " - " << tilesetId << " - " << tileWidth << " - " << tileHeight << endl;

            mTileManager->addTile(tile, height, id, QPoint(currx*tileWidth, curry*tileHeight), tempTileset);

            if(++currx >= mapx)
            {
                currx = 0;
                curry++;
            }
        }
    }

    free(cfg);

    cout << "That's it. I'm dead." << endl;

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

        if(tiles[j]->getTile() == -1)
            continue;

        if(pos.x() >= lx && pos.x() <= rx &&
           pos.y() >= ty && pos.y() <= by)
        {
            mGLWidget->drawImage(tiles[j]->getTileset()->getTextureId(tiles[j]->getTile()), pos.x() - cam.x(), pos.y() - cam.y(), tileWidth, tileHeight);
        }
    }
}
