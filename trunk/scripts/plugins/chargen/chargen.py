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
        
    def closeEvent(self,  event):
        #Hack to prevent user from closing this sub-window without closing the main program, since it cannot currently be restored if that happens.
        #It will still close when the real main window is closed.
        event.ignore()
        
def hajimaru(mainwindow):
    widget = charGen(mainwindow)
