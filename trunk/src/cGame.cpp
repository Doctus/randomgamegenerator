#include "cGame.h"
//#include "cGame.moc" //this is not needed? Qmake handles this itself?

unsigned int FPScounter = 0;

cGame::cGame(QWidget *parent) : QObject(parent)
{
    mGLWidget = new GLWidget(parent);
    ((QMainWindow*)parent)->setCentralWidget(mGLWidget);

    mMenuBar = new cMenuBar(parent, this);

    mDockWidgets = new cDockWidgets((QMainWindow*)parent);

    mTileManager = new cTileManager();
    mTilesetManager = new cTilesetManager();
    mCurrentMap = new cMap(0, mGLWidget, mTileManager, mTilesetManager);
    //mCurrentMap->loadMap("Example.cfg");

    QTimer *timer = new QTimer(this);
    QTimer *timer2 = new QTimer(this);
    QTimer *timer3 = new QTimer(this);
    connect(timer , SIGNAL(timeout()), this, SLOT(draw()));
    connect(timer2, SIGNAL(timeout()), this, SLOT(logic()));
    connect(timer3, SIGNAL(timeout()), this, SLOT(displayFPS()));
    timer ->start(40);
    timer2->start(20);
    timer3->start(5000);
}

cGame::~cGame()
{
    delete mTileManager;
    delete mTilesetManager;
}

void cGame::draw()
{
    if(mCurrentMap != NULL)
        mCurrentMap->draw();

    mGLWidget->updateGL();

    FPScounter++;
}

void cGame::logic()
{
    if(mCurrentMap != NULL)
        mCurrentMap->logic();
}

void cGame::displayFPS()
{
    cout << FPScounter << " frames per 5 seconds" << endl;
    FPScounter = 0;
}


void cGame::loadMap(string fileName)
{
    mCurrentMap->loadMap(fileName);
}

void cGame::saveMap(string fileName)
{
}

void cGame::showTextDockWidget()
{
    this->mDockWidgets->showTextDockWidgets();
}

