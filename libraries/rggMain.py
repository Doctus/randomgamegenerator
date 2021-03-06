# -*- coding: utf-8 -*-
#
#main class
#
#By Oipo (kingoipo@gmail.com)
'''
    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''

from os import path

from libraries.rggQt import QMainWindow, QIcon, QTimer, QSettings
from .glwidget import GLWidget
from libraries.rggJson import loadInteger, jsonload
from libraries.rggConstants import SAVE_DIR

class MainWindow(QMainWindow):

	def __init__(self):
		'''
		Only initialize critical components(like opengl) here, use start() for anything else
		'''
		QMainWindow.__init__(self)

		self.setWindowTitle("RandomGameGenerator")
		self.setObjectName("MainWindow")
		try: self.setWindowIcon(QIcon(path.join("data", "rgglogo2.png")))
		except: pass

		self.glwidget = GLWidget(self)
		self.setCentralWidget(self.glwidget)

		self.drawTimer = QTimer()
		self.drawTimer.timeout.connect(self.drawTimerTimeout)
		try:
			js = jsonload(path.join(SAVE_DIR, "ui_settings.rgs"))
			drawtimer = loadInteger('init.drawtimer', js.get('drawtimer'))
			self.drawTimer.start(drawtimer)
		except:
			self.drawTimer.start(20)

	def readGeometry(self):
		settings = QSettings("AttercopProductions", "RGG")
		settings.beginGroup("MainWindow")
		self.restoreGeometry(settings.value("geometry"))
		self.restoreState(settings.value("windowState"))
		settings.endGroup()

	def closeEvent(self, event):
		settings = QSettings("AttercopProductions", "RGG")
		settings.beginGroup("MainWindow")
		settings.setValue("geometry", self.saveGeometry())
		settings.setValue("windowState", self.saveState())
		settings.endGroup()
		QMainWindow.closeEvent(self, event)

	def drawTimerTimeout(self):
		self.glwidget.updateGL()
