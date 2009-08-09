from PyQt4 import QtGui, QtCore
import os

class newMapDialog(QtCore.QObject):

    def __init__(self, mainWindow):
        super(QtCore.QObject, self).__init__(mainWindow)
        self.grandBox = QtGui.QBoxLayout(2)
        self.theLesserOrFalseBox = QtGui.QBoxLayout(0)
        self.formLayout = QtGui.QFormLayout()
        self.mapNameLineEdit = QtGui.QLineEdit("Generic Map", mainWindow)
        self.formLayout.addRow("Map Name: ", self.mapNameLineEdit)
        self.authNameLineEdit = QtGui.QLineEdit("Anonymous", mainWindow)
        self.formLayout.addRow("Author Name: ", self.authNameLineEdit)
        self.mapHeightEdit = QtGui.QSpinBox(mainWindow)
        self.mapHeightEdit.setRange(1, 65535)
        #self.mapHeightEdit.setSuffix("tiles")
        self.mapHeightEdit.setValue(25)
        self.mapWidthEdit = QtGui.QSpinBox(mainWindow)
        self.mapWidthEdit.setRange(1, 65535)
        #self.mapWidthEdit.setSuffix("tiles")
        self.mapWidthEdit.setValue(25)
        self.formLayout.addRow("Map Width: ", self.mapWidthEdit)
        self.formLayout.addRow("Map Height: ", self.mapHeightEdit)
        self.tilesetEdit = QtGui.QComboBox(mainWindow)
        self.tilesetz = []
        for x in os.walk('data/tilesets'):
          if ".svn" not in x[0]:
            for y in x[2]:
              if ".png" in y or ".jpg" in y or ".jpeg" in y or ".tiff" in y or ".bmp" in y or ".ppm" in y or ".xbm" in y or ".xpm" in y:
                self.tilesetz.append(x[0] + "/" + y)
        for t in self.tilesetz:
            self.tilesetEdit.addItem(t[14:])
        self.formLayout.addRow("Tileset: ", self.tilesetEdit)
        self.tileHeightEdit = QtGui.QSpinBox(mainWindow)
        self.tileHeightEdit.setRange(1, 65535)
        self.tileHeightEdit.setSuffix("px")
        self.tileHeightEdit.setValue(32)
        self.tileWidthEdit = QtGui.QSpinBox(mainWindow)
        self.tileWidthEdit.setRange(1, 65535)
        self.tileWidthEdit.setSuffix("px")
        self.tileWidthEdit.setValue(32)
        self.formLayout.addRow("Per-Tile Width: ", self.tileWidthEdit)
        self.formLayout.addRow("Per-Tile Height: ", self.tileHeightEdit)
        self.newMapOkayButton = QtGui.QPushButton("Create Map")
        self.newMapOkayButton.setDefault(True)
        self.theLesserOrFalseBox.addWidget(self.newMapOkayButton)
        self.newMapCancelButton = QtGui.QPushButton("Cancel")
        self.theLesserOrFalseBox.addWidget(self.newMapCancelButton)
        self.grandBox.addLayout(self.formLayout)
        self.grandBox.addLayout(self.theLesserOrFalseBox)
        self.widget = QtGui.QDialog(mainWindow)
        self.widget.setLayout(self.grandBox)
        self.widget.setModal(True)
        self.widget.setWindowTitle("New Map")
        self.connect(self.newMapCancelButton, QtCore.SIGNAL('pressed()'), self.reject)
        self.connect(self.newMapOkayButton, QtCore.SIGNAL('pressed()'), self.accept)
        self.connect(self.widget, QtCore.SIGNAL('accepted()'), self.emitResult)
        self.widget.show()

    def accept(self):
        self.widget.done(1)

    def reject(self):
        self.widget.done(0)

    def emitResult(self):
        self.emit(QtCore.SIGNAL("newChatInputSignal(QString)"), "/newmap " + " ".join(['n!', unicode(self.mapNameLineEdit.text()), '!n',
                                                                                      'a!', unicode(self.authNameLineEdit.text()), '!a',
                                                                                      'm!', unicode(self.mapWidthEdit.value()), unicode(self.mapHeightEdit.value()),
                                                                                      't!', "data/tilesets/" + unicode(self.tilesetEdit.currentText()),
                                                                                      's!', unicode(self.tileWidthEdit.value()), unicode(self.tileHeightEdit.value())]))
