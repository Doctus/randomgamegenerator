#include "GLWidget.h"

std::string translateGLError(GLenum errorcode)
{
  std::string errorStr = (char*)gluErrorString(errorcode);
  return errorStr;
}

GLWidget::GLWidget(QWidget* parent) : QGLWidget(QGLFormat(QGL::FormatOptions(QGL::DoubleBuffer | QGL::AlphaChannel)), parent)
{
    resize(parent->width(), parent->height());
    grabKeyboard();
    glInit();
}

void GLWidget::initializeGL()
{
    setAutoBufferSwap(false);

    glEnable(GL_TEXTURE_RECTANGLE_ARB);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glViewport(0, 0, 640, 480);
    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);

    cout << "initialized GL" << endl;
}


void GLWidget::paintGL()
{
    if(doubleBuffer())
        swapBuffers();

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}

void GLWidget::drawImage(QImage *originalImage, int x, int y)
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
        glTexCoord2i(0, image.height()); //image/texture
        glVertex3i(x, y, 0); //screen coordinates

        //Bottom-left vertex (corner)
        glTexCoord2i(image.width(), image.height());
        glVertex3i(x+image.width(), y, 0);

        //Bottom-right vertex (corner)
        glTexCoord2i(image.width(), 0);
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

void GLWidget::drawImage(GLuint texture, int x, int y, int w, int h)
{
    GLenum error;

    //cout << "drawing texture " << texture << endl;

    glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture);

    //note, Somehow, qt4 reverses bottom and top. Somehow.
    glBegin(GL_QUADS);
        //Top-left vertex (corner)
        glTexCoord2i(0, h); //image/texture
        glVertex3i(x, y, 0); //screen coordinates

        //Bottom-left vertex (corner)
        glTexCoord2i(w, h);
        glVertex3i(x+w, y, 0);

        //Bottom-right vertex (corner)
        glTexCoord2i(w, 0);
        glVertex3i(x+w, y+h, 0);

        //Top-right vertex (corner)
        glTexCoord2i(0, 0);
        glVertex3i(x, y+h, 0);
    glEnd();


    if((error = glGetError()) != GL_NO_ERROR)
    {
        cout << "GLError: " << translateGLError(error);
    }
}

void GLWidget::resizeGL(int w, int h)
{
    //resize(w, h);
    glViewport (0, 0, w, h);
    glMatrixMode (GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, 640, 480, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);
}

GLuint GLWidget::createTexture(QImage *image)
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
        cout << "GLError: " << translateGLError(error);
        glDeleteTextures(1, &texture);
        throw "GL error"; //replace with an inherited exception.
        return 0; //exception?
    }

    //cout << "created texture " << texture << endl;

    return texture;
}

void GLWidget::deleteTexture(GLuint texture)
{
    glDeleteTextures(1, &texture);
}



void GLWidget::keyPressEvent(QKeyEvent *event)
{
    event->accept();
    cEventManager::getInstance()->keyPress(event->key());
}

void GLWidget::keyReleaseEvent(QKeyEvent *event)
{
    cEventManager::getInstance()->keyRelease(event->key());
}

