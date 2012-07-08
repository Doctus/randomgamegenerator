from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, widgets

class charGen(QMainWindow):

    def __init__(self, mainWindow):
        super(QMainWindow, self).__init__(mainWindow)

        self.setWindowTitle("Character Creator")
        self.setObjectName("Character Creator")
        self.widget = QWidget(self)
        widgets.initWidgets(self.widget, self)
        self.show()
        
def hajimaru(mainwindow):
    widget = charGen(mainwindow)
