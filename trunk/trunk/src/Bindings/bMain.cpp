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

#include "bMain.h"

#include "../cGame.h"

int i = 1;
char *argv[] = {"random game generator"};

QApplication app(i, argv, 0);
QMainWindow *widget;
cGame* bMain::mainGame;

bMain::bMain()
{
    widget = new QMainWindow(); //parent widget
    widget->resize(640, 480);

    QTextCodec::setCodecForTr(QTextCodec::codecForName("utf8"));
    QString locale = QLocale::system().name();
    //QString locale = "nl";
    locale.truncate(2);

    cout << "locale: " << locale.toStdString() << endl;

    QTranslator *t = new QTranslator(widget);
    QTranslator *t2 = new QTranslator(widget);

    if(!t->load(QString("rgg_") + locale))
        cout << "rgg_" << locale.toStdString() << " failed to load" << endl;
    else
        cout << "rgg_" << locale.toStdString() << " loaded" << endl;
    if(!t2->load(QString("rgg_py_") + locale))
        cout << "rgg_py_" << locale.toStdString() << " failed to load" << endl;
    else
        cout << "rgg_py_" << locale.toStdString() << " loaded" << endl;

    app.installTranslator(t);
    app.installTranslator(t2);

    QIcon *icon = new QIcon("./data/FAD-icon.png");

    widget->setWindowIcon(*icon);

    mainGame = new cGame(widget);

    cout << "mainGame initialised" << endl;

    connect(mainGame->mGLWidget, SIGNAL(mouseReleaseSignal(int,int,int)), this, SLOT(mouseReleaseTrigger(int,int,int)));
    connect(mainGame->mGLWidget, SIGNAL(mousePressSignal(int,int,int)), this, SLOT(mousePressTrigger(int,int,int)));
    connect(mainGame->mGLWidget, SIGNAL(mouseMoveSignal(int,int)), this, SLOT(mouseMoveTrigger(int,int)));
}

void bMain::start()
{
    widget->show();

    app.exec();

    return;
}

cGame* bMain::getGameInstance()
{
    return mainGame;
}

/*
  This function might leak some buttons. Hrm.
 */
int bMain::displayUserDialogChoice(QString text, QVector<QString> buttonTexts, int defaultButton)
{
    if(buttonTexts.size() == 0)
        return -1;

    QVector<QPushButton*> buttons;

    QMessageBox questionDialog(widget);
    questionDialog.setText(text);

    for(int j = buttonTexts.size() - 1; j >= 0; j--)
    {
        QPushButton *newButton = questionDialog.addButton(buttonTexts[j], QMessageBox::AcceptRole);
        buttons.push_front(newButton);
        if(j == defaultButton)
            questionDialog.setDefaultButton(newButton);
    }

    questionDialog.exec();

    int i = 0;

    foreach(QPushButton *button, buttons)
    {
        if(questionDialog.clickedButton() == button)
            return i;
        i++;
    }

    return -1;
}

/*
  This function might also leak. Some Actions this time.
*/
int bMain::showPopupMenuAt(int x, int y, QVector<QString> actionTexts)
{
    QMenu *popup = new QMenu((QWidget*)mainGame->parent());
    int idCounter = 0;

    foreach(QString str, actionTexts)
    {
        popup->addAction(new wAction(str, (QWidget*)mainGame->parent(), idCounter++));
    }

    int realx = x + ((QWidget*)mainGame->parent())->x() + mainGame->mGLWidget->x();
    int realy = y + ((QWidget*)mainGame->parent())->y() + mainGame->mGLWidget->y();
    wAction *selectedAction = (wAction*)popup->exec(QPoint(realx, realy));

    if(selectedAction == 0)
        return -1;

    return selectedAction->getId();
}

int bMain::showPopupMenuAtAbs(int x, int y, QVector<QString> actionTexts)
{
    QMenu *popup = new QMenu((QWidget*)mainGame->parent());
    int idCounter = 0;

    foreach(QString str, actionTexts)
    {
        popup->addAction(new wAction(str, (QWidget*)mainGame->parent(), idCounter++));
    }

    wAction *selectedAction = (wAction*)popup->exec(QPoint(x, y));

    if(selectedAction == 0)
        return -1;

    return selectedAction->getId();
}

void bMain::displayTooltip(QString text, int x, int y)
{
    QWidget *w = (QWidget*)mainGame->parent();
    QToolTip::showText(QPoint(x+w->x()+mainGame->mGLWidget->x(), y+w->y()+mainGame->mGLWidget->y()), text, w);
}

/*void bMain::removeTooltip(int id)
{
}*/

QString bMain::getUserTextInput(QString question)
{
     QString text = QInputDialog::getText((QWidget*)mainGame->parent(), "Input", question);
     return text;
}


QMainWindow* bMain::getMainWindow()
{
    return widget;
}


int bMain::getCamX()
{
    return mainGame->mGLWidget->cam->getCam().x();
}

int bMain::getCamY()
{
    return mainGame->mGLWidget->cam->getCam().y();
}

int bMain::getCamW()
{
    return mainGame->mGLWidget->cam->getAbsoluteBounds(getZoom()).x();
}

int bMain::getCamH()
{
    return mainGame->mGLWidget->cam->getAbsoluteBounds(getZoom()).y();
}


void bMain::setCam(int x, int y)
{
    mainGame->mGLWidget->cam->setCam(QPoint(x, y));
}

void bMain::adjustCam(int x, int y)
{
    mainGame->mGLWidget->cam->adjustCam(x, y);
}


void bMain::setZoom(float zoom)
{
    mainGame->mGLWidget->setZoom(zoom);
}

float bMain::getZoom()
{
    return mainGame->mGLWidget->getZoom();
}


void bMain::changeImage(QString oldFilename, QString newFilename, int tileWidth, int tileHeight)
{
    mainGame->mTilesetManager->changeImage(oldFilename, newFilename, tileWidth, tileHeight);
}

int bMain::getTileCountOfImage(QString filename, int tileWidth, int tileHeight)
{
    cTileset *set = mainGame->mTilesetManager->findTileset(filename.toStdString(), tileWidth, tileHeight);

    if(set != NULL)
        return set->getHighestTile();

    return -1;
}

void bMain::addLine(int x, int y, int w, int h, int thickness)
{
    mainGame->mShapeManager->addLine(x, y, w, h, thickness);
}

void bMain::deleteLine(int x, int y, int w, int h, int thickness)
{
    mainGame->mShapeManager->removeLine(x, y, w, h, thickness);
}

void bMain::clearLines()
{
    mainGame->mShapeManager->clearLines();
}

QVector<QRect> bMain::getLineOfThickness(int thickness)
{
    if(thickness < 1)
        thickness = 1;
    if(thickness > 3)
        thickness = 3;
    QVector<QRect> rects = mainGame->mShapeManager->getLines()[thickness-1];
    //cout << "size: " << rects.size() << endl;
    return rects;
}

/* This is a wonderful idea, but it requires all widgets using tr() to re-implement changeEvent
 * and check if a LanguageChange event comes by. If so, re-translate every tr() by
 * calling widget->setText() on everything that requires re-translation. *sigh*
 */

/*void bMain::addTranslationFile(QString filename)
{
    QTranslator *t = new QTranslator(widget);
    bool val = t->load(filename);
    cout << "addTranslationFile: " << val << endl;
    app.installTranslator(t);
}

void bMain::removeTranslationFile(QString filename)
{
    QTranslator *t = new QTranslator(widget);
    bool val = t->load(filename);
    cout << "removeTranslationFile: " << val << endl;
    app.removeTranslator(t);
}*/


void bMain::mouseMoveTrigger(int x, int y)
{
    emit mouseMoveSignal(x, y);
}

void bMain::mousePressTrigger(int x, int y, int type)
{
    emit mousePressSignal(x, y, type);
}

void bMain::mouseReleaseTrigger(int x, int y, int type)
{
    emit mouseReleaseSignal(x, y, type);
}

void bMain::leaveEventTrigger()
{
    emit leaveEventSignal();
}

void bMain::enterEventTrigger()
{
    emit enterEventSignal();
}
