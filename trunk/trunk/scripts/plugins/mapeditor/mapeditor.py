from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem

class mapEditorLabel(QtGui.QLabel):
    
    def __init__(self, tilesize, width, height, currentTile=0):
        super(QtGui.QLabel, self).__init__()
        self.tilex, self.tiley = tilesize
        self.wrap = width / self.tilex
        self.openglfix = (height / self.tiley)-1
        self.currentTile = currentTile
    
    def mousePressEvent(self, ev):
        print self.openglfix
        print ev.y()/self.tiley
        print abs((ev.y()/self.tiley)-self.openglfix)
        self.currentTile = (ev.x()/self.tilex) + abs((ev.y()/self.tiley)-self.openglfix)*self.wrap

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

        self.currentMap = None

        rggEvent.addMapChangedListener(self)
        rggEvent.addMousePressListener(self)
        rggEvent.addMouseMoveListener(self)
        rggEvent.addMouseReleaseListener(self)
        
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
            elif self.isVisible() and self.rectPaintingButton.isChecked():
                self.rectStart = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                            (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
                rggEvent.setEaten()
        elif t == 5:
            if self.isVisible() and (self.singlePaintingButton.isChecked() or self.rectPaintingButton.isChecked()):
                clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                self.tilelabel.currentTile = map.getTile(clickedtile)
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
            self.dragging = False
            if self.isVisible() and self.singlePaintingButton.isChecked():
                rggEvent.setEaten()
            elif self.isVisible() and self.rectPaintingButton.isChecked() and self.rectStart is not None:
                rectEnd = ((rggSystem.cameraPosition()[0] + x) / self.tilelabel.tilex,
                        (rggSystem.cameraPosition()[1] + y) / self.tilelabel.tiley)
                if cmp(rectEnd[0], self.rectStart[0]) != 0:
                    for x in range(self.rectStart[0], rectEnd[0]+cmp(rectEnd[0], self.rectStart[0]), cmp(rectEnd[0], self.rectStart[0])):
                        if cmp(rectEnd[1], self.rectStart[1]) != 0:
                            for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                                if rggViews._state.currentMap.tilePosExists((x, y)):
                                    rggViews.sendTileUpdate(rggViews._state.currentMap.ID, (x, y), self.tilelabel.currentTile)
                        else:
                            if rggViews._state.currentMap.tilePosExists((x, self.rectStart[1])):
                                rggViews.sendTileUpdate(rggViews._state.currentMap.ID, (x, self.rectStart[1]), self.tilelabel.currentTile)
                else:
                    if cmp(rectEnd[1], self.rectStart[1]) != 0:
                        for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                            if rggViews._state.currentMap.tilePosExists((self.rectStart[0], y)):
                                rggViews.sendTileUpdate(rggViews._state.currentMap.ID, (self.rectStart[0], y), self.tilelabel.currentTile)
                    else:
                        print "WHY ARE YOU USING THE RECTANGLE TOOL TO PAINT A SINGLE TILE? THE MIND REELS"
                        if rggViews._state.currentMap.tilePosExists((self.rectStart[0], self.rectStart[1])):
                                rggViews.sendTileUpdate(rggViews._state.currentMap.ID, (self.rectStart[0], self.rectStart[1]), self.tilelabel.currentTile)
                rggEvent.setEaten()

    def mapChangedResponse(self, newMap):
        if newMap != None:
            self.currentMap = newMap
            self.tilepixmap = QtGui.QPixmap()
            self.tilepixmap.load(newMap.tileset)
            if self.tilelabel is None:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height())
            else:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height(), self.tilelabel.currentTile)
            self.tilelabel.setPixmap(self.tilepixmap)
            self.scrollarea.setWidget(self.tilelabel)

def hajimaru(mainwindow):
    widget = mapEditor(mainwindow)
