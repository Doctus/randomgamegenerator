# coding: utf-8

import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

tex = 0
mipmap = 0

class wGLWidget(QGLWidget):

    def __init__(self, parent, mGame):
        self.parent = parent
        self.mGame = mGame
        self.selectedIcon = 0

        super(QGLWidget, self).__init__(QGLFormat(QGL.DoubleBuffer | QGL.AlphaChannel), parent)

        self.resize(parent.width(), parent.height())
        self.glInit()

    def check_size(self, img):
        for size in img.size:
            while True:
                if (size & 1) != 0:
                    break
                size >>= 1
            if size != 1:
                return False
        return True

    def ppm2texture(self, ppm_path):
        ppm = Image.open(ppm_path)
        assert self.check_size(ppm)
        w, h = ppm.size
        data = ppm.tostring()

        tex = glGenTextures(20)
        glBindTexture(GL_TEXTURE_2D, tex[0])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h,
                0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        error = glGetError()

        if error != GL_NO_ERROR:
            print "GLError: " + gluErrorString(error)
            return False

        return tex[0]

    def initializeGL(self):
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        ppm_path = os.path.join(os.path.dirname(__file__), u"texture2.ppm")
        tex = self.ppm2texture(ppm_path)

        self.setAutoBufferSwap(False)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(2.0, -1.0, -50.0)

        glTexCoord2f(5.0, 1.0)
        glVertex3f(2.0, -1.0, 0.0)

        glTexCoord2f(5.0, 0.0)
        glVertex3f(2.0, 1.0, 0.0)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(2.0, 1.0, -50.0)
        glEnd()

        glColor3f(1.0, 0.0, 0.0) 
        glRectf(-25.0, 25.0, 25.0, -25.0)

        glFlush()

        error = glGetError()

        if error != GL_NO_ERROR:
            print "GLError: " + gluErrorString(error)
            return False

        if(self.doubleBuffer()):
            self.swapBuffers()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, 1.0, -1.0, 1.0, 3.0, 10000.0)
        glMatrixMode(GL_MODELVIEW)
        error = glGetError()

        if error != GL_NO_ERROR:
            print "GLError: " + gluErrorString(error)
            return False

