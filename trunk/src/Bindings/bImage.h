#ifndef BIMAGE_H
#define BIMAGE_H

#include <QtOpenGL/QtOpenGL>
#include <QtCore/QString>
#include <QtCore/QRect>

using namespace std;

class bImage
{
    private:
    int tile;
    static int countId;
    int id;
    int x, y, w, h;
    int layer;
    bool isDestroyed;
    QString filename;
    int tilesetId;
    GLuint textureId;

    bImage();

    public:
    bImage(int x, int y, int w, int h, int tile, int layer, QString filename);
    ~bImage();

    int getId();
    int getX();
    int getY();
    int getW();
    int getH();
    int getTile();
    int getLayer();
    QString getFilename();
    int getTilesetId();

    void setX(int x);
    void setY(int y);
    void setW(int w);
    void setH(int h);
    void setTile(int tile);
    void setLayer(int layer);

    //librandom-game-generator only
    GLuint getTextureId();
    void setTextureId(GLuint id);
    QRect getRect();

    void DELETEME();
};

#endif // BIMAGE_H
