#include <QtGui/QApplication>

#include "cGame.h"

#include <libconfig.h++>

int main(int argc, char** argv)
{
    QApplication app(argc, argv);

    QMainWindow *widget = new QMainWindow(); //parent widget
    widget->resize(640, 480);

    cGame *mGame = new cGame(widget);

    widget->show();

    return app.exec();
}

