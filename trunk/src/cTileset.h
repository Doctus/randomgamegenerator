#ifndef CTILESET_GUARD
#define CTILESET_GUARD

#include <string>
#include <iostream>

#include <QtGui/QImage>
#include <QtCore/QPoint>

class cTileset;

#include "cTilesetManager.h"
#include "cTile.h"
#include "Widgets/GLWidget.h"

using namespace std;

class cTileset
{
    private:
    int id;
    int tileWidth;
    int tileHeight;
    string filename;
    QImage *image;
    GLWidget *mGLWidget;
    map<unsigned int, GLuint> textureIds;

    friend class cTilesetManager;

    cTileset(int id, GLWidget *mGLWidget, int tileWidth, int tileHeight, string filename);
    ~cTileset();

    public:
    int getId();
    int getTileWidth();
    int getTileHeight();
    GLuint getTextureId(int tile);

    string getFilename();

    private:
    void loadImage();
};

#endif

