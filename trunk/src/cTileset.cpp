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


#include "cTileset.h"

#include <iostream>

cTileset::cTileset(int id, wGLWidget *mGLWidget, int tileWidth, int tileHeight, string filename)
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

            cout << "Creating texture from " << filename << " at (" << x << "," << y << ")" << endl;

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


