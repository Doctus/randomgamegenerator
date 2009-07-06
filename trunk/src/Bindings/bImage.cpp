#include "bImage.h"

#include "../cTilesetManager.h"
#include "../cGame.h"
#include "bMain.h"

int bImage::countId = 0;

bImage::bImage(int x, int y, int w, int h, int tile, QString filename)
{
    rect = new QRect(x, y, w, h);
    id = countId++;
    this->tile = tile;
    this->filename = filename;

    if(bMain::getGameInstance() == NULL)
        cout << "ERROR! ERROR!" << endl << "ERROR! ERROR!" << endl << "ERROR! ERROR!" << endl;

    bMain::getGameInstance()->mTilesetManager->addImage(this);
}

bImage::~bImage()
{
    bMain::getGameInstance()->mTilesetManager->removeImage(this);
}

int bImage::getId()
{
    return id;
}

int bImage::getX()
{
    return rect->x();
}

int bImage::getY()
{
    return rect->y();
}

int bImage::getW()
{
    return rect->width();
}

int bImage::getH()
{
    return rect->height();
}

int bImage::getTile()
{
    return tile;
}

QString bImage::getFilename()
{
    return filename;
}


void bImage::setX(int x)
{
    rect->setX(x);
}

void bImage::setY(int y)
{
    rect->setY(y);
}

void bImage::setW(int w)
{
    rect->setWidth(w);
}

void bImage::setH(int h)
{
    rect->setHeight(h);
}

void bImage::setTile(int tile)
{
    if(bMain::getGameInstance()->mTilesetManager->changeTileOfImage(this, tile))
        this->tile = tile;
}


GLuint bImage::getTextureId()
{
    return textureId;
}

void bImage::setTextureId(GLuint textureId)
{
    this->textureId = textureId;
}

QRect* bImage::getRect()
{
    return rect;
}
