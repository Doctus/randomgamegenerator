'''
rggViews - for the Random Game Generator project
By Doctus (kirikayuumura.noir@gmail.com)

Actions which occur in response to user commands.

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
from os import path as ospath

from libraries.rggConstants import PING_INTERVAL_SECONDS, SAVE_DIR, LATE_RESPONSE_LEVEL, UNICODE_STRING, MAP_DIR
from libraries.rggConstants import CHARSHEETS_DIR, POG_DIR, PORTRAIT_DIR, TILESET_DIR, COLOURS, CHAR_DIR
from libraries.rggDialogs import hostDialog, newMapDialog, resizeDialog, modifyPogAttributesDialog, gfxSettingsDialog
from libraries.rggDialogs import surveyResultsDialog, respondSurveyDialog, createSurveyDialog, joinDialog
from libraries.rggDice import isRollValid, roll
from libraries.rggEvent import addMouseMoveListener, addMousePressListener, addMouseReleaseListener
from libraries.rggEvent import addKeyPressListener, addKeyReleaseListener, pogUpdateEvent, pogSelectionChangedEvent
from libraries.rggJson import jsondump, jsonload, jsonappend, loadString
from libraries.rggMap import Map
from libraries.rggMenuBar import ICON_SELECT, ICON_MOVE, ICON_DRAW, ICON_DELETE, menuBar
from libraries.rggPog import Pog
from libraries.rggQt import QTimer, QCursor, QMessageBox, QColorDialog, Qt, QPixmap
from libraries.rggResource import crm, srm
from libraries.rggRPC import server, client, serverRPC, clientRPC
from libraries.rggSession import Session
from libraries.rggState import GlobalState
from libraries.rggStyles import sheets
from libraries.rggSystem import clearSelectionCircles, drawSelectionCircle, translate, promptString, promptInteger
from libraries.rggSystem import promptYesNo, showErrorMessage, promptLoadFile, promptSaveFile, mainWindow
from libraries.rggSystem import getZoom, setCameraPosition, cameraPosition, drawLine, drawSegmentedLine
from libraries.rggSystem import drawCircle, drawRectangleMadeOfLines, drawRegularPolygon, deleteLine
from libraries.rggSystem import clearPreviewLines, clearRectangles, drawRectangle, showPopupMenuAt, getMapPosition
from libraries.rggSystem import promptButtonSelection, checkFileExtension, cameraSize, purgeEmptyFiles

# Button enum
BUTTON_LEFT = 0
BUTTON_MIDDLE = 1
BUTTON_RIGHT = 2
BUTTON_CONTROL = 3
BUTTON_SHIFT = 6

def initialize():
	GlobalState.menu = menuBar(mapExists, pogExists, charExists)

	GlobalState.users = {}
	GlobalState.localuser = User(client.username)
	GlobalState.users[client.username] = GlobalState.localuser
	GlobalState.keepalive = 4

	GlobalState.mwidget.moveMapButton.clicked.connect(moveMap)

	purgeEmptyImages()

	GlobalState.pingTimer = QTimer()
	GlobalState.pingTimer.timeout.connect(keepAlive)
	GlobalState.pingTimer.start(PING_INTERVAL_SECONDS*1000)

	GlobalState.dialogs_keepalive = []

	try:
		GlobalState.portraitSize = jsonload(ospath.join(SAVE_DIR, "ui_settings.rgs"))['portraitsize']
	except:
		GlobalState.portraitSize = "64"

	try:
		obj = jsonload(ospath.join(SAVE_DIR, "ui_settings.rgs"))
		setStyle(obj["style"], sheets[obj["style"]][1])
	except:
		setStyle("Default", False)

	try:
		js = jsonload(ospath.join(SAVE_DIR, "ui_settings.rgs"))
		if loadString('chatWidget.notify', js.get('notify')) == "Off":
			GlobalState.alert = False
	except:
		pass

	try:
		js = jsonload(ospath.join(SAVE_DIR, "ui_settings.rgs"))
		if loadString('chatWidget.rightclick', js.get('rightclick')) == "Off":
			GlobalState.rightclickmode = False
	except:
		pass

	try:
		js = jsonload(ospath.join(SAVE_DIR, "ui_settings.rgs"))
		if loadString('chatWidget.gridlock', js.get('gridlock')) == "On":
			GlobalState.gridMode = True
	except:
		pass

	GlobalState.pogMoveTimer = QTimer()
	GlobalState.pogMoveTimer.timeout.connect(autoMovePogs)
	GlobalState.pogMoveTimer.start(40)

	addMouseMoveListener(mouseMoveResponse, LATE_RESPONSE_LEVEL)
	addMousePressListener(mousePressResponse, LATE_RESPONSE_LEVEL)
	addMouseReleaseListener(mouseReleaseResponse, LATE_RESPONSE_LEVEL)
	addKeyPressListener(keyPressResponse, LATE_RESPONSE_LEVEL)
	addKeyReleaseListener(keyReleaseResponse, LATE_RESPONSE_LEVEL)

# Feel free to add fields to the user object
class User(object):
	"""User representation on the server."""

	def __init__(self, username):
		self.username = username

	def __repr__(self):
		return "User(u'{name}')".format(name=self.username)

	def __unicode__(self):
		return self.username

	def __str__(self):
		return self.__unicode__()

def mapExists():
	if len(list(GlobalState.session.maps.values())) > 0:
		return True
	return False

def pogExists():
	if len(list(GlobalState.session.pogs.values())) > 0:
		return True
	return False

def charExists():
	return GlobalState.icwidget.hasCharacters()

def autoMovePogs():
	if GlobalState.pogmove == [0, 0]:
		return
	movePogs(GlobalState.pogmove)

@serverRPC
def respondDreamIncrement(source, target, amount):
	GlobalState.incrementDreams(target, amount)
	if amount == 1:
		say("%s gave %s a dream."%(source, target))
	elif amount > 1:
		say("%s gave %s %s dreams."%(source, target, str(amount)))
	else:
		say("%s removed %s dreams from %s."%(source, str(amount*-1), target))

@clientRPC
def sendDreamIncrement(user, target, amount):
	respondDreamIncrement(allusers(), str(user), target, amount)

def incrementDreams(target, amount):
	if amount == 0: return
	sendDreamIncrement(target, amount)

def getDreams():
	return GlobalState.dreams

def moveMap():
	pass

def changeStyle(act):
	setStyle(str(act.text()), act.isDark)

def setStyle(styleName, isDark):
	GlobalState.menu.changeStyle(styleName)
	GlobalState.cwidget.toggleDarkBackgroundSupport(isDark)
	GlobalState.icwidget.toggleDarkBackgroundSupport(isDark)

@serverRPC
def reconnectTransferSocket():
	client._openXfer()

def drawPogCircles():
	clearSelectionCircles()
	for pog in GlobalState.pogSelection:
		drawSelectionCircle(*pog.getSelectionCircleData())

def addPogSelection(pog):
	GlobalState.pogSelection.add(pog)
	drawPogCircles()

def removePogSelection(pog):
	GlobalState.pogSelection.remove(pog)
	drawPogCircles()

def setPogSelection(pog):
	GlobalState.pogSelection = set()
	addPogSelection(pog)

def addUserToList(name, host=False):
	GlobalState.uwidget.addUser(name, host)

def toggleAlerts(newValue=None):
	"""Toggles messages containing the user's handle causing an alert."""
	if newValue is None:
		GlobalState.alert = not GlobalState.alert
	else:
		GlobalState.alert = newValue
	if GlobalState.alert:
		jsonappend({'notify':'On'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))
	else:
		jsonappend({'notify':'Off'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))

def toggleTimestamps(newValue=None):
	if newValue is None:
		GlobalState.cwidget.timestamp = not GlobalState.cwidget.timestamp
	else:
		GlobalState.cwidget.timestamp = newValue
	if GlobalState.cwidget.timestamp:
		jsonappend({'timestamp':'On'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))
	else:
		jsonappend({'timestamp':'Off'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))

def toggleRightclick(newValue=None):
	if newValue is None:
		GlobalState.rightclickmode = not GlobalState.rightclickmode
	else:
		GlobalState.rightclickmode = newValue
	if GlobalState.rightclickmode:
		jsonappend({'rightclick':'On'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))
	else:
		jsonappend({'rightclick':'Off'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))

def toggleGridlock(newValue=None):
	if newValue is None:
		GlobalState.gridMode = not GlobalState.gridMode
	else:
		GlobalState.gridMode = newValue
	if GlobalState.gridMode:
		jsonappend({'gridlock':'On'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))
	else:
		jsonappend({'gridlock':'Off'}, ospath.join(SAVE_DIR, "ui_settings.rgs"))

def setTimestampFormat(newFormat):
	GlobalState.cwidget.timestampformat = newFormat
	jsonappend({'timestampformat':newFormat}, ospath.join(SAVE_DIR, "ui_settings.rgs"))

def promptTimestampFormat():
	prompt = translate("views", "Please enter a new timestamp format; the default is [%H:%M:%S]")
	newFormat = promptString(prompt, inittext = GlobalState.cwidget.timestampformat)
	if newFormat is None:
		return
	setTimestampFormat(newFormat)

def getPortraitSize():
	return GlobalState.portraitSize

def setPortraitSize():
	prompt = translate("views", "Please enter a portrait size.")
	try:
		defaultsize = jsonload(ospath.join(SAVE_DIR, "ui_settings.rgs"))['portraitsize']
	except:
		defaultsize = 64
	newSize = promptInteger(prompt, default=defaultsize)
	if newSize is None:
		return
	GlobalState.portraitSize = newSize
	jsonappend({'portraitsize':newSize}, ospath.join(SAVE_DIR, "ui_settings.rgs"))

# MESSAGES

def splitword(message):
	"""Split into a pair: word, rest."""
	words = message.split(None, 1)
	if not words:
		return '', ''
	rest = words[1] if len(words) > 1 else ''
	return words[0], rest

def say(message):
	"""Say an IC message. This documentation is a lie."""
	if GlobalState.alert and localhandle().lower() in message.lower():
		GlobalState.App.alert(mainWindow)
	GlobalState.cwidget.insertMessage(message)

def announce(message):
	"""Say an OOC message. This documentation is a lie."""
	GlobalState.cwidget.insertMessage(message)

def ICSay(message):
	GlobalState.icwidget.insertMessage(message)

def linkedName(name):
	return translate('views', '<a href="/tell {name}" title="{name}">{name}</a>').format(name=name)

# NETWORK (Server only)

def allusers():
	"""Get a list of all users."""
	return list(GlobalState.users.values())

def allusersbut(usernameOrUser):
	user = getuser(usernameOrUser)
	if not user:
		raise RuntimeError("No user named {user}.".format(user=usernameOrUser))
	all = allusers()
	assert(user in all)
	all.remove(user)
	return all

def getuser(username):
	"""Returns a user given a username, or None if not valid."""
	if isinstance(username, User):
		assert(username in allusers())
		return username
	username = UNICODE_STRING(username)
	if server.userExists(username):
		username = server.fullname(username)
		assert(username in GlobalState.users)
		return GlobalState.users[username]
	return None

def usernames():
	"""Returns all the usernames."""
	return list(GlobalState.users.keys())

def getNetUserList():
	"""Returns the user names formatted for transfer over net."""
	return GlobalState.uwidget.getUsers()

def getGM():
	return GlobalState.GM

def isGM():
	return getGM() == localhandle()

def changeGM(username):
	GlobalState.GM = username
	GlobalState.uwidget.setGM(username)

@serverRPC
def respondChangeGM(username, origin):
	if GlobalState.GM is None or origin == GlobalState.GM:
		changeGM(username)

@clientRPC
def sendChangeGM(user, username, origin):
	respondChangeGM(allusers(), username, origin)

def selectGM(newname):
	sendChangeGM(newname, localhandle())

def playerOptions(playername):
	loc = mainWindow.mapFromGlobal(QCursor.pos()) #This gives the wrong result on one axis most of the time, and I've no idea why.
	selected = showPopupMenuAt(
					(loc.x(), loc.y()),
					[translate('views', 'Change movement mode'),
						translate('views', 'Make GM')])
	if selected == 0:
		sendToggleMoveMode(getuser(playername))
	elif selected == 1:
		selectGM(playername)


@serverRPC
def respondSetMoveMode(newMode):
	GlobalState.moveMode = UNICODE_STRING(newMode)

@clientRPC
def sendSetMoveMode(user, target, newMode):
	respondSetMoveMode(getuser(target), newMode)

@serverRPC
def respondToggleMoveMode():
	if GlobalState.moveMode == "free":
		GlobalState.moveMode = "fixed"
	else:
		GlobalState.moveMode = "free"

@clientRPC
def sendToggleMoveMode(user, target):
	respondToggleMoveMode(target)

@serverRPC
def respondAddMoveablePog(pogID):
	GlobalState.moveablePogs.append(pogID)

@clientRPC
def sendAddMoveablePog(user, target, pogID):
	respondAddMoveablePog(getuser(target), pogID)

def setUwidgetLocal():
	GlobalState.uwidget.localname = localhandle()

@serverRPC
def respondPing():
	GlobalState.keepalive = 4

@clientRPC
def sendPing(user):
	respondPing(user)

def keepAlive():
	GlobalState.keepalive -= 1
	if GlobalState.keepalive == 1:
		say(translate('views', '<font color="red">Warning:</font> Connection may have been lost.'))
	if GlobalState.keepalive == 0:
		respondPossibleDisconnect()
	sendPing()

def respondPossibleDisconnect():
	say(translate('views', '<font color="red">Connection appears to have been lost.</font>'))
	disconnectGame()

# TODO: Name changing needs to be synched across the wire
# The workaround is to log out and back in.
#def changeName(user, name):
#	assert(name not in GlobalState.usernames)
#	if user.unnamed:
#		user.unnamed = False
#	if user.username in GlobalState.usernames:
#		del GlobalState.usernames[user.username]
#	GlobalState.usernames[name] = user
#	user.username = name

def localuser():
	"""The user for the local player."""
	return GlobalState.localuser

def localhandle():
	return localuser().username

def adduser(user):
	"""Add a user to the list locally."""
	#print "ADD", user.username
	assert(user.username not in GlobalState.users)
	GlobalState.users[user.username] = user
	return user

def renameuser(oldname, newname):
	"""Rename a user locally."""
	#print "RENAME", oldname, newname
	if oldname == newname:
		return
	user = removeuser(oldname)
	server.rename(oldname, newname)
	user.username = newname
	adduser(user)

def removeuser(username):
	"""Remove a user from the list locally."""
	#print "REMOVE", username
	assert(username in GlobalState.users)
	user = GlobalState.users[username]
	del GlobalState.users[username]
	return user

def hostGame():
	"""Allows the user to host a game."""
	if client.isConnected:
		say(translate('views', "You are already in a game."))
		return

	dialog = hostDialog()

	def accept():
		valid = dialog.is_valid()
		if not valid:
			showErrorMessage(dialog.error)
		return valid

	if dialog.exec_(mainWindow, accept):
		connection = dialog.save()
		server.setPassword(connection.password)
		updateBanlist()
		renameuser(localhandle(), connection.username)
		changeGM(connection.username)
		setUwidgetLocal()
		if client.host(connection.port):
			say(translate('views', 'Now listening on port {port}.').format(port=connection.port))
			addUserToList(localhandle(), True)
		else:
			#TODO: better error message here
			say(translate('views', 'Unable to access network; perhaps the port is in use?'))


def updateBanlist():
	"""Update server banlist based on banlist.rgs file."""
	server.clearBanlist()
	try:
		obj = jsonload(ospath.join(SAVE_DIR, "banlist.rgs"))
		for IP in obj["IPs"]:
			try:
				server.addBan(IP)
			except:
				pass
	except:
		pass

def joinGame():
	"""Allows the user to join a game."""
	if client.isConnected:
		say(translate('views', "You are already in a game."))
		return

	dialog = joinDialog()

	def accept():
		valid = dialog.is_valid()
		if not valid:
			showErrorMessage(dialog.error)
		return valid

	if dialog.exec_(mainWindow, accept):
		_clearSession() #Just in case...
		connection = dialog.save()
		renameuser(localhandle(), connection.username)
		client.setPassword(connection.password)
		client.join(connection.host, connection.port)
		say(translate('views', 'Connecting to {host}:{port}...').format(host=connection.host, port=connection.port))

def killConnection():
	"""Kills the connection without reporting anything."""
	client.close()
	assert(localhandle() in usernames())
	assert(localuser() == getuser(localhandle()))
	clearUserList()

def disconnectGame():
	"""Allows the user to disconnect from the internet."""
	if not client.isConnected:
		say(translate('views', "You are not connected."))
		return

	killConnection()
	say(translate('views', "Disconnected."))
	clearUserList()

def kick(username):
	"""Kicks specified user."""
	server.kick(username)

def getSession():
	return GlobalState.session

def transferFileResponse(responsibleClient, filename, eventDescription):
	GlobalState.fwidget.processFileEvent(responsibleClient, filename, eventDescription)

def partialTransferResponse(responsibleClient, filename, size, processed):
	GlobalState.fwidget.processPartialTransferEvent(responsibleClient, filename, size, processed)

# MAPS
def topmap(mapPosition):
	return GlobalState.session.findTopMap(mapPosition)

def getmap(mapID):
	return GlobalState.session.getMap(mapID)

def allmaps():
	return list(GlobalState.session.maps.items())

def getAllMaps():
	return list(GlobalState.session.maps.values())

def chooseMap():
	say(translate('views', 'This function is deprecated. Use the view controller.'))
	return

@serverRPC
def respondCloseAllMaps():
	_closeAllMaps()

@clientRPC
def sendCloseAllMaps(user):
	respondCloseAllMaps(allusersbut(user))

def _closeAllMaps():
	clearPogSelection()
	GlobalState.session.closeAllMaps()

def closeAllMaps():
	if promptYesNo(translate('views', 'Are you sure you want to close all maps for all connected players?')) == 16384:
		_closeAllMaps()
		sendCloseAllMaps()

@serverRPC
def respondClearSession():
	_clearSession()

@clientRPC
def sendClearSession(user):
	respondClearSession(allusersbut(user))

def _clearSession():
	clearPogSelection()
	GlobalState.cameraPog = None
	GlobalState.pogmove = [0, 0]
	GlobalState.moveablePogs = []
	GlobalState.session.clear()

def clearSession():
	if promptYesNo(translate('views', 'Are you sure you want to clear the current session completely for all connected players?')) == 16384:
		_clearSession()
		sendClearSession()

def internalAddMap(map):
	GlobalState.session.addMap(map)
	sendMapCreate(map.ID, map.dump(), map.tileset)

@serverRPC
def respondSession(sess):
	if GlobalState.session is not None:
		GlobalState.session.clear()
	GlobalState.session = Session.load(sess)

@clientRPC
def sendSession(user, session):
	respondSession(allusersbut(user), session)

def newMap():
	"""Allows the user to choose a new map."""
	dialog = newMapDialog(authName=localhandle())

	def accept():
		valid = dialog.is_valid()
		if not valid:
			showErrorMessage(dialog.error)
		return valid

	if dialog.exec_(mainWindow, accept):
		map = dialog.save()
		internalAddMap(map)

def loadMap():
	"""Allows the user to load a new map."""
	filename = promptLoadFile(translate('views', 'Open Map'),
		translate('views', 'Random Game Map files (*.rgm)'),
		MAP_DIR)
	if not filename:
		return
	try:
		obj = jsonload(filename)
		map = Map.load(obj, True)
		internalAddMap(map)
	except Exception as e:
		showErrorMessage(translate('views', "Unable to read {0}.").format(filename))
		print(e)

def saveMap():
	"""Allows the user to save a map."""
	mapNames = []
	mapIDs = []

	for ID, map in list(GlobalState.session.maps.items()):
		mapNames.append("".join((map.mapname, " (", str(ID), ")")))
		mapIDs.append(ID)

	selectedButton = promptButtonSelection("Which map do you want to save?", mapNames, 0)
	try:
		map = GlobalState.session.maps[mapIDs[selectedButton]]
	except IndexError:
		print("Error: no maps exist to save.")
		return

	filename = promptSaveFile(translate('views', 'Save Map'),
		translate('views', 'Random Game Map files (*.rgm)'),
		MAP_DIR)
	if not filename:
		return

	jsondump(map.dump(), checkFileExtension(filename, ".rgm"))

@serverRPC
def respondCloseSpecificMap(ID):
	_closeSpecificMap(ID)

@clientRPC
def sendCloseSpecificMap(user, ID):
	respondCloseSpecificMap(allusersbut(user), ID)

def _closeSpecificMap(ID):
	GlobalState.session.closeMap(ID)

def closeSpecificMap(ID):
	_closeSpecificMap(ID)
	sendCloseSpecificMap(ID)

def closeMap():
	"""Allows the user to close a map."""
	mapNames = []
	mapIDs = []

	for ID, map in list(GlobalState.session.maps.items()):
		mapNames.append("".join((map.mapname, " (", str(ID), ")")))
		mapIDs.append(ID)

	selectedButton = promptButtonSelection("Which map do you want to close?", mapNames, 0)
	map = mapIDs[selectedButton]

	closeSpecificMap(map)

def autoloadSession():
	try:
		obj = jsonload(ospath.join(MAP_DIR, "autosave.rgg"))
		sess = Session.load(obj)
		GlobalState.session = sess
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
		if GlobalState.session is not None:
			GlobalState.session.clear()
		obj = jsonload(filename)
		sess = Session.load(obj)
		GlobalState.session = sess
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

@serverRPC
def respondSurveyAnswers(surveyData, origin):
	d = surveyResultsDialog(surveyData, str(origin), mainWindow)
	GlobalState.dialogs_keepalive.append(d)
	d.show()

@clientRPC
def sendSurveyAnswers(user, target, surveyData):
	respondSurveyAnswers(getuser(target), surveyData, str(user))

@serverRPC
def respondSurvey(surveyData, origin):
	d = respondSurveyDialog(surveyData, mainWindow)
	if d.exec_():
		sendSurveyAnswers(origin, d.getAnswers())

@clientRPC
def sendSurvey(user, target, surveyData):
	respondSurvey(getuser(target), surveyData, str(user))

def createSurvey():
	d = createSurveyDialog(mainWindow)
	if d.exec_():
		for username in str(d.sendTo.text()).split():
			sendSurvey(username, d.addedItems)

def saveChars():

	filename = promptSaveFile(translate('views', 'Save Characters'),
		translate('views', 'Random Game Character files (*.rgc)'),
		CHAR_DIR)
	if not filename:
		return

	jsondump(GlobalState.icwidget.dump(), checkFileExtension(filename, ".rgc"))

def loadChars():

	filename = promptLoadFile(translate('views', 'Open Characters'),
		translate('views', 'Random Game Character files (*.rgc)'),
		CHAR_DIR)
	if not filename:
		return
	try:
		obj = jsonload(filename)
		GlobalState.icwidget.load(obj)
	except Exception as e:
		showErrorMessage(translate('views', "Unable to read {0}.").format(filename))
	return

def configureDrawTimer():
	"""Allows the user to select a drawtimer value."""
	selectedButton = promptButtonSelection("How often should the GL widget (the thing with pogs and maps) refresh? Slower values may work better if you experience problems on less powerful systems. Takes effect only on program restart!", ["Much Faster", "Faster (Default)", "Medium", "Slower", "Much Slower"], 0)
	if selectedButton != -1:
		val = [13, 20, 35, 45, 60][selectedButton]
		sav = dict(drawtimer=val)
		jsonappend(sav, ospath.join(SAVE_DIR, "ui_settings.rgs"))

def configureGfx():
	"""Allows the user to change the opengl settings."""
	dialog = gfxSettingsDialog()

	def accept():
		valid = dialog.is_valid()
		if not valid:
			showErrorMessage(dialog.error)
		return valid

	if dialog.exec_(mainWindow, accept):
		settings = dialog.save()
		jsondump(settings,  ospath.join(SAVE_DIR, "gfx_settings.rgs"))

def setLanguage(new):
	jsondump(dict(language=str(new.iconText())), ospath.join(SAVE_DIR, "lang_settings.rgs"))
	#This should ideally be translated into the newly selected language, but I have no idea how to accomplish that.
	info = QMessageBox(QMessageBox.Information, "Language Changed", "".join(('Your new language setting "', str(new.iconText()), '" will take effect the next time you start RGG.')), QMessageBox.Ok)
	info.exec_()

@serverRPC
def respondUserList(list):
	for item in list:
		addUserToList(item[0], item[1])

@serverRPC
def respondUserRemove(name):
	GlobalState.uwidget.removeUser(name)

def clearUserList():
	GlobalState.uwidget.clearUserList()

@serverRPC
def respondMapCreate(ID, mapDump):
	"""Creates <s>or updates</s> the map with the given ID."""
	print("map create: " + str(ID))
	existed = GlobalState.session.getMapExists(ID)
	if existed:
		print("ignoring map create")
		return
	GlobalState.session.addDumpedMap(mapDump, ID)

@clientRPC
def sendMapCreate(user, ID, map, tileset):
	"""Creates or updates the specified map."""

	srm.processFile(user, tileset)

	respondMapCreate(allusersbut(user), ID, map)

@serverRPC
def respondTileUpdate(mapID, tile, newTileIndex):
	"""Updates the specified map tile to a new tile index."""
	map = getmap(mapID)
	if not map:
		return
	map.setTile(tile, newTileIndex)

@clientRPC
def sendTileUpdate(user, mapID, tile, newTileIndex):
	"""Updates the specified map tile to a new tile index."""
	map = getmap(mapID)
	if not map or not map.tilePosExists(tile):
		return
	respondTileUpdate(allusers(), mapID, tile, newTileIndex)

def _sendTileUpdate(mapID, tile, newTileIndex):
	map = getmap(mapID)
	oldtile = map.getTile(tile)
	sendTileUpdate(mapID, tile, newTileIndex)
	return oldtile

@serverRPC
def respondMultipleTileUpdate(mapID, topLeftTile, bottomRightTile, newTileIndex):
	"""Updates multiple specified map tiles in a rectangular area."""
	map = getmap(mapID)
	if not map:
		return
	for x in range(topLeftTile[0], bottomRightTile[0]+1):
		for y in range(topLeftTile[1], bottomRightTile[1]+1):
			map.setTile((x, y), newTileIndex)

@clientRPC
def sendMultipleTileUpdate(user, mapID, topLeftTile, bottomRightTile, newTileIndex):
	"""Updates multiple specified map tiles in a rectangular area."""
	map = getmap(mapID)
	if not map or not map.tilePosExists(topLeftTile) or not map.tilePosExists(bottomRightTile):
		return
	respondMultipleTileUpdate(allusers(), mapID, topLeftTile, bottomRightTile, newTileIndex)

def _sendMultipleTileUpdate(mapID, topLeftTile, bottomRightTile, newTileIndex):
	oldtiles = []
	map = getmap(mapID)
	for x in range(topLeftTile[0], bottomRightTile[0]+1):
		for y in range(topLeftTile[1], bottomRightTile[1]+1):
			oldtiles.append(map.getTile((x, y)))
	sendMultipleTileUpdate(mapID, topLeftTile, bottomRightTile, newTileIndex)
	return oldtiles

@serverRPC
def respondReleaseChat():
	for message in GlobalState.storedMessages:
		say(message)
	GlobalState.storedMessages = []

@clientRPC
def sendReleaseChat(user):
	respondReleaseChat(allusers())

def releaseChat():
	sendReleaseChat()

@serverRPC
def respondStoreChat(message, username):
	GlobalState.storedMessages.append(message)
	say(" ".join((username, "has stored a message.")))

@clientRPC
def sendStoreChat(user, message, username):
	respondStoreChat(allusers(), message, username)

def storeChat(message):
	sendStoreChat(translate('views', '{name}: {sayText}').format(
		name=linkedName(localuser().username),
		sayText=message), localuser().username)

@serverRPC
def respondArbitraryFile(filepath):
	"""Requests a file that another client requested the client to request. We heard you like file requests?"""
	if promptYesNo(translate('views', "".join(('Do you wish to save the binary file ', filepath, ', overwriting any existing file with that name?')))) == 16384:
		crm._request(filepath)

@clientRPC
def sendArbitraryFile(user, filepath):
	"""Sends any binary file to other users."""
	respondArbitraryFile(allusersbut(user), filepath)

def promptSendFile():
	"""Prompts user to select a file to send."""
	filename = promptLoadFile(translate('views', 'Select File'),
		translate('views', 'All files (*.*)'),
		".")
	if not filename:
		return
	sendArbitraryFile(ospath.relpath(filename))

@serverRPC
def respondCharacterSheet(data, title):
	"""Prompts user to save incoming character sheet."""
	if promptYesNo(translate('views', "".join(('Do you wish to save the character sheet ', title, ', overwriting any existing sheet with that name?')))) == 16384:
		jsondump(data, ospath.join(CHARSHEETS_DIR, title))

@clientRPC
def sendCharacterSheet(user, data, title):
	"""Sends character sheet to other users."""
	respondCharacterSheet(allusersbut(user), data, title)

def clearPogSelection():
	GlobalState.pogSelection = set()
	if GlobalState.pogHover != None:
		GlobalState.pogHover.showTooltip = False
		GlobalState.pogHover = None
	drawPogCircles()

def createPog(pog):
	"""Creates a new pog."""
	pog.ID = GlobalState.session._findUniquePogID(pog.src)
	GlobalState.session.addPog(pog)
	sendUpdatePog(pog.ID, pog.dump())

def modifyPog(pog):
	assert(pog.ID)
	sendUpdatePog(pog.ID, pog.dump())

def deletePog(pog):
	assert(pog.ID)
	sendDeletePog(pog.ID)

@serverRPC
def respondDeleteAllPogs():
	_deleteAllPogs()

@clientRPC
def sendDeleteAllPogs(user):
	respondDeleteAllPogs(allusersbut(user))

def _deleteAllPogs():
	clearPogSelection()
	GlobalState.session.removeAllPogs()

def deleteAllPogs():
	_deleteAllPogs()
	sendDeleteAllPogs()

def placePog(x, y, pogpath):
	"""Places a pog on the map."""
	infograb = QPixmap(pogpath)
	mapPosition = getMapPosition((x, y))
	assert ospath.exists(pogpath)
	assert POG_DIR in pogpath
	pog = Pog(
		mapPosition,
		(infograb.width(), infograb.height()),
		(infograb.width(), infograb.height()),
		200,
		pogpath,
		0,
		0,
		{},
		0,
		infograb.hasAlpha())
	createPog(pog)

def movePogs(displacement):
	"""Moves pogs by a specified displacement."""
	if GlobalState.moveMode != "free" and not isGM():
		selection = set()
		for pog in GlobalState.pogSelection:
			if pog.ID in GlobalState.moveablePogs:
				selection.add(pog)
		if not selection: return
	else:
		selection = GlobalState.pogSelection.copy()
	pogids = []
	poglocs = []
	for pog in selection:
		pog.displace(displacement)
		pogids.append(pog.ID)
		poglocs.append(pog.position)
	sendAbsoluteMovementPog(pogids, poglocs)
	drawPogCircles()

def movePogsAbsolute(newPosition):
	selection = GlobalState.pogSelection.copy()
	pogids = []
	poglocs = []
	for pog in selection:
		pog.move(newPosition)
		pogids.append(pog.ID)
		poglocs.append(pog.position)
	sendAbsoluteMovementPog(pogids, poglocs)
	drawPogCircles()

@serverRPC
def respondUpdatePog(pogID, pogDump):
	"""Creates or updates a pog on the client."""
	pog = Pog.load(pogDump)
	pog.ID = pogID
	if pogID in list(GlobalState.session.pogs.keys()):
		old = GlobalState.session.pogs[pogID]
		if old in GlobalState.pogSelection:
			GlobalState.pogSelection.discard(old)
			addPogSelection(pog)
		if old == GlobalState.pogHover:
			GlobalState.pogHover.showTooltip = False
			GlobalState.pogHover = None
		old.destroy()
	GlobalState.session.addPog(pog)
	drawPogCircles()

@clientRPC
def sendUpdatePog(user, pogID, pogDump):
	"""Creates or updates a pog on the server."""

	# Upload (or check that we already have) the image resource from the client
	srm.processFile(user, pogDump['src'])
	respondUpdatePog(allusersbut(user), pogID, pogDump)

@serverRPC
def respondDeletePog(pogID):
	"""Deletes a pog on the client."""
	if pogID in list(GlobalState.session.pogs.keys()):
		old = GlobalState.session.pogs[pogID]
		if old in GlobalState.pogSelection:
			GlobalState.pogSelection.discard(old)
		if old == GlobalState.pogHover:
			GlobalState.pogHover.showTooltip = False
			GlobalState.pogHover = None
		GlobalState.session.removePog(old)
	if GlobalState.cameraPog and GlobalState.cameraPog.ID == pogID:
		GlobalState.cameraPog = None
	drawPogCircles()

@clientRPC
def sendDeletePog(user, pogID):
	"""Deletes a pog on the server."""
	# HACK: Relies on the fact that responses are locally synchronous
	respondDeletePog(allusers(), pogID)

@serverRPC
def respondMovementPog(pogids, displacement):
	"""Creates or updates a pog on the client."""
	for pogID in pogids:
		if pogID in list(GlobalState.session.pogs.keys()):
			pog = GlobalState.session.pogs[pogID]
			pog.displace(displacement)
	if GlobalState.cameraPog:
		centerOnPog(GlobalState.cameraPog)
	drawPogCircles()

@clientRPC
def sendMovementPog(user, pogids, displacement):
	"""Creates or updates a pog on the server."""
	centerOnPog(GlobalState.cameraPog)
	respondMovementPog(allusersbut(user), pogids, displacement)

@serverRPC
def respondAbsoluteMovementPog(pogids, newloc):
	for i, pogID in enumerate(pogids):
		if pogID in list(GlobalState.session.pogs.keys()):
			pog = GlobalState.session.pogs[pogID]
			pog.move(newloc[i])
	if GlobalState.cameraPog:
		centerOnPog(GlobalState.cameraPog)
	drawPogCircles()

@clientRPC
def sendAbsoluteMovementPog(user, pogids, newloc):
	centerOnPog(GlobalState.cameraPog)
	respondAbsoluteMovementPog(allusersbut(user), pogids, newloc)

@serverRPC
def respondHidePog(pogID, hidden):
	"""Hides or shows a pog on the client."""
	if pogID in list(GlobalState.session.pogs.keys()):
		pog = GlobalState.session.pogs[pogID]
		if hidden:
			pog.hide()
		else:
			pog.show()
	drawPogCircles()

@clientRPC
def sendHidePog(user, pogID, hidden):
	"""Hides or shows a pog on the server."""
	respondHidePog(allusers(), pogID, hidden)

@serverRPC
def respondPogAttributes(pogID, name, layer, properties):
	'''Sends various attributes of a pog over the wire.'''
	if pogID in list(GlobalState.session.pogs.keys()):
		pog = GlobalState.session.pogs[pogID]
		if not pog: return
		pog.name = name
		pog.layer = layer
		pog.properties = properties
		pogUpdateEvent(pog)

@clientRPC
def sendPogAttributes(user, pogID, name, layer, properties):
	'''Sends various attributes of a pog over the wire.'''
	pogUpdateEvent(GlobalState.session.pogs[pogID])
	respondPogAttributes(allusersbut(user), pogID, name, layer, properties)

@serverRPC
def respondLockPog(pogID, locked):
	"""Locks or unlocks a pog on the client."""
	if pogID in list(GlobalState.session.pogs.keys()):
		pog = GlobalState.session.pogs[pogID]
		pog._locked = locked

@clientRPC
def sendLockPog(user, pogID, locked):
	"""Locks or unlocks a pog on the server."""
	respondLockPog(allusers(), pogID, locked)

@serverRPC
def respondPogRotation(pogID, newRotation):
	if pogID in list(GlobalState.session.pogs.keys()):
		pog = GlobalState.session.pogs[pogID]
		pog.setRotation(newRotation)

@clientRPC
def sendPogRotation(user, pogID, newRotation):
	respondPogRotation(allusers(), pogID, newRotation)

@serverRPC
def respondResizePog(pogID, newW, newH):
	if pogID in list(GlobalState.session.pogs.keys()):
		pog = GlobalState.session.pogs[pogID]
		pog.size = (newW, newH)

@clientRPC
def sendResizePog(user, pogID, newW, newH):
	respondResizePog(allusersbut(user), pogID, newW, newH)

def duplicatePog(pog):
	createPog(Pog.load(pog.dump()))

# DRAWING

@serverRPC
def respondLine(x, y, w, h, thickness, r, g, b):
	drawLine(x, y, w, h, thickness, r, g, b)
	GlobalState.session.addLine((float(x), float(y), float(w), float(h), thickness, float(r), float(g), float(b)))

@clientRPC
def sendLine(user, x, y, w, h, thickness, r, g, b):
	respondLine(allusers(), x, y, w, h, thickness, r, g, b)

@serverRPC
def respondSegmentedLine(x, y, w, h, thickness, r, g, b):
	lines = drawSegmentedLine(x, y, w, h, thickness, r, g, b)
	for line in lines:
		GlobalState.session.addLine(line)

@clientRPC
def sendSegmentedLine(user, x, y, w, h, thickness, r, g, b):
	respondSegmentedLine(allusers(), x, y, w, h, thickness, r, g, b)

@serverRPC
def respondCircle(centre, edge, colour, thickness):
	lines = drawCircle(centre, edge, colour, thickness)
	for line in lines:
		GlobalState.session.addLine(line)

@clientRPC
def sendCircle(user, centre, edge, colour, thickness):
	respondCircle(allusers(), centre, edge, colour, thickness)

@serverRPC
def respondRectangle(x, y, w, h, colour, thickness):
	lines = drawRectangleMadeOfLines(x, y, w, h, colour, thickness)
	for line in lines:
		GlobalState.session.addLine(line)

@clientRPC
def sendRectangle(user, x, y, w, h, colour, thickness):
	respondRectangle(allusers(), x, y, w, h, colour, thickness)

@serverRPC
def respondPolygon(sides, centre, edge, colour, thickness):
	lines = drawRegularPolygon(sides, centre, edge, colour, thickness)
	for line in lines:
		GlobalState.session.addLine(line)

@clientRPC
def sendPolygon(user, sides, centre, edge, colour, thickness):
	respondPolygon(allusers(), sides, centre, edge, colour, thickness)

@serverRPC
def respondDeleteLine(x, y, w, h):
	getSession().deleteLine(x, y, w, h)
	deleteLine(x, y, w, h)

@clientRPC
def sendDeleteLine(user, x, y, w, h):
	respondDeleteLine(allusers(), x, y, w, h)

def _setThickness(new):
	GlobalState.thickness = new

def setThickness(new):
	_setThickness(int(new.text()))

def _setLineColour(new):
	GlobalState.linecolour = [new[0], new[1], new[2]]

def setLineColour(menuselection):
	if menuselection.text() == "Custom...":
		result = QColorDialog.getColor(Qt.white, mainWindow)
		_setLineColour((result.redF(), result.greenF(), result.blueF()))
	else:
		_setLineColour(COLOURS[str(menuselection.text())])

def clearLines():
	clearLines()

# DICE

def rollDice(dice, private=False):
	"""Rolls the specified dice."""
	if not isRollValid(dice):
		say(translate('views', "Invalid dice roll. See /roll documentation for help."))
	else:
		try:
			from . import rggRemote
		except ImportError:
			import rggRemote
		text = translate('views', "{name} rolls {roll}").format(
			name=linkedName(localuser().username),
			roll=roll(dice))
		if private:
			say(text)
			ICSay(text)
		else:
			rggRemote.sendDice(text)
		#c.sendNetMessageToAll(text)

def addMacro():
	"""Creates a new dice macro."""
	dice = promptString(translate('views', "What dice should be rolled?"))
	if dice is None:
		return
	if isRollValid(dice):
		name = promptString(translate('views', "What should the macro be called?"))
		if name is None:
			return
		GlobalState.dwidget.addMacro(dice, name)
	else:
		say(translate('views', 'Malformed dice macro. Formatting help is available in "/roll" command.'))

# GENERATION

def generateName(generator, args):
	"""Generates a random name of the specified type."""
	from libraries.rggNameGen import getName
	say(getName(generator, args))

# MISC

@serverRPC
def respondCenterOnPog(pogID):
	if pogID in list(GlobalState.session.pogs.keys()):
		pog = GlobalState.session.pogs[pogID]
		centerOnPog(pog)

@clientRPC
def sendCenterOnPog(user, pogID):
	respondCenterOnPog(allusers(), pogID)

def centerOnPog(pog):
	"""Center the camera on a pog."""
	if not pog: return
	camsiz = cameraSize()
	camzoom = getZoom()
	pospog = pog.position
	cammod = [(-camsiz[0]/2)+pog._tile.getW()/2, (-camsiz[1]/2)+pog._tile.getH()/2]
	newpos = (-(pospog[0]*camzoom + cammod[0]), -(pospog[1]*camzoom + cammod[1]))
	setCameraPosition(newpos)

def reportCamera():
	"""Reports the current camera coordinates."""
	say(translate('views', 'x: {0}\ny: {1}', 'formats camera reporting.').format(*cameraPosition()))

def renamePog(pog, name):
	pog.name = name
	sendPogAttributes(pog.ID, pog.name, pog.layer, pog.properties)

def purgeEmptyImages():
	"""Deletes all empty files in the pog, portrait, and tileset folders."""
	for dir in (POG_DIR, PORTRAIT_DIR, TILESET_DIR):
		purgeEmptyFiles(dir)

def processPogRightclick(selection, pogs):
	#0 CENTER
	#1 SET NAME
	#2 GEN NAME
	#3 SET LAYER
	#4 SET PROPERTY
	#5 RESIZE
	#6 HIDE
	#7 LOCK
	#8 DELETE
	#9 LOCK CAMERA
	#10 DUPLICATE
	#11 ROTATE
	#12 CENTER EVERYONE
	#13 SET MOVEABLE

	mainpog = pogs[0]

	if selection == 0:
		centerOnPog(mainpog)
	elif selection == 1:
		name = promptString(translate('views', "Enter a name for this pog."), inittext = mainpog.name)
		if name is None:
			return
		for pog in pogs:
			renamePog(pog, name)
	elif selection == 2:
		prompt = translate('views', "Enter a generator command. See /generate for syntax. Multi-pog compatible.")
		gentype = promptString(prompt)
		if gentype is None:
			return
		gentype = splitword(gentype.lower())
		from libraries.rggNameGen import getName
		for pog in pogs:
			renamePog(pog, getName(*gentype))
	elif selection == 3:
		prompt = translate('views', "Enter a layer. Pogs on higher layers are displayed over those on lower layers. Should be a positive integer. Multi-pog compatible.")
		newlayer = promptInteger(prompt, min=-150, max=800, default=(mainpog.layer-200))
		if newlayer is None:
			return
		for pog in pogs:
			pog.layer = newlayer+200
			sendPogAttributes(pog.ID, pog.name, pog.layer, pog.properties)
	elif selection == 4:
		d = modifyPogAttributesDialog(mainpog.properties, mainWindow)
		if d.exec_():
			for pog in pogs:
				pog.setProperties(d.currentProperties)
				sendPogAttributes(pog.ID, pog.name, pog.layer, pog.properties)
	elif selection == 5:
		d = resizeDialog(mainpog._tile.getW(), mainpog._tile.getH(), mainpog.size[0], mainpog.size[1], mainWindow)
		if d.exec_():
			for pog in pogs:
				pog.size = (d.wBox.value(), d.hBox.value())
				sendResizePog(pog.ID, d.wBox.value(), d.hBox.value())
				drawPogCircles()
	elif selection == 6:
		for pog in pogs:
			if pog.hidden:
				pog.show()
			else:
				pog.hide()
			sendHidePog(pog.ID, pog.hidden)
			clearPogSelection()
			drawPogCircles()
	elif selection == 7:
		for pog in pogs:
			pog._locked = not pog._locked
			sendLockPog(pog.ID, pog._locked)
	elif selection == 8:
		for pog in pogs:
			deletePog(pog)
	elif selection == 9:
		if GlobalState.cameraPog and GlobalState.cameraPog == mainpog:
			GlobalState.cameraPog = None
		else:
			GlobalState.cameraPog = mainpog
			centerOnPog(mainpog)
	elif selection == 10:
		for pog in pogs:
			duplicatePog(pog)
	elif selection == 11:
		rotation = promptInteger("Enter a rotation angle.", min=0, max=359, default=0)
		if rotation is None: return
		for pog in pogs:
			sendPogRotation(pog.ID, rotation)
	elif selection == 12:
		sendCenterOnPog(mainpog.ID)
	elif selection == 13:
		username = promptString(translate('views', "Enter the name of the user who may move this pog (must be exact)."), inittext = "username")
		if username is None:
			return
		for pog in pogs:
			sendAddMoveablePog(username, pog.ID)

def pogActionList(pog):
	if pog.hidden: hidebutton = "Show"
	else: hidebutton = "Hide"
	if pog._locked: lockbutton = "Unlock"
	else: lockbutton = "Lock"
	if GlobalState.cameraPog and GlobalState.cameraPog == pog: followbutton = "Unlock Camera"
	else: followbutton = "Lock Camera to Pog"
	options = [translate('views', 'Center on pog'),
			translate('views', 'Set name'),
			translate('views', 'Generate name'),
			translate('views', 'Set layer'),
			translate('views', 'Add/edit property'),
			translate('views', 'Resize'),
			translate('views', hidebutton),
			translate('views', lockbutton),
			translate('views', 'Delete'),
			translate('views', followbutton),
			translate('views', 'Duplicate'),
			translate('views', 'Rotate'),
			translate('views', 'Center Everyone')]
	if isGM(): options.append(translate('views', 'Set as moveable for player'))
	return options

# MOUSE ACTIONS

def mouseDrag(screenPosition, mapPosition, displacement):
	if GlobalState.pogSelection and GlobalState.mouseButton == BUTTON_LEFT:
		if not GlobalState.gridMode:
			movePogs(displacement)
		else:
			try:
				movePogsAbsolute(GlobalState.session.findTopMap(mapPosition).nearestGridPoint(mapPosition))
			except:
				movePogs(displacement)
		return
	elif GlobalState.mouseButton == BUTTON_LEFT:
		setCameraPosition(list(map(lambda c, d,  z: c + d*z, cameraPosition(), displacement, (getZoom(), getZoom()))))
		return
	if GlobalState.mouseButton == BUTTON_RIGHT:
		setCameraPosition(list(map(lambda c, d,  z: c + d*z, cameraPosition(), displacement, (getZoom(), getZoom()))))

def mouseMove(screenPosition, mapPosition, displacement):
	icon = GlobalState.menu.selectedIcon
	if icon == ICON_MOVE: # moveIcon
		if GlobalState.mouseButton == BUTTON_LEFT:
			setCameraPosition(list(map(lambda c, d,  z: c + d*z, cameraPosition(), displacement, (getZoom(), getZoom()))))
	if icon == ICON_SELECT: #selectIcon
		if GlobalState.mouseButton is None:
			tooltipPog = GlobalState.session.findTopPog(mapPosition)
			if GlobalState.pogHover == tooltipPog:
				return
			elif GlobalState.pogHover != None:
				GlobalState.pogHover.showTooltip = False
			GlobalState.pogHover = tooltipPog
			if tooltipPog is None:
				return

			tooltipPog.showTooltip = True
		elif GlobalState.mouseButton == BUTTON_LEFT:
			return mouseDrag(screenPosition, mapPosition, displacement)
		elif GlobalState.mouseButton == BUTTON_RIGHT:
			return mouseDrag(screenPosition, mapPosition, displacement)
	elif icon == ICON_DRAW: #drawIcon
		if GlobalState.mouseButton == BUTTON_LEFT:
			if GlobalState.drawmode == "Freehand":
				if GlobalState.previousLinePlacement != None:
					sendLine(GlobalState.previousLinePlacement[0], GlobalState.previousLinePlacement[1], mapPosition[0], mapPosition[1], GlobalState.thickness, GlobalState.linecolour[0], GlobalState.linecolour[1], GlobalState.linecolour[2])
				GlobalState.previousLinePlacement = mapPosition
			elif GlobalState.drawmode == "Rectangle":
				clearPreviewLines()
				if GlobalState.previousLinePlacement != None:
					drawRectangleMadeOfLines(GlobalState.previousLinePlacement[0], GlobalState.previousLinePlacement[1], mapPosition[0], mapPosition[1], GlobalState.linecolour, GlobalState.thickness, True)
			elif GlobalState.drawmode == "Circle":
				clearPreviewLines()
				drawCircle(GlobalState.previousLinePlacement, mapPosition, GlobalState.linecolour, GlobalState.thickness, True)
			elif GlobalState.drawmode == "Line":
				clearPreviewLines()
				drawSegmentedLine(GlobalState.previousLinePlacement[0], GlobalState.previousLinePlacement[1], mapPosition[0], mapPosition[1], GlobalState.thickness, GlobalState.linecolour[0], GlobalState.linecolour[1], GlobalState.linecolour[2], True)
			elif GlobalState.drawmode == "Pentagram" or GlobalState.drawmode == "Hexagram":
				if GlobalState.previousLinePlacement != None:
					clearPreviewLines()
					displacement = max(abs(mapPosition[0]-GlobalState.previousLinePlacement[0]), abs(mapPosition[1]-GlobalState.previousLinePlacement[1]))
					drawRegularPolygon(14-len(GlobalState.drawmode), GlobalState.previousLinePlacement, displacement, GlobalState.linecolour, GlobalState.thickness, False, True)
		elif GlobalState.mouseButton == BUTTON_RIGHT:
			return mouseDrag(screenPosition, mapPosition, displacement)
	elif icon == ICON_DELETE: #deleteIcon
		if GlobalState.mouseButton == BUTTON_LEFT:
			if GlobalState.previousLinePlacement != None:
				clearRectangles()
				GlobalState.nextLinePlacement = mapPosition #this is bottomRight of the square that we want to delete.
				drawRectangle(GlobalState.previousLinePlacement[0], GlobalState.previousLinePlacement[1],
									  GlobalState.nextLinePlacement[0], GlobalState.nextLinePlacement[1], 0.8, 0.8, 1.0)
			else:
				clearRectangles()
				GlobalState.previousLinePlacement = mapPosition #We only do this so that we have a topLeft

def mousePress(screenPosition, mapPosition, button):
	icon = GlobalState.menu.selectedIcon
	if icon == ICON_MOVE:
		return
	if icon == ICON_SELECT:
		if button == BUTTON_LEFT + BUTTON_SHIFT:
			if GlobalState.pogPlacement:
				infograb = QPixmap(GlobalState.pogPath)
				pog = Pog(
					mapPosition,
					(infograb.width(), infograb.height()),
					(infograb.width(), infograb.height()),
					200,
					GlobalState.pogPath,
					0,
					0,
					{},
					infograb.hasAlpha())
				createPog(pog)
				return
			pog = GlobalState.session.findTopPog(mapPosition)
			if not pog:
				return
			if pog in GlobalState.pogSelection:
				removePogSelection(pog)
			else:
				addPogSelection(pog)
			pogSelectionChangedEvent()
		elif button == BUTTON_RIGHT and GlobalState.rightclickmode:
			pog = GlobalState.session.findTopPog(mapPosition)
			if pog is not None:
				if pog not in GlobalState.pogSelection:
					setPogSelection(pog)
				GlobalState.mouseButton = None
				selected = showPopupMenuAt((screenPosition[0]+25, screenPosition[1]), pogActionList(pog))
				processPogRightclick(selected, list(set([pog] + list(GlobalState.pogSelection))))
		elif button == BUTTON_LEFT + BUTTON_CONTROL:
			pog = GlobalState.session.findTopPog(mapPosition)
			if pog is not None:
				GlobalState.pogSelectionCandidate = set()
				GlobalState.pogSelectionCandidate.add(pog)
		elif button == BUTTON_LEFT:
			if GlobalState.pogPlacement:
				GlobalState.pogPlacement = False
				infograb = QPixmap(GlobalState.pogPath)
				pog = Pog(
					mapPosition,
					(infograb.width(), infograb.height()),
					(infograb.width(), infograb.height()),
					200,
					GlobalState.pogPath,
					0,
					0,
					{},
					infograb.hasAlpha())
				createPog(pog)
				return
			pog = GlobalState.session.findTopPog(mapPosition)
			if not pog:
				clearPogSelection()
				return
			if pog not in GlobalState.pogSelection:
				setPogSelection(pog)
			pogSelectionChangedEvent()
	elif icon == ICON_DRAW:
		if button == BUTTON_LEFT:
			GlobalState.previousLinePlacement = mapPosition
		elif button == BUTTON_LEFT + BUTTON_CONTROL:
			modes = ['Freehand', 'Line', 'Circle', 'Rectangle', 'Pentagram', 'Hexagram']
			selected = showPopupMenuAt((screenPosition[0]+25, screenPosition[1]), modes)
			GlobalState.drawmode = modes[selected]
	elif icon == ICON_DELETE:
		if button == BUTTON_LEFT:
			GlobalState.previousLinePlacement = mapPosition


def mouseRelease(screenPosition, mapPosition, button):
	GlobalState.mouseButton = None

	icon = GlobalState.menu.selectedIcon
	if icon == ICON_SELECT:
		if button == BUTTON_LEFT + BUTTON_CONTROL:
			if len(GlobalState.pogSelectionCandidate) > 0:
				pog = GlobalState.session.findTopPog(mapPosition)
				if pog is not None and pog in GlobalState.pogSelectionCandidate:
					if pog not in GlobalState.pogSelection:
						setPogSelection(pog)
					GlobalState.mouseButton = None
					selected = showPopupMenuAt((screenPosition[0]+25, screenPosition[1]), pogActionList(pog))
					processPogRightclick(selected, list(set([pog] + list(GlobalState.pogSelection))))
	elif icon == ICON_DRAW:
		clearPreviewLines()
		if GlobalState.drawmode == "Rectangle":
			if GlobalState.previousLinePlacement != None:
				sendRectangle(GlobalState.previousLinePlacement[0], GlobalState.previousLinePlacement[1], mapPosition[0], mapPosition[1], GlobalState.linecolour, GlobalState.thickness)
		elif GlobalState.drawmode == "Circle":
			sendCircle(GlobalState.previousLinePlacement, mapPosition, GlobalState.linecolour, GlobalState.thickness)
		elif GlobalState.drawmode == "Line":
			sendSegmentedLine(GlobalState.previousLinePlacement[0], GlobalState.previousLinePlacement[1], mapPosition[0], mapPosition[1], GlobalState.thickness, GlobalState.linecolour[0], GlobalState.linecolour[1], GlobalState.linecolour[2])
		elif GlobalState.drawmode == "Pentagram" or GlobalState.drawmode == "Hexagram":
			if GlobalState.previousLinePlacement != None:
				displacement = max(abs(mapPosition[0]-GlobalState.previousLinePlacement[0]), abs(mapPosition[1]-GlobalState.previousLinePlacement[1]))
				sendPolygon(14-len(GlobalState.drawmode), GlobalState.previousLinePlacement, displacement, GlobalState.linecolour, GlobalState.thickness)
		GlobalState.previousLinePlacement = None
	elif icon == ICON_DELETE:
		if(GlobalState.previousLinePlacement != None and GlobalState.nextLinePlacement != None):

			clearRectangles()

			x = GlobalState.previousLinePlacement[0]
			y = GlobalState.previousLinePlacement[1]
			w = GlobalState.nextLinePlacement[0]
			h = GlobalState.nextLinePlacement[1]
			if(x > w):
				x, w = w, x
			if(y > h):
				y, h = h, y

			w -= x
			h -= y
			#print '(x, y, w, h) (' + str(x) + ', ' + str(y) + ', ' + str(w) + ', ' + str(h) + ')'

			sendDeleteLine(x, y, w, h)

			GlobalState.nextLinePlacement = mapPosition

def mouseMoveResponse(x, y):
	#print 'move', x, y

	screenPosition = (x, y)
	mapPosition = getMapPosition(screenPosition)
	displacement = list(map(lambda p,m,d: p/d - m/d, screenPosition, GlobalState.mousePosition,  (getZoom(), getZoom())))

	#print mapPosition
	#print cameraPosition()

	mouseMove(screenPosition, mapPosition, displacement)

	GlobalState.mousePosition = screenPosition

def mousePressResponse(x, y, t):
	#print 'press', x, y, t

	screenPosition = (x, y)
	mapPosition = getMapPosition(screenPosition)

	GlobalState.mousePosition = screenPosition
	GlobalState.mouseButton = t

	mousePress(screenPosition, mapPosition, t)

def mouseReleaseResponse(x, y, t):
	#print 'release', x, y, t

	screenPosition = (x, y)
	mapPosition = getMapPosition(screenPosition)

	GlobalState.mousePosition = screenPosition
	GlobalState.mouseButton = t

	mouseRelease(screenPosition, mapPosition, t)

def keyPressResponse(k):
	if k == Qt.Key_Delete:
		for pog in list(GlobalState.pogSelection):
			deletePog(pog)
	if not GlobalState.cameraPog: return
	setPogSelection(GlobalState.cameraPog)
	if k == Qt.Key_W:
		GlobalState.pogmove[1] = -5
	elif k == Qt.Key_S:
		GlobalState.pogmove[1] = 5
	elif k == Qt.Key_A:
		GlobalState.pogmove[0] = -5
	elif k == Qt.Key_D:
		GlobalState.pogmove[0] = 5

def keyReleaseResponse(k):
	if not GlobalState.cameraPog: return
	if k == Qt.Key_W or k == Qt.Key_S:
		GlobalState.pogmove[1] = 0
	elif k == Qt.Key_A or k == Qt.Key_D:
		GlobalState.pogmove[0] = 0
