#ifndef MENUBAR_H
#define MENUBAR_H

#include <QtGui/QWidget>
#include <QtCore/QObject>

class cMenuBar;

#include "../cGame.h"

class cMenuBar : public QObject
{
    Q_OBJECT;

    QWidget *windowWidget;
    cGame *mGame;

    QAction *loadMap;
    QAction *saveMap;
    QAction *loadServer; //unused
    QAction *connectServer; //unused
    QAction *showAboutDialog;
    QAction *showTextDockWidget;

    QMenu *fileMenu;
    QMenu *serverMenu;
    QMenu *viewMenu;
    QMenu *helpMenu;

    public:
    cMenuBar(QWidget *windowWidget, cGame *game);

    void initActions();
    void initBars();

    private slots:
    void saveMapSlot();
    void loadMapSlot();
    void showTextDockWidgetSlot();
};

#endif // MENUBAR_H
