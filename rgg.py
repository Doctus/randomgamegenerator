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

import sys, os

def fatalError(error):
	'''Displays a dialog about a fatal launch error and exits RGG.'''
	try:
		try:
			import Tkinter as tkinter
		except ImportError:
			import tkinter
		root = tkinter.Tk()
		root.withdraw()
		import tkMessageBox
		tkMessageBox.showerror("RGG: Fatal Error", error)
	except Exception:
		#If even tk isn't available, just print the error to console.
		print("RGG: Fatal Error: " + error)
	sys.exit()

if sys.path[0] != os.getcwd():
	fatalError("Must be launched from the directory containing rgg.py.")

try:
	try:
		from PyQt5.QtCore import *
		from PyQt5.QtGui import *
		from PyQt5.QtWidgets import *
		from PyQt5.QtOpenGL import *
	except ImportError:
		from PyQt4.QtCore import *
		from PyQt4.QtGui import *
		from PyQt4.QtOpenGL import *
except ImportError:
	if sys.version_info >= (3,):
		fatalError("PyQt5 not found. Please ensure it is installed and available.")
	else:
		fatalError("PyQt4 not found. Please ensure it is installed and available.")
try:
	import OpenGL
except ImportError:
	fatalError("PyOpenGL not found. Please ensure it is installed and available.")

from libraries.rggSystem import injectMain, SAVE_DIR
from libraries.rggJson import loadString, jsonload
from libraries.rggConstants import *

if __name__ == '__main__':
	fieldtemp = ["English"]
	app = QApplication(['RGG'])

	try:
		js = jsonload(os.path.join(SAVE_DIR, "lang_settings.rgs"))
		fieldtemp[0] = loadString('lang.language', js.get('language'))
	except:
		pass

	if fieldtemp[0] != "English":
		transfile = ""
		if fieldtemp[0] == "Japanese":
			transfile = "rgg_py_ja"
		if fieldtemp[0] == "Dutch":
			transfile = "rgg_py_nl"
		if fieldtemp[0] == "German":
			transfile = "rgg_py_de"

		trans = QTranslator()
		if not trans.load(transfile):
			print(transfile + " not found")
		app.installTranslator(trans)

	qgf = QGLFormat.defaultFormat()
	qgf.setSampleBuffers(True)
	QGLFormat.setDefaultFormat(qgf)

	main = injectMain()

	from libraries import rggRPC, rggViews
	from libraries import rggChat, rggICChat #bad, but necessary for now to initialize here
	from libraries.rggSignalConfig import connectEvents

	# Initialize view state.
	s = rggViews._state
	s.initialize(app)

	server = rggRPC.server
	client = rggRPC.client

	connectEvents(client, server, s.menu, s.cwidget, s.icwidget, s.dwidget, s.uwidget, main.glwidget)

	# Start execution
	try:
		main.show()
		app.exec_()
	finally:
		rggViews.autosaveSession()
		client.close()
