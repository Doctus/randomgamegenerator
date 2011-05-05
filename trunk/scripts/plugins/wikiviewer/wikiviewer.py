from PyQt4 import QtCore, QtGui, QtWebKit
import rggEvent, rggViews, rggPog, rggSystem

class wikiViewer(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)
        
        #self.__eat = True

        self.setWindowTitle(self.tr("MoMMWiki Browser"))
        self.widget = QtWebKit.QWebView(mainWindow)
        self.widget.load(QtCore.QUrl("http://momm.seiken.co.uk/wiki/TRPG:TRPG_Index"))
        self.setWidget(self.widget)
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
 
def hajimaru(mainwindow):
    widget = wikiViewer(mainwindow)