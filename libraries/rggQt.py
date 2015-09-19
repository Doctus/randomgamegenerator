try:
	from PyQt5.QtCore import *
	from PyQt5.QtGui import *
	from PyQt5.QtWidgets import *
	from PyQt5.QtOpenGL import *
	from PyQt5.QtNetwork import *
except ImportError:
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	from PyQt4.QtOpenGL import *
	from PyQt4.QtNetwork import *

if PYQT_VERSION >= 327680:
	PYQT5 = True
else:
	PYQT5 = False
