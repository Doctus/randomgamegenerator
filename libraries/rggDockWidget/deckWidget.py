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

from random import shuffle

from libraries.rggQt import QDockWidget, QListWidget, QLineEdit, QPushButton, QSpinBox, QWidget, QGridLayout, Qt
from libraries.rggState import GlobalState
from libraries.rggSystem import promptLoadFile

class deckWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)
		self.setToolTip(self.tr("Allows for drawing from a virtual deck of cards."))
		self.setWindowTitle(self.tr("Deck"))
		#self.pristineCards = []
		self.cards = []

		self.deckDisplay = QListWidget()
		self.deckDisplay.itemActivated.connect(self.removeCard)
		self.cardNameField = QLineEdit()
		self.addCardButton = QPushButton("Add")
		self.addCardButton.clicked.connect(self.addCard)
		self.peekAmountField = QSpinBox()
		self.drawCardButton = QPushButton("Draw")
		self.drawCardButton.clicked.connect(self.drawCard)
		self.drawPlaceField = QSpinBox()
		self.peekCardButton = QPushButton("Peek")
		self.peekCardButton.clicked.connect(self.peekCard)
		self.refreshDeckButton = QPushButton("Initialize Deck")
		self.refreshDeckButton.clicked.connect(self.refreshDeck)
		self.shuffleDeckButton = QPushButton("Shuffle Deck")
		self.shuffleDeckButton.clicked.connect(self.shuffleDeck)
		self.loadButton = QPushButton("Load from file")
		self.loadButton.clicked.connect(self.loadFromFile)

		self.widget = QWidget(mainWindow)
		self.layout = QGridLayout()
		self.layout.addWidget(self.deckDisplay, 1, 0, 1, 2)
		self.layout.addWidget(self.cardNameField, 0, 0)
		self.layout.addWidget(self.addCardButton, 0, 1)
		self.layout.addWidget(self.drawCardButton, 2, 0)
		self.layout.addWidget(self.drawPlaceField, 2, 1)
		self.layout.addWidget(self.peekAmountField, 3, 0)
		self.layout.addWidget(self.peekCardButton, 3, 1)
		self.layout.addWidget(self.shuffleDeckButton, 4, 0)
		self.layout.addWidget(self.refreshDeckButton, 4, 1)
		self.layout.addWidget(self.loadButton, 5, 0, 1, 2)
		self.widget.setLayout(self.layout)
		self.setWidget(self.widget)
		self.setObjectName("Deck")

		mainWindow.addDockWidget(Qt.BottomDockWidgetArea, self)

		self.hide()

	def addCard(self, *args, **kwargs):
		self.deckDisplay.addItem(str(self.cardNameField.text()))

	def removeCard(self, card):
		self.deckDisplay.takeItem(self.deckDisplay.currentRow())

	def drawCard(self):
		if len(self.cards) <= 0:
			GlobalState.cwidget.insertMessage("No cards to draw!")
		else:
			card = self.cards.pop(self.drawPlaceField.value())
			GlobalState.cwidget.insertMessage(card)

	def peekCard(self):
		for i in range(self.peekAmountField.value()):
			try:
				GlobalState.cwidget.insertMessage(str(i)+": "+self.cards[i])
			except:
				GlobalState.cwidget.insertMessage(str(i)+": "+"Too few cards to peek on!")

	@property
	def pristineCards(self):
		return [str(self.deckDisplay.item(i).text()) for i in range(self.deckDisplay.count())]

	def refreshDeck(self):
		self.cards = self.pristineCards[:]
		self.shuffleDeck()

	def shuffleDeck(self):
		shuffle(self.cards)

	def loadFromFile(self):
		filename = promptLoadFile('Open Deck File',
			'Text-formatted deck file (*.txt)')
		if not filename:
			return
		with open(filename) as f:
			data = f.read()
		for item in data.split("\n"):
			if len(item) > 0:
				for i in range(int(item.split()[0])):
					self.deckDisplay.addItem(" ".join(item.split()[1:]))
