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
from PyQt4.QtCore import PYQT_VERSION_STR
from rggSystem import translate, mainWindow, SAVE_DIR, VERSION, DEV
from rggJson import loadString, jsonload, jsonappend
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
        
        self.saveCharsAct = QtGui.QAction(translate("menubar", "Save IC Characters As..."), main)
        
        self.loadCharsAct = QtGui.QAction(translate("menubar", "Load IC Characters..."), main)
        
        self.hostGameAct = QtGui.QAction(translate("menubar", "&Host Game..."), main)
        self.hostGameAct.setShortcut("Ctrl+H")

        self.joinGameAct = QtGui.QAction(translate("menubar", "&Join Game..."), main)
        self.joinGameAct.setShortcut("Ctrl+J")
        
        self.disconnectAct = QtGui.QAction(translate("menubar", "&Disconnect"), main)
        self.disconnectAct.setShortcut("Ctrl+D")
        
        self.aboutAct = QtGui.QAction(translate("menubar", "&About"), main)
        self.aboutAct.setShortcut("Ctrl+A")
        
        self.toggleAlertsAct = QtGui.QAction(translate("menubar", "Chat Username Notify"), main)
        self.toggleAlertsAct.setCheckable(True)
        self.toggleAlertsAct.setChecked(True)

        self.toggleTimestampsAct = QtGui.QAction(translate("menubar", "OOC Chat Timestamps"), main)
        self.toggleTimestampsAct.setCheckable(True)
        self.toggleTimestampsAct.setChecked(False)

        try:
            js = jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))
            if loadString('chatWidget.timestamp', js.get('timestamp')) == "On":
                self.toggleTimestampsAct.setChecked(True)
        except:
            pass

        self.setTimestampFormatAct = QtGui.QAction(translate("menubar", "Set Timestamp Format..."), main)

        # MENUS
        
        fileMenu = QtGui.QMenu(translate("menubar", "&File"), main)
        fileMenu.addAction(self.saveCharsAct)
        fileMenu.addAction(self.loadCharsAct)
        
        internetMenu = QtGui.QMenu(translate("menubar", "&Internet"), main)
        internetMenu.addAction(self.hostGameAct)
        internetMenu.addAction(self.joinGameAct)
        internetMenu.addSeparator()
        internetMenu.addAction(self.disconnectAct)
        
        stylesMenu = QtGui.QMenu(translate("menubar", "&Styles"), main)
        for style in rggStyles.sheets.keys():
            stylesMenu.addAction(QtGui.QAction(style, main))
        self.resetStyle()

        self.langMenu = QtGui.QMenu(translate("menubar", "&Language"), main)
        ned = QtGui.QAction(translate("menubar", "Dutch"), main)
        ned.setIconText("Dutch")
        self.langMenu.addAction(ned)
        eng = QtGui.QAction(translate("menubar", "English"), main)
        eng.setIconText("English")
        self.langMenu.addAction(eng)
        nhn = QtGui.QAction(translate("menubar", "Japanese"), main)
        nhn.setIconText("Japanese")
        self.langMenu.addAction(nhn)
        deu = QtGui.QAction(translate("menubar", "German"), main)
        deu.setIconText("German")
        self.langMenu.addAction(deu)
            
        self.optionsMenu = QtGui.QMenu(translate("menubar", "&Options"), main)
        self.optionsMenu.addAction(self.toggleAlertsAct)
        self.optionsMenu.addAction(self.toggleTimestampsAct)
        self.optionsMenu.addAction(self.setTimestampFormatAct)
        
        self.helpMenu = QtGui.QMenu(translate("menubar", "&Help"), main)
        self.helpMenu.addAction(self.aboutAct)
        
        # MENUBAR

        #self.menubar.addMenu(fileMenu)
        self.menubar.addMenu(internetMenu)
        self.optionsMenu.addMenu(stylesMenu)
        self.optionsMenu.addMenu(self.langMenu)
        self.menubar.addMenu(self.optionsMenu)
        self.menubar.addMenu(self.helpMenu)

        # EVENTS
        
        stylesMenu.triggered.connect(self.changeStyle)
       
        self.aboutAct.triggered.connect(self.about)
        
    
    def resetStyle(self):
        try:
            obj = jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))
            mainWindow.setStyleSheet(rggStyles.sheets[obj["style"]])
        except:
            mainWindow.setStyleSheet(rggStyles.sheets["Default"])
    
    def changeStyle(self, act):
        mainWindow.setStyleSheet(rggStyles.sheets[unicode(act.text())])
        jsonappend({'style':unicode(act.text())}, os.path.join(SAVE_DIR, "ui_settings.rgs"))
            
    def about(self):
        msg = QtGui.QMessageBox()
        if DEV:
            aboutText = " ".join(("RChat", VERSION, "Development Version"))
        else:
            aboutText = " ".join(("RChat", VERSION, "Release"))
        msg.setText(aboutText)
        msg.setInformativeText("http://code.google.com/p/randomgamegenerator/")
        msg.setWindowTitle("About")
        msg.exec_()
