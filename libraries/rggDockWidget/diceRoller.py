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


class diceRoller(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)
		self.setWindowTitle(self.tr("Dice"))
		self.realwidget = QWidget(mainWindow) #I messed up on the initial setup and was too lazy to rename everything.
		self.widget = QGridLayout()
		self.diceArea = QListWidget(mainWindow)
		try:
			self.load(jsonload(ospath.join(SAVE_DIR, "dice.rgd")))
		except:
			self.macros = [QListWidgetItem(QIcon('data/dice.png'), "Sample: 2d6"),
						   QListWidgetItem(QIcon('data/dice.png'), "Sample: 4k2"),
						   QListWidgetItem(QIcon('data/dice.png'), "Sample: 1dn3")]
		for m in self.macros:
			self.diceArea.addItem(m)
		self.diceArea.currentRowChanged.connect(self.changeCurrentMacro)
		self.rollbutton = QPushButton(self.tr("Roll"), mainWindow)
		self.rollbutton.setToolTip(self.tr("Roll dice according to the selected macro."))
		self.addmacrobutton = QPushButton(self.tr("Add Macro"), mainWindow)
		self.addmacrobutton.setToolTip(self.tr("Add a new macro via a dialog box."))
		self.removemacrobutton = QPushButton(self.tr("Delete Macro"), mainWindow)
		self.removemacrobutton.setToolTip(self.tr("Remove the currently selected macro."))
		self.rollbutton.clicked.connect(self.rollDice)
		self.addmacrobutton.clicked.connect(self.summonMacro)
		self.removemacrobutton.clicked.connect(self.removeCurrentMacro)
		self.widget.addWidget(self.diceArea, 0, 0)
		self.widget.addWidget(self.rollbutton, 1, 0)
		self.widget.addWidget(self.addmacrobutton, 2, 0)
		self.widget.addWidget(self.removemacrobutton, 3, 0)
		self.realwidget.setLayout(self.widget)
		self.setWidget(self.realwidget)
		self.setObjectName("Dice Widget")
		mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self)
		self.close()
		self.currentMacro = -1

	def changeCurrentMacro(self, n):
		self.currentMacro = n

	def rollDice(self):
		current = self.diceArea.item(self.currentMacro)
		if current is not None:
			text = UNICODE_STRING(current.text())
			self.rollRequested.emit(text[text.rfind(':')+1:])

	def _addMacro(self, macro):
		self.macros.append(QListWidgetItem(QIcon('data/dice.png'), macro))
		self.diceArea.addItem(self.macros[len(self.macros)-1])

	def addMacro(self, mac, macname):
		self.macros.append(QListWidgetItem(QIcon('data/dice.png'), macname + ': ' + mac))
		self.diceArea.addItem(self.macros[len(self.macros)-1])
		jsondump(self.dump(), ospath.join(SAVE_DIR, "dice.rgd"))

	def removeCurrentMacro(self):
		if self.diceArea.item(self.currentMacro) != self.diceArea.currentItem(): #This SHOULD, probably, only occur if there are two items and the first is deleted. Probably.
			self.diceArea.takeItem(0)
			return
		self.diceArea.takeItem(self.currentMacro)
		jsondump(self.dump(), ospath.join(SAVE_DIR, "dice.rgd"))

	def summonMacro(self):
		self.macroRequested.emit()

	def load(self, obj):
		 """Deserialize set of macros from a dictionary."""
		 self.macros = []
		 macroz = loadObject('diceRoller.macros', obj.get('macros'))
		 for ID, macro in list(macroz.items()):
			 self._addMacro(macro)

	def dump(self):
		"""Serialize to an object valid for JSON dumping."""

		macroz = []
		for i in range(0,self.diceArea.count()):
			macroz.append(UNICODE_STRING(self.diceArea.item(i).text()))

		return dict(
			macros=dict([(i, macro) for i, macro in enumerate(macroz)]))

	rollRequested = signal(BASE_STRING, doc=
		"""Called when the roll button is hit.

		roll -- the dice to be rolled

		"""
	)

	macroRequested = signal(doc=
		"""Called when the add macro button is pressed."""
	)
