'''
rggMenuBar - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Menu bar and menu items.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

from PyQt4 import QtGui, QtCore

selectedIcon = None

def selectIconClicked():
    import rggViews
    global selectedIcon
    selectedIcon = rggViews.ICON_SELECT

def moveIconClicked():
    import rggViews
    global selectedIcon
    selectedIcon = rggViews.ICON_MOVE

def getSelectedIcon():
    global selectedIcon
    return selectedIcon

def setupMenuBar(main):
    from rggViews import newMap, saveMap, loadMap, hostGame, joinGame
    
    menubar = main.menuBar()
    
    # ACTIONS
    
    newMapAct = QtGui.QAction("&New Map...", main)
    newMapAct.setShortcut("Ctrl+N")
    
    loadMapAct = QtGui.QAction("&Load Map...", main)
    loadMapAct.setShortcut("Ctrl+L")
    
    saveMapAct = QtGui.QAction("&Save Map...", main)
    saveMapAct.setShortcut("Ctrl+S")
    
    hostGameAct = QtGui.QAction("&Host Game", main)
    hostGameAct.setShortcut("Ctrl+H")

    joinGameAct = QtGui.QAction("&Join Game", main)
    joinGameAct.setShortcut("Ctrl+J")
    
    selectIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-select-icon.png"), "Select Tool", main)
    selectIcon.setShortcut("Ctrl+S");
    selectIcon.setToolTip("Select Tool (Ctrl+S)");
    
    moveIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-move-icon.png"), "Move Tool", main)
    moveIcon.setShortcut("Ctrl+M");
    moveIcon.setToolTip("Move Tool (Ctrl+M)");
    
    # MENUS
    
    fileMenu = QtGui.QMenu("&File", main)
    fileMenu.addAction(newMapAct)
    fileMenu.addAction(loadMapAct)
    fileMenu.addAction(saveMapAct)
    
    internetMenu = QtGui.QMenu("&Internet", main)
    internetMenu.addAction(hostGameAct)
    internetMenu.addAction(joinGameAct)
    
    # MENUBAR

    menubar.addMenu(fileMenu)
    menubar.addMenu(internetMenu)
    menubar.addSeparator()
    menubar.addAction(selectIcon)
    menubar.addAction(moveIcon)

    # EVENTS
    
    QtCore.QObject.connect(newMapAct, QtCore.SIGNAL("triggered()"), newMap)
    QtCore.QObject.connect(loadMapAct, QtCore.SIGNAL("triggered()"), loadMap)
    QtCore.QObject.connect(saveMapAct, QtCore.SIGNAL("triggered()"), saveMap)
    
    QtCore.QObject.connect(hostGameAct, QtCore.SIGNAL("triggered()"), hostGame)
    QtCore.QObject.connect(joinGameAct, QtCore.SIGNAL("triggered()"), joinGame)
    
    
    global selectedIcon
    selectedIcon = 0

    QtCore.QObject.connect(selectIcon, QtCore.SIGNAL("triggered()"), selectIconClicked)
    QtCore.QObject.connect(moveIcon, QtCore.SIGNAL("triggered()"), moveIconClicked)
