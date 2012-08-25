if __name__ == '__main__':
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    import os,  widgets
    
    class MainWindow(QMainWindow):

        def __init__(self):
            QMainWindow.__init__(self)

            self.setWindowTitle("Character Creator")
            self.setObjectName("MainWindow")
            self.widget = QWidget(self)
            self.setCentralWidget(self.widget)
            self.resize(800,  600)
            
        def readGeometry(self):
            settings = QSettings("AttercopProductions", "CHARCRE")
            settings.beginGroup("MainWindow")
            self.restoreGeometry(settings.value("geometry").toByteArray())
            self.restoreState(settings.value("windowState").toByteArray())
            settings.endGroup()
            
        def closeEvent(self, event):
            settings = QSettings("AttercopProductions", "CHARCRE")
            settings.beginGroup("MainWindow")
            settings.setValue("geometry", self.saveGeometry())
            settings.setValue("windowState", self.saveState())
            settings.endGroup()
            QMainWindow.closeEvent(self, event)
    
    app = QApplication(['Character Creator'])
    main = MainWindow()
    widgets.initWidgets(main.widget, main)
    main.show()
    app.exec_()
