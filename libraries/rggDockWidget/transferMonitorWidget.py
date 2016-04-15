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

class transferMonitorWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)
		self.setToolTip(self.tr("Allows for monitoring and control of file transfers."))
		self.setWindowTitle(self.tr("Transfer Monitor"))
		self.transferDict = {}
		self.transferTable = QTableWidget(0, 3, mainWindow)
		self.transferTable.setHorizontalHeaderLabels(["Client", "Filename", "Status"])
		self.widget = QWidget(mainWindow)
		self.status = QLabel("Initializing", mainWindow)
		self.layout = QBoxLayout(2)
		self.layout.addWidget(self.transferTable)
		self.layout.addWidget(self.status)
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("Transfer Monitor")

		mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self)

	def updateItem(self, client, filename, status):
		'''Update the status of a transfer, creating a new table row for it if it's new.'''
		if client.username + filename not in list(self.transferDict.keys()):
			self.transferDict[client.username + filename] = self.transferTable.rowCount()
			self.transferTable.setRowCount(self.transferTable.rowCount() + 1)
			for column in (0, 1, 2):
				self.transferTable.setItem(self.transferTable.rowCount() - 1, column, QTableWidgetItem(""))
				self.transferTable.item(self.transferTable.rowCount() - 1, column).setFlags(Qt.NoItemFlags)
		self.transferTable.item(self.transferDict[client.username + filename], 0).setText(client.username)
		self.transferTable.item(self.transferDict[client.username + filename], 1).setText(filename)
		self.transferTable.item(self.transferDict[client.username + filename], 2).setText(status)
		self.transferTable.update()
		self.update()

	def processFileEvent(self, client, filename, event):
		'''Process a raw file/general status event.'''
		if len(filename) > 1:
			self.updateItem(client, filename, event)
		else:
			self.status.setText(event)
			self.update()

	def processPartialTransferEvent(self, client, filename, size, processed):
		'''Process a partial transfer event.'''
		processedAmount = "".join((UNICODE_STRING(round(float(processed)/float(size)*100, 1)), "%"))
		self.updateItem(client, filename, processedAmount)
