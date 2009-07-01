#include "bImage.h"

#include "../cTilesetManager.h"
#include "../cGame.h"
#include "bMain.h"

bImage::bImage(int x, int y, int w, int h, int tile, QString filename)
{
    this->x = x;
    this->y = y;
    this->w = w;
    this->h = h;
    this->tile = tile;
    this->filename = filename;

    if(bMain::getGameInstance() == NULL)
        cout << "ERROR! ERROR!" << endl << "ERROR! ERROR!" << endl << "ERROR! ERROR!" << endl;

    bMain::getGameInstance()->mTilesetManager->addImage(this);
}

/*bImage::~bImage()
{
    cout << "killing image?" << endl;
}*/

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
