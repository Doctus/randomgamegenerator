'''
rggDialogs - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Design inspired by Django Forms.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import os, os.path
import rggMap
from rggSystem import fake, translate, showErrorMessage, findFiles, makePortableFilename
from rggFields import integerField, floatField, stringField, dropDownField, sliderField, validationError
from rggNet import ConnectionData, localHost
from rggJson import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from rggConstants import *

class dialog(object):
	"""A base class for dialogs.
	
	"""
	
	def __init__(self):
		"""Initializes the dialog, with optional parameters."""
		self.cleanData = None
		self._error = None
	
	def clean(self):
		"""Check for errors and return well-formatted data."""
		raise NotImplementedError()
	
	@property
	def error(self):
		"""Access any errors on this dialog."""
		self.is_valid()
		return self._error
	
	def is_valid(self):
		"""Return true if the data is valid and complete."""
		try:
			self.clean()
			assert(self.cleanData is not None)
			return True
		except validationError as e:
			self.cleanData = None
			if len(e.args) > 0:
				self._error = e.args[0]
			else:
				# Catch-all shouldn't be seen by end-users
				self._error = translate('dialog', "There is an error in your input.")
	
	def save(self):
		"""Utilize validated data to make changes."""
		raise NotImplementedError()

class createSurveyDialog(QDialog):
	""" A dialog for creating surveys to send to other users."""
	
	def __init__(self, mainWindow):
		QDialog.__init__(self, mainWindow)
		
		self.setWindowTitle("Create Survey")
		
		self.addedItems = []
		
		self.addbutton = QPushButton("Add")
		self.types = QComboBox()
		self.sendToLabel = QLabel("Send to: ")
		self.sendTo = QLineEdit()
		
		self.multiChoicePromptLabel = QLabel("Prompt: ")
		self.multiChoicePrompt = QLineEdit()
		self.multiChoiceOptions = QTextEdit()
		self.fillInPromptLabel = QLabel("Prompt: ")
		self.fillInPrompt = QLineEdit()
		self.YesNoPromptLabel = QLabel("Prompt: ")
		self.YesNoPrompt = QLineEdit()
		self.allThatApplyPromptLabel = QLabel("Prompt: ")
		self.allThatApplyPrompt = QLineEdit()
		self.allThatApplyOptions = QTextEdit()
		
		self.okButton = QPushButton("Ok")
		self.cancelButton = QPushButton("Cancel")
	
		self.addbutton.clicked.connect(self.addNewItem)
		self.okButton.clicked.connect(self.okPressed)
		self.cancelButton.clicked.connect(self.cancelPressed)
		
		for itemtype in ("Multiple choice", "Fill-in", "Yes/no", "Check all that apply"):
			self.types.addItem(itemtype)
		
		self.layoutt = QGridLayout()
		self.layoutt.addWidget(self.addbutton, 0, 1)
		self.layoutt.addWidget(self.types, 0, 0)
		self.layoutt.addWidget(self.sendToLabel, 10, 0)
		self.layoutt.addWidget(self.sendTo, 10, 1)
		self.layoutt.addWidget(self.okButton, 11, 0)
		self.layoutt.addWidget(self.cancelButton, 11, 1)
		
		self.layoutt.addWidget(self.multiChoicePromptLabel, 1, 0)
		self.layoutt.addWidget(self.multiChoicePrompt, 1, 1)
		self.layoutt.addWidget(self.multiChoiceOptions, 2, 0, 1, 2)
		self.layoutt.addWidget(self.fillInPromptLabel, 1, 0)
		self.layoutt.addWidget(self.fillInPrompt, 1, 1)
		self.layoutt.addWidget(self.YesNoPromptLabel, 1, 0)
		self.layoutt.addWidget(self.YesNoPrompt, 1, 1)
		self.layoutt.addWidget(self.allThatApplyPromptLabel, 1, 0)
		self.layoutt.addWidget(self.allThatApplyPrompt, 1, 1)
		self.layoutt.addWidget(self.allThatApplyOptions, 2, 0, 1, 2)
		
		self.setLayout(self.layoutt)
		
		self.types.currentIndexChanged.connect(self.displayOptions)
		self.displayOptions()
		
	def displayOptions(self, nothing=True):
		self.multiChoicePromptLabel.hide()
		self.multiChoicePrompt.hide()
		self.multiChoiceOptions.hide()
		self.fillInPromptLabel.hide()
		self.fillInPrompt.hide()
		self.YesNoPromptLabel.hide()
		self.YesNoPrompt.hide()
		self.allThatApplyPromptLabel.hide()
		self.allThatApplyPrompt.hide()
		self.allThatApplyOptions.hide()
		if self.types.currentText() == "Multiple choice":
			self.multiChoicePromptLabel.show()
			self.multiChoicePrompt.show()
			self.multiChoiceOptions.show()
		elif self.types.currentText() == "Fill-in":
			self.fillInPromptLabel.show()
			self.fillInPrompt.show()
		elif self.types.currentText() == "Yes/no":
			self.YesNoPromptLabel.show()
			self.YesNoPrompt.show()
		elif self.types.currentText() == "Check all that apply":
			self.allThatApplyPromptLabel.show()
			self.allThatApplyPrompt.show()
			self.allThatApplyOptions.show()
			
	def addNewItem(self):
		if self.types.currentText() == "Multiple choice":
			self.addedItems.append({"type":"Multiple choice", "prompt":str(self.multiChoicePrompt.text()), "options":list(str(self.multiChoiceOptions.toPlainText()).split("\n"))})
			self.multiChoicePrompt.clear()
			self.multiChoiceOptions.clear()
		elif self.types.currentText() == "Fill-in":
			self.addedItems.append({"type":"Fill-in", "prompt":str(self.fillInPrompt.text())})
			self.fillInPrompt.clear()
		elif self.types.currentText() == "Yes/no":
			self.addedItems.append({"type":"Yes/no", "prompt":str(self.YesNoPrompt.text())})
			self.YesNoPrompt.clear()
		elif self.types.currentText() == "Check all that apply":
			self.addedItems.append({"type":"Check all that apply", "prompt":str(self.allThatApplyPrompt.text()), "options":list(str(self.allThatApplyOptions.toPlainText()).split("\n"))})
			self.allThatApplyPrompt.clear()
			self.allThatApplyOptions.clear()
		
	def okPressed(self, checked):
		self.done(1)

	def cancelPressed(self, checked):
		self.done(0)
		
class respondSurveyDialog(QDialog):
	"""A dialog containing a survey from another user."""
	
	def __init__(self, questions, mainWindow):
		QDialog.__init__(self, mainWindow)
		
		self.layoutt = QGridLayout()
		self.responseAssociation = {}
		
		if len(questions) < 6:
			horiz = 2
		elif len(questions) < 10:
			horiz = 3
		else:
			horiz = 4
		
		for i, question in enumerate(questions):
			if question["type"] == "Multiple choice":
				label = QLabel(question["prompt"])
				options = QButtonGroup()
				box = QGroupBox()
				minilayout = QVBoxLayout()
				minilayout.addWidget(label)
				for option in question["options"]:
					button = QRadioButton(option)
					options.addButton(button)
					minilayout.addWidget(button)
				box.setLayout(minilayout)
				self.layoutt.addWidget(box, i/horiz, i%horiz)
				self.responseAssociation[question["prompt"]] = ("M", options)
			elif question["type"] == "Fill-in":
				label = QLabel(question["prompt"])
				box = QGroupBox()
				minilayout = QVBoxLayout()
				minilayout.addWidget(label)
				lineedit = QLineEdit()
				minilayout.addWidget(lineedit)
				box.setLayout(minilayout)
				self.layoutt.addWidget(box, i/horiz, i%horiz)
				self.responseAssociation[question["prompt"]] = ("F", lineedit)
			elif question["type"] == "Yes/no":
				label = QLabel(question["prompt"])
				options = QButtonGroup()
				box = QGroupBox()
				minilayout = QVBoxLayout()
				minilayout.addWidget(label)
				for option in ("Yes", "No"):
					button = QRadioButton(option)
					options.addButton(button)
					minilayout.addWidget(button)
				box.setLayout(minilayout)
				self.layoutt.addWidget(box, i/horiz, i%horiz)
				self.responseAssociation[question["prompt"]] = ("Y", options)
			elif question["type"] == "Check all that apply":
				label = QLabel(question["prompt"])
				opts = []
				box = QGroupBox()
				minilayout = QVBoxLayout()
				minilayout.addWidget(label)
				for option in question["options"]:
					button = QCheckBox(option)
					opts.append(button)
					minilayout.addWidget(button)
				box.setLayout(minilayout)
				self.layoutt.addWidget(box, i/horiz, i%horiz)
				self.responseAssociation[question["prompt"]] = ("C", opts)
			
		self.okButton = QPushButton("Ok")
		self.cancelButton = QPushButton("Cancel")
		
		self.layoutt.addWidget(self.okButton, 80, 1)
		self.layoutt.addWidget(self.cancelButton, 80, 0)
		self.setLayout(self.layoutt)

		self.okButton.clicked.connect(self.okPressed)
		self.cancelButton.clicked.connect(self.cancelPressed)
	
	def getAnswers(self):
		answers = {}
		for key, value in list(self.responseAssociation.items()):
			if value[0] == "M" or value[0] == "Y":
				answers[key] = str(value[1].checkedButton().text())
			elif value[0] == "F":
				answers[key] = str(value[1].text())
			elif value[0] == "C":
				results = []
				for item in value[1]:
					if item.isChecked():
						results.append(str(item.text()))
				answers[key] = "; ".join(results)
		return answers
	
	def okPressed(self, checked):
		self.done(1)

	def cancelPressed(self, checked):
		self.done(0)

class surveyResultsDialog(QDialog):
	"""A dialog containing another user's answers to a survey."""
	
	def __init__(self, answers, origin, mainWindow):
		QDialog.__init__(self, mainWindow)
		layoutt = QVBoxLayout()
		self.setWindowTitle("Response from " + origin)
		for question, answer in list(answers.items()):
			box = QGroupBox()
			minilayout = QVBoxLayout()
			quest = QLabel(question)
			minilayout.addWidget(quest)
			ans = QLabel(answer)
			minilayout.addWidget(ans)
			box.setLayout(minilayout)
			layoutt.addWidget(box)
		self.setLayout(layoutt)
		
class resizeDialog(QDialog):

	def __init__(self, origx, origy, currw, currh, mainWindow):
		QDialog.__init__(self, mainWindow)
		self.owlabel = QLabel("Current Width:")
		self.ohlabel = QLabel("Current Height:")
		self.owlabel2 = QLabel(str(origx))
		self.ohlabel2 = QLabel(str(origy))
		self.setWindowTitle("Resize Pog")

		self.wlabel = QLabel("New Width:")
		self.hlabel = QLabel("New Height:")

		self.wBox = QSpinBox()
		self.hBox = QSpinBox()
		self.wBox.setRange(1, 4096)
		self.hBox.setRange(1, 4096)
		self.wBox.setValue(currw)
		self.hBox.setValue(currh)

		self.okButton = QPushButton("Ok")
		self.cancelButton = QPushButton("Cancel")

		self.okButton.clicked.connect(self.okPressed)
		self.cancelButton.clicked.connect(self.cancelPressed)

		self.layout = QGridLayout()
		self.layout.addWidget(self.owlabel, 0, 0)
		self.layout.addWidget(self.ohlabel, 1, 0)
		self.layout.addWidget(self.owlabel2, 0, 1)
		self.layout.addWidget(self.ohlabel2, 1, 1)

		self.layout.addWidget(self.wlabel, 2, 0)
		self.layout.addWidget(self.hlabel, 3, 0)
		self.layout.addWidget(self.wBox, 2, 1)
		self.layout.addWidget(self.hBox, 3, 1)
		self.layout.addWidget(self.okButton, 4, 0)
		self.layout.addWidget(self.cancelButton, 4, 1)
		self.setLayout(self.layout)

	def okPressed(self, checked):
		self.done(1)

	def cancelPressed(self, checked):
		self.done(0)
		
class modifyPogAttributesDialog(QDialog):
	"""A dialog allowing the user to view and modify a pog's attributes."""

	def __init__(self, properties, mainWindow):
		QDialog.__init__(self, mainWindow)
		self.setWindowTitle("Edit Attributes")
		
		self.currentProperties = properties
		
		self.table = QTableWidget(len(self.currentProperties)+1, 2, self)
		self.table.setHorizontalHeaderLabels(["Attribute", "Value"])
		for i, key in enumerate(self.currentProperties.keys()):
			self.table.setItem(i, 0, QTableWidgetItem(key))
		for i, value in enumerate(self.currentProperties.values()):
			self.table.setItem(i, 1, QTableWidgetItem(value)) 

		self.okButton = QPushButton("Ok")
		self.cancelButton = QPushButton("Cancel")

		self.okButton.clicked.connect(self.okPressed)
		self.cancelButton.clicked.connect(self.cancelPressed)

		self.layout = QGridLayout()
		self.layout.addWidget(self.table, 0, 0, 1, 2)
		self.layout.addWidget(self.okButton, 1, 0)
		self.layout.addWidget(self.cancelButton, 1, 1)
		self.setLayout(self.layout)
		
		self.table.cellChanged.connect(self.respondChange)
		
	def respondChange(self, row, column):
		self.currentProperties = {}
		for tableRow in range(self.table.rowCount() + 1):
			try:
				assert len(str(self.table.item(tableRow, 0).text())) > 0
				assert len(str(self.table.item(tableRow, 1).text())) > 0
				self.currentProperties[str(self.table.item(tableRow, 0).text())] = str(self.table.item(tableRow, 1).text())
			except AttributeError:
				pass
			except KeyError:
				pass
			except AssertionError:
				pass
		if row == self.table.rowCount() - 1 and self.table.item(row, 0) and len(str(self.table.item(row, 0).text())) > 0:
			self.table.setRowCount(self.table.rowCount() + 1)

	def okPressed(self, checked):
		self.done(1)

	def cancelPressed(self, checked):
		self.done(0)

class banDialog(QDialog):
	"""A dialog used to manage the server banlist."""

	def __init__(self):
		QDialog.__init__(self)
		self.setWindowTitle("Banlist")
		
		self.list = QListWidget(self)
		for item in self.loadList():
			self.list.addItem(QListWidgetItem(item))
			
		self.inputBox = QLineEdit(self)
		
		self.addButton = QPushButton("Add")
		self.deleteButton = QPushButton("Delete")
		self.okButton = QPushButton("Ok")
		self.cancelButton = QPushButton("Cancel")
		
		self.layout = QGridLayout()
		self.layout.addWidget(self.list, 0, 0, 1, 2)
		self.layout.addWidget(self.inputBox, 1, 0, 1, 2)
		self.layout.addWidget(self.addButton, 2, 0)
		self.layout.addWidget(self.deleteButton, 2, 1)
		self.layout.addWidget(self.okButton, 3, 0)
		self.layout.addWidget(self.cancelButton, 3, 1)

		self.addButton.clicked.connect(self.add)
		self.deleteButton.clicked.connect(self.delete)
		self.okButton.clicked.connect(self.okPressed)
		self.cancelButton.clicked.connect(self.cancelPressed)
		
		self.setLayout(self.layout)
		
	def loadList(self):
		"""Returns the currently saved bans, or a blank list if
		   file access fails for any reason."""
		try:
			obj = jsonload(os.path.join(SAVE_DIR, "banlist.rgs"))
			return obj["IPs"]
		except:
			return []
		
	def saveList(self):
		ips = []
		for i in range(self.list.count()):
			ips.append(str(self.list.item(i).text()))
		iplist = {"IPs":ips}
		jsondump(iplist, os.path.join(SAVE_DIR, "banlist.rgs"))
		
	def add(self):
		self.list.addItem(self.inputBox.text())
		self.inputBox.clear()
		
	def delete(self):
		self.list.takeItem(self.list.currentRow())
		
	def okPressed(self, checked):
		self.saveList()
		self.done(1)

	def cancelPressed(self, checked):
		self.done(0)
		
class newMapDialog(dialog):
	"""A dialog used to create a new map."""
	
	def __init__(self, **kwargs):
		"""Initializes the dialog data."""
		super(newMapDialog, self).__init__()
		self.fields = self._createFields(kwargs)
	
	def _createFields(self, data):
		"""Create the fields used by this dialog."""
		
		tilesets = findFiles(TILESET_DIR, IMAGE_EXTENSIONS)
		if len(tilesets) <= 0:
			raise RuntimeError(translate('newMapDialog',
				'Cannot create a map when no tilesets are available.'))
				
		self.tilesetField = dropDownField(translate('newMapDialog', 'Tileset'), tilesets, value=data.get('tileset', tilesets[0]))
		
		return dict(
			mapName=stringField(translate('newMapDialog', 'Map Name'),
				value=data.get('mapName', translate('newMapDialog', 'Generic Map'))),
			authName=stringField(translate('newMapDialog', 'Author Name'),
				value=data.get('authName', translate('newMapDialog', 'Anonymous'))),
			tileset= self.tilesetField,
			mapWidth=integerField(translate('newMapDialog', 'Map Width'),
				min=1, max=65535, value=data.get('mapWidth', 25)),
			mapHeight=integerField(translate('newMapDialog', 'Map Height'),
				min=1, max=65535, value=data.get('mapHeight', 25)),
			tileWidth=integerField(translate('newMapDialog', 'Per-Tile Width'),
				min=1, max=65535, value=data.get('tileWidth', 32)),
			tileHeight=integerField(translate('newMapDialog', 'Per-Tile Height'),
				min=1, max=65535, value=data.get('tileHeight', 32)))
	
	def _interpretFields(self, fields):
		"""Interpret the fields into a dictionary of clean items."""
		return dict((key, field.clean()) for key, field in list(fields.items()))
	
	def exec_(self, parent, accept):
		"""Executes this dialog as modal, ensuring OK is only hit with valid data.
		
		parent -- the parent object of this dialog
		accept() -- Acceptance function;
			return True to accept data, False to continue (you should show an error)
		
		returns: True if the OK button is hit and the acceptance function passes.
		
		"""
		
		widget = QDialog(parent)
		
		# Buttons
		okayButton = QPushButton(translate('newMapDialog', "Create Map"))
		okayButton.setDefault(True)
		cancelButton = QPushButton(translate('newMapDialog', "Cancel"))
		
		# Add fields
		formLayout = QFormLayout()
		for id in ('mapName', 'authName', 'mapWidth', 'mapHeight', 'tileset', 'tileWidth', 'tileHeight'):
			field = self.fields[id]
			formLayout.addRow(translate('newMapDialog', '{0}: ', 'Row layout').format(field.name), field.widget(widget))
		
		# Add buttons
		theLesserOrFalseBox = QBoxLayout(0)
		theLesserOrFalseBox.addWidget(okayButton)
		theLesserOrFalseBox.addWidget(cancelButton)
		
		# Position both
		grandBox = QBoxLayout(2)
		grandBox.addLayout(formLayout)
		grandBox.addLayout(theLesserOrFalseBox)
		
		# Set up the widget
		widget.setLayout(grandBox)
		widget.setModal(True)
		widget.setWindowTitle(translate('newMapDialog', "New Map"))
		
		# Allow user to specify validation
		def okayPressed():
			if accept():
				widget.accept()
		
		# Signals
		okayButton.clicked.connect(okayPressed)
		cancelButton.clicked.connect(widget.reject)
		self.tilesetField.evil.connect(self.loadTilesize)
		
		self.loadTilesize()
		
		# Show to user
		return (widget.exec_() == QDialog.Accepted)
		
	def loadTilesize(self):
		"""Attempt to load a stored tilesize for the current tileset, if it exists."""
		try:
			js = jsonload(os.path.join(SAVE_DIR, "tilesets.rgs"))
			size = loadCoordinates('newMapDialog.'+self.clean()['tileset'], js.get(self.clean()['tileset']))
			self.fields['tileWidth']._widget.setValue(size[0])
			self.fields['tileHeight']._widget.setValue(size[1])
		except:
			pass
		
	def clean(self):
		"""Check for errors and return well-formatted data."""
		self.cleanData = self._interpretFields(self.fields)
		return self.cleanData
	
	def save(self):
		"""Make a new map and return it."""
		assert(self.cleanData)
		jsonappend({self.cleanData['tileset']:[self.cleanData['tileWidth'], self.cleanData['tileHeight']]}, os.path.join(SAVE_DIR, "tilesets.rgs"))
		return rggMap.Map(
			self.cleanData['mapName'],
			self.cleanData['authName'],
			(self.cleanData['mapWidth'], self.cleanData['mapHeight']),
			makePortableFilename(os.path.join('data/tilesets', self.cleanData['tileset'])),
			(self.cleanData['tileWidth'], self.cleanData['tileHeight']))
	
class hostDialog(dialog):
	"""A dialog used to specify parameters to game hosting."""
	
	def __init__(self, **kwargs):
		"""Initializes the dialog data."""
		super(hostDialog, self).__init__()
		self.fields = self._createFields(kwargs)
	
	def _createFields(self, data):
		"""Create the fields used by this dialog."""
		
		self.fieldtemp = [6812, translate('hostDialog', 'Anonymous')]
		
		try:
			js = jsonload(os.path.join(SAVE_DIR, "net_server.rgs"))
			self.fieldtemp[0] = int(loadString('hostDialog.port', js.get('port')))
			self.fieldtemp[1] = loadString('hostDialog.username', js.get('username'))
		except:
			pass
		
		return dict(
			username=stringField(
				translate('hostDialog', 'Username'),
				value=data.get('username', self.fieldtemp[1])),
			port=integerField(
				translate('hostDialog', 'Port'),
				min=1, max=65535, value=data.get('port', self.fieldtemp[0])),
			password=stringField(
				translate('hostDialog', 'Password'),
				value=data.get('password', ''),
				allowEmpty=True))
	
	def _interpretFields(self, fields):
		"""Interpret the fields into a dictionary of clean items."""
		return dict((key, field.clean()) for key, field in list(fields.items()))
	
	def exec_(self, parent, accept):
		"""Executes this dialog as modal, ensuring OK is only hit with valid data.
		
		parent -- the parent object of this dialog
		accept() -- Acceptance function;
			return True to accept data, False to continue (you should show an error)
		
		returns: True if the OK button is hit and the acceptance function passes.
		
		"""
		
		widget = QDialog(parent)
		
		# Buttons
		okayButton = QPushButton(translate('hostDialog', "Host"))
		okayButton.setDefault(True)
		cancelButton = QPushButton(translate('hostDialog', "Cancel"))
		checkIPButton = QPushButton(translate('hostDialog', "Check IP"))
		self.checkIPLabel = QLineEdit()
		self.checkIPLabel.setReadOnly(True)
		self.wordIPLabel = QLineEdit()
		self.wordIPLabel.setReadOnly(True)
		
		# Add fields
		formLayout = QFormLayout()
		for id in ('port', 'username', 'password'):
			field = self.fields[id]
			formLayout.addRow(
				translate('hostDialog', '{0}: ', 'Row layout').format(field.name),
				field.widget(widget))
		
		# Set up layout
		grandBox = QGridLayout()
		grandBox.addLayout(formLayout, 0, 0, 1, 2)
		grandBox.addWidget(checkIPButton, 1, 0)
		grandBox.addWidget(self.checkIPLabel, 1, 1)
		grandBox.addWidget(self.wordIPLabel, 2, 0, 1, 2)
		grandBox.addWidget(okayButton, 3, 0)
		grandBox.addWidget(cancelButton, 3, 1)
		
		# Set up the widget
		widget.setLayout(grandBox)
		widget.setModal(True)
		widget.setWindowTitle(translate('hostDialog', "Host Game"))
		
		# Allow user to specify validation
		def okayPressed():
			if accept():
				widget.accept()
		
		# Signals
		okayButton.clicked.connect(okayPressed)
		cancelButton.clicked.connect(widget.reject)
		checkIPButton.clicked.connect(self.checkIP)
		
		# Show to user
		return (widget.exec_() == QDialog.Accepted)

	def checkIP(self):
		import urllib.request, urllib.error, urllib.parse
		ip = str(urllib.request.urlopen('http://31.25.101.129/rgg_ip.php').read())
		
		with open("2of12inf.txt", "r") as f:
			dat = f.readlines()
			ipdat = ip.split(".")
			vals = ((int(ipdat[0])*256+int(ipdat[1])),(int(ipdat[2])*256+int(ipdat[3])))
			wordresult = " ".join((dat[vals[0]][:-1], dat[vals[1]][:-1]))
			
		self.checkIPLabel.setText(ip)
		self.wordIPLabel.setText(wordresult)
	
	def dump(self):
		return dict(username=self.cleanData['username'],
					port=str(self.cleanData['port']))
		
	def clean(self):
		"""Check for errors and return well-formatted data."""
		self.cleanData = self._interpretFields(self.fields)
		return self.cleanData
	
	def save(self):
		"""Make a new map and return it."""
		assert(self.cleanData)
		try:
			jsondump(self.dump(), os.path.join(SAVE_DIR, "net_server.rgs"))
		except:
			pass
		return ConnectionData(localHost(), self.cleanData['port'],
			self.cleanData['username'], self.cleanData['password'])
	
class joinDialog(dialog):
	"""A dialog used to specify parameters to game joining."""
	
	def __init__(self, **kwargs):
		"""Initializes the dialog data."""
		super(joinDialog, self).__init__()
		self.fields = self._createFields(kwargs)
	
	def _createFields(self, data):
		"""Create the fields used by this dialog."""
		
		self.fieldtemp = [localHost(), 6812, translate('joinDialog', 'Anonymous')]
		
		try:
			js = jsonload(os.path.join(SAVE_DIR, "net_settings.rgs"))
			self.fieldtemp[0] = loadString('joinDialog.host', js.get('host'))
			self.fieldtemp[1] = int(loadString('joinDialog.port', js.get('port')))
			self.fieldtemp[2] = loadString('joinDialog.username', js.get('username'))
		except:
			pass
		
		return dict(
			username=stringField(translate('joinDialog', 'Username'),
				value=data.get('username', self.fieldtemp[2])),
			host=stringField(translate('joinDialog', 'Host Name (IP)'),
				value=data.get('host', self.fieldtemp[0])),
			port=integerField(translate('joinDialog', 'Port'),
				min=1, max=65535, value=data.get('port', self.fieldtemp[1])),
			password=stringField(
				translate('joinDialog', 'Password'),
				value=data.get('password', ''),
				allowEmpty=True))
	
	def _interpretFields(self, fields):
		"""Interpret the fields into a dictionary of clean items."""
		return dict((key, field.clean()) for key, field in list(fields.items()))
	
	def exec_(self, parent, accept):
		"""Executes this dialog as modal, ensuring OK is only hit with valid data.
		
		parent -- the parent object of this dialog
		accept() -- Acceptance function;
			return True to accept data, False to continue (you should show an error)
		
		returns: True if the OK button is hit and the acceptance function passes.
		
		"""
		
		widget = QDialog(parent)
		
		# Buttons
		okayButton = QPushButton(translate('joinDialog', "Join"))
		okayButton.setDefault(True)
		cancelButton = QPushButton(translate('joinDialog', "Cancel"))
		
		warningLabel1 = QLabel(translate('joinDialog', "Warning: open maps or other session"))
		warningLabel2 = QLabel(translate('joinDialog', "data will be replaced upon joining."))
		
		# Add fields
		formLayout = QFormLayout()
		for id in ('host', 'port', 'username', 'password'):
			field = self.fields[id]
			formLayout.addRow(
				translate('joinDialog', '{0}: ', 'Row layout').format(field.name),
				field.widget(widget))
		
		# Add buttons
		theLesserOrFalseBox = QBoxLayout(0)
		theLesserOrFalseBox.addWidget(okayButton)
		theLesserOrFalseBox.addWidget(cancelButton)
		
		# Position both
		grandBox = QBoxLayout(2)
		grandBox.addLayout(formLayout)
		grandBox.addLayout(theLesserOrFalseBox)
		grandBox.addWidget(warningLabel1)
		grandBox.addWidget(warningLabel2)
		
		# Set up the widget
		widget.setLayout(grandBox)
		widget.setModal(True)
		widget.setWindowTitle(translate('joinDialog', "Join Game"))
		
		# Allow user to specify validation
		def okayPressed():
			if accept():
				widget.accept()
		
		# Signals
		okayButton.clicked.connect(okayPressed)
		cancelButton.clicked.connect(widget.reject)
		
		# Show to user
		return (widget.exec_() == QDialog.Accepted)
		
	def clean(self):
		"""Check for errors and return well-formatted data."""
		self.cleanData = self._interpretFields(self.fields)
		if len(self.cleanData['host'].split()) == 2:
			with open("2of12inf.txt", "r") as f:
				inp = self.cleanData['host'].split()
				_dat = f.readlines()
				dat = [d.strip() for d in _dat]
				wordindex = [dat.index(inp[0]), dat.index(inp[1])]
				ipextract = str(".".join((str(wordindex[0]//256), str(wordindex[0]%256), str(wordindex[1]//256), str(wordindex[1]%256))))
				self.cleanData['host'] = ipextract
		return self.cleanData
	
	def dump(self):
		return dict(host=self.cleanData['host'],
					port=str(self.cleanData['port']),
					username=str(self.cleanData['username']))
	
	def save(self):
		"""Make a new map and return it."""
		assert(self.cleanData)
		try:
			jsondump(self.dump(), os.path.join(SAVE_DIR, "net_settings.rgs"))
		except:
			pass
		return ConnectionData(self.cleanData['host'], self.cleanData['port'],
			self.cleanData['username'], self.cleanData['password'])
	
class PortraitFileSystemModel(QFileSystemModel):

	def __init__(self):
		super(QFileSystemModel, self).__init__()
		self.setRootPath(PORTRAIT_DIR)
		self.setNameFilters(IMAGE_NAME_FILTER)
		self.setNameFilterDisables(False)
		self.absRoot = os.path.abspath(str(PORTRAIT_DIR))
		
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

class PortraitTreeView(QTreeView):

	def setParent(self, parent):
		self.call = parent

	def selectionChanged(self, selected, deselected):
		super(QTreeView, self).selectionChanged(selected, deselected)
		self.call.changePort(selected)
		
class newCharacterDialog(dialog):
	"""A dialog used to create a new character for in-character chat."""
	
	def __init__(self, **kwargs):
		"""Initializes the dialog data."""
		super(newCharacterDialog, self).__init__()
		self.fields = self._createFields(kwargs)
	
	def _createFields(self, data):
		"""Create the fields used by this dialog."""
		
		return dict(
			listid=stringField(
				translate('newCharacterDialog', 'List ID'),
				value=data.get('listid', translate('newCharacterDialog', 'New Character'))),
			charactername=stringField(
				translate('newCharacterDialog', 'Character Name'),
				value=data.get('charactername', translate('newCharacterDialog', ' '))),
			portrait=stringField(
				translate('newCharacterDialog', 'Portrait'),
				value=data.get('portrait', translate('newCharacterDialog', ' '))))
	
	def _interpretFields(self, fields):
		"""Interpret the fields into a dictionary of clean items."""
		return dict((key, field.clean()) for key, field in list(fields.items()))
	
	def exec_(self, parent, accept):
		"""Executes this dialog as modal, ensuring OK is only hit with valid data.
		
		parent -- the parent object of this dialog
		accept() -- Acceptance function;
			return True to accept data, False to continue (you should show an error)
		
		returns: True if the OK button is hit and the acceptance function passes.
		
		"""
		
		widget = QDialog(parent)
		
		# Buttons
		okayButton = QPushButton(translate('newCharacterDialog', "Create"))
		okayButton.setDefault(True)
		cancelButton = QPushButton(translate('newCharacterDialog', "Cancel"))
		self.portraitModel = PortraitFileSystemModel()
		self.ROOT_LEN = len(self.portraitModel.absRoot)+1
		self.portraitArea = PortraitTreeView(parent)
		self.portraitArea.setParent(self)
		self.portraitArea.setModel(self.portraitModel)
		self.portraitArea.setRootIndex(self.portraitModel.index(PORTRAIT_DIR))
		self.portraitArea.setColumnHidden(1, True)
		self.portraitArea.setColumnHidden(2, True)
		self.portraitArea.setColumnHidden(3, True)
		self.portraitPreview = QLabel(" ")
		
		# Add fields
		formLayout = QFormLayout()
		for id in ('listid', 'charactername', 'portrait'):
			field = self.fields[id]
			formLayout.addRow(
				translate('newCharacterDialog', '{0}: ', 'Row layout').format(field.name),
				field.widget(widget))
		
		# Add buttons
		theLesserOrFalseBox = QBoxLayout(0)
		theLesserOrFalseBox.addWidget(okayButton)
		theLesserOrFalseBox.addWidget(cancelButton)
		
		# Position both
		grandBox = QBoxLayout(2)
		grandBox.addLayout(formLayout)
		grandBox.addWidget(self.portraitPreview)
		grandBox.addLayout(theLesserOrFalseBox)
		
		evilBox = QBoxLayout(0)
		evilBox.addWidget(self.portraitArea)
		evilBox.addLayout(grandBox)
		
		#self.portraitArea.pressed.connect(self.changePort)
		
		# Set up the widget
		widget.setLayout(evilBox)
		widget.setModal(True)
		widget.setWindowTitle(translate('newCharacterDialog', "Create Character"))
		
		# Allow user to specify validation
		def okayPressed():
			if accept():
				widget.accept()
		
		# Signals
		okayButton.clicked.connect(okayPressed)
		cancelButton.clicked.connect(widget.reject)
		
		#portraits = findFiles(PORTRAIT_DIR, IMAGE_EXTENSIONS)
		#portraits.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
		#for greatJustice in portraits:
		#    icon = QIcon(os.path.join(PORTRAIT_DIR, greatJustice))
		#    self.portraitArea.addItem(QListWidgetItem(icon, greatJustice))
		
		# Show to user
		return (widget.exec_() == QDialog.Accepted)
	
	def changePort(self, selection):
		for i in selection.indexes():
			portrait = i
		self.fields['portrait'].widgett.setText(str(self.portraitModel.filePath(portrait))[self.ROOT_LEN:])
		preview = QPixmap(self.portraitModel.filePath(portrait))
		if preview.isNull():
			#Typically, this means a folder has been selected.
			self.fields['portrait'].widgett.setText(str(" "))
			self.portraitPreview.clear()
			return
		preview = preview.scaled(min(preview.width(), 64), min(preview.height(), 64))
		self.portraitPreview.setPixmap(preview)
		
	def clean(self):
		"""Check for errors and return well-formatted data."""
		self.cleanData = self._interpretFields(self.fields)
		return self.cleanData
	
	def save(self):
		"""Make a new character and return it."""
		assert(self.cleanData)
		return([self.cleanData['listid'], 
				self.cleanData['charactername'], 
				self.cleanData['portrait']])

class gfxSettingsDialog(dialog):
	"""A dialog used to set graphics options."""
	
	def __init__(self, **kwargs):
		"""Initializes the dialog data."""
		super(gfxSettingsDialog, self).__init__()
		self.fields = self._createFields(kwargs)
	
	def _createFields(self, data):
		"""Create the fields used by this dialog."""
		
		self.fields = {}

		try:
			js = jsonload(os.path.join(SAVE_DIR, GFX_SETTINGS_FILE))
			for field in [ANI_FILTER_STRING,]:
				self.fields[field] = loadFloat(GFX_PREFIX + field, js.get(field))
			for field in [MIN_FILTER_STRING, MAG_FILTER_STRING, MIPMIN_FILTER_STRING, FSAA_SETTING_STRING, VBO_SETTING_STRING]:
				self.fields[field] = loadString(GFX_PREFIX + field, js.get(field))
		except IOError as e:
			print("Graphics settings file could not be loaded: %s" % e)
			self.fields = {ANI_FILTER_STRING:1.0, MIN_FILTER_STRING:"GL_NEAREST", MAG_FILTER_STRING:"GL_NEAREST", 
							MIPMIN_FILTER_STRING:"GL_NEAREST_MIPMAP_NEAREST", FSAA_SETTING_STRING:1, VBO_SETTING_STRING:1}

		return dict(
			anifilt=floatField(translate('gfxSettingsDialog', ANI_FILTER_STRING),
				min=1.0, max=16.0, decimals=1, value=data.get(ANI_FILTER_STRING, self.fields[ANI_FILTER_STRING])),
			minfilter=dropDownField(translate('gfxSettingsDialog', MIN_FILTER_STRING), STANDARD_FILTER_OPTIONS,
				value=data.get(MIN_FILTER_STRING, self.fields[MIN_FILTER_STRING])),
			magfilter=dropDownField(translate('gfxSettingsDialog', MAG_FILTER_STRING), STANDARD_FILTER_OPTIONS,
				value=data.get(MAG_FILTER_STRING, self.fields[MAG_FILTER_STRING])),
			mipminfilter=dropDownField(translate('gfxSettingsDialog', MIPMIN_FILTER_STRING), MIP_FILTER_OPTIONS,
				value=data.get(MIPMIN_FILTER_STRING, self.fields[MIPMIN_FILTER_STRING])),
			FSAA=dropDownField(translate('gfxSettingsDialog', FSAA_SETTING_STRING), ON_OFF_OPTIONS,
				value=data.get(FSAA_SETTING_STRING, self.fields[FSAA_SETTING_STRING])),
			VBO=dropDownField(translate('gfxSettingsDialog', VBO_SETTING_STRING), ON_OFF_OPTIONS,
				value=data.get(VBO_SETTING_STRING, self.fields[VBO_SETTING_STRING])))
	
	def _interpretFields(self, fields):
		"""Interpret the fields into a dictionary of clean items."""
		return dict((key, field.clean()) for key, field in list(fields.items()))
	
	def exec_(self, parent, accept):
		"""Executes this dialog as modal, ensuring OK is only hit with valid data.
		
		parent -- the parent object of this dialog
		accept() -- Acceptance function;
			return True to accept data, False to continue (you should show an error)
		
		returns: True if the OK button is hit and the acceptance function passes.
		
		"""
		
		widget = QDialog(parent)
		
		# Buttons
		okayButton = QPushButton(translate('gfxSettingsDialog', "Save"))
		okayButton.setDefault(True)
		cancelButton = QPushButton(translate('gfxSettingsDialog', "Cancel"))
		
		# Add fields
		formLayout = QFormLayout()
		for id in (ANI_FILTER_STRING, MIN_FILTER_STRING, MAG_FILTER_STRING, MIPMIN_FILTER_STRING, FSAA_SETTING_STRING, VBO_SETTING_STRING):
			field = self.fields[id]
			formLayout.addRow(translate('gfxSettingsDialog', '{0}: ', 'Row layout').format(field.name), field.widget(widget))
		
		# Add buttons
		theLesserOrFalseBox = QBoxLayout(0)
		theLesserOrFalseBox.addWidget(okayButton)
		theLesserOrFalseBox.addWidget(cancelButton)
		
		# Position both
		grandBox = QBoxLayout(2)
		grandBox.addLayout(formLayout)
		grandBox.addLayout(theLesserOrFalseBox)
		
		# Set up the widget
		widget.setLayout(grandBox)
		widget.setModal(True)
		widget.setWindowTitle(translate('gfxSettingsDialog', "Configure Graphics"))
		
		# Allow user to specify validation
		def okayPressed():
			if accept():
				widget.accept()
		
		# Signals
		okayButton.clicked.connect(okayPressed)
		cancelButton.clicked.connect(widget.reject)
		
		# Show to user
		return (widget.exec_() == QDialog.Accepted)
		
	def clean(self):
		"""Check for errors and return well-formatted data."""
		self.cleanData = self._interpretFields(self.fields)
		return self.cleanData
	
	def save(self):
		"""Make a new map and return it."""
		assert(self.cleanData)
		return self._interpretFields(self.fields)
