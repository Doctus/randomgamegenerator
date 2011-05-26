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
import rggNameGen, rggDice, rggMap, rggTile, rggPog, rggDockWidget, rggDialogs, rggMenuBar, rggResource, rggSystem
from rggRPC import server, client, serverRPC, clientRPC
from rggJson import jsondump, jsonload
from rggMenuBar import ICON_SELECT, ICON_MOVE, ICON_DRAW, ICON_DELETE
from rggSystem import cameraPosition, setCameraPosition, mainWindow, getMapPosition
from rggSystem import translate, showErrorMessage
from rggSystem import showPopupMenuAt, IMAGE_FILTER
from rggSystem import promptString, promptInteger, promptCoordinates, promptSaveFile, promptLoadFile
from rggSystem import drawLine, deleteLine, drawSelectionCircle, clearSelectionCircles, getZoom
from rggDialogs import newMapDialog, hostDialog, joinDialog
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
    
    Maps = {}
    
    pogSelection = set()
    pogHover = None
    
    mouseButton = None
    mousePosition = (0, 0)
    
    pogPlacement = False
    pogPath = "path"

    previousLinePlacement = None #(0, 0) expected
    nextLinePlacement = None

    thickness = 1
    
    @staticmethod
    def initialize():
        _state.menu = rggMenuBar.menuBar()
        
        _state.dwidget = rggDockWidget.diceRoller(mainWindow)
        _state.pwidget = rggDockWidget.pogPalette(mainWindow)
        _state.cwidget = rggDockWidget.chatWidget(mainWindow)
        _state.icwidget = rggDockWidget.ICChatWidget(mainWindow)
        _state.uwidget = rggDockWidget.userListWidget(mainWindow)
        _state.users = {}
        _state.localuser = User(client.username)
        _state.users[client.username] = _state.localuser
        
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

# MESSAGES

def say(message):
    """Say an IC message. This documentation is a lie."""
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

# MAPS
def topmap(mapPosition):
    for map in _state.Maps.values():
        size = map.pixelSize
        if mapPosition[0] >= map.drawOffset[0] and mapPosition[0] <= map.drawOffset[0] + size[0]:
            if mapPosition[1] >= map.drawOffset[1] and mapPosition[1] <= map.drawOffset[1] + size[1]:
                return map
    return None

def getmap(mapID):
    return _state.Maps.get(mapID, None)

def allmaps():
    return _state.Maps.items()

def getAllMaps():
    return _state.Maps.values()

def createMapID(mapname):
    ID = mapname or rggSystem.findRandomAppend()
    while ID in _state.Maps:
        ID += rggSystem.findRandomAppend()
    return ID

def chooseMap():
    say(translate('views', 'This function is deprecated. Use the view controller.'))
    return
    mapNames = []
    mapIDs = []
    defaultButton = 0
    i = 0

    if len(_state.Maps) <= 1:
        say(translate('views', 'There are no maps to switch between.'))
        return

    for ID in _state.Maps:
        mapNames.append(_state.Maps[ID].mapname)
        mapIDs.append(ID)
        i += 1

    selectedButton = rggSystem.promptButtonSelection("Which map do you want to switch to?", mapNames, defaultButton)
    #sendMapSwitch(mapIDs[selectedButton])
    #_state.Maps[mapIDS[selectedButton]].
    

def closeAllMaps():
    for map in _state.Maps.values():
        map._deleteTiles()
    _state.Maps = {}

def internalAddMap(map):
    pos = 0
    for m in getAllMaps():
        pos += m.pixelSize[0] + 25
    map.drawOffset = (pos, 0)

    ID = createMapID(map.mapname)
    rggResource.srm.processFile(localuser(), map.tileset)
    for pogDump in map.Pogs.values():
        rggResource.srm.processFile(localuser(), pog._src)
    _state.Maps[ID] = map
    map.ID = ID
    
    sendMapCreate(ID, map.dump())

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
        return

def saveMap():
    """Allows the user to save a map."""
    mapNames = []
    mapIDs = []
    i = 0
    
    for ID in _state.Maps:
        mapNames.append(_state.Maps[ID].mapname)
        mapIDs.append(ID)
        i += 1

    selectedButton = rggSystem.promptButtonSelection("Which map do you want to save?", mapNames, 0)
    map = _state.Maps[mapIDs[selectedButton]]
    # TODO: Probably better handled in a Map Properties dialog.
    #if promptChoice("Edit map info?", ['Yes', 'No'], 1) == 0:
    #    map.mapname = unicode(promptString("What is the name of this map?")) or map.mapname
    #    map.authorname = unicode(promptString("Who is the author of this map?")) or map.authorname
    
    filename = promptSaveFile(translate('views', 'Save Map'),
        translate('views', 'Random Game Map files (*.rgm)'),
        rggSystem.MAP_DIR)
    if not filename:
        return
    
    jsondump(map.dump(), filename)

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
        return
    
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
    print "map create"
    existed = (ID in _state.Maps)
    if existed:
        print "ignoring map create"
        return
    map = rggMap.Map.load(mapDump)
    map.ID = ID
    pos = 0
    for map in getAllMaps():
        pos += map.pixelSize[0] + 100
    map.drawOffset = (pos, 0)
    _state.Maps[ID] = map

@clientRPC
def sendMapCreate(user, ID, map):
    """Creates or updates the specified map."""

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

@serverRPC
def respondMapSwitch(ID, handle):
    mappe = getmap(ID)
    if mappe:
        #disallow = rggSystem.promptButtonSelection('User "{user}" has switched to map "{mapname}", do you want to switch too?'.format(user=handle, mapname=mappe.mapname), ['Yes', 'No'], 1)

        #if disallow == 0:
        switchMap(mappe)

@clientRPC
def sendMapSwitch(user, ID):
    mappe = getmap(ID)
    if mappe:
        #respondMapSwitch(allusersbut(user), ID, unicode(user))
        respondMapSwitch(allusers(), ID, unicode(user))

        #switchMap(mappe)

# POGS

def clearPogSelection():
    _state.pogSelection = set()
    if _state.pogHover != None:
        _state.pogHover.showTooltip = False
        _state.pogHover = None
    drawPogCircles()

def createPog(pogMap, pog):
    """Creates a new pog."""
    sendUpdatePog(pogMap.ID, None, pog.dump())

def modifyPog(pogMap, pog):
    assert(pog.ID)
    sendUpdatePog(pogMap.ID, pog.ID, pog.dump())

def deletePog(pogMapID, pog):
    assert(pog.ID)
    sendDeletePog(pogMapID, pog.ID)

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
    sendMovementPog(currentmap().ID, pogids, displacement)
    drawPogCircles()

@serverRPC
def respondUpdatePog(mapID, pogID, pogDump):
    """Creates or updates a pog on the client."""
    pogMap = getmap(mapID)
    if pogMap is None:
        print "Attempt to change pog in nonextant map: {0}".format(mapID)
        return
    pog = rggPog.Pog.load(pogDump)
    pog.ID = pogID
    if pogID in pogMap.Pogs:
        old = pogMap.Pogs[pogID]
        if old in _state.pogSelection:
            _state.pogSelection.discard(old)
            addPogSelection(pog)
        if old == _state.pogHover:
            _state.pogHover.showTooltip = False
            _state.pogHover = None
        old._tile.destroy()
    pogMap.addPog(pog)
    drawPogCircles()

@clientRPC
def sendUpdatePog(user, mapID, pogID, pogDump):
    """Creates or updates a pog on the server."""
    
    #TODO: What happens when we delete a pog then get something like movement or a property change for it?
    # Fix with different messages that don't completely change the pog, and only use this for creation.
    pogMap = getmap(mapID)
    # Upload (or check that we already have) the image resource from the client
    rggResource.srm.processFile(user, pogDump['src'])
    if not pogMap:
        print "no pogmap"
        return
    # HACK: Relies on the fact that responses are locally synchronous
    if not pogID or pogID not in pogMap.Pogs:
        pogID = pogMap._findUniqueID(pogDump['src'])
    respondUpdatePog(allusers(), mapID, pogID, pogDump)

@serverRPC
def respondDeletePog(mapID, pogID):
    """Deletes a pog on the client."""
    pogMap = getmap(mapID)
    if pogMap is None:
        print "Attempt to delete pog in nonextant map: {0}".format(mapID)
        return
    if pogID in pogMap.Pogs:
        old = pogMap.Pogs[pogID]
        if old in _state.pogSelection:
            _state.pogSelection.discard(old)
        if old == _state.pogHover:
            _state.pogHover.showTooltip = False
            _state.pogHover = None
        pogMap.removePog(old)
    drawPogCircles()

@clientRPC
def sendDeletePog(user, mapID, pogID):
    """Deletes a pog on the server."""
    pogMap = getmap(mapID)
    if not pogMap:
        return
    # HACK: Relies on the fact that responses are locally synchronous
    respondDeletePog(allusers(), mapID, pogID)

@serverRPC
def respondMovementPog(mapID, pogids, displacement):
    """Creates or updates a pog on the client."""
    pogMap = getmap(mapID)
    if pogMap is None:
        print "Attempt to move pog in nonexistant map: {0}".format(mapID)
        return
    for pogID in pogids:
        if pogID in pogMap.Pogs:
            pog = pogMap.Pogs[pogID]
            pog.displace(displacement)
    drawPogCircles()

@clientRPC
def sendMovementPog(user, mapID, pogids, displacement):
    """Creates or updates a pog on the server."""
    pogMap = getmap(mapID)
    if not pogMap:
        return
    respondMovementPog(allusersbut(user), mapID, pogids, displacement)

@serverRPC
def respondHidePog(mapID, pogID, hidden):
    """Hides or shows a pog on the client."""
    pogMap = getmap(mapID)
    if pogMap is None:
        print "Attempt to hide pog in nonexistant map: {0}".format(mapID)
        return
    if pogID in pogMap.Pogs:
        pog = pogMap.Pogs[pogID]
        if hidden:
            pog.hide()
        else:
            pog.show()
    drawPogCircles()

@clientRPC
def sendHidePog(user, mapID, pogID, hidden):
    """Hides or shows a pog on the server."""
    pogMap = getmap(mapID)
    if not pogMap:
        return
    respondHidePog(allusers(), mapID, pogID, hidden)

@serverRPC
def respondPogAttributes(mapID, pogID, name, layer, properties):
    '''Sends various attributes of a pog over the wire.'''
    pogMap = getmap(mapID)
    if not pogMap:
        return
    if pogID in pogMap.Pogs:
        pog = pogMap.Pogs[pogID]
        pog.name = name
        pog.layer = layer
        pog.properties = properties
        import rggEvent
        rggEvent.pogUpdateEvent(pog)

@clientRPC
def sendPogAttributes(user, mapID, pogID, name, layer, properties):
    '''Sends various attributes of a pog over the wire.'''
    pogMap = getmap(mapID)
    if not pogMap:
        return
    import rggEvent
    rggEvent.pogUpdateEvent(pogMap.Pogs[pogID])
    respondPogAttributes(allusersbut(user), mapID, pogID, name, layer, properties)

@serverRPC
def respondLockPog(mapID, pogID, locked):
    """Locks or unlocks a pog on the client."""
    pogMap = getmap(mapID)
    if pogMap is None:
        print "Attempt to lock pog in nonexistant map: {0}".format(mapID)
        return
    if pogID in pogMap.Pogs:
        pog = pogMap.Pogs[pogID]
        pog._locked = locked

@clientRPC
def sendLockPog(user, mapID, pogID, locked):
    """Locks or unlocks a pog on the server."""
    pogMap = getmap(mapID)
    if not pogMap:
        return
    respondLockPog(allusers(), mapID, pogID, locked)

# DRAWING

@serverRPC
def respondLine(x, y, w, h, thickness):
    drawLine(x, y, w, h, thickness)
    linesDict = topmap((x, y)).linesDict
    if not thickness in linesDict:
        linesDict[thickness] = []
        
    linesDict[thickness].append((float(x), float(y), float(w), float(h)))
    topmap((x, y)).linesDict = linesDict

@clientRPC
def sendLine(user, x, y, w, h, thickness):
    respondLine(allusers(), x, y, w, h, thickness)

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
        if topmap(mapPosition) is not None:
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
            if topmap(mapPosition) is None:
                return
            tooltipPog = topmap(mapPosition).findTopPog(mapPosition)
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
        if topmap(mapPosition) is None:
            return
        if _state.mouseButton == BUTTON_LEFT:
            if _state.previousLinePlacement != None:
                sendLine(_state.previousLinePlacement[0], _state.previousLinePlacement[1], mapPosition[0], mapPosition[1], _state.thickness)
            _state.previousLinePlacement = mapPosition
    elif icon == ICON_DELETE: #deleteIcon
        if _state.mouseButton == BUTTON_LEFT:
            if _state.previousLinePlacement != None:
                _state.nextLinePlacement = mapPosition #this is bottomRight of the square that we want to delete.
            else:
                _state.previousLinePlacement = mapPosition #We only do this so that we have a topLeft

def mousePress(screenPosition, mapPosition, button):
    
    if topmap(mapPosition) is None:
        return
    
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
                    topmap(mapPosition).ID)
                createPog(topmap(mapPosition), pog)
                return
            pog = topmap(mapPosition).findTopPog(mapPosition)
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
                    topmap(mapPosition).ID,
                    infograb.hasAlpha())
                createPog(topmap(mapPosition), pog)
                return
            pog = topmap(mapPosition).findTopPog(mapPosition)
            if not pog:
                clearPogSelection()
                return
            if pog not in _state.pogSelection:
                setPogSelection(pog)
            rggEvent.pogSelectionChangedEvent()
        elif button == BUTTON_RIGHT:
            pog = topmap(mapPosition).findTopPog(mapPosition)
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
                    sendPogAttributes(topmap(mapPosition).ID, pog.ID, pog.name, pog.layer, pog.properties)
                elif selected == 1:
                    prompt = translate('views', "Enter a generator command. See /randomname for syntax. Multi-pog compatible.")
                    gentype = promptString(prompt)
                    if gentype is None:
                        return
                    gentype = ''.join(gentype.split()).lower()
                    for selectedPog in set([pog] + list(_state.pogSelection)):
                        selectedPog.name = rggNameGen.getName(gentype)
                        modifyPog(topmap(mapPosition), selectedPog)
                        sendPogAttributes(topmap(mapPosition).ID, selectedPog.ID, selectedPog.name, selectedPog.layer, selectedPog.properties)
                elif selected == 2:
                    prompt = translate('views', "Enter a layer. Pogs on higher layers are displayed over those on lower layers. Should be a positive integer. Multi-pog compatible.")
                    newlayer = promptInteger(prompt, min=0, max=65535, default=pog.layer)
                    if newlayer is None:
                        return
                    for selectedPog in set([pog] + list(_state.pogSelection)):
                        selectedPog.layer = newlayer
                        sendPogAttributes(topmap(mapPosition).ID, pog.ID, pog.name, pog.layer, pog.properties)
                elif selected == 3:
                    prompt = translate('views', 'Enter a name for the property (like "Level" or "HP").')
                    key = promptString(prompt)
                    prompt2 = translate('views', 'Enter a value for the property.')
                    value = promptString(prompt2)
                    if key is None or value is None:
                        return
                    pog.editProperty(key, value)
                    sendPogAttributes(topmap(mapPosition).ID, pog.ID, pog.name, pog.layer, pog.properties)
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
                tempw = w
                w = x
                x = tempw
            if(y > h):
                tempy = y
                y = h
                h = tempy

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

