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
import sys, os, rggStyles

ICON_SELECT = 0
ICON_MOVE = 1
ICON_DRAW = 2
ICON_DELETE = 3

class menuBar(object):
    """An object representing the menu bar."""
    
    def __init__(self):
        
        main = mainWindow
        
        self.menubar = main.menuBar()
        
        # ACTIONS
        
        self.newMapAct = QtGui.QAction("&New Map...", main)
        self.newMapAct.setShortcut("Ctrl+N")
        
        self.loadMapAct = QtGui.QAction("Load Map...", main)
        #self.loadMapAct.setShortcut("Ctrl+L")
        
        self.saveMapAct = QtGui.QAction("Save Map As...", main)
        #self.saveMapAct.setShortcut("Ctrl+S")
        
        self.closeMapAct = QtGui.QAction("&Close All Maps", main)
        self.closeMapAct.setShortcut("Ctrl+Shift+W")
        
        self.loadSessAct = QtGui.QAction("&Load Session...", main)
        self.loadSessAct.setShortcut("Ctrl+L")
        
        self.saveSessAct = QtGui.QAction("&Save Session As...", main)
        self.saveSessAct.setShortcut("Ctrl+S")
        
        self.saveCharsAct = QtGui.QAction("Save IC Characters As...", main)
        
        self.loadCharsAct = QtGui.QAction("Load IC Characters...", main)

        self.gfxSettingsAct = QtGui.QAction("Configure Graphics...", main)
        
        self.hostGameAct = QtGui.QAction("&Host Game...", main)
        self.hostGameAct.setShortcut("Ctrl+H")

        self.joinGameAct = QtGui.QAction("&Join Game...", main)
        self.joinGameAct.setShortcut("Ctrl+J")
        
        self.disconnectAct = QtGui.QAction("&Disconnect", main)
        self.disconnectAct.setShortcut("Ctrl+D")

        self.thicknessOneAct = QtGui.QAction("&One", main)
        self.thicknessTwoAct = QtGui.QAction("&Two", main)
        self.thicknessThreeAct = QtGui.QAction("&Three", main)
        
        self.toggleAlertsAct = QtGui.QAction("Chat Username Notify", main)
        self.toggleAlertsAct.setCheckable(True)
        self.toggleAlertsAct.setChecked(True)
        
        self.selectIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-select-icon.png"), "Select Tool", main)
        self.selectIcon.setShortcut("Ctrl+T")
        self.selectIcon.setToolTip("Select Tool (Ctrl+T)")
        
        self.moveIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-move-icon.png"), "Move Tool", main)
        self.moveIcon.setShortcut("Ctrl+M")
        self.moveIcon.setToolTip("Move Tool (Ctrl+M)")

        self.drawIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-freehand-icon.png"), "Draw Tool", main)
        self.drawIcon.setShortcut("Ctrl+E")
        self.drawIcon.setToolTip("Draw Tool (Ctrl+E)")

        self.deleteIcon = QtGui.QAction(QtGui.QIcon("./data/FAD-eraser-icon.png"), "Delete Tool", main)
        self.deleteIcon.setShortcut("Ctrl+R")
        self.deleteIcon.setToolTip("Delete Tool (Ctrl+R)")
        
        # MENUS
        
        fileMenu = QtGui.QMenu("&File", main)
        fileMenu.addAction(self.newMapAct)
        fileMenu.addAction(self.loadMapAct)
        fileMenu.addAction(self.saveMapAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.closeMapAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveCharsAct)
        fileMenu.addAction(self.loadCharsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveSessAct)
        fileMenu.addAction(self.loadSessAct)
        
        internetMenu = QtGui.QMenu("&Internet", main)
        internetMenu.addAction(self.hostGameAct)
        internetMenu.addAction(self.joinGameAct)
        fileMenu.addSeparator()
        internetMenu.addAction(self.disconnectAct)

        self.thicknessMenu = QtGui.QMenu("&Thickness", main)
        for x in range(1, 11):
            self.thicknessMenu.addAction(QtGui.QAction(str(x), main))
        
        self.colourMenu = QtGui.QMenu("&Colour", main)
        self.colourMenu.addAction(QtGui.QAction("White", main))
        self.colourMenu.addAction(QtGui.QAction("Red", main))
        self.colourMenu.addAction(QtGui.QAction("Orange", main))
        self.colourMenu.addAction(QtGui.QAction("Yellow", main))
        self.colourMenu.addAction(QtGui.QAction("Green", main))
        self.colourMenu.addAction(QtGui.QAction("Blue", main))
        self.colourMenu.addAction(QtGui.QAction("Purple", main))
        self.colourMenu.addAction(QtGui.QAction("Black", main))
        self.colourMenu.addAction(QtGui.QAction("Custom...", main))

        drawMenu = QtGui.QMenu("&Draw", main)
        drawMenu.addMenu(self.thicknessMenu)
        drawMenu.addMenu(self.colourMenu)
        
        stylesMenu = QtGui.QMenu("&Styles", main)
        for style in rggStyles.sheets.keys():
            stylesMenu.addAction(QtGui.QAction(style, main))
            
        self.optionsMenu = QtGui.QMenu("&Options", main)
        self.optionsMenu.addAction(self.toggleAlertsAct)
        self.optionsMenu.addAction(self.gfxSettingsAct)
        
        self.pluginsMenu = QtGui.QMenu("&Plugins", main)
        
        self.pluginsModules = []
        self.plugins = {}
        sys.path.append('plugins')
        for folder in os.listdir('plugins'):
            if folder == ".svn":
                continue
            try:
                self.pluginsModules.append(__import__(folder))
                self.pluginsMenu.addAction(QtGui.QAction(unicode(self.pluginsModules[-1].title()), main))
                self.plugins[unicode(self.pluginsModules[-1].title())] = folder
            except:
                pass
        
        # MENUBAR

        self.menubar.addMenu(fileMenu)
        self.menubar.addMenu(internetMenu)
        self.menubar.addMenu(drawMenu)
        self.menubar.addMenu(stylesMenu)
        self.menubar.addMenu(self.optionsMenu)
        self.pluginhide = self.menubar.addMenu(self.pluginsMenu)
        self.menubar.addSeparator()
        self.menubar.addAction(self.selectIcon)
        self.menubar.addAction(self.moveIcon)
        self.menubar.addAction(self.drawIcon)
        self.menubar.addAction(self.deleteIcon)

        # EVENTS
        
        self.selectedIcon = 0
        self.selectIcon.triggered.connect(self.selectIconClicked)
        self.moveIcon.triggered.connect(self.moveIconClicked)
        self.drawIcon.triggered.connect(self.drawIconClicked)
        self.deleteIcon.triggered.connect(self.deleteIconClicked)
        
        stylesMenu.triggered.connect(self.changeStyle)
        self.pluginsMenu.triggered.connect(self.loadPlugin)
        
    def resetIcons(self):
        self.selectIcon.setIcon(QtGui.QIcon("./data/FAD-select-icon.png"))
        self.moveIcon.setIcon(QtGui.QIcon("./data/FAD-move-icon.png"))
        self.drawIcon.setIcon(QtGui.QIcon("./data/FAD-freehand-icon.png"))
        self.deleteIcon.setIcon(QtGui.QIcon("./data/FAD-eraser-icon.png"))
    
    def selectIconClicked(self):
        self.resetIcons()
        self.selectIcon.setIcon(QtGui.QIcon("./data/FAD-select-icon-selected.png"))
        self.selectedIcon = ICON_SELECT
    
    def moveIconClicked(self):
        self.resetIcons()
        self.moveIcon.setIcon(QtGui.QIcon("./data/FAD-move-icon-selected.png"))
        self.selectedIcon = ICON_MOVE

    def drawIconClicked(self):
        self.resetIcons()
        self.drawIcon.setIcon(QtGui.QIcon("./data/FAD-freehand-icon-selected.png"))
        self.selectedIcon = ICON_DRAW

    def deleteIconClicked(self):
        self.resetIcons()
        self.deleteIcon.setIcon(QtGui.QIcon("./data/FAD-eraser-icon-selected.png"))
        self.selectedIcon = ICON_DELETE
        
    def loadPlugin(self, act):
        exec("from " + (self.plugins[unicode(act.text())]) + " import " + (self.plugins[unicode(act.text())]))
        exec(self.plugins[unicode(act.text())] + ".hajimaru(mainWindow)")
        self.pluginsMenu.removeAction(act)
        if len(self.pluginsMenu.actions()) == 0:
            self.pluginhide.setVisible(False)
    
    def changeStyle(self, act):
        mainWindow.setStyleSheet(rggStyles.sheets[unicode(act.text())])
