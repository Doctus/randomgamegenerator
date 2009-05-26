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

#ifdef _WINDOWS
  #define GL_TEXTURE_RECTANGLE_ARB 0x84F5 //HAR HAR. VEE BE EVUL. VEE IS NUT CHECKING IF IT IS SUPPORTED ON PLATFORM.
#endif

#include <iostream>

using namespace std;

class wGLWidget : public QGLWidget
{
    public:
    wGLWidget(QWidget* parent);

    void initializeGL();
    void paintGL();
    void drawImage(QImage *originalImage, int x, int y);
    void drawImage(GLuint texture, int x, int y, int w, int h);
    void resizeGL(int w, int h);

    GLuint createTexture(QImage *image);
    void deleteTexture(GLuint texture);
};

#endif
