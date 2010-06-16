from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem

class mapItem(QtGui.QListWidgetItem):

    def __init__(self, mappe):
        QtGui.QListWidgetItem.__init__(self)
        self.map = mappe
        if self.map.mapname:
            self.setText(self.map.mapname)
        else:
            self.setText("Nameless Map")
            
class mapListWidget(QtGui.QListWidget):

    def __init__(self, parent):
        QtGui.QListWidget.__init__(self)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

    def mousePressEvent(self, event): #listwidget generated events
        pos = event.globalPos()
        x = pos.x()
        y = pos.y()
        item = self.itemAt(event.x(), event.y())
        event.accept()
        super(QtGui.QListWidget, self).mousePressEvent(event)
        if not item: return
        if event.button() == QtCore.Qt.RightButton:
            selection = rggSystem.showPopupMenuAtAbs([x, y], ['Switch to ' + item.text()])
            if selection == 0:
                rggViews.sendMapSwitch(item.map.ID)


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
        self.mapList = mapListWidget(mainWindow)
        self.layout.addWidget(self.layerTitle, 0, 0)
        self.layout.addWidget(self.layerList, 1, 0, 1, 2)
        self.layout.addWidget(self.mapTitle, 3, 0)
        self.layout.addWidget(self.mapList, 4, 0, 1, 2)
        self.layout.setRowMinimumHeight(2, 10)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        currentMap = rggViews.currentmap()
        self.updateMaps()
        
        rggEvent.addMapChangedListener(self)
        
    def updateMaps(self):
        self.mapList.clear()
        mappes = rggViews.getAllMaps()
        mappes.sort(cmp=lambda x,y: cmp(x.mapname.lower(), y.mapname.lower()))
        for map in mappes:
            self.mapList.addItem(mapItem(map))
            
    def mapChangedResponse(self, newMap):
        self.updateMaps()
 
def hajimaru(mainwindow):
    widget = viewController(mainwindow)