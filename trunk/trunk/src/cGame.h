#ifndef CGAME_GUARD
#define CGAME_GUARD

#include <QtGui/QWidget>

class cGame;

#include "cMap.h"
#include "cTileManager.h"
#include "cTilesetManager.h"
#include "Widgets/MenuBar.h"

using namespace std;

class cGame : public QObject
{
    Q_OBJECT;

    private:
    cMap *mCurrentMap;
    cTileManager *mTileManager;
    cTilesetManager *mTilesetManager;
    cMenuBar *mMenuBar;

    QWidget *parent;
    GLWidget *mGLWidget;

    friend class cMenuBar;

    public:
    cGame(QWidget *parent);
    ~cGame();

    private slots:
    void draw();
    void logic();
    void displayFPS();

    public:
    void loadMap(string fileName);
    void saveMap(string fileName);
};

#endif
