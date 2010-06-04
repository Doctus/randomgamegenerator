from PyQt4 import QtCore, QtGui

class demoWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        self.setWindowTitle(self.tr("Plugin Demo!"))
        self.widget = QtGui.QWidget(mainWindow)
        self.demoButton = QtGui.QPushButton(self.tr("SHINY BUTTON"), mainWindow)
        self.layout = QtGui.QBoxLayout(2)
        self.layout.addWidget(self.demoButton)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        
        self.connect(self.demoButton, QtCore.SIGNAL('pressed()'), self.respondPress)
    
    def respondPress(self):
        print "WHAT IS THIS MADNESS YOU PRESSED THE BUTTON"

def hajimaru(mainwindow):
    widget = demoWidget(mainwindow)