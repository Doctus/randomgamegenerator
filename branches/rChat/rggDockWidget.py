from PyQt4 import QtGui, QtCore
from rggSystem import signal, findFiles, POG_DIR, PORTRAIT_DIR, LOG_DIR, IMAGE_EXTENSIONS, IMAGE_NAME_FILTER, CHAR_DIR, MUSIC_DIR, SAVE_DIR, makePortableFilename, promptSaveFile, getMapPosition
from rggDialogs import newCharacterDialog, banDialog
from rggJson import loadObject, loadString, jsondump, jsonload, jsonappend
import os, os.path, time
#import rggEvent

class debugConsoleWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setToolTip(self.tr("A console that prints debug information regarding the program."))
        self.setWindowTitle(self.tr("Debug Console"))
        self.widgetEditor = QtGui.QTextBrowser(mainWindow)
        self.widget = QtGui.QWidget(mainWindow)
        self.widgetEditor.setReadOnly(True)
        self.widgetEditor.setOpenLinks(False)
        self.logToFileToggle = QtGui.QCheckBox(self.tr("Log to file"))
        try:
            if jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))["debuglog"] == "On":
                self.logToFileToggle.setChecked(True)
            else:
                self.logToFileToggle.setChecked(False)
        except:
            self.logToFileToggle.setChecked(True)
        self.logToFileToggle.stateChanged.connect(self.saveLogToggle)
        self.layout = QtGui.QBoxLayout(2)
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
        self.setWindowTitle(self.tr("Chat"))
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

    def processTags(self, message):
        message = message.replace("<", "&lt;").replace(">", "&gt;")
        for validTag in ("i", "b", "u", "s"):
            message = message.replace("".join(("[", validTag, "]")), "".join(("<", validTag, ">")))
            message = message.replace("".join(("[", "/", validTag, "]")), "".join(("<", "/", validTag, ">")))
        return message
    
    def processInput(self):
        self.newmes = unicode(self.widgetLineInput.text())
        self.newmes = self.processTags(self.newmes)
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
        self.characterPreview = QtGui.QLabel(mainWindow)
        self.characterSelector = QtGui.QComboBox(mainWindow)
        self.characterSelector.setToolTip(self.tr("Select the character to be displayed as the speaker of entered text."))
        self.characterAddButton = QtGui.QPushButton(self.tr("Add New"), mainWindow)
        self.characterAddButton.setToolTip(self.tr("Add a new in-character chat character via a dialog box."))
        self.characterDeleteButton = QtGui.QPushButton(self.tr("Delete"), mainWindow)
        self.characterDeleteButton.setToolTip(self.tr("Delete the currently selected in-character chat character."))
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.widgetEditor, 0, 0, 1, 4)
        self.layout.addWidget(self.widgetLineInput, 1, 1, 1, 3)
        self.layout.addWidget(self.characterPreview, 1, 0, 2, 1)
        self.layout.addWidget(self.characterDeleteButton, 2, 3, 1, 1)
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
        self.connect(self.characterAddButton, QtCore.SIGNAL('clicked()'), self.newCharacter)
        self.connect(self.characterDeleteButton, QtCore.SIGNAL('clicked()'), self.deleteCharacter)
        self.connect(self.characterSelector, QtCore.SIGNAL('currentIndexChanged(int)'), self.setCharacterPreview)
        
        self.setCharacterPreview()
        
    def setCharacterPreview(self, newIndex=-1):
        try:
            preview = QtGui.QPixmap(os.path.join(unicode(PORTRAIT_DIR), unicode(self.characters[self.characterSelector.currentIndex()].portrait)))
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
            img = QtGui.QImage(dat)
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
            
    def _newChar(self, char):
        self.characterSelector.addItem(char.id)
        self.characters.append(char)
        jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))
            
    def deleteCharacter(self):
        if len(self.characters) > 0:
            self.characters.pop(self.characterSelector.currentIndex())
            self.characterSelector.removeItem(self.characterSelector.currentIndex())
            jsondump(self.dump(), os.path.join(CHAR_DIR, "autosave.rgc"))

    def processTags(self, message):
        message = message.replace("<", "&lt;").replace(">", "&gt;")
        for validTag in ("i", "b", "u", "s"):
            message = message.replace("".join(("[", validTag, "]")), "".join(("<", validTag, ">")))
            message = message.replace("".join(("[", "/", validTag, "]")), "".join(("<", "/", validTag, ">")))
        return message
        
    def processInput(self):
        self.newmes = unicode(self.widgetLineInput.text())
        self.newmes = self.processTags(self.newmes)
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
        chartemp = [None]*len(chars.keys())
        for ID, char in chars.items():
            chartemp[int(ID)] = char
        for char in chartemp:
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
        try:
            self.load(jsonload(os.path.join(SAVE_DIR, "dice.rgd")))
        except:
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
            
    def _addMacro(self, macro):
        self.macros.append(QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), macro))
        self.diceArea.addItem(self.macros[len(self.macros)-1])

    def addMacro(self, mac, macname):
        self.macros.append(QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), macname + ': ' + mac))
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
         for ID, macro in macroz.items():
             self._addMacro(macro)
    
    def dump(self):
        """Serialize to an object valid for JSON dumping."""
        
        macroz = []
        for i in range(0,self.diceArea.count()):
            macroz.append(unicode(self.diceArea.item(i).text(), 'UTF-8'))

        return dict(
            macros=dict([(i, macro) for i, macro in enumerate(macroz)]))
    
    rollRequested = signal(basestring, doc=
        """Called when the roll button is hit.
        
        roll -- the dice to be rolled
        
        """
    )
    
    macroRequested = signal(doc=
        """Called when the add macro button is pressed."""
    )

class userListList(QtGui.QListWidget):

    def __init__(self, parent, ulmain):
        QtGui.QListWidget.__init__(self)
        self.ulmain = ulmain
        self.itemActivated.connect(self.changeGM)
        
    def changeGM(self, item):
        self.ulmain.provideOptions(self.currentRow())
    
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
                self.kickbutton = QtGui.QPushButton(self.tr("Kick"))
                self.kickbutton.setToolTip(self.tr("Disconnect the selected user."))
                self.layout.addWidget(self.kickbutton, 1, 0)
                self.connect(self.kickbutton, QtCore.SIGNAL('clicked()'), self.requestKick)
                self.banbutton = QtGui.QPushButton(self.tr("Manage Banlist"))
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
        
    selectGM = signal(basestring, doc=
        """Called to request a menu be summoned containing actions targeting the selected player.
            Sorry for the misleading legacy name."""
    )
    
    kickPlayer = signal(basestring, doc=
        """Called to request player kicking."""
    )
    
    requestBanlistUpdate = signal(doc=
        """Called to request that the banlist be updated."""
    )
  