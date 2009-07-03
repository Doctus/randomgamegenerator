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
    QRect *rect;
    QString filename;
    GLuint textureId;

    public:
    bImage(int x, int y, int w, int h, int tile, QString filename);
    //virtual ~bImage();

    int getX();
    int getY();
    int getW();
    int getH();
    int getTile();
    QString getFilename();

    void setX(int x);
    void setY(int y);
    void setW(int w);
    void setH(int h);
    void setTile(int tile);

    //librandom-game-generator only
    GLuint getTextureId();
    void setTextureId(GLuint id);
    QRect* getRect();
};

#endif // BIMAGE_H
