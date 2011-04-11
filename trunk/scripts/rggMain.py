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

        self.glwidget = GLWidget(self)
        self.setCentralWidget(self.glwidget)
        self.glwidget.makeCurrent() 

        self.drawTimer = QTimer()
        self.drawTimer.timeout.connect(self.drawTimerTimeout)
        self.drawTimer.start(13)

    def drawTimerTimeout(self):
        self.glwidget.updateGL()
