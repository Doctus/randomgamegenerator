#ifndef MENUBAR_H
#define MENUBAR_H

#include <QtGui>
#include <QtCore>

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

    QMenu *fileMenu;
    QMenu *serverMenu;
    QMenu *helpMenu;

    public:
    cMenuBar(QWidget *windowWidget, cGame *game);

    void initActions();
    void initBars();

    private slots:
    void saveMapSlot();
    void loadMapSlot();
};

#endif // MENUBAR_H
