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


#ifndef wGLWidget_H
#define wGLWidget_H

#include <QtOpenGL/QtOpenGL>
#include <QtGui/QImage>
#include <QtCore/QRect>
#include <QtGui/QMouseEvent>
#include <QtGui/QToolTip>

#include <iostream>

class wGLWidget;

#include "../cCamera.h"
#include "../cGame.h"
#include "../cShapeManager.h"
#include "../Bindings/bImage.h"
#include "../Bindings/bMain.h"

using namespace std;

class wGLWidget : public QGLWidget
{
    Q_OBJECT;

    private:
    cCamera *cam;
    cGame *mGame;
    int lastx, lasty;
    float zoom;
    bool shiftHeld, ctrlHeld;
    bool mouseButtonHeld;
    //QVector<QTooltip*> tooltips;

    friend class bMain;

    public:
    wGLWidget(QWidget* parent, cGame *mGame);

    void initializeGL();
    void paintGL();
    void drawImage(GLuint texture, int x, int y, int textureW, int textureH, int drawW, int drawH);
    void resizeGL(int w, int h);

    GLuint createTexture(QImage *image);
    void redrawTexture(QImage *image, GLuint texture);
    void deleteTexture(GLuint texture);

    void  setZoom(float zoom);
    float getZoom();

    protected:
    void mouseMoveEvent(QMouseEvent *event);
    void mousePressEvent(QMouseEvent *event);
    void mouseReleaseEvent(QMouseEvent *event);

    void keyPressEvent(QKeyEvent *event);
    void keyReleaseEvent(QKeyEvent *event);

    void wheelEvent(QWheelEvent *event);

    void leaveEvent(QEvent *event);
    void enterEvent(QEvent *event);

    signals:
    void mouseMoveSignal(int x, int y);
    void mousePressSignal(int x, int y, int type);
    void mouseReleaseSignal(int x, int y, int type);

    void leaveSignal();
    void enterSignal();
};

#endif
