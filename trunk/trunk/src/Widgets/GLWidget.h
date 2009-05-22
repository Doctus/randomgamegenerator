#ifndef GLWIDGET_GUARD
#define GLWIDGET_GUARD

#include <QtOpenGL/QtOpenGL>
#include <QtGui/QImage>
#include <QtCore/QRect>

#ifdef _WINDOWS
  #define GL_TEXTURE_RECTANGLE_ARB 0x84F5 //HAR HAR. VEE BE EVUL. VEE IS NUT CHECKING IF IT IS SUPPORTED ON PLATFORM.
#endif

#include <iostream>

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
};

#endif
