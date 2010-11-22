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
import sys, os

ICON_SELECT = 0
ICON_MOVE = 1
ICON_DRAW = 2
ICON_DELETE = 3

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
        
        self.closeMapAct = QtGui.QAction("&Close All Maps", main)
        self.closeMapAct.setShortcut("Ctrl+Shift+W")
        
        self.saveCharsAct = QtGui.QAction("Save IC Characters", main)
        
        self.loadCharsAct = QtGui.QAction("Load IC Characters", main)
        
        self.hostGameAct = QtGui.QAction("&Host Game", main)
        self.hostGameAct.setShortcut("Ctrl+H")

        self.joinGameAct = QtGui.QAction("&Join Game", main)
        self.joinGameAct.setShortcut("Ctrl+J")
        
        self.disconnectAct = QtGui.QAction("&Disconnect", main)
        self.disconnectAct.setShortcut("Ctrl+D")

        self.thicknessOneAct = QtGui.QAction("&One", main)
        self.thicknessTwoAct = QtGui.QAction("&Two", main)
        self.thicknessThreeAct = QtGui.QAction("&Three", main)
        
        self.pluginsActs = []
        self.pluginsModules = []
        self.pluginsInits = []
        sys.path.append('plugins')
        for folder in os.listdir('plugins'):
                if folder == ".svn":
                        continue
                self.pluginsModules.append(__import__(folder))
                self.pluginsModules[-1].initialize(main)
                self.pluginsInits.append(self.pluginsModules[-1].hajimeru)
                self.pluginsActs.append(QtGui.QAction(unicode(self.pluginsModules[-1].title()), main))
                self.pluginsActs[-1].triggered.connect(self.pluginsInits[-1])
        
        selectIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-select-icon.png"), "Select Tool", main)
        selectIcon.setShortcut("Ctrl+T");
        selectIcon.setToolTip("Select Tool (Ctrl+T)");
        
        moveIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-move-icon.png"), "Move Tool", main)
        moveIcon.setShortcut("Ctrl+M");
        moveIcon.setToolTip("Move Tool (Ctrl+M)");

        drawIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-freehand-icon.png"), "Draw Tool", main)
        drawIcon.setShortcut("Ctrl+E");
        drawIcon.setToolTip("Draw Tool (Ctrl+E)");

        deleteIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-eraser-icon.png"), "Delete Tool", main)
        deleteIcon.setShortcut("Ctrl+R");
        deleteIcon.setToolTip("Delete Tool (Ctrl+R)");
        
        # MENUS
        
        fileMenu = QtGui.QMenu("&File", main)
        fileMenu.addAction(self.newMapAct)
        fileMenu.addAction(self.loadMapAct)
        fileMenu.addAction(self.saveMapAct)
        fileMenu.addAction(self.closeMapAct)
        fileMenu.addAction(self.saveCharsAct)
        fileMenu.addAction(self.loadCharsAct)
        
        internetMenu = QtGui.QMenu("&Internet", main)
        internetMenu.addAction(self.hostGameAct)
        internetMenu.addAction(self.joinGameAct)
        internetMenu.addAction(self.disconnectAct)

        thicknessMenu = QtGui.QMenu("&Thickness", main)
        thicknessMenu.addAction(self.thicknessOneAct)
        thicknessMenu.addAction(self.thicknessTwoAct)
        thicknessMenu.addAction(self.thicknessThreeAct)

        drawMenu = QtGui.QMenu("&Draw", main)
        drawMenu.addMenu(thicknessMenu)
        
        pluginsMenu = QtGui.QMenu("&Plugins", main)
        for act in self.pluginsActs:
                pluginsMenu.addAction(act)
        
        # MENUBAR

        menubar.addMenu(fileMenu)
        menubar.addMenu(internetMenu)
        menubar.addMenu(drawMenu)
        menubar.addMenu(pluginsMenu)
        menubar.addSeparator()
        menubar.addAction(selectIcon)
        menubar.addAction(moveIcon)
        menubar.addAction(drawIcon)
        menubar.addAction(deleteIcon)

        # EVENTS
        
        self.selectedIcon = 0
        selectIcon.triggered.connect(self.selectIconClicked)
        moveIcon.triggered.connect(self.moveIconClicked)
        drawIcon.triggered.connect(self.drawIconClicked)
        deleteIcon.triggered.connect(self.deleteIconClicked)
    
    def selectIconClicked(self):
        self.selectedIcon = ICON_SELECT
    
    def moveIconClicked(self):
        self.selectedIcon = ICON_MOVE

    def drawIconClicked(self):
        self.selectedIcon = ICON_DRAW

    def deleteIconClicked(self):
        self.selectedIcon = ICON_DELETE
    
    
