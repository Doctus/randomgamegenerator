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
from rggSystem import translate, mainWindow
from rggJson import loadString, jsonload, jsonappend
import sys, os, rggStyles
from rggConstants import *

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
		
		self.newMapAct = QtGui.QAction(translate("menubar", "&New Map..."), main)
		self.newMapAct.setShortcut("Ctrl+N")
		
		self.loadMapAct = QtGui.QAction(translate("menubar", "Load Map..."), main)
		#self.loadMapAct.setShortcut("Ctrl+L")
		
		self.saveMapAct = QtGui.QAction(translate("menubar", "Save Map As..."), main)
		#self.saveMapAct.setShortcut("Ctrl+S")
		
		self.closeSpecificMapAct = QtGui.QAction(translate("menubar", "Close Map"), main)
		
		self.closeMapAct = QtGui.QAction(translate("menubar", "&Close All Maps"), main)
		self.closeMapAct.setShortcut("Ctrl+Shift+W")
		
		self.loadSessAct = QtGui.QAction(translate("menubar", "&Load Session..."), main)
		self.loadSessAct.setShortcut("Ctrl+L")
		
		self.saveSessAct = QtGui.QAction(translate("menubar", "&Save Session As..."), main)
		self.saveSessAct.setShortcut("Ctrl+S")
		
		self.clearSessAct = QtGui.QAction(translate("menubar", "Clear Session"), main)
		
		self.deletePogsAct = QtGui.QAction(translate("menubar", "Delete All Pogs"), main)
		
		self.saveCharsAct = QtGui.QAction(translate("menubar", "Save IC Characters As..."), main)
		
		self.loadCharsAct = QtGui.QAction(translate("menubar", "Load IC Characters..."), main)

		self.gfxSettingsAct = QtGui.QAction(translate("menubar", "Configure Graphics..."), main)
		
		self.drawTimerSettingsAct = QtGui.QAction(translate("menubar", "Configure FPS..."), main)
		
		self.hostGameAct = QtGui.QAction(translate("menubar", "&Host Game..."), main)
		self.hostGameAct.setShortcut("Ctrl+H")

		self.joinGameAct = QtGui.QAction(translate("menubar", "&Join Game..."), main)
		self.joinGameAct.setShortcut("Ctrl+J")
		
		self.disconnectAct = QtGui.QAction(translate("menubar", "&Disconnect"), main)
		self.disconnectAct.setShortcut("Ctrl+D")
		
		self.sendFileAct = QtGui.QAction(translate("menubar", "Send file..."), main)
		
		self.createSurveyAct = QtGui.QAction(translate("menubar", "Create Survey..."), main)
		
		self.aboutAct = QtGui.QAction(translate("menubar", "&About"), main)
		self.aboutAct.setShortcut("Ctrl+A")

		self.thicknessOneAct = QtGui.QAction(translate("menubar", "&One"), main)
		self.thicknessTwoAct = QtGui.QAction(translate("menubar", "&Two"), main)
		self.thicknessThreeAct = QtGui.QAction(translate("menubar", "&Three"), main)
		
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
		
		self.portraitMenu = QtGui.QAction(translate("menubar", "Set IC Portrait Size..."), main)
		
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
		
		fileMenu = QtGui.QMenu(translate("menubar", "&File"), main)
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
		
		internetMenu = QtGui.QMenu(translate("menubar", "&Internet"), main)
		internetMenu.addAction(self.hostGameAct)
		internetMenu.addAction(self.joinGameAct)
		internetMenu.addSeparator()
		internetMenu.addAction(self.createSurveyAct)
		internetMenu.addAction(self.sendFileAct)
		internetMenu.addSeparator()
		internetMenu.addAction(self.disconnectAct)

		self.thicknessMenu = QtGui.QMenu(translate("menubar", "&Thickness"), main)
		for x in range(1, 11):
			self.thicknessMenu.addAction(QtGui.QAction(str(x), main))
		
		self.colourMenu = QtGui.QMenu(translate("menubar", "&Colour"), main)
		#Don't translate colour names yet
		self.colourMenu.addAction(QtGui.QAction("White", main))
		self.colourMenu.addAction(QtGui.QAction("Red", main))
		self.colourMenu.addAction(QtGui.QAction("Orange", main))
		self.colourMenu.addAction(QtGui.QAction("Yellow", main))
		self.colourMenu.addAction(QtGui.QAction("Green", main))
		self.colourMenu.addAction(QtGui.QAction("Blue", main))
		self.colourMenu.addAction(QtGui.QAction("Purple", main))
		self.colourMenu.addAction(QtGui.QAction("Black", main))
		self.colourMenu.addAction(QtGui.QAction("Custom...", main))

		drawMenu = QtGui.QMenu(translate("menubar", "&Draw"), main)
		drawMenu.addMenu(self.thicknessMenu)
		drawMenu.addMenu(self.colourMenu)
		
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
		self.optionsMenu.addMenu(self.langMenu)
		self.optionsMenu.addMenu(stylesMenu)
		self.optionsMenu.addSeparator()
		self.optionsMenu.addAction(self.toggleAlertsAct)
		self.optionsMenu.addAction(self.toggleTimestampsAct)
		self.optionsMenu.addAction(self.setTimestampFormatAct)
		self.optionsMenu.addAction(self.portraitMenu)
		self.optionsMenu.addAction(self.gfxSettingsAct)
		self.optionsMenu.addAction(self.drawTimerSettingsAct)
		
		
		self.pluginsMenu = QtGui.QMenu(translate("menubar", "&Plugins"), main)
		
		self.pluginsModules = []
		self.plugins = {}
		sys.path.append(PLUGINS_DIR)
		try:
			for folder in os.listdir(PLUGINS_DIR):
				if folder == ".svn":
					continue
				try:
					self.pluginsModules.append(__import__(folder))
					self.pluginsMenu.addAction(QtGui.QAction(unicode(self.pluginsModules[-1].title()), main))
					self.plugins[unicode(self.pluginsModules[-1].title())] = folder
				except:
					pass
		except Exception as e:
			pass
				
		self.windowMenu = QtGui.QMenu(translate("menubar", "Window"), main)
		
		self.helpMenu = QtGui.QMenu(translate("menubar", "&Help"), main)
		self.helpMenu.addAction(self.aboutAct)
		
		# MENUBAR

		self.menubar.addMenu(fileMenu)
		self.menubar.addMenu(internetMenu)
		self.menubar.addMenu(drawMenu)
		self.menubar.addMenu(self.optionsMenu)
		self.pluginhide = self.menubar.addMenu(self.pluginsMenu)
		if list(int(r) for r in PYQT_VERSION_STR.split(".")) < [4,  8,  0]:
			warning = QtGui.QMessageBox()
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
		
		self.windowMenu.aboutToShow.connect(self.updateWidgetMenu)
		
		self.aboutAct.triggered.connect(self.about)
		
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
	
	def resetStyle(self):
		try:
			obj = jsonload(os.path.join(SAVE_DIR, "ui_settings.rgs"))
			mainWindow.setStyleSheet(rggStyles.sheets[obj["style"]])
		except:
			mainWindow.setStyleSheet(rggStyles.sheets["Default"])
	
	def changeStyle(self, act):
		mainWindow.setStyleSheet(rggStyles.sheets[unicode(act.text())])
		jsonappend({'style':unicode(act.text())}, os.path.join(SAVE_DIR, "ui_settings.rgs"))
		
	def updateWidgetMenu(self):
		self.windowMenu.clear()
		for action in mainWindow.createPopupMenu().actions():
			self.windowMenu.addAction(action)
			
	def about(self):
		msg = QtGui.QMessageBox(mainWindow)
		if DEV:
			aboutText = " ".join(("RGG", VERSION, "Development Version"))
		else:
			aboutText = " ".join(("RGG", VERSION, "Release"))
		msg.setText(aboutText)
		msg.setInformativeText("http://code.google.com/p/randomgamegenerator/")
		msg.setWindowTitle("About")
		msg.exec_()
