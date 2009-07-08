from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *

import Image

import sys

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError:
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "Random Game Generator",
                            "PyOpenGL must be installed to run this example.",
                            QMessageBox.Ok | QMessageBox.Default,
                            QMessageBox.NoButton)
    sys.exit(1)


#import ../cCamera

class wGLWidget(QGLWidget):

    def __init__(self, parent, mGame):
        self.parent = parent
        self.mGame = mGame

        self.selectedIcon = 0

        super(QGLWidget, self).__init__(QGLFormat(QGL.DoubleBuffer | QGL.AlphaChannel), parent)
        #self.cam = cCamera.cCamera(0, 0, 800, 600)

        #self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)

        #self.glIinit()

    def initializeGL(self):
        self.setAutoBufferSwap(False)

        glEnable(GL_TEXTURE_RECTANGLE_ARB)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, 640, 480)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        print 'Initialized GL'

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self.drawTexture(self.mGame.testTexture, 0, 0, 64, 64)

        if(self.doubleBuffer()):
            self.swapBuffers()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def drawTexture(self, textureId, x, y, w, h):
        #print "drawing id " + str(textureId) + " at (" + str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h) + ")" 
        glBindTexture(GL_TEXTURE_2D, textureId)

        glBegin(GL_QUADS)
        glTexCoord2i(0, 1)
        glVertex3i(x, y, 0)

        glTexCoord2i(1, 1)
        glVertex3i(x+w, y, 0)

        glTexCoord2i(1, 0)
        glVertex3i(x+w, y+h, 0)

        glTexCoord2i(0, 0)
        glVertex3i(x, y+h, 0)
        glEnd()

        error = glGetError()

        if error != GL_NO_ERROR:
            print "GLError: " + gluErrorString(error)
            return False

        return True

    def createTexture(self, image):
        #newImage = self.convertToGLFormat(image)
        texture = -1

        texture = glGenTextures(1)

        print 'texture is ' + str(texture)

        glBindTexture(GL_TEXTURE_2D, texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        #glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, newImage.width(), newImage.height(), 0,
                 #GL_RGBA, GL_UNSIGNED_BYTE, newImage.bits().asstring(newImage.numBytes()))
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 64, 64, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, image.tostring())

        error = glGetError()

        if error != GL_NO_ERROR:
            glDeleteTextures(1, texture)

            errorDialog = QMessageBox(self.parent)
            errorDialog.setDetailedText("OpenGL Error: " + gluErrorString(error) + "\r\n\r\n" + "Please contact the author with this message")
            errorDialog.exec_()

            return 0

        return texture
