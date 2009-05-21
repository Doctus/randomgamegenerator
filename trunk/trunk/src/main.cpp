#include <QtGui/QApplication>

#include "cGame.h"

int main(int argc, char** argv)
{
    QApplication app(argc, argv);

    QWidget *widget = new QWidget(); //parent widget
    widget->resize(640, 480);

    cGame *mGame = new cGame(widget);

    widget->show();

    return app.exec();
}

