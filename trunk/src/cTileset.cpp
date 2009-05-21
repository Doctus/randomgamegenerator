#include "cTileset.h"

#include <iostream>

cTileset::cTileset(int id, GLWidget *mGLWidget, int tileWidth, int tileHeight, string filename)
{
    this->id = id;
    this->mGLWidget = mGLWidget;

    this->tileWidth = tileWidth;
    this->tileHeight = tileHeight;
    this->filename = filename;

    loadImage();
}

cTileset::~cTileset()
{
    int tile = 0;
    for(int y = 0; y < image->height(); y += tileHeight)
    {
        for(int x = 0; x < image->width(); x += tileWidth)
        {
            mGLWidget->deleteTexture(textureIds[tile]);
            tile++;
        }
    }

    if(image != NULL)
        delete image;
}


int cTileset::getId()
{
    return id;
}

int cTileset::getTileWidth()
{
    return tileWidth;
}

int cTileset::getTileHeight()
{
    return tileHeight;
}


string cTileset::getFilename()
{
    return filename;
}


GLuint cTileset::getTextureId(int tile)
{
    return textureIds[tile];
}


void cTileset::loadImage()
{
    image = new QImage(filename.c_str());

    int tile = 0;
    for(int y = 0; y < image->height(); y += tileHeight)
    {
        for(int x = 0; x < image->width(); x += tileWidth)
        {
            QRect rect(x, y, tileWidth, tileHeight);
            QImage texture = image->copy(rect);

            try
            {
                textureIds.insert(pair<unsigned int, GLuint>(tile, mGLWidget->createTexture(&texture)));
            }
            catch (...)
            {
                //add handling here?
                throw;
                return;
            }
            tile++;
        }
    }
}


