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
        self.rectStart = None

        self.setWindowTitle(self.tr("Map Editor"))
        self.widget = QtGui.QWidget(mainWindow)
        self.layout = QtGui.QBoxLayout(2)
        self.scrollarea = QtGui.QScrollArea(mainWindow)
        self.noPaintingButton = QtGui.QRadioButton(self.tr("Stop Painting"), mainWindow)
        self.singlePaintingButton = QtGui.QRadioButton(self.tr("Single Tile Brush"), mainWindow)
        self.singlePaintingButton.setChecked(True)
        self.rectPaintingButton = QtGui.QRadioButton(self.tr("Area (Rectangle) Brush"), mainWindow)
        self.layout.addWidget(self.scrollarea)
        self.layout.addWidget(self.noPaintingButton)
        self.layout.addWidget(self.singlePaintingButton)
        self.layout.addWidget(self.rectPaintingButton)
        self.tilelabel = None
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        currentMap = rggViews._state.currentMap
        self.mapChangedResponse(currentMap)

        rggEvent.addMapChangedListener(self)
        rggEvent.addMousePressListener(self)
        rggEvent.addMouseMoveListener(self)
        rggEvent.addMouseReleaseListener(self)
        
    def mousePressResponse(self, x, y, t):
        self.dragging = True
        if self.isVisible() and self.singlePaintingButton.isChecked():
            clickedtile = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                           (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
            if not rggViews._state.currentMap.tilePosExists(clickedtile):
                rggEvent.setEaten()
                return
            rggViews.sendTileUpdate(rggViews._state.currentMap.ID, clickedtile, self.tilelabel.currentTile)
            rggEvent.setEaten()
        elif self.isVisible() and self.rectPaintingButton.isChecked():
            self.rectStart = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                           (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
            rggEvent.setEaten()

    def mouseMoveResponse(self, x, y):
        if self.isVisible() and self.singlePaintingButton.isChecked() and self.dragging:
            clickedtile = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                           (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
            if not rggViews._state.currentMap.tilePosExists(clickedtile):
                rggEvent.setEaten()
                return
            currentmap = rggViews._state.currentMap
            if currentmap.tilePosExists(clickedtile) and currentmap.getTile(clickedtile) != self.tilelabel.currentTile:
                rggViews.sendTileUpdate(currentmap.ID, clickedtile, self.tilelabel.currentTile)
            rggEvent.setEaten()
            
    def mouseReleaseResponse(self, x, y, t):
        self.dragging = False
        if self.isVisible() and self.singlePaintingButton.isChecked():
            rggEvent.setEaten()
        elif self.isVisible() and self.rectPaintingButton.isChecked() and self.rectStart is not None:
            rectEnd = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                       (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
            for x in range(self.rectStart[0], rectEnd[0]+cmp(rectEnd[0], self.rectStart[0]), cmp(rectEnd[0], self.rectStart[0])):
                for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                    if rggViews._state.currentMap.tilePosExists((x, y)):
                        rggViews.sendTileUpdate(rggViews._state.currentMap.ID, (x, y), self.tilelabel.currentTile)
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
