#ifndef GLWIDGET_GUARD
#define GLWIDGET_GUARD

#include <QtOpenGL/QtOpenGL>
#include <QtGui/QImage>
#include <QtCore/QRect>

#ifdef WINDOWS
  #include <glext.h>
#endif

#include <iostream>

#include "../cEventManager.h"

using namespace std;

class GLWidget : public QGLWidget
{
    public:
    GLWidget(QWidget* parent);

    void initializeGL();
    void paintGL();
    void drawImage(QImage *originalImage, int x, int y);
    void drawImage(GLuint texture, int x, int y, int w, int h);
    void resizeGL(int w, int h);

    GLuint createTexture(QImage *image);
    void deleteTexture(GLuint texture);

    private:
    void keyPressEvent(QKeyEvent *event);
    void keyReleaseEvent(QKeyEvent *event);
};

#endif
