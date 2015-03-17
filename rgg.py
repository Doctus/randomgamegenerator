import sys, os

if sys.version_info > (3, 0, 0):
	from PyQt5.QtCore import *
	from PyQt5.QtGui import *
	from PyQt5.QtWidgets import *
	from PyQt5.QtOpenGL import *
	from libraries.python3.rggSystem import injectMain, SAVE_DIR
	from libraries.python3.rggJson import loadString, jsonload
	from libraries.python3.rggConstants import *
else:
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	from PyQt4.QtOpenGL import *
	from libraries.python2.rggSystem import injectMain, SAVE_DIR
	from libraries.python2.rggJson import loadString, jsonload
	from libraries.python2.rggConstants import *

if __name__ == '__main__':
	fieldtemp = ["English"]
	app = QApplication(['RGG in Space'])

	try:
		js = jsonload(os.path.join(SAVE_DIR, "lang_settings.rgs"))
		fieldtemp[0] = loadString('lang.language', js.get('language'))
	except:
		print("no language settings detected")

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
	
	if sys.version_info > (3, 0, 0):
		from libraries.python3 import rggRPC, rggViews
		from libraries.python3 import rggChat, rggICChat #bad, but necessary for now to initialize here
		from libraries.python3.rggSignalConfig import connectEvents
	else:
		from libraries.python2 import rggRPC, rggViews
		from libraries.python2 import rggChat, rggICChat #bad, but necessary for now to initialize here
		from libraries.python2.rggSignalConfig import connectEvents
	
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
