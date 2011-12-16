from PyQt4 import QtGui, QtCore, phonon
from rggSystem import signal, findFiles, POG_DIR, LOG_DIR, IMAGE_EXTENSIONS, CHAR_DIR, MUSIC_DIR, SAVE_DIR, makePortableFilename
from rggDialogs import newCharacterDialog, FIRECharacterSheetDialog
from rggJson import loadObject, loadString, jsondump, jsonload
import os, os.path, time
import rggFIRECharacter

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
        self.setToolTip(self.tr("A widget for out-of-character chat and system messages."))
        self.setWindowTitle(self.tr("OOC Chat / System"))
        self.widgetEditor = QtGui.QTextBrowser(mainWindow)
        self.widgetLineInput = chatLineEdit(mainWindow)
        self.widgetLineInput.setToolTip(self.tr("Type text here and press Enter or Return to transmit it."))
        self.widget = QtGui.QWidget(mainWindow)
        self.widgetEditor.setReadOnly(True)
        self.widgetEditor.setOpenLinks(False)
        self.layout = QtGui.QBoxLayout(2)
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
        
        self.widgetLineInput.returnPressed.connect(self.processInput)

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
    
class ICChatWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setToolTip(self.tr("A widget for in-character chat."))
        self.setWindowTitle(self.tr("IC Chat"))
        self.widgetEditor = QtGui.QTextBrowser(mainWindow)
        self.widgetLineInput = chatLineEdit(mainWindow)
        self.widgetLineInput.setToolTip(self.tr("Type text here and press Enter or Return to transmit it."))
        self.widget = QtGui.QWidget(mainWindow)
        self.widgetEditor.setReadOnly(True)
        self.widgetEditor.setOpenLinks(False)
        self.characterSelector = QtGui.QComboBox(mainWindow)
        self.characterSelector.setToolTip(self.tr("Select the character to be displayed as the speaker of entered text."))
        self.characterAddButton = QtGui.QPushButton(self.tr("Add New"), mainWindow)
        self.characterAddButton.setToolTip(self.tr("Add a new in-character chat character via a dialog box."))
        self.characterDeleteButton = QtGui.QPushButton(self.tr("Delete"), mainWindow)
        self.characterDeleteButton.setToolTip(self.tr("Delete the currently selected in-character chat character."))
        self.layout = QtGui.QBoxLayout(2)
        self.layoutni = QtGui.QBoxLayout(1)
        self.layout.addWidget(self.widgetEditor)
        self.layout.addWidget(self.widgetLineInput)
        self.layoutni.addWidget(self.characterDeleteButton)
        self.layoutni.addWidget(self.characterAddButton)
        self.layoutni.addWidget(self.characterSelector)
        self.layout.addLayout(self.layoutni)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.setObjectName("IC Chat Widget")
        mainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
        
        #TODO: Store and access characters in a better fashion.
        try:
            self.load(jsonload(os.path.join(CHAR_DIR, "autosave.rgc")))
        except:
            self.characters = []
        
        self.widgetLineInput.returnPressed.connect(self.processInput)
        self.connect(self.characterAddButton, QtCore.SIGNAL('clicked()'), self.newCharacter)
        self.connect(self.characterDeleteButton, QtCore.SIGNAL('clicked()'), self.deleteCharacter)
    
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
            
    def _newChar(self, char):
        self.characterSelector.addItem(char.id)
        self.characters.append(char)
        jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))
            
    def deleteCharacter(self):
        if self.characters is not None:
            self.characters.pop(self.characterSelector.currentIndex())
            self.characterSelector.removeItem(self.characterSelector.currentIndex())
            jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))
        
    def processInput(self):
        self.newmes = unicode(self.widgetLineInput.text())
        self.widgetLineInput.clear()
        self.widgetLineInput.addMessage(self.newmes)
        self.ICChatInput.emit(self.newmes,
                            unicode(self.characters[self.characterSelector.currentIndex()].name),
                            unicode(self.characters[self.characterSelector.currentIndex()].portrait))
                            
    def dump(self):
        """Serialize to an object valid for JSON dumping."""

        return dict(
            chars=dict([(i, char.dump()) for i, char in enumerate(self.characters)]))
    
    def load(self, obj):
        """Deserialize set of IC characters from a dictionary."""
        
        self.characters = []
        self.characterSelector.clear()
        
        chars = loadObject('ICChatWidget.chars', obj.get('chars'))
        for ID, char in chars.items():
            loaded = ICChar.load(char)
            self._newChar(loaded)
    
    ICChatInput = signal(basestring, basestring, basestring, doc=
        """Called when in-character chat input is received.
        
        charname -- the character name currently selected
        text -- the message entered
        portrait -- the portrait path, relative to data/portraits
        
        """)
    
class diceRoller(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setWindowTitle(self.tr("Dice"))
        self.realwidget = QtGui.QWidget(mainWindow) #I messed up on the initial setup and was too lazy to rename everything.
        self.widget = QtGui.QGridLayout()
        self.diceArea = QtGui.QListWidget(mainWindow)
        self.macros = [QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), "Sample: 2d6"),
                       QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), "Sample: 4k2"),
                       QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), "Sample: 1dn3")]
        for m in self.macros:
            self.diceArea.addItem(m)
        self.diceArea.currentRowChanged.connect(self.changeCurrentMacro)
        self.rollbutton = QtGui.QPushButton(self.tr("Roll"), mainWindow)
        self.rollbutton.setToolTip(self.tr("Roll dice according to the selected macro."))
        self.addmacrobutton = QtGui.QPushButton(self.tr("Add Macro"), mainWindow)
        self.addmacrobutton.setToolTip(self.tr("Add a new macro via a dialog box."))
        self.removemacrobutton = QtGui.QPushButton(self.tr("Delete Macro"), mainWindow)
        self.removemacrobutton.setToolTip(self.tr("Remove the currently selected macro."))
        self.connect(self.rollbutton, QtCore.SIGNAL('clicked()'), self.rollDice)
        self.connect(self.addmacrobutton, QtCore.SIGNAL('clicked()'), self.summonMacro)
        self.connect(self.removemacrobutton, QtCore.SIGNAL('clicked()'), self.removeCurrentMacro)
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

class pogPalette(QtGui.QDockWidget):
    """The list of loaded pogs."""
    
    def __init__(self, mainWindow):
        """Initializes the pog palette."""
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setToolTip(self.tr("Double-click on a pog, then click once in the game window to place it."))
        self.setWindowTitle(self.tr("Pog Palette"))
        self.widget = QtGui.QWidget(mainWindow)
        self.mainLayout = QtGui.QBoxLayout(2)
        self.pogArea = QtGui.QListWidget(mainWindow)
        self.mainLayout.addWidget(self.pogArea)
        self.widget.setLayout(self.mainLayout)
        self.setWidget(self.widget)
        self.setObjectName("Pog Palette")
        mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
        
        self.matoi = QtCore.QFileSystemWatcher(self)
        self.matoi.addPath(POG_DIR)
        self.matoi.directoryChanged.connect(self.addPog)

        self.pogArea.itemActivated.connect(self.place)
        self.addPog()
    
    def addPog(self, truth=False):
        """Add all pogs from the pog directory."""
        #TODO: Refactor into a view.
        self.pogArea.clear()
        self.pogs = findFiles(POG_DIR, IMAGE_EXTENSIONS)
        self.pogs.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
        for greatJustice in self.pogs:
            icon = QtGui.QIcon(QtGui.QIcon(os.path.join(POG_DIR, greatJustice)).pixmap(QtCore.QSize(32, 32)))
            self.pogArea.addItem(QtGui.QListWidgetItem(icon, greatJustice))
    
    def place(self, pog):
        """Place a pog on the map."""
        self.pogPlaced.emit(makePortableFilename(os.path.join(POG_DIR, unicode(pog.text()))))

    pogPlaced = signal(basestring, doc=
        """Called to request pog placement on the map."""
    )
    
class userListList(QtGui.QListWidget):

    def __init__(self, parent, ulmain):
        QtGui.QListWidget.__init__(self)
        self.ulmain = ulmain
        self.itemActivated.connect(self.changeGM)
        
    def changeGM(self, item):
        self.ulmain.setGMByID(self.currentRow())
    
class userListWidget(QtGui.QDockWidget):
    """The list of connected users."""
    
    def __init__(self, mainWindow):
        """Initializes the user list."""
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setToolTip(self.tr("People presently playing."))
        self.setWindowTitle(self.tr("Connected Users"))
        self.widget = QtGui.QWidget(mainWindow)
        self.listOfUsers = userListList(mainWindow, self)
        self.internalList = []
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.listOfUsers, 0, 0)
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
        
    def setGMByID(self, ID):
        if self.gmname != self.localname:
            return
        name = self.internalList[ID][0]
        #self.setGM(name)
        self.selectGM.emit(name)
        
    selectGM = signal(basestring, doc=
        """Called to request GM change."""
    )
    
class FIRECharactersWidget(QtGui.QDockWidget):
    """The list of FIRE characters."""
    
    def __init__(self, mainWindow):
        """Initializes the FIRE character list."""
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setToolTip(self.tr("Character sheets."))
        self.setWindowTitle(self.tr("Character Sheets"))
        self.widget = QtGui.QWidget(mainWindow)
        self.characterList = QtGui.QListWidget(mainWindow)
        self.characterAddButton = QtGui.QPushButton(self.tr("Add New"), mainWindow)
        self.characterAddButton.setToolTip(self.tr("Create a new character sheet."))
        self.characterEditButton = QtGui.QPushButton(self.tr("Edit"), mainWindow)
        self.characterEditButton.setToolTip(self.tr("Edit the selected character sheet."))
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.characterList, 0, 0, 1, 2)
        self.layout.addWidget(self.characterAddButton, 1, 0)
        self.layout.addWidget(self.characterEditButton, 1, 1)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.setObjectName("FIRE Character Widget")
        
        self.characters = []
        
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        
        self.connect(self.characterAddButton, QtCore.SIGNAL('clicked()'), self.newCharacter)
        self.connect(self.characterEditButton, QtCore.SIGNAL('clicked()'), self.editCharacter)
        
    def newCharacter(self):
        dialog = FIRECharacterSheetDialog()
        
        def accept():
            valid = dialog.is_valid()
            if not valid:
                showErrorMessage(dialog.error)
            return valid
        
        if dialog.exec_(self.parentWidget(), accept):
            newchardat = dialog.save()
            char = rggFIRECharacter.FIRECharacter()
            char.initFromDump(*newchardat)
            self.characters.append(char)
            self.characterList.addItem(char.name)
            if len(self.characters) == 1:
                self.characterList.setCurrentRow(0)
    
    def editCharacter(self):
        characterBeingEdited = self.characters[self.characterList.currentRow()]
        
        dialog = FIRECharacterSheetDialog(char=characterBeingEdited)
        
        def accept():
            valid = dialog.is_valid()
            if not valid:
                showErrorMessage(dialog.error)
            return valid
        
        if dialog.exec_(self.parentWidget(), accept, characterBeingEdited):
            newchardat = dialog.save()
            char = rggFIRECharacter.FIRECharacter()
            char.initFromDump(*newchardat)
            self.characters.pop(self.characterList.currentRow())
            self.characterList.takeItem(self.characterList.currentRow())
            self.characters.append(char)
            self.characterList.addItem(char.name)
    
class fileItem(QtGui.QListWidgetItem):

    def __init__(self, file, dir, panel):
        QtGui.QListWidgetItem.__init__(self)
        self.file = file
        self.dir = dir
        
        self.setText(file[5:len(file)-3])
        
class musicListWidget(QtGui.QListWidget):

    def __init__(self, panel):
        QtGui.QListWidget.__init__(self)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.panel = panel

class MusPanel(QtGui.QDockWidget):
    '''Provides controls for local music playback.'''

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        
        self.mediaobject = phonon.Phonon.MediaObject(self)
        self.audioOutput = phonon.Phonon.AudioOutput(phonon.Phonon.MusicCategory, self)
        phonon.Phonon.createPath(self.mediaobject, self.audioOutput)
        
        self.setObjectName("Music Panel")

        self.next = None
        self.contents = QtGui.QWidget(self)
        self.musicList = musicListWidget(self)
        self.musicList.itemActivated.connect(self.playClicked)
        self.play = QtGui.QPushButton("Play")
        self.stop = QtGui.QPushButton("Stop")
        self.pause = QtGui.QPushButton("Pause")
        self.shuffle = QtGui.QCheckBox("Shuffle")
        
        self.addFilesInDir(MUSIC_DIR)
        
        x = 0
        grid = QtGui.QGridLayout()

        grid.addWidget(self.musicList, x, 0, 1, 3)
        x += 1
        
        grid.addWidget(phonon.Phonon.SeekSlider(self.mediaobject), x, 0, 1, 3)
        x += 1
        
        grid.addWidget(self.play, x, 0)
        grid.addWidget(self.stop, x, 1)
        grid.addWidget(self.pause, x, 2)
        x += 1
        
        grid.addWidget(self.shuffle, x, 0)
        x += 1

        self.contents.setLayout(grid)
        
        self.play.clicked.connect(self.playClicked)
        self.stop.clicked.connect(self.stopClicked)
        self.pause.clicked.connect(self.pauseClicked)
        self.mediaobject.aboutToFinish.connect(self.enqueueNext)
        self.mediaobject.currentSourceChanged.connect(self.updateList)
        
        self.setWindowTitle("Music Panel")
        self.setWidget(self.contents)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

    def addFilesInDir(self, dir):
        fdir = os.listdir(dir)
        
        for file in fdir:
            if os.path.isdir(dir + '/' + file):
                self.addFilesInDir(dir + '/' + file)

        for file in fdir:
            if file[-3:] == "mp3":
                self.musicList.addItem(fileItem(file, dir, self))

    def updateList(self):
        if self.next != None:
            self.musicList.setCurrentItem(self.next)
        
    def enqueueNext(self):
        if self.shuffle.isChecked():
            rand = self.musicList.currentRow()
            count = self.musicList.count()
            
            while rand == self.musicList.currentRow() and count > 1:
                rand = random.randint(0, count-1)

            item = self.musicList.item(rand)
            self.mediaobject.enqueue(phonon.Phonon.MediaSource(item.dir + '/' + item.file))
        else:
            count = self.musicList.count()
            currentrow = self.musicList.currentRow()
            next = 0
            
            if currentrow + 1 < count:
                next = currentrow + 1
            
            item = self.musicList.item(next)
            self.mediaobject.enqueue(phonon.Phonon.MediaSource(item.dir + '/' + item.file))
            
        self.next = item
            
    def playClicked(self, checked):
        item = self.musicList.item(self.musicList.currentRow())
        
        if self.mediaobject.state() == phonon.Phonon.PausedState:
            self.mediaobject.play()
            return
        
        self.mediaobject.setCurrentSource(phonon.Phonon.MediaSource(item.dir + '/' + item.file))
        
        if self.mediaobject.state() != phonon.Phonon.PlayingState:
            self.mediaobject.play()
            
    def stopClicked(self, checked):
        self.mediaobject.stop()
    
    def pauseClicked(self, checked):
        if self.mediaobject.state() == phonon.Phonon.PausedState:
            self.mediaobject.play()
        if self.mediaobject.state() == phonon.Phonon.PlayingState:
            self.mediaobject.pause()
