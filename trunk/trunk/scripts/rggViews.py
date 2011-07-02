'''
rggViews - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Actions which occur in response to user commands.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''
import time, random, os, base64
import rggNameGen, rggDice, rggMap, rggTile, rggPog, rggDockWidget, rggDialogs, rggMenuBar, rggResource, rggSystem, rggSession
from rggRPC import server, client, serverRPC, clientRPC
from rggJson import jsondump, jsonload
from rggMenuBar import ICON_SELECT, ICON_MOVE, ICON_DRAW, ICON_DELETE
from rggSystem import *
from rggDialogs import *
from PyQt4 import QtCore, QtGui

# Button enum
BUTTON_LEFT = 0
BUTTON_MIDDLE = 1
BUTTON_RIGHT = 2
BUTTON_CONTROL = 3
BUTTON_SHIFT = 6

# Feel free to add fields to the user object
class User(object):
    """User representation on the server."""
    
    def __init__(self, username):
        self.username = username
    
    def __repr__(self):
        return u"User(u'{name}')".format(name=self.username)
    
    def __unicode__(self):
        return self.username
    
    def __str__(self):
        return self.__unicode__()

class _state(object):
    """A state class build to avoid all these global statements."""
    
    session = rggSession.Session()
    
    alert = True
    
    pogSelection = set()
    pogHover = None
    
    mouseButton = None
    mousePosition = (0, 0)
    
    pogPlacement = False
    pogPath = "path"

    previousLinePlacement = None #(0, 0) expected
    nextLinePlacement = None

    thickness = 1
    linecolour = [1.0, 1.0, 1.0]
    
    @staticmethod
    def initialize(mainApp):
        _state.menu = rggMenuBar.menuBar()
        
        _state.dwidget = rggDockWidget.diceRoller(mainWindow)
        _state.pwidget = rggDockWidget.pogPalette(mainWindow)
        _state.cwidget = rggDockWidget.chatWidget(mainWindow)
        _state.icwidget = rggDockWidget.ICChatWidget(mainWindow)
        _state.uwidget = rggDockWidget.userListWidget(mainWindow)
        _state.users = {}
        _state.localuser = User(client.username)
        _state.users[client.username] = _state.localuser
        
        _state.App = mainApp
        
def drawPogCircles():
    clearSelectionCircles()
    for pog in _state.pogSelection:
        drawSelectionCircle(*pog.getSelectionCircleData())

def addPogSelection(pog):
    _state.pogSelection.add(pog)
    drawPogCircles()

def removePogSelection(pog):
    _state.pogSelection.remove(pog)
    drawPogCircles()
    
def setPogSelection(pog):
    _state.pogSelection = set()
    addPogSelection(pog)
    
def addUserToList(name, host=False):
    _state.uwidget.addUser(name, host)
    
def toggleAlerts(newValue=None):
    """Toggles messages containing the user's handle causing an alert."""
    if newValue is None:
        _state.alert = not _state.alert
    else:
        _state.alert = newValue

# MESSAGES

def say(message):
    """Say an IC message. This documentation is a lie."""
    if _state.alert and localhandle().lower() in message.lower():
        _state.App.alert(mainWindow)
    _state.cwidget.insertMessage(message)

def announce(message):
    """Say an OOC message. This documentation is a lie."""
    _state.cwidget.insertMessage(message)
    
def ICSay(message):
    _state.icwidget.insertMessage(message)

def linkedName(name):
    return translate('views', '<a href="/tell {name}" title="{name}">{name}</a>').format(name=name)

# NETWORK (Server only)

def allusers():
    """Get a list of all users."""
    return _state.users.values()

def allusersbut(usernameOrUser):
    user = getuser(usernameOrUser)
    if not user:
        raise RuntimeError("No user named {user}.".format(user=idOrNameOrUser))
    all = allusers()
    assert(user in all)
    all.remove(user)
    return all

def getuser(username):
    """Returns a user given a username, or None if not valid."""
    if isinstance(username, User):
        assert(username in allusers())
        return username
    username = unicode(username)
    #print server.userExists(username), server.users
    if server.userExists(username):
        username = server.fullname(username)
        assert(username in _state.users)
        return _state.users[username]
    return None

def usernames():
    """Returns all the usernames."""
    return _state.users.keys()

def getNetUserList():
    """Returns the user names formatted for transfer over net."""
    return _state.uwidget.getUsers()

# TODO: Name changing needs to be synched across the wire
# The workaround is to log out and back in.
#def changeName(user, name):
#    assert(name not in _state.usernames)
#    if user.unnamed:
#        user.unnamed = False
#    if user.username in _state.usernames:
#        del _state.usernames[user.username]
#    _state.usernames[name] = user
#    user.username = name

def localuser():
    """The user for the local player."""
    return _state.localuser

def localhandle():
    return localuser().username

def adduser(user):
    """Add a user to the list locally."""
    #print "ADD", user.username
    assert(user.username not in _state.users)
    _state.users[user.username] = user
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
    assert(username in _state.users)
    user = _state.users[username]
    del _state.users[username]
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
        renameuser(localhandle(), connection.username)
        if client.host(connection.port):
            say(translate('views', 'Now listening on port {port}.').format(port=connection.port))
            addUserToList(localhandle(), True)
        else:
            #TODO: better error message here
            say(translate('views', 'Unable to access network; perhaps the port is in use?'))
        

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
        connection = dialog.save()
        renameuser(localhandle(), connection.username)
        client.join(connection.host, connection.port)
        say(translate('views', 'Connecting to {host}:{port}...').format(host=connection.host, port=connection.port))

def killConnection():
    """Kills the connection without reporting anything."""
    client.close()
    assert(localhandle() in usernames())
    assert(localuser() == getuser(localhandle()))
    users = {localhandle(): localuser()}
    clearUserList()
    #print "KILL"

def disconnectGame():
    """Allows the user to disconnect from the internet."""
    if not client.isConnected:
        say(translate('views', "You are not connected."))
        return
    
    killConnection()
    say(translate('views', "Disconnected."))
    clearUserList()
    
def getSession():
    return _state.session

# MAPS
def topmap(mapPosition):
    return _state.session.findTopMap(mapPosition)

def getmap(mapID):
    return _state.session.getMap(mapID)

def allmaps():
    return _state.session.maps.items()

def getAllMaps():
    return _state.session.maps.values()

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
    _state.session.closeAllMaps()
    
def closeAllMaps():
    _closeAllMaps()
    sendCloseAllMaps()

def internalAddMap(map):
    _state.session.addMap(map)
    sendMapCreate(map.ID, map.dump(), map.tileset)
    
@serverRPC
def respondSession(sess):
    _state.session = rggSession.Session.load(sess)
    
@clientRPC
def sendSession(user):
    respondSession(allusersbut(user), _state.session.dump())

def newMap():
    """Allows the user to choose a new map."""
    dialog = newMapDialog()
    
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
        rggSystem.MAP_DIR)
    if not filename:
        return
    try:
        obj = jsonload(filename)
        map = rggMap.Map.load(obj, True)
        internalAddMap(map)
    except Exception as e:
        showErrorMessage(translate('views', "Unable to read {0}.").format(filename))
        print e

def saveMap():
    """Allows the user to save a map."""
    mapNames = []
    mapIDs = []
    
    for ID, map in _state.session.maps.items():
        mapNames.append(map.mapname)
        mapIDs.append(ID)

    selectedButton = rggSystem.promptButtonSelection("Which map do you want to save?", mapNames, 0)
    map = _state.session.maps[mapIDs[selectedButton]]
    
    filename = promptSaveFile(translate('views', 'Save Map'),
        translate('views', 'Random Game Map files (*.rgm)'),
        rggSystem.MAP_DIR)
    if not filename:
        return
    
    jsondump(map.dump(), filename)
    
def loadSession():
    """Allows the user to load a new map."""
    filename = promptLoadFile(translate('views', 'Open Game Session'),
        translate('views', 'Random Game files (*.rgg)'),
        rggSystem.MAP_DIR)
    if not filename:
        return
    try:
        obj = jsonload(filename)
        sess = rggSession.Session.load(obj)
        _state.session = sess
        sendSession()
    except Exception as e:
        showErrorMessage(translate('views', "Unable to read {0}.").format(filename))
        print e

def saveSession():
    filename = promptSaveFile(translate('views', 'Save Game Session'),
        translate('views', 'Random Game files (*.rgg)'),
        rggSystem.MAP_DIR)
    if not filename:
        return
    
    jsondump(_state.session.dump(), filename)

def saveChars():
    
    filename = promptSaveFile(translate('views', 'Save Characters'),
        translate('views', 'Random Game Character files (*.rgc)'),
        rggSystem.CHAR_DIR)
    if not filename:
        return
    
    jsondump(_state.icwidget.dump(), filename)
    
def loadChars():
    
    filename = promptLoadFile(translate('views', 'Open Characters'),
        translate('views', 'Random Game Character files (*.rgc)'),
        rggSystem.CHAR_DIR)
    if not filename:
        return
    try:
        obj = jsonload(filename)
        _state.icwidget.load(obj)
    except Exception as e:
        showErrorMessage(translate('views', "Unable to read {0}.").format(filename))
	print e
        return

def configureGfx():
    """Allows the user to the opengl settings."""
    dialog = gfxSettingsDialog()
    
    def accept():
        valid = dialog.is_valid()
        if not valid:
            showErrorMessage(dialog.error)
        return valid
    
    if dialog.exec_(mainWindow, accept):
        settings = dialog.save()
        jsondump(settings,  os.path.join(SAVE_DIR, "gfx_settings.rgs"))
    
@serverRPC
def respondUserList(list):
    for item in list:
        addUserToList(item[0], item[1])
        
@serverRPC
def respondUserRemove(name):
    _state.uwidget.removeUser(name)
    
def clearUserList():
    _state.uwidget.clearUserList()

@serverRPC
def respondMapCreate(ID, mapDump):
    """Creates <s>or updates</s> the map with the given ID."""
    print "map create: " + str(ID)
    existed = _state.session.getMapExists(ID)
    if existed:
        print "ignoring map create"
        return
    _state.session.addDumpedMap(mapDump, ID)

@clientRPC
def sendMapCreate(user, ID, map, tileset):
    """Creates or updates the specified map."""
    
    rggResource.srm.processFile(user, tileset)

    respondMapCreate(allusersbut(user), ID, map)

@serverRPC
def respondTileUpdate(mapID, tile, newTileIndex):
    """Creates or updates the map with the given ID."""
    map = getmap(mapID)
    if not map:
        return
    map.setTile(tile, newTileIndex)

@clientRPC
def sendTileUpdate(user, mapID, tile, newTileIndex):
    """Creates or updates the specified map."""
    map = getmap(mapID)
    if not map or not map.tilePosExists(tile):
        return
    respondTileUpdate(allusers(), mapID, tile, newTileIndex)

def clearPogSelection():
    _state.pogSelection = set()
    if _state.pogHover != None:
        _state.pogHover.showTooltip = False
        _state.pogHover = None
    drawPogCircles()

def createPog(pog):
    """Creates a new pog."""
    pog.ID = _state.session._findUniquePogID(pog.src)
    _state.session.addPog(pog)
    sendUpdatePog(pog.ID, pog.dump())

def modifyPog(pog):
    assert(pog.ID)
    sendUpdatePog(pog.ID, pog.dump())

def deletePog(pog):
    assert(pog.ID)
    sendDeletePog(pog.ID)

def placePog(pogpath):
    """Places a pog on the map."""
    _state.pogPlacement = True
    _state.pogPath = pogpath

def movePogs(displacement):
    """Moves pogs by a specified displacement."""
    selection = _state.pogSelection.copy()
    pogids = []
    for pog in selection:
        pog.displace(displacement)
        pogids.append(pog.ID)
    sendMovementPog(pogids, displacement)
    drawPogCircles()

@serverRPC
def respondUpdatePog(pogID, pogDump):
    """Creates or updates a pog on the client."""
    pog = rggPog.Pog.load(pogDump)
    pog.ID = pogID
    if pogID in _state.session.pogs.keys():
        old = _state.session.pogs[pogID]
        if old in _state.pogSelection:
            _state.pogSelection.discard(old)
            addPogSelection(pog)
        if old == _state.pogHover:
            _state.pogHover.showTooltip = False
            _state.pogHover = None
        old.destroy()
    _state.session.addPog(pog)
    drawPogCircles()

@clientRPC
def sendUpdatePog(user, pogID, pogDump):
    """Creates or updates a pog on the server."""
    
    # Upload (or check that we already have) the image resource from the client
    rggResource.srm.processFile(user, pogDump['src'])
    respondUpdatePog(allusersbut(user), pogID, pogDump)

@serverRPC
def respondDeletePog(pogID):
    """Deletes a pog on the client."""
    if pogID in _state.session.pogs.keys():
        old = _state.session.pogs[pogID]
        if old in _state.pogSelection:
            _state.pogSelection.discard(old)
        if old == _state.pogHover:
            _state.pogHover.showTooltip = False
            _state.pogHover = None
        _state.session.removePog(old)
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
        if pogID in _state.session.pogs.keys():
            pog = _state.session.pogs[pogID]
            pog.displace(displacement)
    drawPogCircles()

@clientRPC
def sendMovementPog(user, pogids, displacement):
    """Creates or updates a pog on the server."""
    respondMovementPog(allusersbut(user), pogids, displacement)

@serverRPC
def respondHidePog(pogID, hidden):
    """Hides or shows a pog on the client."""
    if pogID in _state.session.pogs.keys():
        pog = _state.session.pogs[pogID]
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
    if pogID in _state.session.pogs.keys():
        pog = _state.session.pogs[pogID]
        pog.name = name
        pog.layer = layer
        pog.properties = properties
        import rggEvent
        rggEvent.pogUpdateEvent(pog)

@clientRPC
def sendPogAttributes(user, pogID, name, layer, properties):
    '''Sends various attributes of a pog over the wire.'''
    import rggEvent
    rggEvent.pogUpdateEvent(_state.session.pogs[pogID])
    respondPogAttributes(allusersbut(user), pogID, name, layer, properties)

@serverRPC
def respondLockPog(pogID, locked):
    """Locks or unlocks a pog on the client."""
    if pogID in _state.session.pogs.keys():
        pog = _state.session.pogs[pogID]
        pog._locked = locked

@clientRPC
def sendLockPog(user, pogID, locked):
    """Locks or unlocks a pog on the server."""
    respondLockPog(allusers(), pogID, locked)

# DRAWING

@serverRPC
def respondLine(x, y, w, h, thickness, r, g, b):
    drawLine(x, y, w, h, thickness, r, g, b)
    _state.session.addLine((float(x), float(y), float(w), float(h), thickness, float(r), float(g), float(b)))

@clientRPC
def sendLine(user, x, y, w, h, thickness, r, g, b):
    respondLine(allusers(), x, y, w, h, thickness, r, g, b)

@serverRPC
def respondDeleteLine(x, y, w, h):
    deleteLine(x, y, w, h)

@clientRPC
def sendDeleteLine(user, x, y, w, h):
    respondDeleteLine(allusers(), x, y, w, h)
    
def _setThickness(new):
    _state.thickness = new

def setThickness(new):
    _setThickness(int(new.text()))
    
def _setLineColour(new):
    _state.linecolour = [new[0], new[1], new[2]]
    
def setLineColour(menuselection):
    if menuselection.text() == "Custom...":
        result = QtGui.QColorDialog.getColor(QtCore.Qt.white, mainWindow)
        _setLineColour((result.redF(), result.greenF(), result.blueF()))
    else:
        _setLineColour(rggSystem.COLOURS[str(menuselection.text())])

def clearLines():
    rggSystem.clearLines()

# DICE

def rollDice(dice, private=False):
    """Rolls the specified dice."""
    if not rggDice.isRollValid(dice):
        say(translate('views', "Invalid dice roll. See /roll documentation for help."))
    else:
        import rggRemote
        text = translate('views', "{name} rolls {roll}").format(
            name=linkedName(localuser().username),
            roll=rggDice.roll(dice))
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
    if rggDice.isRollValid(dice):
        name = promptString(translate('views', "What should the macro be called?"))
        if name is None:
            return
        _state.dwidget.addMacro(dice, name)
    else:
        say(translate('views', 'Malformed dice macro. Formatting help is available in "/roll" command.'))

# GENERATION

def generateName(nametype):
    """Generates a random name of the specified type."""
    say(rggNameGen.getName(nametype))

def generateTechnique(parameters=""):
    """Generates a technique name from the specified (optional) parameters."""
    say(rggNameGen.getTechniqueName(parameters))

def generateAdvice():
    """Generates random advice."""
    say(rggNameGen.getAdvice())


# MISC

def reportCamera():
    """Reports the current camera coordinates."""
    say(translate('views', 'x: {0}\ny: {1}', 'formats camera reporting.').format(*cameraPosition()))


# MOUSE ACTIONS

def mouseDrag(screenPosition, mapPosition, displacement):
    if _state.pogSelection and _state.mouseButton == BUTTON_LEFT:
        movePogs(displacement)
        return
    elif _state.mouseButton == BUTTON_LEFT:
        setCameraPosition(map(lambda c, d,  z: c + d*z, cameraPosition(), displacement, (getZoom(), getZoom())))
        return
    if _state.mouseButton == BUTTON_RIGHT:
        setCameraPosition(map(lambda c, d,  z: c + d*z, cameraPosition(), displacement, (getZoom(), getZoom())))

def mouseMove(screenPosition, mapPosition, displacement):
    icon = _state.menu.selectedIcon
    if icon == ICON_MOVE: # moveIcon
        if _state.mouseButton == BUTTON_LEFT:
            setCameraPosition(map(lambda c, d,  z: c + d*z, cameraPosition(), displacement, (getZoom(), getZoom())))
        elif _state.mouseButton == BUTTON_RIGHT:
            if topmap(mapPosition) is None:
                return
            drawOffset = list(topmap(mapPosition).drawOffset)
            drawOffset[0] += displacement[0]*getZoom()
            drawOffset[1] += displacement[1]*getZoom()
            topmap(mapPosition).drawOffset = drawOffset
        return
    if icon == ICON_SELECT: #selectIcon
        if _state.mouseButton is None:
            tooltipPog = _state.session.findTopPog(mapPosition)
            if _state.pogHover == tooltipPog:
                return
            elif _state.pogHover != None:
                _state.pogHover.showTooltip = False
            _state.pogHover = tooltipPog
            if tooltipPog is None:
                return

            tooltipPog.showTooltip = True
        elif _state.mouseButton == BUTTON_LEFT:
            return mouseDrag(screenPosition, mapPosition, displacement)
        elif _state.mouseButton == BUTTON_RIGHT:
            return mouseDrag(screenPosition, mapPosition, displacement)
    elif icon == ICON_DRAW: #drawIcon
        if _state.mouseButton == BUTTON_LEFT:
            if _state.previousLinePlacement != None:
                sendLine(_state.previousLinePlacement[0], _state.previousLinePlacement[1], mapPosition[0], mapPosition[1], _state.thickness, _state.linecolour[0], _state.linecolour[1], _state.linecolour[2])
            _state.previousLinePlacement = mapPosition
    elif icon == ICON_DELETE: #deleteIcon
        if _state.mouseButton == BUTTON_LEFT:
            if _state.previousLinePlacement != None:
                _state.nextLinePlacement = mapPosition #this is bottomRight of the square that we want to delete.
            else:
                _state.previousLinePlacement = mapPosition #We only do this so that we have a topLeft

def mousePress(screenPosition, mapPosition, button):
    
    import rggEvent
    
    icon = _state.menu.selectedIcon
    if icon == ICON_MOVE:
        return
    if icon == ICON_SELECT:
        if button == BUTTON_LEFT + BUTTON_CONTROL:
            if _state.pogPlacement:
                infograb = QtGui.QPixmap(_state.pogPath)
                pog = rggPog.Pog(
                    mapPosition,
                    (infograb.width(), infograb.height()),
                    (infograb.width(), infograb.height()),
                    1,
                    _state.pogPath,
                    0,
                    0,
                    {},
                    infograb.hasAlpha())
                createPog(pog)
                return
            pog = _state.session.findTopPog(mapPosition)
            if not pog:
                return
            if pog in _state.pogSelection:
                removePogSelection(pog)
            else:
                addPogSelection(pog)
            rggEvent.pogSelectionChangedEvent()
        elif button == BUTTON_LEFT:
            if _state.pogPlacement:
                _state.pogPlacement = False
                infograb = QtGui.QPixmap(_state.pogPath)
                pog = rggPog.Pog(
                    mapPosition,
                    (infograb.width(), infograb.height()),
                    (infograb.width(), infograb.height()),
                    1,
                    _state.pogPath,
                    0,
                    0,
                    {},
                    infograb.hasAlpha())
                createPog(pog)
                return
            pog = _state.session.findTopPog(mapPosition)
            if not pog:
                clearPogSelection()
                return
            if pog not in _state.pogSelection:
                setPogSelection(pog)
            rggEvent.pogSelectionChangedEvent()
        elif button == BUTTON_RIGHT:
            pog = _state.session.findTopPog(mapPosition)
            if pog is not None:
                _state.mouseButton = None
                selected = showPopupMenuAt(
                    (screenPosition[0], screenPosition[1]),
                    [translate('views', 'Set name'),
                        translate('views', 'Generate name'),
                        translate('views', 'Set Layer'),
                        translate('views', 'Add/Edit Property')])
                if selected == 0:
                    name = promptString(translate('views', "Enter a name for this pog."))
                    if name is None:
                        return
                    pog.name = name
                    sendPogAttributes(pog.ID, pog.name, pog.layer, pog.properties)
                elif selected == 1:
                    prompt = translate('views', "Enter a generator command. See /randomname for syntax. Multi-pog compatible.")
                    gentype = promptString(prompt)
                    if gentype is None:
                        return
                    gentype = ''.join(gentype.split()).lower()
                    for selectedPog in set([pog] + list(_state.pogSelection)):
                        selectedPog.name = rggNameGen.getName(gentype)
                        modifyPog(selectedPog)
                        sendPogAttributes(selectedPog.ID, selectedPog.name, selectedPog.layer, selectedPog.properties)
                elif selected == 2:
                    prompt = translate('views', "Enter a layer. Pogs on higher layers are displayed over those on lower layers. Should be a positive integer. Multi-pog compatible.")
                    newlayer = promptInteger(prompt, min=0, max=65535, default=pog.layer)
                    if newlayer is None:
                        return
                    for selectedPog in set([pog] + list(_state.pogSelection)):
                        selectedPog.layer = newlayer
                        sendPogAttributes(pog.ID, pog.name, pog.layer, pog.properties)
                elif selected == 3:
                    prompt = translate('views', 'Enter a name for the property (like "Level" or "HP").')
                    key = promptString(prompt)
                    prompt2 = translate('views', 'Enter a value for the property.')
                    value = promptString(prompt2)
                    if key is None or value is None:
                        return
                    pog.editProperty(key, value)
                    sendPogAttributes(pog.ID, pog.name, pog.layer, pog.properties)
            else:
                pass
    elif icon == ICON_DRAW:
        if button == BUTTON_LEFT:
            _state.previousLinePlacement = mapPosition
    elif icon == ICON_DELETE:
        if button == BUTTON_LEFT:
            _state.previousLinePlacement = mapPosition
                


def mouseRelease(screenPosition, mapPosition, button):
    _state.mouseButton = None

    icon = _state.menu.selectedIcon
    if(icon == ICON_DELETE):
        if(_state.previousLinePlacement != None and _state.nextLinePlacement != None):

            x = _state.previousLinePlacement[0]
            y = _state.previousLinePlacement[1]
            w = _state.nextLinePlacement[0]
            h = _state.nextLinePlacement[1]
            if(x > w):
                x, w = w, x
            if(y > h):
                y, h = h, y
            
            w -= x
            h -= y
            #print '(x, y, w, h) (' + str(x) + ', ' + str(y) + ', ' + str(w) + ', ' + str(h) + ')' 

            sendDeleteLine(x, y, w, h)

            _state.nextLinePlacement = mapPosition

def mouseMoveResponse(x, y):
    #print 'move', x, y

    screenPosition = (x, y)
    mapPosition = getMapPosition(screenPosition)
    displacement = map(lambda p,m,d: p/d - m/d, screenPosition, _state.mousePosition,  (getZoom(), getZoom()))
    
    #print mapPosition
    #print cameraPosition()
    
    mouseMove(screenPosition, mapPosition, displacement)
    
    _state.mousePosition = screenPosition

def mousePressResponse(x, y, t):
    #print 'press', x, y, t

    screenPosition = (x, y)
    mapPosition = getMapPosition(screenPosition)
    
    _state.mousePosition = screenPosition
    _state.mouseButton = t
    
    mousePress(screenPosition, mapPosition, t)
    
def mouseReleaseResponse(x, y, t):
    #print 'release', x, y, t
    
    screenPosition = (x, y)
    mapPosition = getMapPosition(screenPosition)
    
    _state.mousePosition = screenPosition
    _state.mouseButton = t
    
    mouseRelease(screenPosition, mapPosition, t)

