#include "MenuBar.h"

cMenuBar::cMenuBar(QWidget *windowWidget, cGame *game)
{
    this->windowWidget = windowWidget;
    this->mGame = game;

    initActions();
    initBars();
}

void cMenuBar::initActions()
{
    loadMap = new QAction(tr("&Load Map..."), windowWidget);
    loadMap->setShortcut(tr("Ctrl+L"));
    QAction::connect(loadMap, SIGNAL(triggered()), this, SLOT(loadMapSlot()));

}

void cMenuBar::initBars()
{
    fileMenu = new QMenu(tr("&File"), windowWidget);
    fileMenu->addAction(loadMap);

    QMenuBar *bar = ((QMainWindow*)windowWidget)->menuBar();
    bar->addMenu(fileMenu);
}


void cMenuBar::saveMapSlot()
{
}

void cMenuBar::loadMapSlot()
{
    QString fileName = QFileDialog::getOpenFileName(windowWidget, tr("Open File"), QDir::currentPath());

    if (!fileName.isEmpty())
        mGame->loadMap(fileName.toStdString());
}
