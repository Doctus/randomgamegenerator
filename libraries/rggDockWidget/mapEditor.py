'''
    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''

from libraries.rggQt import QLabel, QDockWidget, QWidget, QGridLayout, QBoxLayout, QScrollArea, QRadioButton, QPushButton, Qt, QPixmap, QRect
from libraries.rggSystem import getMapPosition
from libraries.rggConstants import NORMAL_RESPONSE_LEVEL
from libraries.rggEvent import addMapChangedListener, addMousePressListener, addMouseMoveListener, addMouseReleaseListener

class mapEditorLabel(QLabel):

	def __init__(self, tilesize, width, height, par, currentTile=0):
		super(QLabel, self).__init__()
		self.tilex, self.tiley = tilesize
		self.wid = width
		self.hei = height
		self.wrap = width / self.tilex
		self.openglfix = (height / self.tiley)-1
		self.currentTile = currentTile
		self.par = par

	def mousePressEvent(self, ev):
		self.currentTile = (int(ev.x()/self.tilex)) + abs(int(ev.y()/self.tiley)-self.openglfix)*self.wrap
		self.updateTile()

	def updateTile(self):
		self.currentTileDimensions = (self.currentTile%(self.wid/self.tilex)*self.tilex, (self.hei - self.tiley) - (int((self.currentTile*self.tilex)/self.wid)*self.tiley), self.tilex, self.tiley)
		self.par.updateCurrentTile()

class mapEditor(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)

		#self.__eat = True
		self.painting = True
		self.dragging = False
		self.rectStart = None

		self.setWindowTitle(self.tr("Map Editor"))
		self.widget = QWidget(mainWindow)
		self.layout = QGridLayout()
		self.currentTileLayout = QBoxLayout(1)
		self.scrollarea = QScrollArea(mainWindow)
		self.noPaintingButton = QRadioButton(self.tr("Stop Painting"), mainWindow)
		self.singlePaintingButton = QRadioButton(self.tr("Single Tile Brush"), mainWindow)
		self.noPaintingButton.setChecked(True)
		self.rectPaintingButton = QRadioButton(self.tr("Area (Rectangle) Brush"), mainWindow)
		self.hollowRectPaintingButton = QRadioButton(self.tr("Hollow Rectangle Brush"), mainWindow)
		self.currentTileLabel = QLabel()
		self.currentTileLabelLabel = QLabel(self.tr("Current tile: "))
		self.undoButton = QPushButton("Undo", mainWindow)
		self.redoButton = QPushButton("Redo", mainWindow)
		#self.moveMapButton = QPushButton("Move Map", mainWindow)
		self.layout.addWidget(self.scrollarea, 0, 0, 1, 2)
		self.layout.addWidget(self.noPaintingButton, 1, 0)
		self.layout.addWidget(self.singlePaintingButton, 2, 0)
		self.layout.addWidget(self.rectPaintingButton, 3, 0)
		self.layout.addWidget(self.hollowRectPaintingButton, 4, 0)
		self.layout.addWidget(self.undoButton, 1, 1)
		self.layout.addWidget(self.redoButton, 2, 1)
		#self.layout.addWidget(self.moveMapButton, 3, 1)
		self.layout.addWidget(self.currentTileLabel, 5, 1)
		self.layout.addWidget(self.currentTileLabelLabel, 5, 0)
		self.tilelabel = None
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("Map Editor")
		mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)

		self.currentMap = None
		self.copyData = None

		self.undo = []
		self.undoButton.clicked.connect(self._undo)
		self.undoButton.setEnabled(False)

		self.redo = []
		self.redoButton.clicked.connect(self._redo)
		self.redoButton.setEnabled(False)

		addMapChangedListener(self.mapChangedResponse, NORMAL_RESPONSE_LEVEL)
		addMousePressListener(self.mousePressResponse, NORMAL_RESPONSE_LEVEL)
		addMouseMoveListener(self.mouseMoveResponse, NORMAL_RESPONSE_LEVEL)
		addMouseReleaseListener(self.mouseReleaseResponse, NORMAL_RESPONSE_LEVEL)

	def _undo(self):
		try:
			from libraries.rggViews import _sendTileUpdate
		except ImportError:
			from rggViews import _sendTileUpdate
		redoTiles = []
		for data in self.undo.pop():
			redoTiles.append((data[0], data[1], _sendTileUpdate(data[0], data[1], data[2])))
		self.redo.append(redoTiles)
		self.redoButton.setEnabled(True)
		if len(self.undo) == 0:
			self.undoButton.setEnabled(False)

	def _redo(self):
		try:
			from libraries.rggViews import _sendTileUpdate
		except ImportError:
			from rggViews import _sendTileUpdate
		undoTiles = []
		for data in self.redo.pop():
			undoTiles.append((data[0], data[1], _sendTileUpdate(data[0], data[1], data[2])))
		self.undo.append(undoTiles)
		self.undoButton.setEnabled(True)
		if len(self.redo) == 0:
			self.redoButton.setEnabled(False)

	def updateCurrentTile(self):
		self.tilepix = QPixmap()
		self.tilepix.load(self.currentMap.tileset)
		self.tilepix = self.tilepix.copy(QRect(*self.tilelabel.currentTileDimensions))
		self.currentTileLabel.setPixmap(self.tilepix)

	def mousePressResponse(self, x, y, t):
		mapPosition = getMapPosition((x, y))

		#This and similar things were a regrettable necessity in the plugin -> nonplugin conversion process.
		try:
			from libraries.rggViews import topmap, _sendTileUpdate
		except ImportError:
			from rggViews import topmap, _sendTileUpdate

		map = topmap(mapPosition)
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
					return True
				oldtile = _sendTileUpdate(map.ID, clickedtile, self.tilelabel.currentTile)
				self.undo.append([(map.ID, clickedtile, oldtile),])
				self.redo = []
				self.redoButton.setEnabled(False)
				self.undoButton.setEnabled(True)
				return True
			elif self.isVisible() and (self.rectPaintingButton.isChecked() or self.hollowRectPaintingButton.isChecked()):
				self.rectStart = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
				if not map.tilePosExists(self.rectStart):
					self.rectStart = None
				return True
		elif t == 5:
			if self.isVisible() and not self.noPaintingButton.isChecked():
				clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
				self.tilelabel.currentTile = map.getTile(clickedtile)
				self.tilelabel.updateTile()
				return True
		elif t == 6:
			if self.isVisible() and not self.noPaintingButton.isChecked() and self.copyData:
				if self.singlePaintingButton.isChecked():
					clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
								int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
					for row, columns in enumerate(self.copyData):
						for column, tile in enumerate(columns):
							_sendTileUpdate(map.ID, (clickedtile[0]+row, clickedtile[1]+column), tile)
				elif self.rectPaintingButton.isChecked():
					self.rectStart = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
								int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
					if not map.tilePosExists(self.rectStart):
						self.rectStart = None
					return True
		elif t == 8:
			if self.isVisible() and not self.noPaintingButton.isChecked():
				self.rectStart = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
								int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
				if not map.tilePosExists(self.rectStart):
					self.rectStart = None
				return True

	def mouseMoveResponse(self, x, y):
		if self.dragging and self.isVisible() and self.singlePaintingButton.isChecked():
			try:
				from libraries.rggViews import topmap
			except ImportError:
				from rggViews import topmap
			mapPosition = getMapPosition((x, y))
			map = topmap(mapPosition)
			if map == None:
				self.dragging = False
				return
			clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))

			if map.tilePosExists(clickedtile) and map.getTile(clickedtile) != self.tilelabel.currentTile:
				try:
					from libraries.rggViews import _sendTileUpdate
				except ImportError:
					from rggViews import _sendTileUpdate
				oldtile = _sendTileUpdate(map.ID, clickedtile, self.tilelabel.currentTile)
				self.undo[-1].append((map.ID, clickedtile, oldtile))
			return True

	def mouseReleaseResponse(self, x, y, t):
		if t == 0:
			try:
				from libraries.rggViews import topmap, _sendTileUpdate, _sendMultipleTileUpdate
			except ImportError:
				from rggViews import topmap, _sendTileUpdate, _sendMultipleTileUpdate
			if self.currentMap == None:
				return
			mapPosition = getMapPosition((x, y))
			map = topmap(mapPosition)
			self.dragging = False
			if map == None or map != self.currentMap:
				return
			if self.isVisible() and self.singlePaintingButton.isChecked():
				return True
			elif self.isVisible() and self.rectPaintingButton.isChecked() and self.rectStart is not None:
				rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
				if not map.tilePosExists(rectEnd):
					self.rectStart = None
					self.rectEnd = None
					return
				self.undo.append([])
				self.undoButton.setEnabled(True)
				self.redo = []
				self.redoButton.setEnabled(False)
				oldtiles = _sendMultipleTileUpdate(self.currentMap.ID, (min(rectEnd[0], self.rectStart[0]), min(rectEnd[1], self.rectStart[1])), (max(rectEnd[0], self.rectStart[0]), max(rectEnd[1], self.rectStart[1])), self.tilelabel.currentTile)
				for x in range(min(rectEnd[0], self.rectStart[0]), max(rectEnd[0], self.rectStart[0])+1):
					for y in range(min(rectEnd[1], self.rectStart[1]), max(rectEnd[1], self.rectStart[1])+1):
						self.undo[-1].append((map.ID, (x, y), oldtiles.pop(0)))
				return True
			elif self.isVisible() and self.hollowRectPaintingButton.isChecked() and self.rectStart is not None:
				rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
				if not map.tilePosExists(rectEnd):
					self.rectStart = None
					self.rectEnd = None
					return
				self.undo.append([])
				self.undoButton.setEnabled(True)
				self.redo = []
				self.redoButton.setEnabled(False)
				if rectEnd[0] != self.rectStart[0]:
					for x in range(self.rectStart[0], rectEnd[0]+(1*(rectEnd[0]-self.rectStart[0])), 1*(rectEnd[0]-self.rectStart[0])):
						if rectEnd[1] != self.rectStart[1]:
							#TODO: Less lazy and inefficient implementation for this case.
							for y in range(self.rectStart[1], rectEnd[1]+1*(rectEnd[1]-self.rectStart[1]), 1*(rectEnd[1]-self.rectStart[1])):
								if x == self.rectStart[0] or x == rectEnd[0] or y == self.rectStart[1] or y == rectEnd[1]:
									if self.currentMap.tilePosExists((x, y)):
										oldtile = _sendTileUpdate(self.currentMap.ID, (x, y), self.tilelabel.currentTile)
										self.undo[-1].append((map.ID, (x, y), oldtile))
						else:
							if self.currentMap.tilePosExists((x, self.rectStart[1])):
								oldtile = _sendTileUpdate(self.currentMap.ID, (x, self.rectStart[1]), self.tilelabel.currentTile)
								self.undo[-1].append((map.ID, (x, self.rectStart[1]), oldtile))
				else:
					if rectEnd[1] != self.rectStart[1]:
						for y in range(self.rectStart[1], rectEnd[1]+1*(rectEnd[1]-self.rectStart[1]), 1*(rectEnd[1], self.rectStart[1])):
							if self.currentMap.tilePosExists((self.rectStart[0], y)):
								oldtile = _sendTileUpdate(self.currentMap.ID, (self.rectStart[0], y), self.tilelabel.currentTile)
								self.undo[-1].append((map.ID, (self.rectStart[0], y), oldtile))
					else:
						if self.currentMap.tilePosExists((self.rectStart[0], self.rectStart[1])):
								oldtile = _sendTileUpdate(self.currentMap.ID, (self.rectStart[0], self.rectStart[1]), self.tilelabel.currentTile)
								self.undo[-1].append((map.ID, (self.rectStart[0], self.rectStart[1]), oldtile))
				return True
		elif t == 6:
			if self.isVisible() and self.rectPaintingButton.isChecked() and self.copyData:
				try:
					from libraries.rggViews import topmap, _sendTileUpdate
				except ImportError:
					from rggViews import topmap, _sendTileUpdate
				if self.currentMap == None:
					return
				mapPosition = getMapPosition((x, y))
				map = topmap(mapPosition)
				self.dragging = False
				if map == None or map != self.currentMap:
					return
				rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
				if not map.tilePosExists(rectEnd):
					self.rectStart = None
					self.rectEnd = None
					return
				topleft = (min(self.rectStart[0], rectEnd[0]), min(self.rectStart[1], rectEnd[1]))
				bottomright = (max(self.rectStart[0], rectEnd[0]), max(self.rectStart[1], rectEnd[1]))
				for row in range(1+(bottomright[0]-topleft[0])):
					for column in range(1+(bottomright[1]-topleft[1])):
						_sendTileUpdate(self.currentMap.ID, (topleft[0]+row, topleft[1]+column), self.copyData[row%len(self.copyData)][column%len(self.copyData[row%len(self.copyData)])])
				return True
		elif t == 8:
			if self.isVisible() and not self.noPaintingButton.isChecked():
				try:
					from libraries.rggViews import topmap
				except ImportError:
					from rggViews import topmap
				if self.currentMap == None:
					return
				mapPosition = getMapPosition((x, y))
				map = topmap(mapPosition)
				self.dragging = False
				if map == None or map != self.currentMap:
					return
				rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
				if not map.tilePosExists(rectEnd):
					self.rectStart = None
					self.rectEnd = None
					return
				topleft = (min(self.rectStart[0], rectEnd[0]), min(self.rectStart[1], rectEnd[1]))
				bottomright = (max(self.rectStart[0], rectEnd[0]), max(self.rectStart[1], rectEnd[1]))
				copypaste = []
				for row in range(1+(bottomright[0]-topleft[0])):
					copypaste.append([])
					for column in range(1+(bottomright[1]-topleft[1])):
						copypaste[row].append(map.getTile((topleft[0]+row, topleft[1]+column)))
				self.copyData = copypaste
				return True

	def mapChangedResponse(self, newMap):
		if newMap != None:
			self.currentMap = newMap
			self.tilepixmap = QPixmap()
			self.tilepixmap.load(newMap.tileset)
			if self.tilelabel is None:
				self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height(), self)
			else:
				self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height(), self, self.tilelabel.currentTile)
			self.tilelabel.setPixmap(self.tilepixmap)
			self.scrollarea.setWidget(self.tilelabel)
