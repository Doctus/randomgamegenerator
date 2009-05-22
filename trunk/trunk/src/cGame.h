#ifndef CGAME_GUARD
#define CGAME_GUARD

#include <QtGui/QWidget>

class cGame;

#include "cMap.h"
#include "cTileManager.h"
#include "cTilesetManager.h"
#include "Widgets/MenuBar.h"
#include "Widgets/DockWidgets.h"

using namespace std;

class cGame : public QObject
{
    Q_OBJECT;

    private:
    cMap *mCurrentMap;
    cTileManager *mTileManager;
    cTilesetManager *mTilesetManager;
    cMenuBar *mMenuBar;
    GLWidget *mGLWidget;
    cDockWidgets *mDockWidgets;

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
    void showTextDockWidget();
};

#endif
