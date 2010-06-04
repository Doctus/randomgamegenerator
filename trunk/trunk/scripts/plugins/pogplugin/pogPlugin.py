from PyQt4 import QtCore, QtGui
import rggEvent, rggViews, rggPog

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

class pogWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)

        self.setWindowTitle(self.tr("Pogs"))
        self.listWidget = QtGui.QListWidget(mainWindow)
        self.setWidget(self.listWidget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        currentMap = rggViews._state.currentMap
        self.mapChangedResponse(currentMap)

        rggEvent.addPogAddedListener(self)
        rggEvent.addMapChangedListener(self)
        
    def pogAddedResponse(self, pog):
        for x in xrange(self.listWidget.count()):
            if self.listWidget.item(x).getPog().ID == pog.ID:
                self.listWidget.item(x).setPog(pog)
                return

        self.listWidget.addItem(pogItem(pog))

    def mapChangedResponse(self, newMap):
        self.listWidget.clear()
        if newMap != None:
            for pog in newMap.Pogs:
                self.pogAddedResponse(newMap.Pogs[pog])

def hajimaru(mainwindow):
    widget = pogWidget(mainwindow)
