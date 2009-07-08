from PyQt4 import QtCore, QtGui, QtOpenGL

#import ../cCamera

class wGLWidget(QtOpenGL.QGLWidget):

    def __init__(self, parent, mGame):
        self.parent = parent
        self.mGame = mGame

        self.selectedIcon = 0
        #self.cam = cCamera.cCamera(0, 0, 800, 600)

        #self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)

        super(QtOpenGL.QGLWidget, self).glIinit()

    def initializeGL(self):
        self.setAutoBufferSwap(false)

        glEnable(GL_TEXTURE_RECTANGLE_ARB)
        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, 800, 600)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        print 'Initialized GL'
