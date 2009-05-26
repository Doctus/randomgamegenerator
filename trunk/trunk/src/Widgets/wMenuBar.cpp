/*
Random Game Generator - The generation of time transcending tabletop games!
Copyright (C) 2009 Michael de Lang

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/


#include "wMenuBar.h"

wMenuBar::wMenuBar(QWidget *windowWidget, cGame *game)
{
    this->windowWidget = windowWidget;
    this->mGame = game;
    mConnectionManager = new nConnectionManager(windowWidget);

    initActions();
    initBars();
}

void wMenuBar::initActions()
{
    loadMap = new QAction(tr("&Load Map..."), windowWidget);
    loadMap->setShortcut(tr("Ctrl+L"));
    QAction::connect(loadMap, SIGNAL(triggered()), this, SLOT(loadMapSlot()));

    showTextDockWidget = new QAction(tr("&Text Widget"), windowWidget);
    showTextDockWidget->setShortcut(tr("Ctrl+T"));
    QAction::connect(showTextDockWidget, SIGNAL(triggered()), this, SLOT(showTextDockWidgetSlot()));

    hostServer = new QAction(tr("&Host Server"), windowWidget);
    hostServer->setShortcut(tr("Ctrl+H"));
    QAction::connect(hostServer, SIGNAL(triggered()), this, SLOT(hostServerSlot()));

    connectToServer = new QAction(tr("&Connect to Server"), windowWidget);
    connectToServer->setShortcut(tr("Ctrl+C"));
    QAction::connect(connectToServer, SIGNAL(triggered()), this, SLOT(connectToServerSlot()));

}

void wMenuBar::initBars()
{
    fileMenu = new QMenu(tr("&File"), windowWidget);
    fileMenu->addAction(loadMap);

    internetMenu = new QMenu(tr("&Internet"), windowWidget);
    internetMenu->addAction(hostServer);
    internetMenu->addAction(connectToServer);

    viewMenu = new QMenu(tr("&View"), windowWidget);
    viewMenu->addAction(showTextDockWidget);

    QMenuBar *bar = ((QMainWindow*)windowWidget)->menuBar();
    bar->addMenu(fileMenu);
    bar->addMenu(internetMenu);
    bar->addMenu(viewMenu);
}


void wMenuBar::saveMapSlot()
{
}

void wMenuBar::loadMapSlot()
{
    QString fileName = QFileDialog::getOpenFileName(windowWidget, tr("Open File"), QDir::currentPath());

    if (!fileName.isEmpty())
    {
        mGame->loadMap(fileName.toStdString());
    }
}

void wMenuBar::showTextDockWidgetSlot()
{
    mGame->showTextDockWidget();
}


void wMenuBar::hostServerSlot()
{
    bool okStuff = false;
    int port = QInputDialog::getInt(windowWidget, "Port", "Which port to host on?", 6812, 1025, 65535, 1, &okStuff);

    if(!okStuff)
        return;

    mConnectionManager->startServer(port);
}

void wMenuBar::connectToServerSlot()
{
    bool okStuff = false;
    QString host = QInputDialog::getText(windowWidget, "Host", "Which host to connect to?", QLineEdit::Normal, "localhost", &okStuff);

    if(!okStuff)
        return;

    int port = QInputDialog::getInt(windowWidget, "Port", "Which port to use?", 6812, 1025, 65535, 1, &okStuff);

    if(!okStuff)
        return;

    mConnectionManager->connectTo(host, port);
}
