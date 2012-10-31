# -*- coding: utf-8 -*-
#
#main class
#
#By Oipo (kingoipo@gmail.com)

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from rggJson import loadInteger, jsonload
from rggSystem import SAVE_DIR

class MainWindow(QMainWindow):
    '''Wrapper class for...well, the game? Maybe this needs to be called the game engine then'''

    def __init__(self):
        '''
        Only initialize critical components(like opengl) here, use start() for anything else
        '''
        QMainWindow.__init__(self)

        self.setWindowTitle("RChat")
        self.setObjectName("MainWindow")
        try: self.setWindowIcon(QIcon(os.path.join("data", "rgglogo2.png")))
        except: pass
        
        self.glwidget = QWidget()
        self.setCentralWidget(self.glwidget)