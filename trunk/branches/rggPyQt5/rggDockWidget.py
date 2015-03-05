from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from rggSystem import signal, findFiles, makePortableFilename, promptSaveFile, promptYesNo, getMapPosition, mainWindow
from rggDialogs import newCharacterDialog, banDialog
from rggJson import loadObject, loadString, jsondump, jsonload, jsonappend
import os, os.path, time, re
from rggConstants import *
from rggEvent import addMapChangedListener, addMousePressListener, addMouseMoveListener, addMouseReleaseListener
#import rggEvent

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
		
		mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
		
	def updateItem(self, client, filename, status):
		'''Update the status of a transfer, creating a new table row for it if it's new.'''
		if client.username + filename not in list(self.transferDict.keys()):
			self.transferDict[client.username + filename] = self.transferTable.rowCount()
			self.transferTable.setRowCount(self.transferTable.rowCount() + 1)
			for column in (0, 1, 2):
				self.transferTable.setItem(self.transferTable.rowCount() - 1, column, QTableWidgetItem(""))
				self.transferTable.item(self.transferTable.rowCount() - 1, column).setFlags(QtCore.Qt.NoItemFlags)
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
		processedAmount = "".join((str(round(float(processed)/float(size)*100, 1)), "%"))
		self.updateItem(client, filename, processedAmount)

class debugConsoleWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)
		self.setToolTip(self.tr("A console that prints debug information regarding the program."))
		self.setWindowTitle(self.tr("Debug Console"))
		self.widgetEditor = QTextBrowser(mainWindow)
		self.widget = QWidget(mainWindow)
		self.widgetEditor.setReadOnly(True)
		self.widgetEditor.setOpenLinks(False)
		self.logToFileToggle = QCheckBox(self.tr("Log to file"))
		try:
			if jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))["debuglog"] == "On":
				self.logToFileToggle.setChecked(True)
			else:
				self.logToFileToggle.setChecked(False)
		except:
			self.logToFileToggle.setChecked(True)
		self.logToFileToggle.stateChanged.connect(self.saveLogToggle)
		self.layout = QBoxLayout(2)
		self.layout.addWidget(self.widgetEditor)
		self.layout.addWidget(self.logToFileToggle)
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("Debug Console")
		
		self.buffer = []
		
		mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
		
	def saveLogToggle(self, int):
		if int == 0:
			jsonappend({'debuglog':'Off'}, os.path.join(SAVE_DIR, "ui_settings.rgs"))
		else:
			jsonappend({'debuglog':'On'}, os.path.join(SAVE_DIR, "ui_settings.rgs"))
		
	def write(self, data):
		try:
			self.buffer.append(data)
			if data.endswith('\n'):
				self.widgetEditor.append(''.join(self.buffer))
				if self.logToFileToggle.isChecked():
					with open(os.path.join(LOG_DIR, time.strftime("%b_%d_%Y_debug.log", time.localtime())), 'a') as f:
						f.write(''.join(self.buffer))
				self.buffer = []
		except UnicodeEncodeError:
			return
			
	def flush(self):
		pass

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
		if event.key() == QtCore.Qt.Key_Up and self.position > 0:
			#print "up!"
			if self.position == len(self.messageHistory):
				self.lastInput = self.text()
			self.position -= 1
			self.setText(self.messageHistory[self.position])
		elif event.key() == QtCore.Qt.Key_Down:
			#print "down!"
			if self.position < len(self.messageHistory) - 1:
				self.position += 1
				self.setText(self.messageHistory[self.position])
			elif self.position == len(self.messageHistory) - 1:
				self.setText(self.lastInput)
				self.position += 1
		QLineEdit.keyPressEvent(self, event)

class chatWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)
		self.setToolTip(self.tr("A widget for out-of-character chat and system messages."))
		self.setWindowTitle(self.tr("OOC Chat / System"))
		self.widgetEditor = QTextBrowser(mainWindow)
		self.widgetLineInput = chatLineEdit(mainWindow)
		self.widgetLineInput.setToolTip(self.tr("Type text here and press Enter or Return to transmit it."))
		self.widget = QWidget(mainWindow)
		self.widgetEditor.setReadOnly(True)
		self.widgetEditor.setOpenLinks(False)
		self.layout = QBoxLayout(2)
		self.layout.addWidget(self.widgetEditor)
		self.layout.addWidget(self.widgetLineInput)
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("Chat Widget")
		self.timestamp = False
		self.timestampformat = "[%H:%M:%S]"

		try:
			js = jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))
		except:
			pass
		try:
			self.toggleTimestamp(loadString('chatWidget.timestamp', js.get('timestamp')))
		except:
			pass
		try:
			self.timestampformat = loadString('chatWidget.timestampformat', js.get('timestampformat'))
		except:
			pass
		
		mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
		
		self.widgetEditor.anchorClicked.connect(self.anchorClicked)
		self.widgetLineInput.returnPressed.connect(self.processInput)
		
	def anchorClicked(self, url):
		'''If the url appears to be one of the /tell links in a player name, load it to the input.'''
		if "/tell" in str(url):
			self.widgetLineInput.setText(url.toString())
		else:
			QDesktopServices.openUrl(QtCore.QUrl(url))

	def toggleTimestamp(self, newsetting):
		if newsetting == "On":
			self.timestamp = True
		else:
			self.timestamp = False
	
	def insertMessage(self, mes):
		self.scroll = (self.widgetEditor.verticalScrollBar().value() ==
				   self.widgetEditor.verticalScrollBar().maximum())
		if self.timestamp:
			self.widgetEditor.append(" ".join((time.strftime(self.timestampformat, time.localtime()), mes)))
		else:
			self.widgetEditor.append(mes)
		if self.scroll:
			self.widgetEditor.verticalScrollBar().setValue(self.widgetEditor.verticalScrollBar().maximum())
		try:
			try:
				self.logfile = open(os.path.join(LOG_DIR, time.strftime("%b_%d_%Y.log", time.localtime())), 'a')
				self.logfile.write(mes+"\n")
			finally:
				self.logfile.close()
		except:
			pass

	def processTags(self, message):
		message = message.replace("<", "&lt;").replace(">", "&gt;")
		for validTag in ("i", "b", "u", "s"):
			message = message.replace("".join(("[", validTag, "]")), "".join(("<", validTag, ">")))
			message = message.replace("".join(("[", "/", validTag, "]")), "".join(("<", "/", validTag, ">")))
		message = re.sub(r"\[url\](.*?)\[/url\]", r"<a href=\1>\1</a>", message)
		message = message.replace("/>", ">") #prevents anchor from closing with trailing slash in URL
		return message
	
	def processInput(self):
		self.newmes = str(self.widgetLineInput.text())
		self.newmes = self.processTags(self.newmes)
		self.widgetLineInput.clear()
		self.widgetLineInput.addMessage(self.newmes)
		self.chatInput.emit(self.newmes)
	
	chatInput = signal(str, doc=
		"""Called when chat input is received.
		
		text -- the message entered
		
		"""
	)
	
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
		
		self.setAcceptDrops(True)
		
		mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
		
		#TODO: Store and access characters in a better fashion.
		try:
			self.load(jsonload(os.path.join(CHAR_DIR, "autosave.rgc")))
		except:
			self.characters = []
		
		self.widgetLineInput.returnPressed.connect(self.processInput)
		self.characterAddButton.clicked.connect(self.newCharacter)
		self.characterDeleteButton.clicked.connect(self.deleteCharacter)
		self.characterClearButton.clicked.connect(self.clearCharacters)
		self.characterSelector.currentIndexChanged.connect(self.setCharacterPreview)
		
		self.updateDeleteButton()
		
		self.setCharacterPreview()
	
	def updateDeleteButton(self):
		if len(self.characters) == 0:
			self.characterDeleteButton.setEnabled(False)
		else:
			self.characterDeleteButton.setEnabled(True)
	
	def setCharacterPreview(self, newIndex=-1):
		try:
			preview = QPixmap(os.path.join(str(PORTRAIT_DIR), str(self.characters[self.characterSelector.currentIndex()].portrait)))
			if preview.isNull(): #Sadly, we have to check ahead, because Qt is dumb and prints an error about the scaling instead of raising one we can catch.
				raise TypeError
			preview = preview.scaled(min(preview.width(), 64), min(preview.height(), 64))
			self.characterPreview.setPixmap(preview)
		except:
			self.characterPreview.clear()
	
	def insertMessage(self, mes):
		self.scroll = (self.widgetEditor.verticalScrollBar().value() ==
				   self.widgetEditor.verticalScrollBar().maximum())
		self.widgetEditor.append(mes)
		if self.scroll:
			self.widgetEditor.verticalScrollBar().setValue(self.widgetEditor.verticalScrollBar().maximum())
		try:
			try:
				self.logfile = open(os.path.join(LOG_DIR, time.strftime("%b_%d_%Y.log", time.localtime())), 'a')
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
			jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))
			self.characterSelector.setCurrentIndex(self.characterSelector.count()-1)
			self.updateDeleteButton()
			self.setCharacterPreview()
			
	def _newChar(self, char):
		self.characterSelector.addItem(char.id)
		self.characters.append(char)
		jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))
			
	def deleteCharacter(self):
		if len(self.characters) > 0:
			self.characters.pop(self.characterSelector.currentIndex())
			self.characterSelector.removeItem(self.characterSelector.currentIndex())
			jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))
			self.updateDeleteButton()
			
	def clearCharacters(self):
		if promptYesNo('Really clear all characters?') == 16384:
			self.characters = []
			self.characterSelector.clear()
			jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))
			self.updateDeleteButton()
			self.setCharacterPreview()

	def processTags(self, message):
		message = message.replace("<", "&lt;").replace(">", "&gt;")
		for validTag in ("i", "b", "u", "s"):
			message = message.replace("".join(("[", validTag, "]")), "".join(("<", validTag, ">")))
			message = message.replace("".join(("[", "/", validTag, "]")), "".join(("<", "/", validTag, ">")))
		return message
		
	def processInput(self):
		self.newmes = str(self.widgetLineInput.text())
		self.newmes = self.processTags(self.newmes)
		self.widgetLineInput.clear()
		self.widgetLineInput.addMessage(self.newmes)
		self.ICChatInput.emit(self.newmes,
							str(self.characters[self.characterSelector.currentIndex()].name),
							str(self.characters[self.characterSelector.currentIndex()].portrait))
							
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
	
	ICChatInput = signal(str, str, str, doc=
		"""Called when in-character chat input is received.
		
		charname -- the character name currently selected
		text -- the message entered
		portrait -- the portrait path, relative to data/portraits
		
		""")
	
class diceRoller(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)
		self.setWindowTitle(self.tr("Dice"))
		self.realwidget = QWidget(mainWindow) #I messed up on the initial setup and was too lazy to rename everything.
		self.widget = QGridLayout()
		self.diceArea = QListWidget(mainWindow)
		try:
			self.load(jsonload(os.path.join(SAVE_DIR, "dice.rgd")))
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
		mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
		self.close()
		self.currentMacro = -1

	def changeCurrentMacro(self, n):
		self.currentMacro = n
	
	def rollDice(self):
		current = self.diceArea.item(self.currentMacro)
		if current is not None:
			text = str(current.text())
			self.rollRequested.emit(text[text.rfind(':')+1:])
			
	def _addMacro(self, macro):
		self.macros.append(QListWidgetItem(QIcon('data/dice.png'), macro))
		self.diceArea.addItem(self.macros[len(self.macros)-1])

	def addMacro(self, mac, macname):
		self.macros.append(QListWidgetItem(QIcon('data/dice.png'), macname + ': ' + mac))
		self.diceArea.addItem(self.macros[len(self.macros)-1])
		jsondump(self.dump(), os.path.join(SAVE_DIR, "dice.rgd"))

	def removeCurrentMacro(self):
		if self.diceArea.item(self.currentMacro) != self.diceArea.currentItem(): #This SHOULD, probably, only occur if there are two items and the first is deleted. Probably.
			self.diceArea.takeItem(0)
			return
		self.diceArea.takeItem(self.currentMacro)
		jsondump(self.dump(), os.path.join(SAVE_DIR, "dice.rgd"))

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
			macroz.append(str(self.diceArea.item(i).text(), 'UTF-8'))

		return dict(
			macros=dict([(i, macro) for i, macro in enumerate(macroz)]))
	
	rollRequested = signal(str, doc=
		"""Called when the roll button is hit.
		
		roll -- the dice to be rolled
		
		"""
	)
	
	macroRequested = signal(doc=
		"""Called when the add macro button is pressed."""
	)

class PogFileSystemModel(QFileSystemModel):

	def __init__(self):
		super(QFileSystemModel, self).__init__()
		self.setRootPath(POG_DIR)
		self.setNameFilters(IMAGE_NAME_FILTER)
		self.setNameFilterDisables(False)
		self.absRoot = os.path.abspath(str(POG_DIR))
		
	def data(self, index, role):
		return None
		basedata = QFileSystemModel.data(self, index, role)
		if basedata.canConvert(69):
			nodes = [index,]
			while nodes[0].parent().isValid():
				nodes.insert(0, nodes[0].parent())
			paths = []
			for node in nodes:
				paths.append(str(self.data(node, 0).toString()))
			if len(os.path.splitdrive(os.getcwd())[0]) > 0:
				paths[0] = os.path.splitdrive(os.getcwd())[0]+"\\"
			path = os.path.join(*paths)
			if os.path.isfile(path):
				return QIcon(path)
		return basedata
		
	def mimeData(self, indices):
		path = makePortableFilename(os.path.join(POG_DIR, str(self.filePath(indices[0])[len(self.absRoot)+1:])))
		
		if not os.path.isfile(path): return None
		
		mime = QtCore.QMimeData()
		mime.setText(str(path))
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
			drag.setHotSpot(QtCore.QPoint(0, 0))
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
		self.controlArea = QWidget(mainWindow)
		self.controlLayout = QBoxLayout(2)
		self.controlArea.setLayout(self.controlLayout)
		self.mainLayout.addWidget(self.pogArea)
		self.mainLayout.addWidget(self.controlArea)
		self.widget.setLayout(self.mainLayout)
		self.setWidget(self.widget)
		self.setObjectName("Pog Palette")
		mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
	
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
		mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
		
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
		
	selectGM = signal(str, doc=
		"""Called to request a menu be summoned containing actions targeting the selected player.
			Sorry for the misleading legacy name."""
	)
	
	kickPlayer = signal(str, doc=
		"""Called to request player kicking."""
	)
	
	requestBanlistUpdate = signal(doc=
		"""Called to request that the banlist be updated."""
	)
	
class fileItem(QListWidgetItem):

	def __init__(self, file, dir, panel):
		QListWidgetItem.__init__(self)
		self.file = file
		self.dir = dir
		
		self.setText(file[5:len(file)-3])

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
		self.currentTile = (ev.x()/self.tilex) + abs((ev.y()/self.tiley)-self.openglfix)*self.wrap
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
		self.moveMapButton = QPushButton("Move Map", mainWindow)
		self.layout.addWidget(self.scrollarea, 0, 0, 1, 2)
		self.layout.addWidget(self.noPaintingButton, 1, 0)
		self.layout.addWidget(self.singlePaintingButton, 2, 0)
		self.layout.addWidget(self.rectPaintingButton, 3, 0)
		self.layout.addWidget(self.hollowRectPaintingButton, 4, 0)
		self.layout.addWidget(self.undoButton, 1, 1)
		self.layout.addWidget(self.redoButton, 2, 1)
		self.layout.addWidget(self.moveMapButton, 3, 1)
		self.layout.addWidget(self.currentTileLabel, 5, 1)
		self.layout.addWidget(self.currentTileLabelLabel, 5, 0)
		self.tilelabel = None
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("Map Editor")
		mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

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
		from rggViews import _sendTileUpdate
		redoTiles = []
		for data in self.undo.pop():
			redoTiles.append((data[0], data[1], _sendTileUpdate(data[0], data[1], data[2])))
		self.redo.append(redoTiles)
		self.redoButton.setEnabled(True)
		if len(self.undo) == 0:
			self.undoButton.setEnabled(False)
			
	def _redo(self):
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
		self.tilepix = self.tilepix.copy(QtCore.QRect(*self.tilelabel.currentTileDimensions))
		self.currentTileLabel.setPixmap(self.tilepix)
		
	def mousePressResponse(self, x, y, t):
		mapPosition = getMapPosition((x, y))
		
		#This and similar things were a regrettable necessity in the plugin -> nonplugin conversion process.
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
			from rggViews import topmap
			mapPosition = getMapPosition((x, y))
			map = topmap(mapPosition)
			if map == None:
				self.dragging = False
				return
			clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
							int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
			
			if map.tilePosExists(clickedtile) and map.getTile(clickedtile) != self.tilelabel.currentTile:
				from rggViews import _sendTileUpdate
				oldtile = _sendTileUpdate(map.ID, clickedtile, self.tilelabel.currentTile)
				self.undo[-1].append((map.ID, clickedtile, oldtile))
			return True
			
	def mouseReleaseResponse(self, x, y, t):
		if t == 0:
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
