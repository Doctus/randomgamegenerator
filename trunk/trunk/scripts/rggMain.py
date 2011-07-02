# -*- coding: utf-8 -*-
#
#main class
#
#By Oipo (kingoipo@gmail.com)

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from glwidget import *

class MainWindow(QMainWindow):
    '''Wrapper class for...well, the game? Maybe this needs to be called the game engine then'''

    def __init__(self):
        '''
        Only initialize critical components(like opengl) here, use start() for anything else
        '''
        QMainWindow.__init__(self)

        self.setWindowTitle("RandomGameGenerator")
        self.setObjectName("MainWindow")
        try: self.setWindowIcon(QIcon(os.path.join("data", "FAD-icon.png")))
        except: pass

        self.glwidget = GLWidget(self)
        self.setCentralWidget(self.glwidget)
        self.glwidget.makeCurrent() 

        self.drawTimer = QTimer()
        self.drawTimer.timeout.connect(self.drawTimerTimeout)
        self.drawTimer.start(13)
        
    def readGeometry(self):
        settings = QSettings("AttercopProductions", "RGG")
        settings.beginGroup("MainWindow")
        self.restoreGeometry(settings.value("geometry").toByteArray())
        self.restoreState(settings.value("windowState").toByteArray())
        settings.endGroup()
        
    def closeEvent(self, event):
        settings = QSettings("AttercopProductions", "RGG")
        settings.beginGroup("MainWindow")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.endGroup()
        QMainWindow.closeEvent(self, event)

    def drawTimerTimeout(self):
        self.glwidget.updateGL()
