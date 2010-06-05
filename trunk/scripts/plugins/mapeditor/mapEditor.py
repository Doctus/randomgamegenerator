from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem

class mapEditorLabel(QtGui.QLabel):
    
    def __init__(self, tilesize, width, currentTile=0):
        super(QtGui.QLabel, self).__init__()
        self.tilex, self.tiley = tilesize
        self.wrap = width / self.tilex
        self.currentTile = currentTile
    
    def mousePressEvent(self, ev):
        self.currentTile = (ev.x()/self.tilex) + (ev.y()/self.tiley)*self.wrap

class mapEditor(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        
        #self.__eat = True

        self.setWindowTitle(self.tr("Map Editor"))
        self.widget = QtGui.QWidget(mainWindow)
        self.layout = QtGui.QBoxLayout(2)
        self.scrollarea = QtGui.QScrollArea(mainWindow)
        self.layout.addWidget(self.scrollarea)
        self.tilelabel = None
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        currentMap = rggViews._state.currentMap
        self.mapChangedResponse(currentMap)

        rggEvent.addMapChangedListener(self)
        rggEvent.addMousePressListener(self)
        rggEvent.addMouseReleaseListener(self)
        
    def mousePressResponse(self, x, y, t):
        if self.isVisible():
            clickedtile = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                           (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
            rggViews._state.currentMap.setTile(clickedtile, self.tilelabel.currentTile)
            rggViews.modifyCurrentMap()
            rggEvent.setEaten()
            
    def mouseReleaseResponse(self, x, y, t):
        if self.isVisible():
            rggEvent.setEaten()

    def mapChangedResponse(self, newMap):
        if newMap != None:
            self.tilepixmap = QtGui.QPixmap()
            self.tilepixmap.load(newMap.tileset)
            if self.tilelabel is None:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width())
            else:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilelabel.currentTile)
            self.tilelabel.setPixmap(self.tilepixmap)
            self.scrollarea.setWidget(self.tilelabel)

def hajimaru(mainwindow):
    widget = mapEditor(mainwindow)
