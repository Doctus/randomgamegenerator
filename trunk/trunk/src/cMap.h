#ifndef MAP_GUARD
#define MAP_GUARD

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <libconfig.h++>

class cMap;

#include "cTilesetManager.h"
#include "cTileManager.h"
#include "cEventManager.h"
#include "cCamera.h"
#include "Widgets/GLWidget.h"

using namespace libconfig;
using namespace std;

class cMap
{
    private:
    cTilesetManager *mTilesetManager;
    cTileManager *mTileManager;
    cEventManager *mEventManager;
    vector<int> tilesetIds;
    vector<int> layers;
    int id;
    cCamera *mCamera;
    int tileWidth, tileHeight;
    GLWidget *mGLWidget;

    public:
    cMap(int id, GLWidget *mGLWidget, cTileManager *tileManager, cTilesetManager *tilesetManager);
    ~cMap();

    bool loadMap(string filename);
    void draw();
    void logic();
};

#endif

