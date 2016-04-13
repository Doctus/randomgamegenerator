APPLICATION = [None,]
MAIN = [None,]
SERVER = [None,]
CLIENT = [None,]
PROGRESS = [None,]

def loadMain():
	from .rggQt import Qt, QApplication
	progress = PROGRESS[0]

	from . import rggRPC, rggState, rggViews, rggDockWidget
	progress.setValue(2)
	QApplication.processEvents()
	from . import rggChat, rggICChat #bad, but necessary for now to initialize here
	progress.setValue(3)
	QApplication.processEvents()

	progress.setLabelText("Connecting events...")

	from .rggSignalConfig import connectEvents
	progress.setValue(4)
	QApplication.processEvents()

	# Initialize view state.
	progress.setLabelText("Initializing widgets...")
	rggState.GlobalState.initialize(APPLICATION[0])
	progress.setValue(5)
	QApplication.processEvents()
	rggDockWidget.initialize(MAIN[0])
	progress.setValue(6)
	QApplication.processEvents()
	rggViews.initialize()

	progress.setValue(7)
	QApplication.processEvents()

	progress.setLabelText("Initializing network capabilities...")

	SERVER[0] = rggRPC.server
	CLIENT[0] = rggRPC.client

	progress.setValue(8)
	QApplication.processEvents()

	progress.setLabelText("Finalizing GUI...")

	connectEvents(CLIENT[0], SERVER[0], MAIN[0].glwidget)

	progress.setValue(9)
	QApplication.processEvents()

	progress.setLabelText("Loading autosaved session...")

	rggViews.autoloadSession()

	progress.setValue(10)
	QApplication.processEvents()

	PROGRESS[0] = None
