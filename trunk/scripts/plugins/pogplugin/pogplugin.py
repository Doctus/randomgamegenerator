from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem
from rggSystem import translate

'''class resizeDialog(QtGui.QDialog):

    def __init__(self, origx, origy, currw, currh):
        QtGui.QDialog.__init__(self)
        self.owlabel = QtGui.QLabel("Original Width:")
        self.ohlabel = QtGui.QLabel("Orignal Height:")
        self.owlabel2 = QtGui.QLabel(str(origx))
        self.ohlabel2 = QtGui.QLabel(str(origy))
        self.setWindowTitle("Resize Pog")

        self.wlabel = QtGui.QLabel("Width:")
        self.hlabel = QtGui.QLabel("Height:")

        self.wBox = QtGui.QSpinBox()
        self.hBox = QtGui.QSpinBox()
        self.wBox.setRange(1, 1000)
        self.hBox.setRange(1, 1000)
        self.wBox.setValue(currw)
        self.hBox.setValue(currh)

        self.okButton = QtGui.QPushButton("Ok")
        self.cancelButton = QtGui.QPushButton("Cancel")

        self.okButton.clicked.connect(self.okPressed)
        self.cancelButton.clicked.connect(self.cancelPressed)

        self.layout = QtGui.QGridLayout()
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
        self.done(0)'''

'''class layerDialog(QtGui.QDialog):

    def __init__(self, currl):
        QtGui.QDialog.__init__(self)
        self.label = QtGui.QLabel("Layer:")
        self.box = QtGui.QSpinBox()
        self.setWindowTitle("Set Layer")

        self.box.setRange(-150, 800)
        self.box.setValue(currl)

        self.okButton = QtGui.QPushButton("Ok")
        self.cancelButton = QtGui.QPushButton("Cancel")

        self.okButton.clicked.connect(self.okPressed)
        self.cancelButton.clicked.connect(self.cancelPressed)

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.box, 0, 1)
        self.layout.addWidget(self.okButton, 1, 0)
        self.layout.addWidget(self.cancelButton, 1, 1)
        self.setLayout(self.layout)

    def okPressed(self, checked):
        self.done(1)

    def cancelPressed(self, checked):
        self.done(0)'''

class pogItem(QtGui.QListWidgetItem):

    def __init__(self, pog):
        QtGui.QListWidgetItem.__init__(self)
        self.setPog(pog)
        self.dead = False

    def getPog(self):
        return self.__pog

    def setPog(self, pog):
        self.__pog = pog
        name = pog.name
        if name == None or len(name) <= 0:
            name = "No name (" + pog._src + ")"
        if pog._locked:
            name += " [L]"
        if pog.hidden:
            name += " [H]"
        self.setText(name)

class pogListWidget(QtGui.QListWidget):

    def __init__(self, parent, pogwidget):
        QtGui.QListWidget.__init__(self)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.pogwidget = pogwidget

    def mousePressEvent(self, event): #listwidget generated events
        pos = event.globalPos()
        x = pos.x()
        y = pos.y()
        specificItem = self.itemAt(event.x(), event.y())
        if specificItem not in self.selectedItems():
            self.setItemSelected(specificItem, True)
        items = self.selectedItems()
        self.pogs = []
        for item in items:
            self.pogs.append(item.getPog())
        event.accept()

        if items is None or specificItem is None:
            return

        if event.button() == QtCore.Qt.RightButton:
            hide = 'Hide'
            lock = 'Lock'

            if specificItem.getPog().hidden:
                hide = 'Show'
            if specificItem.getPog()._locked:
                lock = 'Unlock'

            selection = rggSystem.showPopupMenuAtAbs([x, y], [translate('views', 'Center on pog'),
                        translate('views', 'Set name'),
                        translate('views', 'Generate name'),
                        translate('views', 'Set layer'),
                        translate('views', 'Add/edit property'),
                        translate('views', 'Resize'),
                        translate('views', hide),
                        translate('views', lock),
                        translate('views', 'Delete')])
            rggViews.processPogRightclick(selection, self.pogs)
            self.pogwidget.refresh()
        else:
            self.pogwidget.refresh()
            super(QtGui.QListWidget, self).mousePressEvent(event)

    def selectionChanged(self, selected, deselected):
        super(QtGui.QListWidget, self).selectionChanged(selected, deselected)
        for index in selected.indexes():
            item = self.item(index.row())
            if not item.dead:
                rggViews._state.pogSelection.add(item.getPog())
        for index in deselected.indexes():
            item = self.item(index.row())
            if not item.dead:
                rggViews._state.pogSelection.discard(item.getPog())

class pogWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)

        self.setWindowTitle(self.tr("Pogs"))
        self.listWidget = pogListWidget(mainWindow, self)
        self.setWidget(self.listWidget)
        self.setObjectName("Pog Plugin")
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        self.pogSelectionChangedResponse()
        
        for pog in rggViews.getSession().pogs.values():
            self.pogUpdateResponse(pog)

        rggEvent.addPogUpdateListener(self)
        rggEvent.addPogDeleteListener(self)
        rggEvent.addPogSelectionChangedListener(self)
        
    def refresh(self):
        self.listWidget.clear()
        for pog in rggViews.getSession().pogs.values():
            self.pogUpdateResponse(pog)
        
    def pogUpdateResponse(self, pog):
        for x in xrange(self.listWidget.count()):
            if self.listWidget.item(x).getPog().ID == pog.ID:
                self.listWidget.item(x).setPog(pog)
                return

        self.listWidget.addItem(pogItem(pog))

    def pogDeleteResponse(self, pog):
        for x in xrange(self.listWidget.count()):
            if self.listWidget.item(x).getPog().ID == pog.ID:
                self.listWidget.takeItem(x)
                return

    def pogSelectionChangedResponse(self):
        selectedPogs = rggViews._state.pogSelection

        for x in xrange(self.listWidget.count()):
            item = self.listWidget.item(x)
            if item.getPog() in selectedPogs:
                item.setSelected(True)
            else:
                item.setSelected(False)

def hajimaru(mainwindow):
    widget = pogWidget(mainwindow)
