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

    showTextDockWidget = new QAction(tr("&Text Widget..."), windowWidget);
    showTextDockWidget->setShortcut(tr("Ctrl+T"));
    QAction::connect(showTextDockWidget, SIGNAL(triggered()), this, SLOT(showTextDockWidgetSlot()));

}

void cMenuBar::initBars()
{
    fileMenu = new QMenu(tr("&File"), windowWidget);
    fileMenu->addAction(loadMap);

    viewMenu = new QMenu(tr("&View"), windowWidget);
    viewMenu->addAction(showTextDockWidget);

    QMenuBar *bar = ((QMainWindow*)windowWidget)->menuBar();
    bar->addMenu(fileMenu);
    bar->addMenu(viewMenu);
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

void cMenuBar::showTextDockWidgetSlot()
{
    mGame->showTextDockWidget();
}
