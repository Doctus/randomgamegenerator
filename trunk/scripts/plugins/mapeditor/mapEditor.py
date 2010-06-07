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
        self.painting = True
        self.dragging = False

        self.setWindowTitle(self.tr("Map Editor"))
        self.widget = QtGui.QWidget(mainWindow)
        self.layout = QtGui.QBoxLayout(2)
        self.scrollarea = QtGui.QScrollArea(mainWindow)
        self.togglePaintingButton = QtGui.QCheckBox(self.tr("Tile Painting"), mainWindow)
        self.togglePaintingButton.setTristate(False)
        self.togglePaintingButton.setCheckState(2)
        self.layout.addWidget(self.scrollarea)
        self.layout.addWidget(self.togglePaintingButton)
        self.tilelabel = None
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        currentMap = rggViews._state.currentMap
        self.mapChangedResponse(currentMap)
        
        self.connect(self.togglePaintingButton, QtCore.SIGNAL('stateChanged(int)'), self.togglePainting)

        rggEvent.addMapChangedListener(self)
        rggEvent.addMousePressListener(self)
        rggEvent.addMouseMoveListener(self)
        rggEvent.addMouseReleaseListener(self)
        
    def mousePressResponse(self, x, y, t):
        self.dragging = True
        if self.isVisible() and self.painting:
            clickedtile = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                           (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
            rggViews.sendTileUpdate(rggViews._state.currentMap.ID, clickedtile, self.tilelabel.currentTile)
            rggEvent.setEaten()

    def mouseMoveResponse(self, x, y):
        if self.isVisible() and self.painting and self.dragging:
            clickedtile = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                           (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
            currentmap = rggViews._state.currentMap
            if currentmap.tilePosExists(clickedtile) and currentmap.getTile(clickedtile) != self.tilelabel.currentTile:
                rggViews.sendTileUpdate(currentmap.ID, clickedtile, self.tilelabel.currentTile)
            rggEvent.setEaten()
            
    def mouseReleaseResponse(self, x, y, t):
        self.dragging = False
        if self.isVisible() and self.painting:
            rggEvent.setEaten()
            
    def togglePainting(self, stat):
        self.painting = stat
        self.togglePaintingButton.setCheckState(stat)
        self.dragging = False

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
