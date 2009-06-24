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


#ifndef DOCKWIDGETS_H
#define DOCKWIDGETS_H

#include <QtGui/QMainWindow>
#include <QtGui/QTextEdit>
#include <QtGui/QLineEdit>
#include <QtGui/QDockWidget>
#include <QtGui/QVBoxLayout>
#include <QtCore/QObject>

class wDockWidgets;

#include "../cGame.h"

class wDockWidgets : public QObject
{
    Q_OBJECT;

    private:
    QTextEdit *dockWidgetEditor;
    QLineEdit *dockWidgetLineInput;
    QDockWidget *dockWidget;
    cGame *mGame;

    public:
    wDockWidgets(QMainWindow *mainWindow, cGame *mGame);

    void showTextDockWidgets();
    void insertMessage(QString message);

    private slots:
    void processInput();

    signals:
    void newChatInputSignal(QString msg);
};

#endif // DOCKWIDGETS_H
