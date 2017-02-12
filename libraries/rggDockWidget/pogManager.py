from libraries.rggConstants import EARLY_RESPONSE_LEVEL
from libraries.rggEvent import addPogUpdateListener, addPogDeleteListener, addPogSelectionChangedListener
from libraries.rggQt import QListWidgetItem, QListWidget, QDockWidget, QAbstractItemView, Qt
from libraries.rggState import GlobalState
from libraries.rggSystem import showPopupMenuAtAbs
from libraries.rggViews.views import pogActionList, processPogRightclick

class pogItem(QListWidgetItem):

	def __init__(self, pog):
		QListWidgetItem.__init__(self)
		self.setPog(pog)
		self.dead = False

	def getPog(self):
		return self.__pog

	def setPog(self, pog):
		self.__pog = pog
		name = pog.name
		if name == None or len(name) <= 0:
			name = "No name (" + pog._src + ")"
		if pog._locked:
			name += " [L]"
		if pog.hidden:
			name += " [H]"
		self.setText(name)

class pogListWidget(QListWidget):

	def __init__(self, parent, pogwidget):
		QListWidget.__init__(self)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.pogwidget = pogwidget

	def mousePressEvent(self, event): #listwidget generated events
		pos = event.globalPos()
		x = pos.x()
		y = pos.y()
		specificItem = self.itemAt(event.x(), event.y())
		event.accept()
		if specificItem is None:
			return
		self.setCurrentItem(specificItem)

		if event.button() == Qt.RightButton:
			selection = showPopupMenuAtAbs([x, y], pogActionList(specificItem.getPog()))
			processPogRightclick(selection, [specificItem.getPog(),])
		self.pogwidget.refresh()


	def selectionChanged(self, selected, deselected):
		super(QListWidget, self).selectionChanged(selected, deselected)
		for index in selected.indexes():
			item = self.item(index.row())
			if not item.dead:
				GlobalState.pogSelection.add(item.getPog())
		for index in deselected.indexes():
			item = self.item(index.row())
			if not item.dead:
				GlobalState.pogSelection.discard(item.getPog())

class pogManagerWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(pogManagerWidget, self).__init__(mainWindow)

		self.setWindowTitle(self.tr("Pogs"))
		self.listWidget = pogListWidget(mainWindow, self)
		self.setWidget(self.listWidget)
		self.setObjectName("Pog Plugin")

		self.pogSelectionChangedResponse()

		addPogUpdateListener(self, EARLY_RESPONSE_LEVEL)
		addPogDeleteListener(self, EARLY_RESPONSE_LEVEL)
		addPogSelectionChangedListener(self.pogSelectionChangedResponse, EARLY_RESPONSE_LEVEL)

		mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)

	def refresh(self):
		self.listWidget.clear()
		for pog in GlobalState.session.pogs.values():
			self.pogUpdateResponse(pog)
		self.update()

	def pogUpdateResponse(self, pog):
		for x in range(self.listWidget.count()):
			if self.listWidget.item(x) is not None and self.listWidget.item(x).getPog().ID == pog.ID:
				self.listWidget.item(x).setPog(pog)
				self.update()
				return

		self.listWidget.addItem(pogItem(pog))
		self.update()

	def pogDeleteResponse(self, pog):
		for x in range(self.listWidget.count()):
			if self.listWidget.item(x) is not None and self.listWidget.item(x).getPog().ID == pog.ID:
				self.listWidget.takeItem(x)
				self.update()
				#return

	def pogSelectionChangedResponse(self):
		selectedPogs = GlobalState.pogSelection

		for x in range(self.listWidget.count()):
			item = self.listWidget.item(x)
			if item.getPog() in selectedPogs:
				item.setSelected(True)
			else:
				item.setSelected(False)

		self.update()
