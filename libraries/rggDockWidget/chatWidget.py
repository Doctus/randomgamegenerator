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

from libraries.rggQt import QLineEdit, Qt, QDockWidget, QTextBrowser, QWidget, QBoxLayout, QDesktopServices, QUrl
from libraries.rggSystem import signal
from libraries.rggJson import loadString, jsonload
from libraries.rggConstants import SAVE_DIR, UNICODE_STRING, LOG_DIR, BASE_STRING

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
		self.messageCache = []

		try:
			js = jsonload(ospath.join(SAVE_DIR, "ui_settings.rgs"))
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

		mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self)

		self.widgetEditor.anchorClicked.connect(self.anchorClicked)
		self.widgetLineInput.returnPressed.connect(self.processInput)

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

	def anchorClicked(self, url):
		'''If the url appears to be one of the /tell links in a player name, load it to the input.'''
		if "/tell" in UNICODE_STRING(url):
			self.widgetLineInput.setText(url.toString())
		else:
			QDesktopServices.openUrl(QUrl(url))

	def toggleTimestamp(self, newsetting):
		if newsetting == "On":
			self.timestamp = True
		else:
			self.timestamp = False

	def insertMessage(self, mes):
		self.scroll = (self.widgetEditor.verticalScrollBar().value() ==
				   self.widgetEditor.verticalScrollBar().maximum())
		if self.timestamp:
			message = " ".join((strftime(self.timestampformat, localtime()), mes))
			self.messageCache.append(message)
			self.widgetEditor.append(message)
		else:
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

	def processTags(self, message):
		message = message.replace("<", "&lt;").replace(">", "&gt;")
		for validTag in ("i", "b", "u", "s"):
			message = message.replace("".join(("[", validTag, "]")), "".join(("<", validTag, ">")))
			message = message.replace("".join(("[", "/", validTag, "]")), "".join(("<", "/", validTag, ">")))
		message = sub(r"\[url\](.*?)\[/url\]", r"<a href=\1>\1</a>", message)
		message = message.replace("/>", ">") #prevents anchor from closing with trailing slash in URL
		return message

	def processInput(self):
		self.newmes = UNICODE_STRING(self.widgetLineInput.text())
		self.newmes = self.processTags(self.newmes)
		self.widgetLineInput.clear()
		self.widgetLineInput.addMessage(self.newmes)
		self.chatInput.emit(self.newmes)

	chatInput = signal(BASE_STRING, doc=
		"""Called when chat input is received.

		text -- the message entered

		"""
	)
