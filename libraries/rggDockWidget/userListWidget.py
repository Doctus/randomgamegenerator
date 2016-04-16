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

from libraries.rggQt import QListWidget, QDockWidget, QWidget, QGridLayout, Qt, QPushButton
from libraries.rggSystem import signal
from libraries.rggDialogs import banDialog
from libraries.rggConstants import BASE_STRING

class userListList(QListWidget):

	def __init__(self, parent, ulmain):
		QListWidget.__init__(self)
		self.ulmain = ulmain
		self.itemActivated.connect(self.changeGM)

	def changeGM(self, item):
		self.ulmain.provideOptions(self.currentRow())

class userListWidget(QDockWidget):
	"""The list of connected users."""

	def __init__(self, mainWindow):
		"""Initializes the user list."""
		super(QDockWidget, self).__init__(mainWindow)
		self.setToolTip(self.tr("People presently playing."))
		self.setWindowTitle(self.tr("Connected Users"))
		self.widget = QWidget(mainWindow)
		self.listOfUsers = userListList(mainWindow, self)
		self.internalList = []
		self.layout = QGridLayout()
		self.layout.addWidget(self.listOfUsers, 0, 0, 1, 2)
		self.widget.setLayout(self.layout)
		self.widget.setMaximumWidth(200) #Arbitrary; keeps it from taking over 1/3 of the screen
		self.setWidget(self.widget)
		self.setObjectName("User List Widget")
		self.gmname = None
		self.localname = None
		mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self)

	def addUser(self, name, host=False):
		self.internalList.append((name, host))
		nametmp = name
		if host:
			if name == self.localname:
				self.kickbutton = QPushButton(self.tr("Kick"))
				self.kickbutton.setToolTip(self.tr("Disconnect the selected user."))
				self.layout.addWidget(self.kickbutton, 1, 0)
				self.kickbutton.clicked.connect(self.requestKick)
				self.banbutton = QPushButton(self.tr("Manage Banlist"))
				self.banbutton.setToolTip(self.tr("View and edit a list of banned IPs."))
				self.layout.addWidget(self.banbutton, 1, 1)
				self.banbutton.clicked.connect(self.openBanDialog)
			nametmp = "[Host] " + nametmp
		if self.gmname == name:
			nametmp = "[GM] " + nametmp
		self.listOfUsers.addItem(nametmp)

	def removeUser(self, name):
		for i, item in enumerate(self.internalList):
			if item[0] == name:
				self.internalList.pop(i)
				self.listOfUsers.takeItem(i)

	def getUsers(self):
		return self.internalList

	def clearUserList(self):
		self.internalList = []
		self.listOfUsers.clear()

	def refreshDisplay(self):
		self.listOfUsers.clear()
		for item in self.internalList:
			nametmp = item[0]
			if item[1]:
				nametmp = "[Host] " + nametmp
			if self.gmname == item[0]:
				nametmp = "[GM] " + nametmp
			self.listOfUsers.addItem(nametmp)

	def setGM(self, new):
		self.gmname = new
		self.refreshDisplay()

	def provideOptions(self, ID):
		if self.gmname != self.localname:
			return
		name = self.internalList[ID][0]
		#self.setGM(name)
		self.selectGM.emit(name)

	def requestKick(self):
		name = self.internalList[self.listOfUsers.currentRow()][0]
		if name == self.localname:
			return
		self.kickPlayer.emit(name)

	def openBanDialog(self):
		banDialog().exec_()
		self.requestBanlistUpdate.emit()

	selectGM = signal(BASE_STRING, doc=
		"""Called to request a menu be summoned containing actions targeting the selected player.
			Sorry for the misleading legacy name."""
	)

	kickPlayer = signal(BASE_STRING, doc=
		"""Called to request player kicking."""
	)

	requestBanlistUpdate = signal(doc=
		"""Called to request that the banlist be updated."""
	)
