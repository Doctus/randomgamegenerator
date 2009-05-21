#ifndef CGAME_GUARD
#define CGAME_GUARD

#include <QtGui/QWidget>

class cGame;

#include "cMap.h"
#include "cTileManager.h"
#include "cTilesetManager.h"

class cGame : public QObject
{
    Q_OBJECT;

    private:
    cMap *mCurrentMap;
    cTileManager *mTileManager;
    cTilesetManager *mTilesetManager;

    QWidget *parent;
    GLWidget *mGLWidget;

    public:
    cGame(QWidget *parent);
    ~cGame();

    private slots:
    void draw();
    void logic();
    void displayFPS();
};

#endif
