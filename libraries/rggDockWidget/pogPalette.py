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

from re import sub
from time import strftime, localtime
from os import path as ospath
from random import shuffle

from libraries.rggQt import *
from libraries.rggSystem import signal, findFiles, makePortableFilename, promptSaveFile, promptYesNo, getMapPosition, mainWindow, promptLoadFile
from libraries.rggDialogs import newCharacterDialog, banDialog
from libraries.rggJson import loadObject, loadString, jsondump, jsonload, jsonappend
from libraries.rggConstants import *
from libraries.rggEvent import addMapChangedListener, addMousePressListener, addMouseMoveListener, addMouseReleaseListener
from libraries.rggState import GlobalState

class PogFileSystemModel(QFileSystemModel):

	def __init__(self):
		super(QFileSystemModel, self).__init__()
		self.setRootPath(POG_DIR)
		self.setNameFilters(IMAGE_NAME_FILTER)
		self.setNameFilterDisables(False)
		self.absRoot = ospath.abspath(UNICODE_STRING(POG_DIR))

	def data(self, index, role):
		basedata = QFileSystemModel.data(self, index, role)
		if role == 1 and ospath.isfile(self.filePath(index)):
			initial = QPixmap(self.filePath(index))
			if not initial.isNull():
				return QIcon(initial.scaled(16, 16))
		return basedata

	def mimeData(self, indices):
		path = makePortableFilename(ospath.join(POG_DIR, UNICODE_STRING(self.filePath(indices[0])[len(self.absRoot)+1:])))

		if not ospath.isfile(path): return None

		mime = QMimeData()
		mime.setText(UNICODE_STRING(path))
		return mime

class pogTree(QTreeView):

	def startDrag(self, event):
		for i in self.selectedIndexes():
			drag = QDrag(self)

			#Don't drag folders.
			if not self.model().mimeData([i]): return

			#print self.model().mimeData([i]).text()

			drag.setMimeData(self.model().mimeData([i]))
			basePixmap = QPixmap(self.model().mimeData([i]).text())
			scaledPixmap = basePixmap.scaled(basePixmap.width()*mainWindow.glwidget.zoom, basePixmap.height()*mainWindow.glwidget.zoom)
			drag.setPixmap(scaledPixmap)
			drag.setHotSpot(QPoint(0, 0))
			drag.exec_()

class pogPalette(QDockWidget):
	"""The list of loaded pogs."""

	def __init__(self, mainWindow):
		"""Initializes the pog palette."""
		super(QDockWidget, self).__init__(mainWindow)
		self.setToolTip(self.tr("Drag a file from this widget into the game window to place a pog."))
		self.setWindowTitle(self.tr("Pog Palette"))
		self.widget = QWidget(mainWindow)
		self.mainLayout = QBoxLayout(2)
		self.pogsModel = PogFileSystemModel()
		self.ROOT_LEN = len(self.pogsModel.absRoot)+1
		self.pogArea = pogTree(mainWindow)
		self.pogArea.setModel(self.pogsModel)
		self.pogArea.setRootIndex(self.pogsModel.index(POG_DIR))
		self.pogArea.setColumnHidden(1, True)
		self.pogArea.setColumnHidden(2, True)
		self.pogArea.setColumnHidden(3, True)
		self.pogArea.setDragDropMode(QAbstractItemView.DragDrop)
		self.mainLayout.addWidget(self.pogArea)
		self.widget.setLayout(self.mainLayout)
		self.setWidget(self.widget)
		self.setObjectName("Pog Palette")
		mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self)
