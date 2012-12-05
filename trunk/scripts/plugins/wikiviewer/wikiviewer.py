from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem
from rggSystem import translate






class gameWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        
        self.setWindowTitle(self.tr("Game"))
        
        #basic generic layout; should probably change in the future
        self.widget = QtGui.QWidget(mainWindow)
        self.layout = QtGui.QGridLayout()

        self.hideButton = QtGui.QPushButton("Hide Game")
        self.showButton = QtGui.QPushButton("Show Game")

        self.hideButton.clicked.connect(self.hideGame)
        self.showButton.clicked.connect(self.showGame)
        
        self.layout.addWidget(self.showButton, 0, 0)
        self.layout.addWidget(self.hideButton, 0, 1)
        
        self.widget.setLayout(self.layout)
        
        self.setWidget(self.widget)
        self.setObjectName("Game Plugin")
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)    ,
        
    def showGame(self):
        rggViews._state.session.hide()
        
    def hideGame(self):
        rggViews._state.session.show()

def hajimaru(mainwindow):
    widget = gameWidget(mainwindow)
