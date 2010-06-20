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

#ifdef WIN32
  #define GL_TEXTURE_RECTANGLE_ARB GL_TEXTURE_2D //This abolishes POT textures, but at least it works! (god damn microsoft and its shitty products)

//blatantly stolen from Box2D
inline uint b2NextPowerOfTwo(uint x)
{
        x |= (x >> 1);
        x |= (x >> 2);
        x |= (x >> 4);
        x |= (x >> 8);
        x |= (x >> 16);
        return x + 1;
}
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
    cam = new cCamera(0, 0, 640, 480);
    ctrlHeld = false;
    shiftHeld = false;
    mouseButtonHeld = false;
    zoom = 1;

    resize(parent->width(), parent->height());

    setSizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);

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

    //glPointSize(5);

    /*cout << "db: " << doubleBuffer() << endl;
    cout << "ac: " << format().alpha() << endl;
    cout << "rg: " << format().rgba() << endl;
    cout << "de: " << format().depth() << endl;*/

    cout << "initialized GL" << endl;
}


void wGLWidget::paintGL()
{
    glClear(GL_COLOR_BUFFER_BIT);

    glEnable(GL_TEXTURE_RECTANGLE_ARB);

    vector< vector<bImage*> > images = mGame->mTilesetManager->getImages();
    QRect *camTest = new QRect(cam->getCam(), cam->getBounds(zoom));

    foreach(vector<bImage*> layer, images)
    {
        foreach(bImage *img, layer)
        {
            if(!img->getHidden() && camTest->intersects(img->getRect()))
                drawImage(img->getTextureId(), img->getX()-cam->getCam().x(), img->getY()-cam->getCam().y(), img->getW(), img->getH(),
                          img->getDrawW(), img->getDrawH());
        }
    }

    glDisable(GL_TEXTURE_RECTANGLE_ARB);

    short i = 2;
    foreach(QVector<QRect> lines, mGame->mShapeManager->getLines())
    {
        glLineWidth(i);
        glBegin(GL_LINES);
        foreach(QRect line, lines)
        {
            if(camTest->contains(line.topLeft()) || camTest->contains(line.bottomRight()))
            {
                int x = (line.x()-cam->getCam().x())*zoom;
                int y = (line.y()-cam->getCam().y())*zoom;
                int w = (line.width()-cam->getCam().x())*zoom;
                int h = (line.height()-cam->getCam().y())*zoom;
                glVertex2i(x, y);
                glVertex2i(w, h);
            }
        }
        glEnd();
        i += 2;
    }

    delete(camTest);

    if(doubleBuffer()) //This check seems a bit redundant...as we force it to double buffer. But nonetheless.
        swapBuffers();
}

void wGLWidget::drawImage(GLuint texture, int x, int y, int textureW, int textureH, int drawW, int drawH)
{
    GLenum error;

    //cout << "drawing texture " << texture << " at (" << x << "," << y << ") (" << w << "," << h << ")" << endl;

    glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture);

    //note, Somehow, qt4 reverses bottom and top. Somehow.
    glBegin(GL_QUADS);
        //Top-left vertex (corner)
#ifdef WIN32
        glTexCoord2i(0, 1);
#else
        glTexCoord2i(0, textureH); //image/texture
#endif
        glVertex3f(x*zoom, y*zoom, 0); //screen coordinates

        //Bottom-left vertex (corner)
#ifdef WIN32
        glTexCoord2i(1, 1);
#else
        glTexCoord2i(textureW, textureH);
#endif
        glVertex3f((x+drawW)*zoom, y*zoom, 0);

        //Bottom-right vertex (corner)
#ifdef WIN32
        glTexCoord2i(1, 0);
#else
        glTexCoord2i(textureW, 0);
#endif
        glVertex3f((x+drawW)*zoom, (y+drawH)*zoom, 0);

        //Top-right vertex (corner)
        glTexCoord2i(0, 0);
        glVertex3f(x*zoom, (y+drawH)*zoom, 0);
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

#ifdef WIN32
    GLvoid *scaledImage = new char[b2NextPowerOfTwo(img.width())*b2NextPowerOfTwo(img.height())*4];
    GLint ret = gluScaleImage(GL_RGBA, img.width(), img.height(), GL_UNSIGNED_BYTE, img.bits(),
                  b2NextPowerOfTwo(img.width()), b2NextPowerOfTwo(img.height()), GL_UNSIGNED_BYTE, scaledImage);

    if(ret != 0)
    {
		delete scaledImage;

        cout << "A gl error happened in gluScaleImage: " << translateGLError(glGetError()) << endl;
        throw "GL error";
        return 0;
    }

    glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, b2NextPowerOfTwo(img.width()), b2NextPowerOfTwo(img.height()), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, scaledImage);
	delete scaledImage;
#else
    glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, img.width(), img.height(), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img.bits());
#endif


    //cout << "Generated texture number: " << texture << endl;

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

#ifdef WIN32
    GLvoid *scaledImage[b2NextPowerOfTwo(img.width())*b2NextPowerOfTwo(img.height())];
    GLint ret = gluScaleImage(GL_RGBA, img.width(), img.height(), GL_UNSIGNED_BYTE, img.bits(),
                  b2NextPowerOfTwo(img.width()), b2NextPowerOfTwo(img.height()), GL_UNSIGNED_BYTE, scaledImage);

    if(ret != 0)
    {
        cout << "A gl error happened in gluScaleImage: " << translateGLError(glGetError()) << endl;
        throw "GL error";
        return;
    }

    glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, b2NextPowerOfTwo(img.width()), b2NextPowerOfTwo(img.height()), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, scaledImage);
#else
    glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, img.width(), img.height(), 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img.bits());
#endif

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


void wGLWidget::setZoom(float zoom)
{
    if(zoom < 0.25)
        zoom = 0.25;
    if(zoom > 4.00)
        zoom = 4.00;

    this->zoom = zoom;
}

float wGLWidget::getZoom()
{
    return zoom;
}


void wGLWidget::mouseMoveEvent(QMouseEvent *event)
{
    /*if(selectedIcon == IconType::select && mouseButtonHeld)
        emit mouseDragSignal(event->pos().x() * (1/zoom), event->pos().y() * (1/zoom));
    else if(selectedIcon == IconType::select)
        emit mouseMoveSignal(event->pos().x() * (1/zoom), event->pos().y() * (1/zoom));
    else if(mouseButtonHeld)
    {
        cam->adjustCam((lastx - event->pos().x()) * (1/zoom), (lasty - event->pos().y()) * (1/zoom));
        lastx = event->pos().x();
        lasty = event->pos().y();
    }*/

    emit mouseMoveSignal(int(event->pos().x() * (1/zoom)), int(event->pos().y() * (1/zoom)));

    event->accept();
}

void wGLWidget::mousePressEvent(QMouseEvent *event)
{
    lastx = event->pos().x();
    lasty = event->pos().y();
    mouseButtonHeld = true;

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
    emit mousePressSignal(int(event->pos().x() * (1/zoom)), int(event->pos().y() * (1/zoom)), type);

    event->accept();
}

void wGLWidget::mouseReleaseEvent(QMouseEvent *event)
{
    mouseButtonHeld = false;

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
    emit mouseReleaseSignal(int(event->pos().x() * (1/zoom)), int(event->pos().y() * (1/zoom)), type);

    event->accept();
}

void wGLWidget::keyPressEvent(QKeyEvent *event)
{
    //cout << "key press" << endl;
    if(event->key() == Qt::Key_Control)
        ctrlHeld = true;
    else if(event->key() == Qt::Key_Shift)
        shiftHeld = true;
}

void wGLWidget::keyReleaseEvent(QKeyEvent *event)
{
    //cout << "key release" << endl;
    if(event->key() == Qt::Key_Control)
        ctrlHeld = false;
    else if(event->key() == Qt::Key_Shift)
        shiftHeld = false;
}

void wGLWidget::wheelEvent(QWheelEvent *event)
{
    if(event->delta() < 0)
    {
        if(zoom > 0.25)
            zoom /= 2;
    }
    else if(event->delta() > 0)
    {
        if(zoom < 4.0)
            zoom *= 2;
    }
    //cout << "new zoom: " << zoom << endl << "1/zoom: " << 1/zoom << endl;
    //cout << "Bounds: " << cam->getBounds(zoom).x() << endl;
}

void wGLWidget::leaveEvent(QEvent *event)
{
    ctrlHeld = false;
    shiftHeld = false;
    emit leaveSignal();
}

void wGLWidget::enterEvent(QEvent *event)
{
    emit enterSignal();
}

