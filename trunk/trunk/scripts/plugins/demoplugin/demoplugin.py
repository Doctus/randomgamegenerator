from PyQt4 import QtCore, QtGui
import rggEvent

class demoWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)

        self.__eat = False

        self.setWindowTitle(self.tr("Plugin Demo!"))
        self.widget = QtGui.QWidget(mainWindow)
        self.demoButton = QtGui.QPushButton(self.tr("SHINY BUTTON"), mainWindow)
        self.layout = QtGui.QBoxLayout(2)
        self.layout.addWidget(self.demoButton)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

        rggEvent.addMousePressListener(self)
        rggEvent.addMouseReleaseListener(self)
        
        self.connect(self.demoButton, QtCore.SIGNAL('pressed()'), self.respondPress)
    
    def respondPress(self):
        print "WHAT IS THIS MADNESS YOU PRESSED THE BUTTON"
        self.__eat = not self.__eat
        if self.__eat:
            print 'going to eat press events'
        else:
            print 'not going to eat press events'

    def mousePressResponse(self, x, y, t):
        if self.__eat:
            print 'eating press event'
            rggEvent.setEaten()

    def mouseReleaseResponse(self, x, y, t):
        if self.__eat:
            rggEvent.setEaten()

def hajimaru(mainwindow):
    widget = demoWidget(mainwindow)
