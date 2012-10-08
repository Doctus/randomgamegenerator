from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem

class mapEditorLabel(QtGui.QLabel):
    
    def __init__(self, tilesize, width, height, par, currentTile=0):
        super(QtGui.QLabel, self).__init__()
        self.tilex, self.tiley = tilesize
        self.wid = width
        self.hei = height
        self.wrap = width / self.tilex
        self.openglfix = (height / self.tiley)-1
        self.currentTile = currentTile
        self.par = par
    
    def mousePressEvent(self, ev):
        self.currentTile = (ev.x()/self.tilex) + abs((ev.y()/self.tiley)-self.openglfix)*self.wrap
        self.updateTile()
        
    def updateTile(self):
        self.currentTileDimensions = (self.currentTile%(self.wid/self.tilex)*self.tilex, (self.hei - self.tiley) - (int((self.currentTile*self.tilex)/self.wid)*self.tiley), self.tilex, self.tiley)
        self.par.updateCurrentTile()

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
        self.currentTileLayout = QtGui.QBoxLayout(1)
        self.scrollarea = QtGui.QScrollArea(mainWindow)
        self.noPaintingButton = QtGui.QRadioButton(self.tr("Stop Painting"), mainWindow)
        self.singlePaintingButton = QtGui.QRadioButton(self.tr("Single Tile Brush"), mainWindow)
        self.noPaintingButton.setChecked(True)
        self.rectPaintingButton = QtGui.QRadioButton(self.tr("Area (Rectangle) Brush"), mainWindow)
        self.hollowRectPaintingButton = QtGui.QRadioButton(self.tr("Hollow Rectangle Brush"), mainWindow)
        self.currentTileLabel = QtGui.QLabel()
        self.currentTileLabelLabel = QtGui.QLabel(self.tr("Current tile: "))
        self.layout.addWidget(self.scrollarea)
        self.layout.addWidget(self.noPaintingButton)
        self.layout.addWidget(self.singlePaintingButton)
        self.layout.addWidget(self.rectPaintingButton)
        self.layout.addWidget(self.hollowRectPaintingButton)
        self.currentTileLayout.addWidget(self.currentTileLabel)
        self.currentTileLayout.addWidget(self.currentTileLabelLabel)
        self.layout.addLayout(self.currentTileLayout)
        self.tilelabel = None
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.setObjectName("Map Editor")
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        self.currentMap = None

        rggEvent.addMapChangedListener(self)
        rggEvent.addMousePressListener(self)
        rggEvent.addMouseMoveListener(self)
        rggEvent.addMouseReleaseListener(self)
        
    def updateCurrentTile(self):
        self.tilepix = QtGui.QPixmap()
        self.tilepix.load(self.currentMap.tileset)
        self.tilepix = self.tilepix.copy(QtCore.QRect(*self.tilelabel.currentTileDimensions))
        self.currentTileLabel.setPixmap(self.tilepix)
        
    def mousePressResponse(self, x, y, t):
        mapPosition = rggSystem.getMapPosition((x, y))
        map = rggViews.topmap(mapPosition)
        if map == None:
            return
        if map != self.currentMap:
            self.mapChangedResponse(map)
        if t == 0:
            self.dragging = True
            if self.isVisible() and self.singlePaintingButton.isChecked():
                clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                if not map.tilePosExists(clickedtile):
                    rggEvent.setEaten()
                    return
                rggViews.sendTileUpdate(map.ID, clickedtile, self.tilelabel.currentTile)
                rggEvent.setEaten()
            elif self.isVisible() and (self.rectPaintingButton.isChecked() or self.hollowRectPaintingButton.isChecked()):
                self.rectStart = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                if not map.tilePosExists(self.rectStart):
                    rggEvent.setEaten()
                    self.rectStart = None
                    return
                rggEvent.setEaten()
        elif t == 5:
            if self.isVisible() and not self.noPaintingButton.isChecked():
                clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                self.tilelabel.currentTile = map.getTile(clickedtile)
                self.tilelabel.updateTile()
                rggEvent.setEaten()

    def mouseMoveResponse(self, x, y):
        if self.dragging and self.isVisible() and self.singlePaintingButton.isChecked():
            mapPosition = rggSystem.getMapPosition((x, y))
            map = rggViews.topmap(mapPosition)
            if map == None:
                self.dragging = False
                return
            clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
            
            if not map.tilePosExists(clickedtile):
                rggEvent.setEaten()
                return
            if map.tilePosExists(clickedtile) and map.getTile(clickedtile) != self.tilelabel.currentTile:
                rggViews.sendTileUpdate(map.ID, clickedtile, self.tilelabel.currentTile)
            rggEvent.setEaten()
            
    def mouseReleaseResponse(self, x, y, t):
        if t == 0:
            if self.currentMap == None:
                return
            mapPosition = rggSystem.getMapPosition((x, y))
            map = rggViews.topmap(mapPosition)
            self.dragging = False
            if map == None:
                return
            if self.isVisible() and self.singlePaintingButton.isChecked():
                rggEvent.setEaten()
            elif self.isVisible() and self.rectPaintingButton.isChecked() and self.rectStart is not None:
                rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                if not map.tilePosExists(rectEnd):
                    rggEvent.setEaten()
                    self.rectStart = None
                    self.rectEnd = None
                    return
                if cmp(rectEnd[0], self.rectStart[0]) != 0:
                    for x in range(self.rectStart[0], rectEnd[0]+cmp(rectEnd[0], self.rectStart[0]), cmp(rectEnd[0], self.rectStart[0])):
                        if cmp(rectEnd[1], self.rectStart[1]) != 0:
                            for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                                if self.currentMap.tilePosExists((x, y)):
                                    rggViews.sendTileUpdate(self.currentMap.ID, (x, y), self.tilelabel.currentTile)
                        else:
                            if self.currentMap.tilePosExists((x, self.rectStart[1])):
                                rggViews.sendTileUpdate(self.currentMap.ID, (x, self.rectStart[1]), self.tilelabel.currentTile)
                else:
                    if cmp(rectEnd[1], self.rectStart[1]) != 0:
                        for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                            if self.currentMap.tilePosExists((self.rectStart[0], y)):
                                rggViews.sendTileUpdate(self.currentMap.ID, (self.rectStart[0], y), self.tilelabel.currentTile)
                    else:
                        #print "WHY ARE YOU USING THE RECTANGLE TOOL TO PAINT A SINGLE TILE? THE MIND REELS"
                        if self.currentMap.tilePosExists((self.rectStart[0], self.rectStart[1])):
                                rggViews.sendTileUpdate(self.currentMap.ID, (self.rectStart[0], self.rectStart[1]), self.tilelabel.currentTile)
                rggEvent.setEaten()
            elif self.isVisible() and self.hollowRectPaintingButton.isChecked() and self.rectStart is not None:
                rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                if not map.tilePosExists(rectEnd):
                    rggEvent.setEaten()
                    self.rectStart = None
                    self.rectEnd = None
                    return
                if cmp(rectEnd[0], self.rectStart[0]) != 0:
                    for x in range(self.rectStart[0], rectEnd[0]+cmp(rectEnd[0], self.rectStart[0]), cmp(rectEnd[0], self.rectStart[0])):
                        if cmp(rectEnd[1], self.rectStart[1]) != 0:
                            #TODO: Less lazy and inefficient implementation for this case.
                            for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                                if x == self.rectStart[0] or x == rectEnd[0] or y == self.rectStart[1] or y == rectEnd[1]:
                                    if self.currentMap.tilePosExists((x, y)):
                                        rggViews.sendTileUpdate(self.currentMap.ID, (x, y), self.tilelabel.currentTile)
                        else:
                            if self.currentMap.tilePosExists((x, self.rectStart[1])):
                                rggViews.sendTileUpdate(self.currentMap.ID, (x, self.rectStart[1]), self.tilelabel.currentTile)
                else:
                    if cmp(rectEnd[1], self.rectStart[1]) != 0:
                        for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                            if self.currentMap.tilePosExists((self.rectStart[0], y)):
                                rggViews.sendTileUpdate(self.currentMap.ID, (self.rectStart[0], y), self.tilelabel.currentTile)
                    else:
                        if self.currentMap.tilePosExists((self.rectStart[0], self.rectStart[1])):
                                rggViews.sendTileUpdate(self.currentMap.ID, (self.rectStart[0], self.rectStart[1]), self.tilelabel.currentTile)
                rggEvent.setEaten()

    def mapChangedResponse(self, newMap):
        if newMap != None:
            self.currentMap = newMap
            self.tilepixmap = QtGui.QPixmap()
            self.tilepixmap.load(newMap.tileset)
            if self.tilelabel is None:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height(), self)
            else:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height(), self, self.tilelabel.currentTile)
            self.tilelabel.setPixmap(self.tilepixmap)
            self.scrollarea.setWidget(self.tilelabel)

def hajimaru(mainwindow):
    widget = mapEditor(mainwindow)
