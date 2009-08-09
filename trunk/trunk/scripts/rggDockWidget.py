from PyQt4 import QtGui, QtCore
import os

class diceRoller(QtGui.QDockWidget):

  def __init__(self, mainWindow):
    super(QtGui.QDockWidget, self).__init__("Dice", mainWindow)
    self.realwidget = QtGui.QWidget(mainWindow) #I messed up on the initial setup and was too lazy to rename everything.
    self.widget = QtGui.QBoxLayout(2)
    self.diceArea = QtGui.QListWidget(mainWindow)
    self.macros = [QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), "Sample: 2d6"),
                   QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), "Sample: 4k2")]
    for m in self.macros:
      self.diceArea.addItem(m)
    self.connect(self.diceArea, QtCore.SIGNAL('currentRowChanged(int)'), self.changeCurrentMacro)    
    self.controlArea = QtGui.QWidget(mainWindow)
    self.controlLayout = QtGui.QBoxLayout(2)
    self.rollbutton = QtGui.QPushButton("Roll", mainWindow)
    self.addmacrobutton = QtGui.QPushButton("Add Macro", mainWindow)
    self.removemacrobutton = QtGui.QPushButton("Delete Macro", mainWindow)
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
    mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
    self.currentMacro = -1

  def changeCurrentMacro(self, n):
    self.currentMacro = n

  def rollDice(self):
    if self.diceArea.item(self.currentMacro) is not None:
      self.emit(QtCore.SIGNAL("newChatInputSignal(QString)"), "/roll " + unicode(self.diceArea.item(self.currentMacro).text())[unicode(self.diceArea.item(self.currentMacro).text()).rfind(':')+1:])

  def addMacro(self, mac, macname):
    self.macros.append(QtGui.QListWidgetItem(QtGui.QIcon('data/dice.png'), macname + ': ' + mac))
    self.diceArea.addItem(self.macros[len(self.macros)-1])

  def removeCurrentMacro(self):
    if self.diceArea.item(self.currentMacro) != self.diceArea.currentItem(): #This SHOULD, probably, only occur if there are two items and the first is deleted. Probably.
      self.diceArea.takeItem(0)
      return
    self.diceArea.takeItem(self.currentMacro)

  def summonMacro(self):
    self.emit(QtCore.SIGNAL("newChatInputSignal(QString)"), "/addmacro")

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

  def __init__(self, mainWindow):
    super(QtGui.QDockWidget, self).__init__("Pog Palette", mainWindow)
    self.widget = QtGui.QWidget(mainWindow)
    self.mainLayout = QtGui.QBoxLayout(2)
    self.pogArea = QtGui.QListWidget(mainWindow)
    self.pogs = []
    for x in os.walk('data/pogs'):
      if ".svn" not in x[0]:
        for y in x[2]:
          if ".png" in y or ".jpg" in y or ".jpeg" in y or ".tiff" in y or ".bmp" in y or ".ppm" in y or ".xbm" in y or ".xpm" in y:
            self.pogs.append(x[0] + "/" + y)
    for p in self.pogs:
      self.pogArea.addItem(QtGui.QListWidgetItem(QtGui.QIcon(QtGui.QIcon(p).pixmap(QtCore.QSize(32, 32))), p[10:])) #It is vital that the relative path from data/pogs be the text.
    self.controlArea = QtGui.QWidget(mainWindow)
    self.controlLayout = QtGui.QBoxLayout(2)
    self.addpogbutton = QtGui.QPushButton("Update (UNTESTED)", mainWindow)
    self.connect(self.addpogbutton, QtCore.SIGNAL('pressed()'), self.addPog)
    self.connect(self.pogArea, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.placePog)
    self.controlLayout.addWidget(self.addpogbutton)
    self.controlArea.setLayout(self.controlLayout)
    self.mainLayout.addWidget(self.pogArea)
    self.mainLayout.addWidget(self.controlArea)
    self.widget.setLayout(self.mainLayout)
    self.setWidget(self.widget)
    mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

  def addPog(self):
    self.pogstemp = []
    for x in os.walk('data/pogs'):
      if ".svn" not in x[0]:
        for y in x[2]:
          if ".png" in y or ".jpg" in y or ".jpeg" in y or ".tiff" in y or ".bmp" in y or ".ppm" in y or ".xbm" in y or ".xpm" in y:
            if (x[0] + "/" + y) not in self.pogs:
              self.pogstemp.append(x[0] + "/" + y)
    if self.pogstemp is not []:
      for greatjustice in self.pogstemp:
        self.pogArea.addItem(QtGui.QListWidgetItem(QtGui.QIcon(QtGui.QIcon(p).pixmap(QtCore.QSize(32, 32))), greatjustice[10:]))

  def placePog(self, pog):
    self.emit(QtCore.SIGNAL("newChatInputSignal(QString)"), "/placepog data/pogs/" + pog.text())
