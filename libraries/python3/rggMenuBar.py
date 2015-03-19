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

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QT_VERSION_STR
from .rggSystem import translate, mainWindow
from .rggJson import loadString, jsonload, jsonappend
from .rggRPC import client
import sys, os
from . import rggStyles
from .rggConstants import *

ICON_SELECT = 0
ICON_MOVE = 1
ICON_DRAW = 2
ICON_DELETE = 3

class menuBar(object):
	"""An object representing the menu bar."""
	
	def __init__(self, mapExistenceCheck=None, pogExistenceCheck=None, charExistenceCheck=None):
		
		main = mainWindow
		
		self.menubar = main.menuBar()
		
		self.mapExistenceCheck = mapExistenceCheck
		self.pogExistenceCheck = pogExistenceCheck
		self.charExistenceCheck = charExistenceCheck
		
		# ACTIONS
		
		self.newMapAct = QAction(translate("menubar", "&New Map..."), main)
		self.newMapAct.setShortcut("Ctrl+N")
		
		self.loadMapAct = QAction(translate("menubar", "Load Map..."), main)
		#self.loadMapAct.setShortcut("Ctrl+L")
		
		self.saveMapAct = QAction(translate("menubar", "Save Map As..."), main)
		#self.saveMapAct.setShortcut("Ctrl+S")
		
		self.closeSpecificMapAct = QAction(translate("menubar", "Close Map"), main)
		
		self.closeMapAct = QAction(translate("menubar", "&Close All Maps"), main)
		self.closeMapAct.setShortcut("Ctrl+Shift+W")
		
		self.loadSessAct = QAction(translate("menubar", "&Load Session..."), main)
		self.loadSessAct.setShortcut("Ctrl+L")
		
		self.saveSessAct = QAction(translate("menubar", "&Save Session As..."), main)
		self.saveSessAct.setShortcut("Ctrl+S")
		
		self.clearSessAct = QAction(translate("menubar", "Clear Session"), main)
		
		self.deletePogsAct = QAction(translate("menubar", "Delete All Pogs"), main)
		
		self.saveCharsAct = QAction(translate("menubar", "Save IC Characters As..."), main)
		
		self.loadCharsAct = QAction(translate("menubar", "Load IC Characters..."), main)

		self.gfxSettingsAct = QAction(translate("menubar", "Configure Graphics..."), main)
		
		self.drawTimerSettingsAct = QAction(translate("menubar", "Configure FPS..."), main)
		
		self.hostGameAct = QAction(translate("menubar", "&Host Game..."), main)
		self.hostGameAct.setShortcut("Ctrl+H")

		self.joinGameAct = QAction(translate("menubar", "&Join Game..."), main)
		self.joinGameAct.setShortcut("Ctrl+J")
		
		self.disconnectAct = QAction(translate("menubar", "&Disconnect"), main)
		self.disconnectAct.setShortcut("Ctrl+D")
		
		self.sendFileAct = QAction(translate("menubar", "Send file..."), main)
		
		self.createSurveyAct = QAction(translate("menubar", "Create Survey..."), main)
		
		self.aboutAct = QAction(translate("menubar", "&About"), main)
		self.aboutAct.setShortcut("Ctrl+A")

		self.thicknessOneAct = QAction(translate("menubar", "&One"), main)
		self.thicknessTwoAct = QAction(translate("menubar", "&Two"), main)
		self.thicknessThreeAct = QAction(translate("menubar", "&Three"), main)
		
		self.toggleAlertsAct = QAction(translate("menubar", "Chat Username Notify"), main)
		self.toggleAlertsAct.setCheckable(True)
		self.toggleAlertsAct.setChecked(True)

		self.toggleTimestampsAct = QAction(translate("menubar", "OOC Chat Timestamps"), main)
		self.toggleTimestampsAct.setCheckable(True)
		self.toggleTimestampsAct.setChecked(False)

		try:
			js = jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))
			if loadString('chatWidget.timestamp', js.get('timestamp')) == "On":
				self.toggleTimestampsAct.setChecked(True)
		except:
			pass

		self.setTimestampFormatAct = QAction(translate("menubar", "Set Timestamp Format..."), main)
		
		self.portraitMenu = QAction(translate("menubar", "Set IC Portrait Size..."), main)
		
		self.selectIcon = QAction(QIcon("./data/FAD-select-icon.png"), "Select Tool", main)
		self.selectIcon.setShortcut("Ctrl+T")
		self.selectIcon.setToolTip("Select Tool (Ctrl+T)")
		
		self.moveIcon = QAction(QIcon("./data/FAD-move-icon.png"), "Move Tool", main)
		self.moveIcon.setShortcut("Ctrl+M")
		self.moveIcon.setToolTip("Move Tool (Ctrl+M)")

		self.drawIcon = QAction(QIcon("./data/FAD-freehand-icon.png"), "Draw Tool", main)
		self.drawIcon.setShortcut("Ctrl+E")
		self.drawIcon.setToolTip("Draw Tool (Ctrl+E)")

		self.deleteIcon = QAction(QIcon("./data/FAD-eraser-icon.png"), "Delete Tool", main)
		self.deleteIcon.setShortcut("Ctrl+R")
		self.deleteIcon.setToolTip("Delete Tool (Ctrl+R)")

		# MENUS
		
		fileMenu = QMenu(translate("menubar", "&File"), main)
		fileMenu.addAction(self.newMapAct)
		fileMenu.addAction(self.loadMapAct)
		fileMenu.addAction(self.saveMapAct)
		fileMenu.addSeparator()
		fileMenu.addAction(self.closeSpecificMapAct)
		fileMenu.addAction(self.closeMapAct)
		fileMenu.addSeparator()
		fileMenu.addAction(self.deletePogsAct)
		fileMenu.addSeparator()
		fileMenu.addAction(self.saveCharsAct)
		fileMenu.addAction(self.loadCharsAct)
		fileMenu.addSeparator()
		fileMenu.addAction(self.saveSessAct)
		fileMenu.addAction(self.loadSessAct)
		fileMenu.addAction(self.clearSessAct)
		
		self.mapExistsActs = [self.saveMapAct, self.closeSpecificMapAct, self.closeMapAct]
		self.pogExistsActs = [self.deletePogsAct,]
		self.characterExistsActs = [self.saveCharsAct,]
		
		self.internetMenu = QMenu(translate("menubar", "&Internet"), main)
		self.internetMenu.addAction(self.hostGameAct)
		self.internetMenu.addAction(self.joinGameAct)
		self.internetMenu.addSeparator()
		self.internetMenu.addAction(self.createSurveyAct)
		self.internetMenu.addAction(self.sendFileAct)
		self.internetMenu.addSeparator()
		self.internetMenu.addAction(self.disconnectAct)
		
		self.connectedActs = [self.createSurveyAct, self.sendFileAct, self.disconnectAct]
		self.disconnectedActs = [self.hostGameAct, self.joinGameAct]

		self.thicknessMenu = QMenu(translate("menubar", "&Thickness"), main)
		for x in range(1, 11):
			self.thicknessMenu.addAction(QAction(str(x), main))
		
		self.colourMenu = QMenu(translate("menubar", "&Colour"), main)
		#Don't translate colour names yet
		self.colourMenu.addAction(QAction("White", main))
		self.colourMenu.addAction(QAction("Red", main))
		self.colourMenu.addAction(QAction("Orange", main))
		self.colourMenu.addAction(QAction("Yellow", main))
		self.colourMenu.addAction(QAction("Green", main))
		self.colourMenu.addAction(QAction("Blue", main))
		self.colourMenu.addAction(QAction("Purple", main))
		self.colourMenu.addAction(QAction("Black", main))
		self.colourMenu.addAction(QAction("Custom...", main))

		drawMenu = QMenu(translate("menubar", "&Draw"), main)
		drawMenu.addMenu(self.thicknessMenu)
		drawMenu.addMenu(self.colourMenu)
		
		stylesMenu = QMenu(translate("menubar", "&Styles"), main)
		for style in list(rggStyles.sheets.keys()):
			stylesMenu.addAction(QAction(style, main))
		self.resetStyle()

		self.langMenu = QMenu(translate("menubar", "&Language"), main)
		ned = QAction(translate("menubar", "Dutch"), main)
		ned.setIconText("Dutch")
		self.langMenu.addAction(ned)
		eng = QAction(translate("menubar", "English"), main)
		eng.setIconText("English")
		self.langMenu.addAction(eng)
		nhn = QAction(translate("menubar", "Japanese"), main)
		nhn.setIconText("Japanese")
		self.langMenu.addAction(nhn)
		deu = QAction(translate("menubar", "German"), main)
		deu.setIconText("German")
		self.langMenu.addAction(deu)
			
		self.optionsMenu = QMenu(translate("menubar", "&Options"), main)
		self.optionsMenu.addMenu(self.langMenu)
		self.optionsMenu.addMenu(stylesMenu)
		self.optionsMenu.addSeparator()
		self.optionsMenu.addAction(self.toggleAlertsAct)
		self.optionsMenu.addAction(self.toggleTimestampsAct)
		self.optionsMenu.addAction(self.setTimestampFormatAct)
		self.optionsMenu.addAction(self.portraitMenu)
		self.optionsMenu.addAction(self.gfxSettingsAct)
		self.optionsMenu.addAction(self.drawTimerSettingsAct)
		
		
		self.pluginsMenu = QMenu(translate("menubar", "&Plugins"), main)
		
		self.pluginsModules = []
		self.plugins = {}
		sys.path.append(PLUGINS_DIR)
		try:
			for folder in os.listdir(PLUGINS_DIR):
				if folder == ".svn":
					continue
				try:
					self.pluginsModules.append(__import__(folder))
					self.pluginsMenu.addAction(QAction(str(self.pluginsModules[-1].title()), main))
					self.plugins[str(self.pluginsModules[-1].title())] = folder
				except:
					pass
		except Exception as e:
			pass
				
		self.windowMenu = QMenu(translate("menubar", "Window"), main)
		
		self.helpMenu = QMenu(translate("menubar", "&Help"), main)
		self.helpMenu.addAction(self.aboutAct)
		
		# MENUBAR

		self.menubar.addMenu(fileMenu)
		self.menubar.addMenu(self.internetMenu)
		self.menubar.addMenu(drawMenu)
		self.menubar.addMenu(self.optionsMenu)
		self.pluginhide = self.menubar.addMenu(self.pluginsMenu)
		if list(int(r) for r in PYQT_VERSION_STR.split(".")) < [4,  8,  0]:
			warning = QMessageBox()
			warning.setText("".join(("Your version of PyQt (", PYQT_VERSION_STR, ") is incompatible with RGG's Window menu, which requires 4.8.0 or newer. Right-click on the menu bar to get an alternate menu.")))
			warning.exec_()
		else:
			self.menubar.addMenu(self.windowMenu)
		self.menubar.addMenu(self.helpMenu)
		self.menubar.addSeparator()
		self.menubar.addAction(self.selectIcon)
		self.menubar.addAction(self.moveIcon)
		self.menubar.addAction(self.drawIcon)
		self.menubar.addAction(self.deleteIcon)

		# EVENTS
		
		self.selectIconClicked()
		self.selectIcon.triggered.connect(self.selectIconClicked)
		self.moveIcon.triggered.connect(self.moveIconClicked)
		self.drawIcon.triggered.connect(self.drawIconClicked)
		self.deleteIcon.triggered.connect(self.deleteIconClicked)
		
		stylesMenu.triggered.connect(self.changeStyle)
		self.pluginsMenu.triggered.connect(self.loadPlugin)
		
		fileMenu.aboutToShow.connect(self.updateFileMenu)
		self.internetMenu.aboutToShow.connect(self.updateInternetMenu)
		self.windowMenu.aboutToShow.connect(self.updateWidgetMenu)
		
		self.aboutAct.triggered.connect(self.about)
		
	def resetIcons(self):
		self.selectIcon.setIcon(QIcon("./data/FAD-select-icon.png"))
		self.moveIcon.setIcon(QIcon("./data/FAD-move-icon.png"))
		self.drawIcon.setIcon(QIcon("./data/FAD-freehand-icon.png"))
		self.deleteIcon.setIcon(QIcon("./data/FAD-eraser-icon.png"))
	
	def selectIconClicked(self):
		self.resetIcons()
		self.selectIcon.setIcon(QIcon("./data/FAD-select-icon-selected.png"))
		self.selectedIcon = ICON_SELECT
	
	def moveIconClicked(self):
		self.resetIcons()
		self.moveIcon.setIcon(QIcon("./data/FAD-move-icon-selected.png"))
		self.selectedIcon = ICON_MOVE

	def drawIconClicked(self):
		self.resetIcons()
		self.drawIcon.setIcon(QIcon("./data/FAD-freehand-icon-selected.png"))
		self.selectedIcon = ICON_DRAW

	def deleteIconClicked(self):
		self.resetIcons()
		self.deleteIcon.setIcon(QIcon("./data/FAD-eraser-icon-selected.png"))
		self.selectedIcon = ICON_DELETE
		
	def loadPlugin(self, act):
		exec("from " + (self.plugins[str(act.text())]) + " import " + (self.plugins[str(act.text())]))
		exec(self.plugins[str(act.text())] + ".hajimaru(mainWindow)")
		self.pluginsMenu.removeAction(act)
		if len(self.pluginsMenu.actions()) == 0:
			self.pluginhide.setVisible(False)
	
	def resetStyle(self):
		try:
			obj = jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))
			mainWindow.setStyleSheet(rggStyles.sheets[obj["style"]])
		except:
			mainWindow.setStyleSheet(rggStyles.sheets["Default"])
	
	def changeStyle(self, act):
		#TODO: make this instead linked to rggViews which calls this and also toggleDarkBackgroundSupport on chat widgets
		mainWindow.setStyleSheet(rggStyles.sheets[str(act.text())])
		jsonappend({'style':str(act.text())}, os.path.join(SAVE_DIR, "ui_settings.rgs"))
		
	def updateWidgetMenu(self):
		self.windowMenu.clear()
		for action in mainWindow.createPopupMenu().actions():
			self.windowMenu.addAction(action)
			
	def updateFileMenu(self):
		for act in self.mapExistsActs:
			act.setEnabled(self.mapExistenceCheck())
		for act in self.pogExistsActs:
			act.setEnabled(self.pogExistenceCheck())
		for act in self.characterExistsActs:
			act.setEnabled(self.charExistenceCheck())
			
	def updateInternetMenu(self):
		for act in self.connectedActs:
			act.setEnabled(client.isConnected)
		for act in self.disconnectedActs:
			act.setEnabled(not client.isConnected)
			
	def about(self):
		msg = QMessageBox(mainWindow)
		if DEV:
			aboutText = " ".join(("RGG", VERSION, "Development Version", "\nPython", ".".join(str(x) for x in sys.version_info[:3]), "\nPyQt", PYQT_VERSION_STR, "(Qt", QT_VERSION_STR+")"))
		else:
			aboutText = " ".join(("RGG", VERSION, "Release", "\nPython", ".".join(str(x) for x in sys.version_info[:3]), "\nPyQt", PYQT_VERSION_STR, "(Qt", QT_VERSION_STR+")"))
		msg.setText(aboutText)
		msg.setInformativeText(REPOSITORY_LINK)
		msg.setWindowTitle("About")
		msg.exec_()
