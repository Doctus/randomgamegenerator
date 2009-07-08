from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Image

#import Network/nConnectionManager
from Widgets import wGLWidget
#import Widgets/wMenuBar
#import Widgets/wDockWidgets

#import cTilesetManager

class cGame(QObject):

    def __init__(self, parent):
        #self.mConnectionManager = nConnectionManager.nConnectionManager(parent, self)
        self.mGLWidget = wGLWidget.wGLWidget(parent, self)
        #self.mMenuBar = wMenuBar.wMenuBar(parent, self, self.mConnectionManager)
        #self.wDockWidgets = wDockWidgets(parent, self)
        #self.mTilesetManager = cTilesetManager.cTilesetManager(self.mGLWidget)
        self.FPScounter = 0
        self.parent = parent

        self.parent.setCentralWidget(self.mGLWidget)

        testImage = Image.open("test.png")
        self.testTexture = self.mGLWidget.createTexture(testImage)

        self.drawTimer = QTimer()
        self.FPSTimer = QTimer()
        QObject.connect(self.drawTimer, SIGNAL("timeout()"), self.draw)
        QObject.connect(self.FPSTimer, SIGNAL("timeout()"), self.displayFPS)
        self.drawTimer.start(25)
        self.FPSTimer.start(1000)

    def draw(self):
        self.FPScounter = self.FPScounter + 1
        self.mGLWidget.updateGL()
        pass

    def displayFPS(self):
        self.parent.setWindowTitle("Random Game Generator | FPS: " + str(self.FPScounter))
        self.FPScounter = 0
