from PyQt4 import QtGui, QtCore
import _bmainmod
global selectedIcon
selectedIcon = None

def selectIconClicked():
    global selectedIcon
    selectedIcon = 0

def moveIconClicked():
    global selectedIcon
    selectedIcon = 1

def getSelectedIcon():
    global selectedIcon
    return selectedIcon

def setupMenuBar(c):
    menubar = c.getMainWindow().menuBar()

    selectIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-select-icon.png"), "Select Tool", c.getMainWindow())
    selectIcon.setShortcut("Ctrl+S");
    selectIcon.setToolTip("Select Tool (Ctrl+S)");
    menubar.addAction(selectIcon)

    moveIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-move-icon.png"), "Move Tool", c.getMainWindow())
    moveIcon.setShortcut("Ctrl+M");
    moveIcon.setToolTip("Move Tool (Ctrl+M)");
    menubar.addAction(moveIcon)

    global selectedIcon
    selectedIcon = 0

    QtCore.QObject.connect(selectIcon, QtCore.SIGNAL("triggered()"), selectIconClicked)
    QtCore.QObject.connect(moveIcon, QtCore.SIGNAL("triggered()"), moveIconClicked)
