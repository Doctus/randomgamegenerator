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
        self.buffer.append(data)
        if data.endswith('\n'):
            self.widgetEditor.append(''.join(self.buffer))
            if self.logToFileToggle.isChecked():
                with open(os.path.join(LOG_DIR, time.strftime("%b_%d_%Y_debug.log", time.localtime())), 'a') as f:
                    f.write(''.join(self.buffer))
            self.buffer = []

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

class PogFileSystemModel(QtGui.QFileSystemModel):

    def __init__(self):
        super(QtGui.QFileSystemModel, self).__init__()
        self.setRootPath(POG_DIR)
        self.setNameFilters(IMAGE_NAME_FILTER)
        self.setNameFilterDisables(False)
        self.absRoot = os.path.abspath(POG_DIR)
        
    def data(self, index, role):
        basedata = QtGui.QFileSystemModel.data(self, index, role)
        if basedata.canConvert(69):
            nodes = [index,]
            while nodes[0].parent().isValid():
                nodes.insert(0, nodes[0].parent())
            paths = []
            for node in nodes:
                paths.append(unicode(self.data(node, 0).toString()))
            if len(os.path.splitdrive(os.getcwd())[0]) > 0:
                paths[0] = os.path.splitdrive(os.getcwd())[0]+"\\"
            path = os.path.join(*paths)
            if os.path.isfile(path):
                return QtGui.QIcon(path)
        return basedata
        
    def mimeData(self, indices):
        path = QtCore.QString(makePortableFilename(os.path.join(POG_DIR, unicode(self.filePath(indices[0])[len(self.absRoot)+1:]))))
        
        #If there's no "." in the path, assume it's a folder.
        if "." not in unicode(path): return None
        
        mime = QtCore.QMimeData()
        mime.setText(path)
        return mime

class pogTree(QtGui.QTreeView):

    def startDrag(self, event):
        for i in self.selectedIndexes(): 
            drag = QtGui.QDrag(self)
            
            #Don't drag folders.
            if not self.model().mimeData([i]): return
            
            drag.setMimeData(self.model().mimeData([i]))
            drag.setPixmap(QtGui.QPixmap(self.model().mimeData([i]).text()))
            drag.setHotSpot(QtCore.QPoint(0, 0))
            drag.start()
        
class pogPalette(QtGui.QDockWidget):
    """The list of loaded pogs."""
    
    def __init__(self, mainWindow):
        """Initializes the pog palette."""
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setToolTip(self.tr("Double-click on a pog, then click once in the game window to place it."))
        self.setWindowTitle(self.tr("Pog Palette"))
        self.widget = QtGui.QWidget(mainWindow)
        self.mainLayout = QtGui.QBoxLayout(2)
        self.pogsModel = PogFileSystemModel()
        self.ROOT_LEN = len(self.pogsModel.absRoot)+1
        self.pogArea = pogTree(mainWindow)
        self.pogArea.setModel(self.pogsModel)
        self.pogArea.setRootIndex(self.pogsModel.index(POG_DIR))
        self.pogArea.setColumnHidden(1, True)
        self.pogArea.setColumnHidden(2, True)
        self.pogArea.setColumnHidden(3, True)
        self.pogArea.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.controlArea = QtGui.QWidget(mainWindow)
        self.controlLayout = QtGui.QBoxLayout(2)
        self.controlArea.setLayout(self.controlLayout)
        self.mainLayout.addWidget(self.pogArea)
        self.mainLayout.addWidget(self.controlArea)
        self.widget.setLayout(self.mainLayout)
        self.setWidget(self.widget)
        self.setObjectName("Pog Palette")
        mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
    
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
        
    def setGMByID(self, ID):
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
        """Called to request GM change."""
    )
    
    kickPlayer = signal(basestring, doc=
        """Called to request player kicking."""
    )
    
    requestBanlistUpdate = signal(doc=
        """Called to request that the banlist be updated."""
    )
    
class fileItem(QtGui.QListWidgetItem):

    def __init__(self, file, dir, panel):
        QtGui.QListWidgetItem.__init__(self)
        self.file = file
        self.dir = dir
        
        self.setText(file[5:len(file)-3])

class mapEditorLabel(QtGui.QLabel):
    
    def __init__(self, tilesize, width, height, par, currentTile=0):
        super(QtGui.QLabel, self).__init__()
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

class mapEditor(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        
        #self.__eat = True
        self.painting = True
        self.dragging = False
        self.rectStart = None

        self.setWindowTitle(self.tr("Map Editor"))
        self.widget = QtGui.QWidget(mainWindow)
        self.layout = QtGui.QBoxLayout(2)
        self.currentTileLayout = QtGui.QBoxLayout(1)
        self.scrollarea = QtGui.QScrollArea(mainWindow)
        self.noPaintingButton = QtGui.QRadioButton(self.tr("Stop Painting"), mainWindow)
        self.singlePaintingButton = QtGui.QRadioButton(self.tr("Single Tile Brush"), mainWindow)
        self.noPaintingButton.setChecked(True)
        self.rectPaintingButton = QtGui.QRadioButton(self.tr("Area (Rectangle) Brush"), mainWindow)
        self.hollowRectPaintingButton = QtGui.QRadioButton(self.tr("Hollow Rectangle Brush"), mainWindow)
        self.currentTileLabel = QtGui.QLabel()
        self.currentTileLabelLabel = QtGui.QLabel(self.tr("Current tile: "))
        self.layout.addWidget(self.scrollarea)
        self.layout.addWidget(self.noPaintingButton)
        self.layout.addWidget(self.singlePaintingButton)
        self.layout.addWidget(self.rectPaintingButton)
        self.layout.addWidget(self.hollowRectPaintingButton)
        self.currentTileLayout.addWidget(self.currentTileLabel)
        self.currentTileLayout.addWidget(self.currentTileLabelLabel)
        self.layout.addLayout(self.currentTileLayout)
        self.tilelabel = None
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.setObjectName("Map Editor")
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        self.currentMap = None
        
        from rggEvent import addMapChangedListener, addMousePressListener, addMouseMoveListener, addMouseReleaseListener

        addMapChangedListener(self)
        addMousePressListener(self)
        addMouseMoveListener(self)
        addMouseReleaseListener(self)
        
    def updateCurrentTile(self):
        self.tilepix = QtGui.QPixmap()
        self.tilepix.load(self.currentMap.tileset)
        self.tilepix = self.tilepix.copy(QtCore.QRect(*self.tilelabel.currentTileDimensions))
        self.currentTileLabel.setPixmap(self.tilepix)
        
    def mousePressResponse(self, x, y, t):
        mapPosition = getMapPosition((x, y))
        
        #This and similar things were a regrettable necessity in the plugin -> nonplugin conversion process.
        from rggViews import topmap, sendTileUpdate
        from rggEvent import setEaten
        
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
                    setEaten()
                    return
                sendTileUpdate(map.ID, clickedtile, self.tilelabel.currentTile)
                setEaten()
            elif self.isVisible() and (self.rectPaintingButton.isChecked() or self.hollowRectPaintingButton.isChecked()):
                self.rectStart = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                if not map.tilePosExists(self.rectStart):
                    setEaten()
                    self.rectStart = None
                    return
                setEaten()
        elif t == 5:
            if self.isVisible() and not self.noPaintingButton.isChecked():
                clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                self.tilelabel.currentTile = map.getTile(clickedtile)
                self.tilelabel.updateTile()
                setEaten()

    def mouseMoveResponse(self, x, y):
        if self.dragging and self.isVisible() and self.singlePaintingButton.isChecked():
            from rggViews import topmap
            from rggEvent import setEaten
            mapPosition = getMapPosition((x, y))
            map = topmap(mapPosition)
            if map == None:
                self.dragging = False
                return
            clickedtile = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
            
            if not map.tilePosExists(clickedtile):
                setEaten()
                return
            if map.tilePosExists(clickedtile) and map.getTile(clickedtile) != self.tilelabel.currentTile:
                from rggViews import sendTileUpdate
                sendTileUpdate(map.ID, clickedtile, self.tilelabel.currentTile)
            setEaten()
            
    def mouseReleaseResponse(self, x, y, t):
        if t == 0:
            from rggViews import topmap, sendTileUpdate
            from rggEvent import setEaten
            if self.currentMap == None:
                return
            mapPosition = getMapPosition((x, y))
            map = topmap(mapPosition)
            self.dragging = False
            if map == None:
                return
            if self.isVisible() and self.singlePaintingButton.isChecked():
                setEaten()
            elif self.isVisible() and self.rectPaintingButton.isChecked() and self.rectStart is not None:
                rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                if not map.tilePosExists(rectEnd):
                    setEaten()
                    self.rectStart = None
                    self.rectEnd = None
                    return
                if cmp(rectEnd[0], self.rectStart[0]) != 0:
                    for x in range(self.rectStart[0], rectEnd[0]+cmp(rectEnd[0], self.rectStart[0]), cmp(rectEnd[0], self.rectStart[0])):
                        if cmp(rectEnd[1], self.rectStart[1]) != 0:
                            for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                                if self.currentMap.tilePosExists((x, y)):
                                    sendTileUpdate(self.currentMap.ID, (x, y), self.tilelabel.currentTile)
                        else:
                            if self.currentMap.tilePosExists((x, self.rectStart[1])):
                                sendTileUpdate(self.currentMap.ID, (x, self.rectStart[1]), self.tilelabel.currentTile)
                else:
                    if cmp(rectEnd[1], self.rectStart[1]) != 0:
                        for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                            if self.currentMap.tilePosExists((self.rectStart[0], y)):
                                sendTileUpdate(self.currentMap.ID, (self.rectStart[0], y), self.tilelabel.currentTile)
                    else:
                        if self.currentMap.tilePosExists((self.rectStart[0], self.rectStart[1])):
                                sendTileUpdate(self.currentMap.ID, (self.rectStart[0], self.rectStart[1]), self.tilelabel.currentTile)
                setEaten()
            elif self.isVisible() and self.hollowRectPaintingButton.isChecked() and self.rectStart is not None:
                rectEnd = (int(((mapPosition[0] - map.drawOffset[0]) / self.tilelabel.tilex)),
                            int(((mapPosition[1] - map.drawOffset[1]) / self.tilelabel.tiley)))
                if not map.tilePosExists(rectEnd):
                    setEaten()
                    self.rectStart = None
                    self.rectEnd = None
                    return
                if cmp(rectEnd[0], self.rectStart[0]) != 0:
                    for x in range(self.rectStart[0], rectEnd[0]+cmp(rectEnd[0], self.rectStart[0]), cmp(rectEnd[0], self.rectStart[0])):
                        if cmp(rectEnd[1], self.rectStart[1]) != 0:
                            #TODO: Less lazy and inefficient implementation for this case.
                            for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                                if x == self.rectStart[0] or x == rectEnd[0] or y == self.rectStart[1] or y == rectEnd[1]:
                                    if self.currentMap.tilePosExists((x, y)):
                                        sendTileUpdate(self.currentMap.ID, (x, y), self.tilelabel.currentTile)
                        else:
                            if self.currentMap.tilePosExists((x, self.rectStart[1])):
                                sendTileUpdate(self.currentMap.ID, (x, self.rectStart[1]), self.tilelabel.currentTile)
                else:
                    if cmp(rectEnd[1], self.rectStart[1]) != 0:
                        for y in range(self.rectStart[1], rectEnd[1]+cmp(rectEnd[1], self.rectStart[1]), cmp(rectEnd[1], self.rectStart[1])):
                            if self.currentMap.tilePosExists((self.rectStart[0], y)):
                                sendTileUpdate(self.currentMap.ID, (self.rectStart[0], y), self.tilelabel.currentTile)
                    else:
                        if self.currentMap.tilePosExists((self.rectStart[0], self.rectStart[1])):
                                sendTileUpdate(self.currentMap.ID, (self.rectStart[0], self.rectStart[1]), self.tilelabel.currentTile)
                setEaten()

    def mapChangedResponse(self, newMap):
        if newMap != None:
            self.currentMap = newMap
            self.tilepixmap = QtGui.QPixmap()
            self.tilepixmap.load(newMap.tileset)
            if self.tilelabel is None:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height(), self)
            else:
                self.tilelabel = mapEditorLabel(newMap.tilesize, self.tilepixmap.width(), self.tilepixmap.height(), self, self.tilelabel.currentTile)
            self.tilelabel.setPixmap(self.tilepixmap)
            self.scrollarea.setWidget(self.tilelabel)