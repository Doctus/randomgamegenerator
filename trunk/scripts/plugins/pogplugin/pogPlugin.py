from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog, rggSystem

class pogItem(QtGui.QListWidgetItem):

    def __init__(self, pog):
        QtGui.QListWidgetItem.__init__(self)
        self.setPog(pog)

    def getPog(self):
        return self.__pog

    def setPog(self, pog):
        self.__pog = pog
        name = pog.name
        if name == None or len(name) <= 0:
          name = "No name"
        if pog.hidden:
          name += " (hidden)"
        self.setText(name)

class pogListWidget(QtGui.QListWidget):

    def __init__(self, parent):
        QtGui.QListWidget.__init__(self)

    def mousePressEvent(self, event): #listwidget generated events
        pos = event.globalPos()
        x = pos.x()
        y = pos.y()
        item = self.itemAt(event.x(), event.y())
        event.accept()

        if item is None:
            return

        if event.button == QtCore.Qt.LeftButton:
            if item.isSelected():
                rggViews._state.pogSelection.remove(item.getPog())
                item.setSelected(False)
                print 'pog', item.getPog().ID, 'deselected'
            else:
                rggViews._state.pogSelection.add(item.getPog())
                item.setSelected(True)
                print 'pog', item.getPog().ID, 'selected'
        elif event.button() == QtCore.Qt.RightButton:
            selection = rggSystem.showPopupMenuAtAbs([x, y], ['center'])
            if selection == 0:
                camsiz = rggSystem.cameraSize()
                pospog = item.getPog().position
                pogw = item.getPog()._tile.getW()
                pogh = item.getPog()._tile.getH()
                newpos = (pospog[0] - camsiz[0]/2 + pogw/2, pospog[1] - camsiz[1]/2 + pogh/2)
                rggSystem.setCameraPosition(newpos)

class pogWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)

        self.setWindowTitle(self.tr("Pogs"))
        self.listWidget = pogListWidget(mainWindow)
        self.setWidget(self.listWidget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        currentMap = rggViews._state.currentMap
        self.mapChangedResponse(currentMap)
        self.pogSelectionChangedResponse()

        rggEvent.addPogUpdateListener(self)
        rggEvent.addMapChangedListener(self)
        rggEvent.addPogSelectionChangedListener(self)
        
    def pogUpdateResponse(self, pog):
        for x in xrange(self.listWidget.count()):
            if self.listWidget.item(x).getPog().ID == pog.ID:
                self.listWidget.item(x).setPog(pog)
                return

        self.listWidget.addItem(pogItem(pog))

    def pogSelectionChangedResponse(self):
        selectedPogs = rggViews._state.pogSelection
        print 'selectedPogs:', selectedPogs

        for x in xrange(self.listWidget.count()):
            item = self.listWidget.item(x)
            print 'item:', item.getPog()
            if item.getPog() in selectedPogs:
                item.setSelected(True)
                print 'pog', item.getPog().ID, 'selected'
            else:
                item.setSelected(False)
                print 'pog', item.getPog().ID, 'deselected'


    def mapChangedResponse(self, newMap):
        self.listWidget.clear()
        if newMap != None:
            for pog in newMap.Pogs:
                self.pogUpdateResponse(newMap.Pogs[pog])

def hajimaru(mainwindow):
    widget = pogWidget(mainwindow)
