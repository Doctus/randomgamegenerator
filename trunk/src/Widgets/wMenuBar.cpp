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

wMenuBar::wMenuBar(QWidget *windowWidget, cGame *game, nConnectionManager *mConnectionManager)
{
    this->windowWidget = windowWidget;
    this->mGame = game;
    this->mConnectionManager = mConnectionManager;

    initActions();
    initBars();
}

void wMenuBar::initActions()
{
    newMap = new QAction(tr("&New Map..."), windowWidget);
    newMap->setShortcut(tr("Ctrl+N"));
    QAction::connect(newMap, SIGNAL(triggered()), this, SLOT(newMapSlot()));

    loadMap = new QAction(tr("&Load Map..."), windowWidget);
    loadMap->setShortcut(tr("Ctrl+L"));
    QAction::connect(loadMap, SIGNAL(triggered()), this, SLOT(loadMapSlot()));

    saveMap = new QAction(tr("&Save Map..."), windowWidget);
    saveMap->setShortcut(tr("Ctrl+S"));
    QAction::connect(saveMap, SIGNAL(triggered()), this, SLOT(saveMapSlot()));

    hostServer = new QAction(tr("&Host Server"), windowWidget);
    hostServer->setShortcut(tr("Ctrl+H"));
    QAction::connect(hostServer, SIGNAL(triggered()), this, SLOT(hostServerSlot()));

    connectToServer = new QAction(tr("Co&nnect to Server"), windowWidget);
    connectToServer->setShortcut(tr("Ctrl+J"));
    QAction::connect(connectToServer, SIGNAL(triggered()), this, SLOT(connectToServerSlot()));
}

void wMenuBar::initBars()
{
    fileMenu = new QMenu(tr("&File"), windowWidget);
    fileMenu->addAction(newMap);
    fileMenu->addAction(loadMap);
    fileMenu->addAction(saveMap);

    internetMenu = new QMenu(tr("&Internet"), windowWidget);
    internetMenu->addAction(hostServer);
    internetMenu->addAction(connectToServer);

    QMenuBar *bar = ((QMainWindow*)windowWidget)->menuBar();
    bar->addMenu(fileMenu);
    bar->addMenu(internetMenu);

    bar->addSeparator();
}

void wMenuBar::newMapSlot()
{
    emit newMapSignal();
}

void wMenuBar::saveMapSlot()
{
    QString fileName = QFileDialog::getSaveFileName(windowWidget, tr("Save File"), QDir::currentPath());

    if(!fileName.isEmpty())
    {
        emit saveMapSignal(fileName);
    }
}

void wMenuBar::loadMapSlot()
{
    QString fileName = QFileDialog::getOpenFileName(windowWidget, tr("Open File"), QDir::currentPath());

    if(!fileName.isEmpty())
    {
        emit loadMapSignal(fileName);
    }
}


void wMenuBar::hostServerSlot()
{
    bool okStuff = false;
    QString handle = QInputDialog::getText(windowWidget, tr("Name"), tr("Which handle are you going to use?"), QLineEdit::Normal, tr("Host"), &okStuff);

    if(!okStuff) //if user pressed cancel
        return;

    int port = QInputDialog::getInt(windowWidget, tr("Port"), tr("Which port to host on?"), 6812, 1025, 65535, 1, &okStuff);

    if(!okStuff)
        return;

    mConnectionManager->startServer(port, handle);
}

void wMenuBar::connectToServerSlot()
{
    bool okStuff = false;
    QString handle = QInputDialog::getText(windowWidget, tr("Name"), tr("Which handle are you going to use?"), QLineEdit::Normal, tr("Guest"), &okStuff);

    if(!okStuff) //if user pressed cancel
        return;

    QString host = QInputDialog::getText(windowWidget, tr("Host"), tr("Which host to connect to?"), QLineEdit::Normal, "localhost", &okStuff);

    if(!okStuff)
        return;

    int port = QInputDialog::getInt(windowWidget, tr("Port"), tr("Which port to use?"), 6812, 1025, 65535, 1, &okStuff);

    if(!okStuff)
        return;

    mConnectionManager->connectTo(host, port, handle);
}
