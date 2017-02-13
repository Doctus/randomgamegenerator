# -*- coding: utf-8 -*-
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
if __name__ == '__main__':

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
		from sys import exit
		exit()

	from sys import version_info
	if version_info < (3,):
		fatalError("RGG must be run with Python 3, not Python 2.")

	try:
		from PyQt5.QtWidgets import QProgressDialog, QApplication
	except:
		fatalError("PyQt5 not found. Please ensure it is installed and available.")
	application = QApplication(['RGG'])
	progress = QProgressDialog("Loading...", "Exit", 0, 9)
	progress.setWindowTitle("RGG Loading")
	progress.setWindowModality(2)
	progress.setWindowFlags(progress.windowFlags() | 262144)

	progress.setMinimumDuration(1)

	progress.setValue(1)

	progress.setLabelText("Loading internals...")


	from sys import version_info
	from os import path

	try:
		from libraries.rggQt import QTranslator, QGLFormat, QTimer
	except ImportError:
		fatalError("PyQt5 could not be loaded fully. Please ensure it is properly installed and available.")
	try:
		import OpenGL
	except ImportError:
		fatalError("PyOpenGL not found. Please ensure it is installed and available.")

	QApplication.processEvents()

	from libraries.rggSystem import injectMain
	from libraries.rggJson import loadString, jsonload
	from libraries.rggConstants import SAVE_DIR

	QApplication.processEvents()

	fieldtemp = ["English"]

	try:
		js = jsonload(path.join(SAVE_DIR, "lang_settings.rgs"))
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
		application.installTranslator(trans)

	QApplication.processEvents()

	qgf = QGLFormat.defaultFormat()
	qgf.setSampleBuffers(True)
	QGLFormat.setDefaultFormat(qgf)

	QApplication.processEvents()

	main = injectMain()

	QApplication.processEvents()

	from libraries.rggLoadMain import loadMain, APPLICATION, MAIN, CLIENT, PROGRESS

	QApplication.processEvents()

	APPLICATION[0] = application
	MAIN[0] = main
	PROGRESS[0] = progress
	progress = None

	QApplication.processEvents()

	loadTimer = QTimer.singleShot(10, loadMain)

	# Start execution
	try:
		main.show()
		application.exec_()
	finally:
		from libraries.rggViews.session import autosaveSession
		autosaveSession()
		CLIENT[0].close()
