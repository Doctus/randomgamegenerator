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


#include "cTilesetManager.h"

cTilesetManager::cTilesetManager(wGLWidget *mGLWidget)
{
    id = 0;
    this->mGLWidget = mGLWidget;
}

cTileset* cTilesetManager::loadTileset(int tileWidth, int tileHeight, string filename)
{
    id++;
    cTileset* set = findTileset(filename, tileWidth, tileHeight);

    if(set != NULL)
        return set;

    try
    {
        set = new cTileset(id, mGLWidget, tileWidth, tileHeight, filename);
        tilesets.push_back(set);
    }
    catch (...) //this needs to be handled better than just catching any and all exception...although it works <_<
    {
        id--;
    }

    return set;
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

int cTilesetManager::getTilesetId(string filename, int tileWidth, int tileHeight)
{
    cTileset *set = findTileset(filename, tileWidth, tileHeight);

    if(set != NULL)
        return set->getId();

    return -1;
}

cTileset* cTilesetManager::findTileset(string filename, int tileWidth, int tileHeight)
{
    for(unsigned int i = 0; i < tilesets.size(); i++)
    {
        if(tilesets[i]->getFilename() == filename && tilesets[i]->getTileWidth() == tileWidth && tilesets[i]->getTileHeight() == tileHeight)
            return tilesets[i];
    }

    return NULL; //exception?
}

vector<cTileset*> cTilesetManager::findTilesets(string filename)
{
    vector<cTileset*> sets;

    for(unsigned int i = 0; i < tilesets.size(); i++)
    {
        if(tilesets[i]->getFilename() == filename)
            sets.push_back(tilesets[i]);
    }

    return sets; //exception?
}


void cTilesetManager::addImage(bImage* img, int layer)
{
    vector<cTileset*> sets = findTilesets(img->getFilename().toStdString());
    cTileset* set = NULL;
    bool triedSetting = false;

    if(sets.size() == 0)
    {
        set = loadTileset(img->getW(), img->getH(), img->getFilename().toStdString()); //this can still return NULL.
        triedSetting = true;
    }
    else
    {
        for(unsigned i = 0; i < sets.size(); i++)
        {
            cTileset* tempset = sets[i];
            if(tempset->getTileWidth() == img->getW() || tempset->getTileHeight() == img->getH())
                set = tempset;
        }
    }

    if(set == NULL && !triedSetting)
        set = loadTileset(img->getW(), img->getH(), img->getFilename().toStdString()); //this can still return NULL.

    if(set != NULL)
    {
        img->setTextureId(set->getTextureId(img->getTile()));

        while(layer >= int(images.size()))
        {
            images.push_back(vector<bImage*>());
        }

        images[layer].push_back(img);
    }
}

void cTilesetManager::removeImage(bImage* img, int layer)
{
    for(uint i = 0; i < images[layer].size(); i++)
    {
        if(images[layer][i]->getId() == img->getId())
        {
            images[layer].erase(images[layer].begin() + i);
            return;
        }
    }
}

bool cTilesetManager::changeTileOfImage(bImage *img, int tile)
{
    cTileset *set = findTileset(img->getFilename().toStdString(), img->getW(), img->getH());

    if(set != NULL)
    {
        if(tile > set->getHighestTile())
            img->setTextureId(set->getTextureId(0));
        else
            img->setTextureId(set->getTextureId(tile));
        return true;
    }

    return false;
}

void cTilesetManager::changeLayerOfImage(bImage *img, int oldLayer, int newLayer)
{
    removeImage(img, oldLayer);

    if(newLayer > int(images.size())-1)
        images.resize(newLayer+1);
    images[newLayer].push_back(img);
}

void cTilesetManager::changeImage(QString oldFilename, QString newFilename, int tileWidth, int tileHeight)
{
    changeImage(oldFilename.toStdString(), newFilename.toStdString(), tileWidth, tileHeight);
}

void cTilesetManager::changeImage(string oldFilename, string newFilename, int tileWidth, int tileHeight)
{
    cTileset *set = findTileset(oldFilename, tileWidth, tileHeight); //This needs to be changed everywhere, to accomodate for UTF-8 T_T?

    if(set != NULL)
    {
        if(oldFilename == newFilename)
        {
            map<unsigned int, GLuint> textureIds = set->reload();
            if(textureIds.size() > 0)
            {
                foreach(vector<bImage*> layer, images)
                {
                    foreach(bImage *image, layer)
                    {
                        if(image->getTilesetId() == set->id)
                            image->setTextureId(set->getTextureId(image->getTile()));
                    }
                }
            }
        }
    }
}

vector< vector<bImage*> > cTilesetManager::getImages()
{
    return images;
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



