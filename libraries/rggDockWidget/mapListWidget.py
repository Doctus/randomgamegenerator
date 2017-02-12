from libraries.rggConstants import EARLY_RESPONSE_LEVEL
from libraries.rggEvent import addMapCreatedListener, addMapRemovedListener
from libraries.rggQt import QListWidgetItem, QListWidget, QDockWidget, QAbstractItemView, Qt
from libraries.rggState import GlobalState
from libraries.rggSystem import showPopupMenuAtAbs
from libraries.rggViews.views import mapActionList, processMapCommand

class mappeItem(QListWidgetItem):

	def __init__(self, mappe):
		QListWidgetItem.__init__(self)
		self.setMappe(mappe)
		self.dead = False

	def setMappe(self, mappe):
		self.mappeID = mappe.ID
		name = mappe.mapname
		name += " (" + mappe.tileset + ") "
		name += mappe.ID
		self.setText(name)

class mapListListWidget(QListWidget):

	def __init__(self, parent, mappewidget):
		QListWidget.__init__(self)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.mappewidget = mappewidget

	def mousePressEvent(self, event):
		pos = event.globalPos()
		x = pos.x()
		y = pos.y()
		specificItem = self.itemAt(event.x(), event.y())
		event.accept()
		if specificItem is None:
			return
		self.setCurrentItem(specificItem)

		if event.button() == Qt.RightButton:
			selection = showPopupMenuAtAbs([x, y], mapActionList(specificItem.mappeID))
			processMapCommand(selection, specificItem.mappeID)

class mapListWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(mapListWidget, self).__init__(mainWindow)

		self.setWindowTitle(self.tr("Map Manager"))
		self.listWidget = mapListListWidget(mainWindow, self)
		self.setWidget(self.listWidget)
		self.setObjectName("Map Manager")

		addMapCreatedListener(self.mapAddedResponse, EARLY_RESPONSE_LEVEL)
		addMapRemovedListener(self.mapRemovedResponse, EARLY_RESPONSE_LEVEL)

		mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)

	def mapAddedResponse(self, mappe):
		for x in range(self.listWidget.count()):
			if self.listWidget.item(x) is not None and self.listWidget.item(x).mappeID == mappe.ID:
				self.listWidget.item(x).setMappe(mappe)
				self.update()
				return

		self.listWidget.addItem(mappeItem(mappe))
		self.update()

	def mapRemovedResponse(self, ID):
		for x in range(self.listWidget.count()):
			if self.listWidget.item(x) is not None and self.listWidget.item(x).mappeID == mappe.ID:
				self.listWidget.takeItem(x)
				self.update()
