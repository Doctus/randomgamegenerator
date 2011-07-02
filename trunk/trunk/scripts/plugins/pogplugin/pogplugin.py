from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem

class resizeDialog(QtGui.QDialog):

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
        self.done(0)

class layerDialog(QtGui.QDialog):

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
        self.done(0)

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
            name = "No name"
        if pog._locked:
            name += " [L]"
        if pog.hidden:
            name += " [H]"
        self.setText(name)

class pogListWidget(QtGui.QListWidget):

    def __init__(self, parent):
        QtGui.QListWidget.__init__(self)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def mousePressEvent(self, event): #listwidget generated events
        pos = event.globalPos()
        x = pos.x()
        y = pos.y()
        specificItem = self.itemAt(event.x(), event.y())
        if specificItem not in self.selectedItems():
            self.setItemSelected(specificItem, True)
        items = self.selectedItems()
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

            selection = rggSystem.showPopupMenuAtAbs([x, y], ['Center', hide, 'Resize', lock, 'Change Layer', 'Delete'])
            if selection == 0:
                camsiz = rggSystem.cameraSize()
                pospog = specificItem.getPog().position
                pogw = specificItem.getPog()._tile.getW()
                pogh = specificItem.getPog()._tile.getH()
                newpos = (pospog[0] - camsiz[0]/2 + pogw/2, pospog[1] - camsiz[1]/2 + pogh/2)
                rggSystem.setCameraPosition(newpos)
            elif selection == 1:
                for item in items:
                    pog = item.getPog()
                    if pog.hidden:
                        pog.show()
                    else:
                        pog.hide()
                    item.setPog(pog)
                    rggViews.sendHidePog(pog.ID, pog.hidden)
            elif selection == 2:
                specificPog = specificItem.getPog()
                d = resizeDialog(specificPog._tile.getW(), specificPog._tile.getH(), specificPog.size[0], specificPog.size[1])
                if d.exec_():
                    for item in items:
                        pog = item.getPog()
                        pog.size = (d.wBox.value(), d.hBox.value())
                        rggViews.sendResizePog(pog.ID, d.wBox.value(), d.hBox.value())
            elif selection == 3:
                for item in items:
                    pog = item.getPog()
                    pog._locked = not pog._locked
                    item.setPog(pog)
                    rggViews.sendLockPog(pog.ID, pog._locked)
            elif selection == 4:
                specificPog = specificItem.getPog()
                d = layerDialog(specificPog.layer-200)
                if d.exec_():
                    for item in items:
                        pog = item.getPog()
                        pog.layer = d.box.value()+200
            elif selection == 5:
                for item in items:
                    rggViews.deletePog(item.getPog())
                    item.dead = True
                    self.takeItem(self.row(item))
        else:
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
        self.listWidget = pogListWidget(mainWindow)
        self.setWidget(self.listWidget)
        self.setObjectName("Pog Plugin")
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        self.pogSelectionChangedResponse()
        
        for pog in rggViews.getSession().pogs.values():
            self.pogUpdateResponse(pog)

        rggEvent.addPogUpdateListener(self)
        rggEvent.addPogDeleteListener(self)
        rggEvent.addPogSelectionChangedListener(self)
        
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
