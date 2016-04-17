from os import path as ospath

from libraries.rggConstants import MAP_DIR
from libraries.rggJson import jsonload, jsondump
from libraries.rggRPC import serverRPC, clientRPC
from libraries.rggSession import Session
from libraries.rggState import GlobalState
from libraries.rggSystem import translate, showErrorMessage, promptSaveFile, checkFileExtension, promptLoadFile, promptYesNo
from libraries.rggViews.views import allusersbut, clearPogSelection

@serverRPC
def respondSession(session):
	_loadSession(session)

@clientRPC
def sendSession(user, session):
	respondSession(allusersbut(user), session)

@serverRPC
def respondClearSession():
	_clearSession()

@clientRPC
def sendClearSession(user):
	respondClearSession(allusersbut(user))

def _loadSession(data):
	if GlobalState.session is not None:
		GlobalState.session.clear()
	GlobalState.session = Session.load(data)
	GlobalState.pogmanagerwidget.refresh()

def _clearSession():
	clearPogSelection()
	GlobalState.cameraPog = None
	GlobalState.pogmove = [0, 0]
	GlobalState.moveablePogs = []
	try:
		GlobalState.session.clear()
	except AttributeError:
		GlobalState.session = Session()
	GlobalState.pogmanagerwidget.refresh()

def clearSession():
	if promptYesNo(translate('views', 'Are you sure you want to clear the current session completely for all connected players?')) == 16384:
		_clearSession()
		sendClearSession()

def autoloadSession():
	try:
		obj = jsonload(ospath.join(MAP_DIR, "autosave.rgg"))
		_loadSession(obj)
		#Don't bother sending since we shouldn't be connected to anything yet.
	except:
		GlobalState.session = Session()
	if GlobalState.session is None: #catch a few further edge cases
		GlobalState.session = Session()

def loadSession():
	"""Allows the user to load a new map."""
	filename = promptLoadFile(translate('views', 'Open Game Session'),
		translate('views', 'Random Game files (*.rgg)'),
		MAP_DIR)
	if not filename:
		return
	try:
		obj = jsonload(filename)
		_loadSession(obj)
		sendSession(GlobalState.session.dump())
	except Exception as e:
		showErrorMessage(translate('views', "Unable to read {0}.").format(filename))
		print(e)

def saveSession():
	filename = promptSaveFile(translate('views', 'Save Game Session'),
		translate('views', 'Random Game files (*.rgg)'),
		MAP_DIR)
	if not filename:
		return
	jsondump(GlobalState.session.dump(), checkFileExtension(filename, ".rgg"))

def autosaveSession():
	jsondump(GlobalState.session.dump(), ospath.join(MAP_DIR, "autosave.rgg"))
