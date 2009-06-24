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


#include "wDockWidgets.h"

wDockWidgets::wDockWidgets(QMainWindow *mainWindow, cGame *mGame) : QObject(mainWindow)
{
    this->mGame = mGame;

    dockWidgetEditor = new QTextBrowser(mainWindow);
    dockWidgetLineInput = new QLineEdit(mainWindow);
    dockWidget = new QDockWidget(QObject::tr("Dock Widget"), mainWindow);

    dockWidgetEditor->setReadOnly(true);
    dockWidgetEditor->setOpenLinks(false);

    QWidget *dockWidgetContents = new QWidget(mainWindow);
    QVBoxLayout *layout = new QVBoxLayout(dockWidgetContents);

    layout->addWidget(dockWidgetEditor);
    layout->addWidget(dockWidgetLineInput);

    dockWidget->show();
    dockWidget->setAllowedAreas(Qt::LeftDockWidgetArea |
                                 Qt::BottomDockWidgetArea);
    dockWidget->setWidget(dockWidgetContents);
    mainWindow->addDockWidget(Qt::LeftDockWidgetArea, dockWidget);

    QObject::connect((QObject*)dockWidgetLineInput, SIGNAL(returnPressed()), (QObject*)this, SLOT(processInput()));
}

void wDockWidgets::showTextDockWidgets()
{
    dockWidget->show();
}

void wDockWidgets::insertMessage(QString message)
{
    bool scroll = (dockWidgetEditor->verticalScrollBar()->value() == dockWidgetEditor->verticalScrollBar()->maximum()) ?
                    true : false;

    dockWidgetEditor->insertHtml(message + "<br />");

    if(scroll)
        dockWidgetEditor->verticalScrollBar()->setValue(dockWidgetEditor->verticalScrollBar()->maximum());
}

void wDockWidgets::processInput()
{
    QString str = dockWidgetLineInput->text();
    dockWidgetLineInput->clear();
    emit newChatInputSignal(str);
}
