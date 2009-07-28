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


#include "wGLWidget.h"

#ifdef _WINDOWS
  #define GL_TEXTURE_RECTANGLE_ARB GL_TEXTURE_2D //This abolishes POT textures, but at least it works! (god damn microsoft and its shitty products)
#endif

std::string translateGLError(GLenum errorcode)
{
  std::string errorStr = (char*)gluErrorString(errorcode);
  return errorStr;
}

//QwGLWidget doesn't do Alpha by default(and neither does it do DoubleBuffering, I think), so I forced it.
wGLWidget::wGLWidget(QWidget* parent, cGame *mGame) : QGLWidget(QGLFormat(QGL::FormatOptions(QGL::DoubleBuffer | QGL::AlphaChannel)), parent)
{
    this->mGame = mGame;
    selectedIcon = IconType::select;
    cam = new cCamera(0, 0, 640, 480);
    ctrlHeld = false;
    shiftHeld = false;
    zoom = 1;

    resize(parent->width(), parent->height());

    setSizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
    setFocusPolicy(Qt::StrongFocus);

    //OpenGL is initialized here, instead of somewhere inside Qt4, otherwise it Segfaults due to doing stuff prior to OpenGL being initialized. Or something.
    glInit();
}

void wGLWidget::initializeGL()
{
    setAutoBufferSwap(false); //Otherwise we can't sync buffer swapping to clearing. Resulting in total darkness.

    glEnable(GL_TEXTURE_RECTANGLE_ARB);
    glEnable(GL_BLEND);
    glDisable(GL_DEPTH_TEST);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glViewport(0, 0, width(), height());
    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);

    /*cout << "db: " << doubleBuffer() << endl;
    cout << "ac: " << format().alpha() << endl;
    cout << "rg: " << format().rgba() << endl;
    cout << "de: " << format().depth() << endl;*/

    cout << "initialized GL" << endl;
}


void wGLWidget::paintGL()
{
    glClear(GL_COLOR_BUFFER_BIT);

    vector< vector<bImage*> > images = mGame->mTilesetManager->getImages();
    QRect *camTest = new QRect(cam->getCam(zoom), cam->getBounds(zoom));

    foreach(vector<bImage*> layer, images)
    {
        foreach(bImage *img, layer)
        {
            if(camTest->intersects(img->getRect()))
                drawImage(img->getTextureId(), img->getX()-cam->getAbsoluteCam().x(), img->getY()-cam->getAbsoluteCam().y(), img->getW(), img->getH());
        }
    }

    delete(camTest);

    if(doubleBuffer()) //This check seems a bit redundant...as we force it to double buffer. But nonetheless.
        swapBuffers();
}

void wGLWidget::drawImage(QImage *originalImage, int x, int y)
{
    GLuint texture;
    GLenum error;

    QImage image = QGLWidget::convertToGLFormat(*originalImage);

    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture);

    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

    glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, 4, image.width(), image.height(), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, image.bits());

    //note, Somehow, qt4 reverses bottom and top. Somehow.
    glBegin(GL_QUADS);
        //Top-left vertex (corner)
#ifdef _WINDOWS
        glTexCoord2i(0, 1);
#else
        glTexCoord2i(0, image.height()); //image/texture
#endif
        glVertex3i(x, y, 0); //screen coordinates

        //Bottom-left vertex (corner)
#ifdef _WINDOWS
        glTexCoord2i(1, 1);
#else
        glTexCoord2i(image.width(), image.height());
#endif
        glVertex3i(x+image.width(), y, 0);

        //Bottom-right vertex (corner)
#ifdef _WINDOWS
        glTexCoord2i(1, 0);
#else
        glTexCoord2i(image.width(), 0);
#endif
        glVertex3i(x+image.width(), y+image.height(), 0);

        //Top-right vertex (corner)
        glTexCoord2i(0, 0);
        glVertex3i(x, y+image.height(), 0);
    glEnd();

    glDeleteTextures(1, &texture);

    if((error = glGetError()) != GL_NO_ERROR)
    {
        cout << "GLError: " << translateGLError(error);
    }
}

void wGLWidget::drawImage(GLuint texture, int x, int y, int w, int h)
{
    GLenum error;

    //cout << "drawing texture " << texture << " at (" << x << "," << y << ") (" << w << "," << h << ")" << endl;

    glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture);

    //note, Somehow, qt4 reverses bottom and top. Somehow.
    glBegin(GL_QUADS);
        //Top-left vertex (corner)
#ifdef _WINDOWS
        glTexCoord2i(0, 1);
#else
        glTexCoord2i(0, h); //image/texture
#endif
        glVertex3f(x*zoom, y*zoom, 0); //screen coordinates

        //Bottom-left vertex (corner)
#ifdef _WINDOWS
        glTexCoord2i(1, 1);
#else
        glTexCoord2i(w, h);
#endif
        glVertex3f((x+w)*zoom, y*zoom, 0);

        //Bottom-right vertex (corner)
#ifdef _WINDOWS
        glTexCoord2i(1, 0);
#else
        glTexCoord2i(w, 0);
#endif
        glVertex3f((x+w)*zoom, (y+h)*zoom, 0);

        //Top-right vertex (corner)
        glTexCoord2i(0, 0);
        glVertex3f(x*zoom, (y+h)*zoom, 0);
    glEnd();

    if((error = glGetError()) != GL_NO_ERROR)
    {
        cout << "GLError: " << translateGLError(error);
    }
}

void wGLWidget::resizeGL(int w, int h)
{
    //resize(w, h);
    glViewport (0, 0, w, h);
    glMatrixMode (GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, w, h, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    cam->setBounds(w, h);
}

GLuint wGLWidget::createTexture(QImage *image)
{
    GLuint texture;
    GLenum error;

    QImage img = QGLWidget::convertToGLFormat(*image);

    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture);

    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

    glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, img.width(), img.height(), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img.bits());



    if((error = glGetError()) != GL_NO_ERROR)
    {
        glDeleteTextures(1, &texture);

        QMessageBox lol((QWidget*)parent());
        lol.setDetailedText("OpenGL Error: " + QString::fromStdString(translateGLError(error)) +
                            "\r\n\r\n" + "Please contact the author with this message.");
        lol.exec();

        throw "GL error"; //replace with an inherited exception.
        return 0;
    }

    return texture;
}

void wGLWidget::redrawTexture(QImage *image, GLuint texture)
{
    GLenum error;

    QImage img = QGLWidget::convertToGLFormat(*image);

    glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture);

    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

    glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, img.width(), img.height(), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img.bits());

    if((error = glGetError()) != GL_NO_ERROR)
    {
        glDeleteTextures(1, &texture);

        QMessageBox lol((QWidget*)parent());
        lol.setDetailedText("OpenGL Error: " + QString::fromStdString(translateGLError(error)) +
                            "\r\n\r\n" + "Please contact the author with this message.");
        lol.exec();

        throw "GL error"; //replace with an inherited exception.
    }

    return;
}

void wGLWidget::deleteTexture(GLuint texture)
{
    glDeleteTextures(1, &texture);
}


void wGLWidget::setSelectedIcon(IconType::IconEnum selected)
{
    selectedIcon = selected;
}


void wGLWidget::mouseMoveEvent(QMouseEvent *event)
{
    if(selectedIcon == IconType::select)
        emit mouseMoveSignal(event->pos().x() * (1/zoom), event->pos().y() * (1/zoom));
    else
    {
        cam->adjustCam((lastx - event->pos().x()) * (1/zoom), (lasty - event->pos().y()) * (1/zoom));
        lastx = event->pos().x();
        lasty = event->pos().y();
    }

    event->accept();
}

void wGLWidget::mousePressEvent(QMouseEvent *event)
{
    lastx = event->pos().x();
    lasty = event->pos().y();

    if(selectedIcon == IconType::select)
    {
        int type = 0;
        int offset = 0;
        if(ctrlHeld)
            offset += 3;
        if(shiftHeld)
            offset += 6;
        switch(event->button())
        {
            case Qt::LeftButton:
            type = 0 + offset;
            break;
            case Qt::MidButton:
            type = 1 + offset;
            break;
            case Qt::RightButton:
            type = 2 + offset;
            break;
            default:
            type = -1;
            break;
        }
        emit mousePressSignal(event->pos().x() * (1/zoom), event->pos().y() * (1/zoom), type);
    }

    event->accept();
}

void wGLWidget::mouseReleaseEvent(QMouseEvent *event)
{
    if(selectedIcon == IconType::select)
    {
        int type = 0;
        int offset = 0;
        if(ctrlHeld)
            offset += 3;
        if(shiftHeld)
            offset += 6;
        switch(event->button())
        {
            case Qt::LeftButton:
            type = 0 + offset;
            break;
            case Qt::MidButton:
            type = 1 + offset;
            break;
            case Qt::RightButton:
            type = 2 + offset;
            break;
            default:
            type = -1;
            break;
        }
        emit mouseReleaseSignal(event->pos().x() * (1/zoom), event->pos().y() * (1/zoom), type);
    }

    event->accept();
}

void wGLWidget::keyPressEvent(QKeyEvent *event)
{
    cout << "key press" << endl;
    if(event->key() == Qt::Key_Control)
        ctrlHeld = true;
    else if(event->key() == Qt::Key_Shift)
        shiftHeld = true;
}

void wGLWidget::keyReleaseEvent(QKeyEvent *event)
{
    cout << "key release" << endl;
    if(event->key() == Qt::Key_Control)
        ctrlHeld = false;
    else if(event->key() == Qt::Key_Shift)
        shiftHeld = false;
}

void wGLWidget::wheelEvent(QWheelEvent *event)
{
    if(event->delta() < 0)
    {
        if(zoom > 0.50)
            zoom /= 2;
    }
    else if(event->delta() > 0)
    {
        if(zoom < 4.0)
            zoom *= 2;
    }
    cout << "new zoom: " << zoom << endl << "1/zoom: " << 1/zoom << endl;
    cout << "Bounds: " << cam->getBounds(zoom).x() << endl;
}

void wGLWidget::leaveEvent(QEvent *event)
{
    ctrlHeld = false;
    shiftHeld = false;
}

