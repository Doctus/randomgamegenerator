from PyQt4 import QtGui, QtCore
from rggSystem import signal, findFiles, POG_DIR, IMAGE_EXTENSIONS
import os, os.path

class chatLineEdit(QtGui.QLineEdit):

    def __init__(self, mainWindow):
        super(QtGui.QLineEdit, self).__init__(mainWindow)
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
        QtGui.QLineEdit.keyPressEvent(self, event)

class chatWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setWindowTitle(self.tr("Chat"))
        self.widgetEditor = QtGui.QTextBrowser(mainWindow)
        self.widgetLineInput = chatLineEdit(mainWindow)
        self.widget = QtGui.QWidget(mainWindow)
        self.widgetEditor.setReadOnly(True)
        self.widgetEditor.setOpenLinks(False)
        self.layout = QtGui.QBoxLayout(2)
        self.layout.addWidget(self.widgetEditor)
        self.layout.addWidget(self.widgetLineInput)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
        
        self.widgetLineInput.returnPressed.connect(self.processInput)
    
    def insertMessage(self, mes):
        self.scroll = (self.widgetEditor.verticalScrollBar().value() ==
                   self.widgetEditor.verticalScrollBar().maximum())
        self.widgetEditor.append(mes)
        if self.scroll:
            self.widgetEditor.verticalScrollBar().setValue(self.widgetEditor.verticalScrollBar().maximum())
    
    def processInput(self):
        self.newmes = unicode(self.widgetLineInput.text())
        self.widgetLineInput.clear()
        self.widgetLineInput.addMessage(self.newmes)
        self.chatInput.emit(self.newmes)
    
    chatInput = signal(basestring, doc=
        """Called when chat input is received.
        
        text -- the message entered
        
        """
    )
    
class diceRoller(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setWindowTitle(self.tr("Dice"))
        self.realwidget = QtGui.QWidget(mainWindow) #I messed up on the initial setup and was too lazy to rename everything.
        self.widget = QtGui.QBoxLayout(2)
        self.diceArea = QtGui.QListWidget(mainWindow)
        self.macros = [QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), "Sample: 2d6"),
                       QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), "Sample: 4k2")]
        for m in self.macros:
            self.diceArea.addItem(m)
        self.diceArea.currentRowChanged.connect(self.changeCurrentMacro)
        
        self.controlArea = QtGui.QWidget(mainWindow)
        self.controlLayout = QtGui.QBoxLayout(2)
        self.rollbutton = QtGui.QPushButton(self.tr("Roll"), mainWindow)
        self.addmacrobutton = QtGui.QPushButton(self.tr("Add Macro"), mainWindow)
        self.removemacrobutton = QtGui.QPushButton(self.tr("Delete Macro"), mainWindow)
        self.connect(self.rollbutton, QtCore.SIGNAL('pressed()'), self.rollDice)
        self.connect(self.addmacrobutton, QtCore.SIGNAL('pressed()'), self.summonMacro)
        self.connect(self.removemacrobutton, QtCore.SIGNAL('pressed()'), self.removeCurrentMacro)
        self.controlLayout.addWidget(self.rollbutton)
        self.controlLayout.addWidget(self.addmacrobutton)
        self.controlLayout.addWidget(self.removemacrobutton)
        self.controlArea.setLayout(self.controlLayout)
        self.widget.addWidget(self.diceArea)
        self.widget.addWidget(self.controlArea)
        self.realwidget.setLayout(self.widget)
        self.setWidget(self.realwidget)
        mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
        self.currentMacro = -1

    def changeCurrentMacro(self, n):
        self.currentMacro = n
    
    def rollDice(self):
        current = self.diceArea.item(self.currentMacro)
        if current is not None:
            text = unicode(current.text())
            self.rollRequested.emit(text[text.rfind(':')+1:])

    def addMacro(self, mac, macname):
        self.macros.append(QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), macname + ': ' + mac))
        self.diceArea.addItem(self.macros[len(self.macros)-1])

    def removeCurrentMacro(self):
        if self.diceArea.item(self.currentMacro) != self.diceArea.currentItem(): #This SHOULD, probably, only occur if there are two items and the first is deleted. Probably.
            self.diceArea.takeItem(0)
            return
        self.diceArea.takeItem(self.currentMacro)

    def summonMacro(self):
        self.macroRequested.emit()
    
    rollRequested = signal(basestring, doc=
        """Called when the roll button is hit.
        
        roll -- the dice to be rolled
        
        """
    )
    
    macroRequested = signal(doc=
        """Called when the add macro button is pressed."""
    )
    


#It turns out to be hard to do the map editor as I intended because HTML can't get individual tiles,
# and nothing that can display individual tiles seems to have appropriate "word wrap". -Doctus
'''class mapEditor(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__("Map Editor", mainWindow)
        self.widget = QtGui.QWidget(mainWindow)
        self.mainLayout = QtGui.QBoxLayout(2)
        self.tileArea = QtGui.QTextEdit(' ', mainWindow)
        self.tileArea.setReadOnly(True)
        self.mainLayout.addWidget(self.tileArea)
        self.widget.setLayout(self.mainLayout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)

    def updateTileset(self, tileset, maxtiles):
        self.extraordinaryPineapple = []
        for tile in range(0, maxtiles):
            self.extraordinaryPineapple.append(<img src="data/pogs/yue.png">
        self.tileArea.setHTML('''

class pogPalette(QtGui.QDockWidget):
    """The list of loaded pogs."""
    
    def __init__(self, mainWindow):
        """Initializes the pog palette."""
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setWindowTitle(self.tr("Pog Palette"))
        self.widget = QtGui.QWidget(mainWindow)
        self.mainLayout = QtGui.QBoxLayout(2)
        self.pogArea = QtGui.QListWidget(mainWindow)
        self.controlArea = QtGui.QWidget(mainWindow)
        self.controlLayout = QtGui.QBoxLayout(2)
        self.addpogbutton = QtGui.QPushButton(self.tr("Update"), mainWindow)
        self.controlLayout.addWidget(self.addpogbutton)
        self.controlArea.setLayout(self.controlLayout)
        self.mainLayout.addWidget(self.pogArea)
        self.mainLayout.addWidget(self.controlArea)
        self.widget.setLayout(self.mainLayout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
        
        self.addpogbutton.pressed.connect(self.addPog)
        self.pogArea.itemActivated.connect(self.place)
        self.addPog()
    
    def addPog(self):
        """Add all pogs from the pog directory."""
        #TODO: Refactor into a view.
        self.pogArea.clear()
        self.pogs = findFiles(POG_DIR, IMAGE_EXTENSIONS)
        for greatJustice in self.pogs:
            icon = QtGui.QIcon(QtGui.QIcon(greatJustice).pixmap(QtCore.QSize(32, 32)))
            self.pogArea.addItem(QtGui.QListWidgetItem(icon, greatJustice))
    
    def place(self, pog):
        """Place a pog on the map."""
        self.pogPlaced.emit(os.path.join(POG_DIR, unicode(pog.text())))

    pogPlaced = signal(basestring, doc=
        """Called to request pog placement on the map."""
    )
    
class characterSheet(QtGui.QDockWidget):

    def __init__(self, mainWindow, charName):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        try:
            self.setWindowTitle(charName)
        except:
            self.setWindowTitle(self.tr("Character Sheet"))
        self.fields = []

class characterSheet_DND3dot5e(characterSheet):
    
    def __init__(self, mainWindow, charName):
        characterSheet.__init__(self, mainWindow, charName)
    
