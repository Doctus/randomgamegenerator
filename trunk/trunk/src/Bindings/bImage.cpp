#include "bImage.h"

#include "../cTilesetManager.h"
#include "../cGame.h"
#include "bMain.h"

int bImage::countId = 0;

bImage::bImage()
{
    x = 0;
    y = 0;
    w = 0;
    h = 0;
    tile = 0;
    layer = 0;
    id = 0;
    filename = "";
}

bImage::bImage(int x, int y, int w, int h, int tile, int layer, QString filename)
{
    this->x = x;
    this->y = y;
    this->w = w;
    this->h = h;
    this->layer = layer;
    id = countId++;
    this->tile = tile;
    this->filename = filename;

    if(bMain::getGameInstance() == NULL)
        cout << "ERROR! ERROR!" << endl << "ERROR! ERROR!" << endl << "ERROR! ERROR!" << endl;

    bMain::getGameInstance()->mTilesetManager->addImage(this, layer);

    //cout << "created image " << id << ":" << filename.toStdString() << endl;
}

bImage::~bImage()
{
    bMain::getGameInstance()->mTilesetManager->removeImage(this, layer);
    //cout << "removed image " << id << ":" << filename.toStdString() << endl;
}

int bImage::getId()
{
    return id;
}

int bImage::getX()
{
    return x;
}

int bImage::getY()
{
    return y;
}

int bImage::getW()
{
    return w;
}

int bImage::getH()
{
    return h;
}

int bImage::getTile()
{
    return tile;
}

int bImage::getLayer()
{
    return layer;
}

QString bImage::getFilename()
{
    return filename;
}


void bImage::setX(int x)
{
    this->x = x;
}

void bImage::setY(int y)
{
    this->y = y;
}

void bImage::setW(int w)
{
    this->w = w;
}

void bImage::setH(int h)
{
    this->h = h;
}

void bImage::setTile(int tile)
{
    if(bMain::getGameInstance()->mTilesetManager->changeTileOfImage(this, tile))
        this->tile = tile;
}

void bImage::setLayer(int layer)
{
    if(layer < 0)
        return;

    bMain::getGameInstance()->mTilesetManager->changeLayerOfImage(this, this->layer, layer);
    this->layer = layer;
}


GLuint bImage::getTextureId()
{
    return textureId;
}

void bImage::setTextureId(GLuint textureId)
{
    this->textureId = textureId;
}

QRect bImage::getRect()
{
    return QRect(x, y, w, h);
}
