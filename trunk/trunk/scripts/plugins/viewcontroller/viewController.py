from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem

class viewController(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        
        #self.__eat = True

        self.setWindowTitle(self.tr("View Controller"))
        self.widget = QtGui.QWidget(mainWindow)
        self.layout = QtGui.QGridLayout()
        self.layerTitle = QtGui.QLabel("Layers")
        self.layerList = QtGui.QListWidget(mainWindow)
        self.mapTitle = QtGui.QLabel("Maps")
        self.mapList = QtGui.QListWidget(mainWindow)
        self.layout.addWidget(self.layerTitle, 0, 0)
        self.layout.addWidget(self.layerList, 1, 0, 1, 2)
        self.layout.addWidget(self.mapTitle, 3, 0)
        self.layout.addWidget(self.mapList, 4, 0, 1, 2)
        self.layout.setRowMinimumHeight(2, 10)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        currentMap = rggViews.currentmap()
 
def hajimaru(mainwindow):
    widget = viewController(mainwindow)