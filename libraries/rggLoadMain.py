'''
rggLoadMain - for the Random Game Generator project
By Doctus (kirikayuumura.noir@gmail.com)

Deferred loading and progress display for main components.

    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''

APPLICATION = [None,]
MAIN = [None,]
SERVER = [None,]
CLIENT = [None,]
PROGRESS = [None,]

def loadMain():
	from libraries.rggQt import QApplication
	progress = PROGRESS[0]

	from . import rggRPC, rggState, rggViews
	from libraries.rggDockWidget import initialize as dockInitialize
	progress.setValue(2)
	QApplication.processEvents()
	from . import rggChat, rggICChat #bad, but necessary for now to initialize here
	progress.setValue(3)
	QApplication.processEvents()

	# Initialize view state.
	progress.setLabelText("Initializing widgets...")
	rggState.GlobalState.initialize(APPLICATION[0])
	progress.setValue(4)
	QApplication.processEvents()
	dockInitialize(MAIN[0])
	progress.setValue(5)
	QApplication.processEvents()
	rggViews.initialize()

	progress.setValue(6)
	QApplication.processEvents()

	progress.setLabelText("Initializing network capabilities...")

	SERVER[0] = rggRPC.server
	CLIENT[0] = rggRPC.client

	progress.setValue(7)
	QApplication.processEvents()

	progress.setLabelText("Finalizing GUI...")

	try:
		MAIN[0].readGeometry()
	except:
		pass

	progress.setValue(8)
	QApplication.processEvents()

	progress.setLabelText("Loading autosaved session...")

	rggViews.autoloadSession()

	progress.setValue(9)
	QApplication.processEvents()

	progress.setLabelText("Connecting events...")

	from libraries.rggSignalConfig import connectEvents
	progress.setValue(10)
	connectEvents(CLIENT[0], SERVER[0], MAIN[0].glwidget)
	QApplication.processEvents()

	PROGRESS[0] = None
