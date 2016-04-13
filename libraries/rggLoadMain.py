APPLICATION = [None,]
MAIN = [None,]
SERVER = [None,]
CLIENT = [None,]
PROGRESS = [None,]

def loadMain():
	from .rggQt import Qt
	progress = PROGRESS[0]

	from . import rggRPC, rggState, rggViews, rggDockWidget
	progress.setValue(2)
	from . import rggChat, rggICChat #bad, but necessary for now to initialize here
	progress.setValue(3)

	progress.setLabelText("Connecting events...")

	from .rggSignalConfig import connectEvents
	progress.setValue(4)

	# Initialize view state.
	progress.setLabelText("Initializing widgets...")
	rggState.GlobalState.initialize(APPLICATION[0])
	progress.setValue(5)
	rggDockWidget.initialize(MAIN[0])
	progress.setValue(6)
	rggViews.initialize()

	progress.setValue(7)

	progress.setLabelText("Initializing network capabilities...")

	SERVER[0] = rggRPC.server
	CLIENT[0] = rggRPC.client

	progress.setValue(8)

	progress.setLabelText("Finalizing GUI...")

	connectEvents(CLIENT[0], SERVER[0], MAIN[0].glwidget)

	progress.setValue(9)

	progress.setLabelText("Loading autosaved session...")

	rggViews.autoloadSession()

	progress.setValue(10)

	PROGRESS[0] = None
