from PyQt4 import QtGui, QtCore

class testWidget(QtGui.QDockWidget):

  def __init__(self, mainWindow):
    super(QtGui.QDockWidget, self).__init__("Useless Widget", mainWindow)
    self.widget = QtGui.QTextEdit(mainWindow)
    self.widget.setHtml("<b>AWESOME</b>")
    self.setWidget(self.widget)
    mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
