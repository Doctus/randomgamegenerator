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

from time import strftime, localtime
from os import path as ospath

from libraries.rggQt import QLineEdit, Qt, QDockWidget, QTextBrowser, QWidget, QLabel, QComboBox, QPushButton, QGridLayout, QPixmap, QImage
from libraries.rggSystem import signal, promptSaveFile, promptYesNo, showErrorMessage
from libraries.rggDialogs import newCharacterDialog
from libraries.rggJson import loadObject, loadString, jsondump, jsonload
from libraries.rggConstants import CHAR_DIR, UNICODE_STRING, PORTRAIT_DIR, LOG_DIR, BASE_STRING

class chatLineEdit(QLineEdit):

	def __init__(self, mainWindow):
		super(QLineEdit, self).__init__(mainWindow)
		self.position = 0
		self.messageHistory = []
		self.lastInput = ''

	def addMessage(self, mes):
		self.messageHistory.append(mes)
		self.position = len(self.messageHistory)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Up and self.position > 0:
			#print "up!"
			if self.position == len(self.messageHistory):
				self.lastInput = self.text()
			self.position -= 1
			self.setText(self.messageHistory[self.position])
		elif event.key() == Qt.Key_Down:
			#print "down!"
			if self.position < len(self.messageHistory) - 1:
				self.position += 1
				self.setText(self.messageHistory[self.position])
			elif self.position == len(self.messageHistory) - 1:
				self.setText(self.lastInput)
				self.position += 1
		QLineEdit.keyPressEvent(self, event)

class ICChar():
	"""I should probably be in another file but I'm here anyway! Nyah!"""

	def __init__(self, i, na, por):
		self.id = i
		self.name = na
		self.portrait = por

	def dump(self):
		"""Serialize to a (ry"""
		return dict(
			id=self.id,
			name=self.name,
			portrait=self.portrait)

	@staticmethod
	def load(obj):
		"""Deserialize (ry"""
		char = ICChar(
			loadString('ICChar.id', obj.get('id')),
			loadString('ICChar.name', obj.get('name')),
			loadString('ICChar.portrait', obj.get('portrait')))
		return char

class ICChatWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)
		self.setToolTip(self.tr("A widget for in-character chat."))
		self.setWindowTitle(self.tr("IC Chat"))
		self.widgetEditor = QTextBrowser(mainWindow)
		self.widgetLineInput = chatLineEdit(mainWindow)
		self.widgetLineInput.setToolTip(self.tr("Type text here and press Enter or Return to transmit it."))
		self.widget = QWidget(mainWindow)
		self.widgetEditor.setReadOnly(True)
		self.widgetEditor.setOpenLinks(False)
		self.characterPreview = QLabel(mainWindow)
		self.characterSelector = QComboBox(mainWindow)
		self.characterSelector.setToolTip(self.tr("Select the character to be displayed as the speaker of entered text."))
		self.characterAddButton = QPushButton(self.tr("Add New"), mainWindow)
		self.characterAddButton.setToolTip(self.tr("Add a new in-character chat character via a dialog box."))
		self.characterDeleteButton = QPushButton(self.tr("Delete"), mainWindow)
		self.characterDeleteButton.setToolTip(self.tr("Delete the currently selected in-character chat character."))
		self.characterClearButton = QPushButton(self.tr("Clear"), mainWindow)
		self.characterClearButton.setToolTip(self.tr("Deletes all in-character chat characters."))
		self.layout = QGridLayout()
		self.layout.addWidget(self.widgetEditor, 0, 0, 1, 4)
		self.layout.addWidget(self.widgetLineInput, 1, 1, 1, 3)
		self.layout.addWidget(self.characterPreview, 1, 0, 2, 1)
		self.layout.addWidget(self.characterDeleteButton, 2, 3, 1, 1)
		self.layout.addWidget(self.characterClearButton, 3, 3, 1, 1)
		self.layout.addWidget(self.characterAddButton, 2, 2, 1, 1)
		self.layout.addWidget(self.characterSelector, 2, 1, 1, 1)
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("IC Chat Widget")
		self.messageCache = []

		self.setAcceptDrops(True)

		mainWindow.addDockWidget(Qt.LeftDockWidgetArea, self)

		#TODO: Store and access characters in a better fashion.
		try:
			self.load(jsonload(ospath.join(CHAR_DIR, "autosave.rgc")))
		except:
			self.characters = []

		self.widgetLineInput.returnPressed.connect(self.processInput)
		self.characterAddButton.clicked.connect(self.newCharacter)
		self.characterDeleteButton.clicked.connect(self.deleteCharacter)
		self.characterClearButton.clicked.connect(self.clearCharacters)
		self.characterSelector.currentIndexChanged.connect(self.setCharacterPreview)

		self.updateDeleteButton()

		self.setCharacterPreview()

	def toggleDarkBackgroundSupport(self, dark):
		if dark:
			self.widgetEditor.document().setDefaultStyleSheet("a {color: cyan; }")
		else:
			self.widgetEditor.document().setDefaultStyleSheet("a {color: blue; }")
		self.refreshMessages()

	def refreshMessages(self):
		'''Clear the text display and re-add all messages with current style settings etc.'''
		self.widgetEditor.clear()
		for message in self.messageCache:
			self.widgetEditor.append(message)

	def updateDeleteButton(self):
		self.characterDeleteButton.setEnabled(self.hasCharacters())
		self.characterClearButton.setEnabled(self.hasCharacters())
		self.characterSelector.setEnabled(self.hasCharacters())
		self.widgetLineInput.setEnabled(self.hasCharacters())

	def setCharacterPreview(self, newIndex=-1):
		try:
			preview = QPixmap(ospath.join(UNICODE_STRING(PORTRAIT_DIR), UNICODE_STRING(self.characters[self.characterSelector.currentIndex()].portrait)))
			if preview.isNull(): #Sadly, we have to check ahead, because Qt is dumb and prints an error about the scaling instead of raising one we can catch.
				raise TypeError
			preview = preview.scaled(min(preview.width(), 64), min(preview.height(), 64))
			self.characterPreview.setPixmap(preview)
		except:
			self.characterPreview.clear()

	def insertMessage(self, mes):
		self.scroll = (self.widgetEditor.verticalScrollBar().value() ==
				   self.widgetEditor.verticalScrollBar().maximum())
		self.messageCache.append(mes)
		self.widgetEditor.append(mes)
		if self.scroll:
			self.widgetEditor.verticalScrollBar().setValue(self.widgetEditor.verticalScrollBar().maximum())
		try:
			try:
				self.logfile = open(ospath.join(LOG_DIR, strftime("%b_%d_%Y.log", localtime())), 'a')
				self.logfile.write(mes+"\n")
			finally:
				self.logfile.close()
		except:
			pass

	def dragEnterEvent(self, event):
		if event.mimeData().hasImage():
			event.acceptProposedAction()

	def dropEvent(self, event):
		if event.mimeData().hasImage():
			dat = event.mimeData().imageData()
			img = QImage(dat)
			filename = promptSaveFile('Save Portrait', 'Portrait files (*.png)', PORTRAIT_DIR)
			if filename is not None:
				img.save(filename, "PNG")
			event.acceptProposedAction()

	def newCharacter(self):
		dialog = newCharacterDialog()

		def accept():
			valid = dialog.is_valid()
			if not valid:
				showErrorMessage(dialog.error)
			return valid

		if dialog.exec_(self.parentWidget(), accept):
			newchardat = dialog.save()
			newchar = ICChar(*newchardat)
			self.characterSelector.addItem(newchar.id)
			self.characters.append(newchar)
			jsondump(self.dump(), ospath.join(CHAR_DIR, "autosave.rgc"))
			self.characterSelector.setCurrentIndex(self.characterSelector.count()-1)
			self.updateDeleteButton()
			self.setCharacterPreview()

	def _newChar(self, char):
		self.characterSelector.addItem(char.id)
		self.characters.append(char)
		jsondump(self.dump(), ospath.join(CHAR_DIR, "autosave.rgc"))

	def deleteCharacter(self):
		if self.hasCharacters():
			self.characters.pop(self.characterSelector.currentIndex())
			self.characterSelector.removeItem(self.characterSelector.currentIndex())
			jsondump(self.dump(), ospath.join(CHAR_DIR, "autosave.rgc"))
			self.updateDeleteButton()

	def clearCharacters(self):
		if promptYesNo('Really clear all characters?') == 16384:
			self.characters = []
			self.characterSelector.clear()
			jsondump(self.dump(), ospath.join(CHAR_DIR, "autosave.rgc"))
			self.updateDeleteButton()
			self.setCharacterPreview()

	def processTags(self, message):
		message = message.replace("<", "&lt;").replace(">", "&gt;")
		for validTag in ("i", "b", "u", "s"):
			message = message.replace("".join(("[", validTag, "]")), "".join(("<", validTag, ">")))
			message = message.replace("".join(("[", "/", validTag, "]")), "".join(("<", "/", validTag, ">")))
		return message

	def processInput(self):
		self.newmes = UNICODE_STRING(self.widgetLineInput.text())
		self.newmes = self.processTags(self.newmes)
		self.widgetLineInput.clear()
		self.widgetLineInput.addMessage(self.newmes)
		self.ICChatInput.emit(self.newmes,
							UNICODE_STRING(self.characters[self.characterSelector.currentIndex()].name),
							UNICODE_STRING(self.characters[self.characterSelector.currentIndex()].portrait))

	def hasCharacters(self):
		return len(self.characters) > 0

	def dump(self):
		"""Serialize to an object valid for JSON dumping."""

		return dict(
			chars=dict([(i, char.dump()) for i, char in enumerate(self.characters)]))

	def load(self, obj):
		"""Deserialize set of IC characters from a dictionary."""

		self.characters = []
		self.characterSelector.clear()

		chars = loadObject('ICChatWidget.chars', obj.get('chars'))
		chartemp = [None]*len(list(chars.keys()))
		for ID, char in list(chars.items()):
			chartemp[int(ID)] = char
		for char in chartemp:
			loaded = ICChar.load(char)
			self._newChar(loaded)
		self.updateDeleteButton()
		self.setCharacterPreview()

	ICChatInput = signal(BASE_STRING, BASE_STRING, BASE_STRING, doc=
		"""Called when in-character chat input is received.

		charname -- the character name currently selected
		text -- the message entered
		portrait -- the portrait path, relative to data/portraits

		""")
