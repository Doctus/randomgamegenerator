from PyQt4 import QtCore

#import Network/nConnectionManager
from Widgets import wGLWidget
#import Widgets/wMenuBar
#import Widgets/wDockWidgets

#import cTilesetManager

class cGame(QtCore.QObject):

    def __init__(self, parent):
        #self.mConnectionManager = nConnectionManager.nConnectionManager(parent, self)
        self.mGLWidget = wGLWidget.wGLWidget(parent, self)
        #self.mMenuBar = wMenuBar.wMenuBar(parent, self, self.mConnectionManager)
        #self.wDockWidgets = wDockWidgets(parent, self)
        #self.mTilesetManager = cTilesetManager.cTilesetManager(self.mGLWidget)
        self.FPScounter = 0
        self.parent = parent

        self.drawTimer = QtCore.QTimer()
        self.FPSTimer = QtCore.QTimer()
        QtCore.QObject.connect(self.drawTimer, QtCore.SIGNAL("timeout()"), self.draw)
        QtCore.QObject.connect(self.FPSTimer, QtCore.SIGNAL("timeout()"), self.displayFPS)
        self.drawTimer.start(100)
        self.FPSTimer.start(1000)

    def draw(self):
        self.FPScounter = self.FPScounter + 1
        pass

    def displayFPS(self):
        self.parent.setWindowTitle("Random Game Generator | FPS: " + str(self.FPScounter))
        self.FPScounter = 0
