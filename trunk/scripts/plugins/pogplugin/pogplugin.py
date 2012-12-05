from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem
from rggSystem import translate

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
                        translate('views', 'Delete'),
                        translate('views', "Lock Camera to Pog")]) #BUG: We can't do the check from here to see if the message should be "unlock camera."
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
        self.update()
        
    def pogUpdateResponse(self, pog):
        for x in xrange(self.listWidget.count()):
            if self.listWidget.item(x).getPog().ID == pog.ID:
                self.listWidget.item(x).setPog(pog)
                self.update()
                return

        self.listWidget.addItem(pogItem(pog))
        self.update()

    def pogDeleteResponse(self, pog):
        for x in xrange(self.listWidget.count()):
            if self.listWidget.item(x).getPog().ID == pog.ID:
                self.listWidget.takeItem(x)
                self.update()
                return

    def pogSelectionChangedResponse(self):
        selectedPogs = rggViews._state.pogSelection

        for x in xrange(self.listWidget.count()):
            item = self.listWidget.item(x)
            if item.getPog() in selectedPogs:
                item.setSelected(True)
            else:
                item.setSelected(False)
                
        self.update()

def hajimaru(mainwindow):
    widget = pogWidget(mainwindow)
