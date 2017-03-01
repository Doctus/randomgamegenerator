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

from os import path as ospath

from libraries.rggQt import QDockWidget, QWidget, QGridLayout, Qt, QPushButton, QTextEdit, QLabel
from libraries.rggSystem import signal
from libraries.rggDialogs import banDialog
from libraries.rggConstants import BASE_STRING, SAVE_DIR

class scratchPadWidget(QDockWidget):
	"""A mutually-editable shared text widget."""

	def __init__(self, mainWindow):
		"""Initializes the user list."""
		super(QDockWidget, self).__init__(mainWindow)
		self.setWindowTitle(self.tr("Scratch Pad"))
		self.widget = QWidget(mainWindow)
		self.textArea = QTextEdit(mainWindow)
		self.currentEditingLabel = QLabel("No one is editing.")
		self.getLockButton = QPushButton("Edit")
		self.releaseLockButton = QPushButton("Confirm")
		#self.saveToFileButton = QPushButton("Save...")
		#self.loadButton = QPushButton("Load")
		self.layout = QGridLayout()
		self.layout.addWidget(self.currentEditingLabel, 0, 0, 1, 2)
		self.layout.addWidget(self.textArea, 1, 0, 1, 2)
		self.layout.addWidget(self.getLockButton, 2, 0)
		self.layout.addWidget(self.releaseLockButton, 2, 1)
		self.releaseLockButton.pressed.connect(self._releaseLock)
		self.getLockButton.pressed.connect(self._getLock)
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("Scratch Pad Widget")
		self.hasLock = False
		self.updateButtonStatus()
		try:
			with open(ospath.join(SAVE_DIR, "scratchpad.txt"), 'r') as autosave:
				self.textArea.setText(autosave.read())
		except:
			pass
		mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self)

	@property
	def currentText(self):
		return self.textArea.toPlainText()

	def updateButtonStatus(self):
		self.getLockButton.setEnabled(not self.hasLock)
		self.textArea.setReadOnly(not self.hasLock)
		self.releaseLockButton.setEnabled(self.hasLock)

	def _getLock(self):
		self.getScratchPadLock.emit()

	def _releaseLock(self):
		self.updateScratchPad.emit()
		self.releaseScratchPadLock.emit()

	def getLock(self):
		self.hasLock = True
		self.updateButtonStatus()

	def releaseLock(self, name):
		self.hasLock = False
		if name:
			self.currentEditingLabel.setText("%s is editing." % name)
		else:
			self.currentEditingLabel.setText("No one is editing.")
		self.updateButtonStatus()

	def updateText(self, txt):
		if len(txt) > 100000:
			print("Excessively long scratchpad data received. Might be an attack or just a bug.")
			return
		self.textArea.setText(txt)
		try:
			with open(ospath.join(SAVE_DIR, "scratchpad.txt"), 'w') as autosave:
				autosave.write(txt)
		except:
			pass

	getScratchPadLock = signal(doc=
		"""Called to request lock for scratch pad."""
	)

	releaseScratchPadLock = signal(doc=
		"""Called to indicate relinquishment of scratch pad lock."""
	)

	updateScratchPad = signal(doc=
		"""Called to request that the scratchpad be updated."""
	)
