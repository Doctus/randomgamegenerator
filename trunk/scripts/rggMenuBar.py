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
from rggSystem import translate, mainWindow

ICON_SELECT = 0
ICON_MOVE = 1

class menuBar(object):
    """An object representing the menu bar."""
    
    def __init__(self):
        
        main = mainWindow
        
        menubar = main.menuBar()
        
        # ACTIONS
        
        self.newMapAct = QtGui.QAction("&New Map...", main)
        self.newMapAct.setShortcut("Ctrl+N")
        
        self.loadMapAct = QtGui.QAction("&Load Map...", main)
        self.loadMapAct.setShortcut("Ctrl+L")
        
        self.saveMapAct = QtGui.QAction("&Save Map As...", main)
        self.saveMapAct.setShortcut("Ctrl+S")
        
        self.hostGameAct = QtGui.QAction("&Host Game", main)
        self.hostGameAct.setShortcut("Ctrl+H")

        self.joinGameAct = QtGui.QAction("&Join Game", main)
        self.joinGameAct.setShortcut("Ctrl+J")
        
        self.disconnectAct = QtGui.QAction("&Disconnect", main)
        self.disconnectAct.setShortcut("Ctrl+D")
        
        selectIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-select-icon.png"), "Select Tool", main)
        selectIcon.setShortcut("Ctrl+T");
        selectIcon.setToolTip("Select Tool (Ctrl+T)");
        
        moveIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-move-icon.png"), "Move Tool", main)
        moveIcon.setShortcut("Ctrl+M");
        moveIcon.setToolTip("Move Tool (Ctrl+M)");
        
        # MENUS
        
        fileMenu = QtGui.QMenu("&File", main)
        fileMenu.addAction(self.newMapAct)
        fileMenu.addAction(self.loadMapAct)
        fileMenu.addAction(self.saveMapAct)
        
        internetMenu = QtGui.QMenu("&Internet", main)
        internetMenu.addAction(self.hostGameAct)
        internetMenu.addAction(self.joinGameAct)
        internetMenu.addAction(self.disconnectAct)
        
        # MENUBAR

        menubar.addMenu(fileMenu)
        menubar.addMenu(internetMenu)
        menubar.addSeparator()
        menubar.addAction(selectIcon)
        menubar.addAction(moveIcon)

        # EVENTS
        
        self.selectedIcon = 0
        selectIcon.triggered.connect(self.selectIconClicked)
        moveIcon.triggered.connect(self.moveIconClicked)
    
    def selectIconClicked(self):
        self.selectedIcon = ICON_SELECT
    
    def moveIconClicked(self):
        self.selectedIcon = ICON_MOVE
    
    
