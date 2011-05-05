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

    def __init__(self, parent, controller):
        QtGui.QListWidget.__init__(self)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.controller = controller

    def mousePressEvent(self, event): #listwidget generated events
        pos = event.globalPos()
        x = pos.x()
        y = pos.y()
        item = self.itemAt(event.x(), event.y())
        event.accept()
        super(QtGui.QListWidget, self).mousePressEvent(event)
        if not item: return
        self.controller.setCurrentMap(item.map)
        if event.button() == QtCore.Qt.RightButton:
            hide = "Hide " + item.text()
            if item.map.hidden:
                hide = "Show " + item.text()
            selection = rggSystem.showPopupMenuAtAbs([x, y], [hide])
            if selection == 0:
                if item.map.hidden:
                    item.map.show()
                else:
                    item.map.hide()


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
        self.mapList = mapListWidget(mainWindow, self)
        self.layout.addWidget(self.layerTitle, 0, 0)
        self.layout.addWidget(self.layerList, 1, 0, 1, 2)
        self.layout.addWidget(self.mapTitle, 3, 0)
        self.layout.addWidget(self.mapList, 4, 0, 1, 2)
        self.refreshbutton = QtGui.QPushButton(self.tr("Force Refresh"), mainWindow)
        self.refreshbutton.setToolTip(self.tr("Force refresh of all pog images. This really should be elsewhere but there were dependency issues."))
        self.layout.addWidget(self.refreshbutton, 5, 0)
        self.refreshbutton.pressed.connect(self.refreshPogs)
        self.layout.setRowMinimumHeight(2, 10)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        self.mainWindow = mainWindow

        self.updateMaps()
        self.currentMap = None
        
        rggEvent.addMapChangedListener(self)
        
    def updateMaps(self):
        self.mapList.clear()
        mappes = rggViews.getAllMaps()
        mappes.sort(cmp=lambda x,y: cmp(x.mapname.lower(), y.mapname.lower()))
        for map in mappes:
            self.mapList.addItem(mapItem(map))
            
    def mapChangedResponse(self, newMap):
        self.updateMaps()
        
    def setCurrentMap(self, map):
        self.currentMap = map
        
    def refreshPogs(self):
        if self.currentMap != None:
            self.currentMap.refreshPogs()
 
def hajimaru(mainwindow):
    widget = viewController(mainwindow)