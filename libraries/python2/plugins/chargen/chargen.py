from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, widgets

class charGen(QDockWidget):

    def __init__(self, mainWindow):
        super(charGen, self).__init__(mainWindow)

        self.setWindowTitle("Character Creator")
        self.setObjectName("Character Creator")
        
        self.widget = QWidget(self)
        self.layout = QGridLayout()
        widgets.initWidgets(self.widget, self, self.layout)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        
        mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)
        
def hajimaru(mainwindow):
    widget = charGen(mainwindow)