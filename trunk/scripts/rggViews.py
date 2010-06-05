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
from rggSystem import cameraPosition, setCameraPosition, mainWindow
from rggSystem import translate, showErrorMessage, displayTooltip
from rggSystem import showPopupMenuAt, IMAGE_FILTER
from rggSystem import promptString, promptInteger, promptCoordinates, promptSaveFile, promptLoadFile
from rggSystem import drawLine, deleteLine
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
    currentMap = None
    
    pogSelection = set()
    pogHover = None
    
    mouseButton = None
    mousePosition = (0, 0)
    
    tilePasting = False
    tilePastingIndex = 0
    
    pogPlacement = False
    pogPath = "path"

    previousLinePlacement = None #(0, 0) expected
    nextLinePlacement = None

    thickness = 1;
    
    @staticmethod
    def initialize():
        _state.menu = rggMenuBar.menuBar()
        
        _state.dwidget = rggDockWidget.diceRoller(mainWindow)
        _state.pwidget = rggDockWidget.pogPalette(mainWindow)
        _state.cwidget = rggDockWidget.chatWidget(mainWindow)
        _state.icwidget = rggDockWidget.ICChatWidget(mainWindow)
        _state.users = {}
        _state.localuser = User(client.username)
        _state.users[client.username] = _state.localuser
        

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
    #print "KILL"

def disconnectGame():
    """Allows the user to disconnect from the internet."""
    if not client.isConnected:
        say(translate('views', "You are not connected."))
        return
    
    killConnection()
    say(translate('views', "Disconnected."))

# MAPS

def currentmap():
    return _state.currentMap

def getmap(mapID):
    return _state.Maps.get(mapID, None)

def allmaps():
    return _state.Maps.items()

def createMapID(mapname):
    ID = mapname or rggSystem.findRandomAppend()
    while ID in _state.Maps:
        ID += rggSystem.findRandomAppend()
    return ID

def modifyCurrentMap():
    sendMapUpdate(currentmap().ID, currentmap().dump())

def pasteTile(position):
    """Pastes a tile at a designated position."""
    # TODO: RPC that just sends a tile instead of the whole map.
    if not currentmap():
        return
    tile = map(lambda p, d: p // d, position, currentmap().tilesize)
    currentmap().setTile(tile, _state.tilePastingIndex)
    modifyCurrentMap()

def switchMap(map):
    """Switches to the specified map."""
    import rggEvent
    if _state.currentMap:
        _state.currentMap.hide()
    clearPogSelection()
    clearLines()
    _state.currentMap = map
    rggEvent.mapChangedEvent(map)
    if _state.currentMap:
        _state.currentMap.show()
        print "Changed to map: {0}".format(_state.currentMap)

def chooseMap():
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
        if ID == _state.currentMap.ID:
            defaultButton = i
        i += 1

    selectedButton = rggSystem.promptButtonSelection("Which map do you want to switch to?", mapNames, defaultButton)
    sendMapSwitch(mapIDs[selectedButton])
    

def closeAllMaps():
    switchMap(None)
    _state.Maps = {}

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
        sendMapUpdate(None, map.dump())

def loadMap():
    """Allows the user to load a new map."""
    filename = promptLoadFile(translate('views', 'Open Map'),
        translate('views', 'Random Game Map files (*.rgm)'))
    if not filename:
        return
    try:
        obj = jsonload(filename)
        map = rggMap.Map.load(obj)
    except Exception as e:
        showErrorMessage(translate('views', "Unable to read {0}.").format(filename))
        return
    sendMapUpdate(None, map.dump())

def saveMap():
    """Allows the user to save the current map."""
    
    map = _state.currentMap
    if _state.currentMap is None:
        return
    # TODO: Probably better handled in a Map Properties dialog.
    #if promptChoice("Edit map info?", ['Yes', 'No'], 1) == 0:
    #    map.mapname = unicode(promptString("What is the name of this map?")) or map.mapname
    #    map.authorname = unicode(promptString("Who is the author of this map?")) or map.authorname
    
    filename = promptSaveFile(translate('views', 'Save Map'),
        translate('views', 'Random Game Map files (*.rgm)'))
    if not filename:
        return
    
    jsondump(map.dump(), filename)

@serverRPC
def respondMapUpdate(ID, mapDump):
    """Creates or updates the map with the given ID."""
    map = rggMap.Map.load(mapDump)
    map.ID = ID
    existed = (ID in _state.Maps)
    _state.Maps[ID] = map
    if not existed or (_state.currentMap and _state.currentMap.ID == ID):
        switchMap(map)

@clientRPC
def sendMapUpdate(user, ID, mapDump):
    """Creates or updates the specified map."""
    if not getmap(ID):
        ID = createMapID(mapDump['mapname'])
    rggResource.srm.processFile(user, mapDump['tileset'])
    for pogDump in mapDump['pogs'].values():
        rggResource.srm.processFile(user, pogDump['src'])
    respondMapUpdate(allusers(), ID, mapDump)

@serverRPC
def respondMapSwitch(ID, handle):
    map = getmap(ID)
    if map:
        disallow = rggSystem.promptButtonSelection('User "{user}" has switched to map "{map}", do you want to switch too?'.format(user=handle, map=map.mapname), ['Yes', 'No'], 1)

        if not disallow:
            switchMap(map)

@clientRPC
def sendMapSwitch(user, ID):
    if getmap(ID):
        respondMapSwitch(allusersbut(user), ID, unicode(user))

        map = getmap(ID)
        if map:
            switchMap(map)

# POGS

def clearPogSelection():
    _state.pogSelection = set()
    _state.pogHover = None

def createPog(pogMap, pog):
    """Creates a new pog."""
    sendUpdatePog(pogMap.ID, None, pog.dump())

def modifyPog(pogMap, pog):
    assert(pog.ID)
    sendUpdatePog(pogMap.ID, pog.ID, pog.dump())

def placePog(pogpath):
    """Places a pog on the map."""
    if _state.currentMap is None:
        return
    _state.pogPlacement = True
    _state.pogPath = pogpath

# TODO: Make pog movement transfer much more efficient.
def movePogs(displacement):
    """Moves pogs by a specified displacement."""
    selection = _state.pogSelection.copy()
    for pog in selection:
        pog.displace(displacement)
        #modifyPog(currentmap(), pog)
        sendMovementPog(currentmap().ID, pog.ID, pog.dump())

@serverRPC
def respondUpdatePog(mapID, pogID, pogDump):
    """Creates or updates a pog on the client."""
    pogMap = getmap(mapID)
    if pogMap is None:
        print "Attempt to change pog in nonextant map: {0}".format(mapID)
        return
    pogMap = _state.Maps[mapID]
    pog = rggPog.Pog.load(pogDump)
    pog.ID = pogID
    if pogID in pogMap.Pogs:
        old = pogMap.Pogs[pogID]
        if old in _state.pogSelection:
            _state.pogSelection.discard(old)
            _state.pogSelection.add(pog)
        if old == _state.pogHover:
            _state.pogHover = None
    pogMap.addPog(pog)

@clientRPC
def sendUpdatePog(user, mapID, pogID, pogDump):
    """Creates or updates a pog on the server."""
    #TODO: What happens when we delete a pog then get something like movement or a property change for it?
    # Fix with different messages that don't completely change the pog, and only use this for creation.
    pogMap = getmap(mapID)
    # Upload (or check that we already have) the image resource from the client
    rggResource.srm.processFile(user, pogDump['src'])
    if not pogMap:
        return
    # HACK: Relies on the fact that responses are locally synchronous
    if not pogID or pogID not in pogMap.Pogs:
        pogID = pogMap._findUniqueID(pogDump['src'])
    respondUpdatePog(allusers(), mapID, pogID, pogDump)

@clientRPC
def sendMovementPog(user, mapID, pogID, pogDump):
    """Creates or updates a pog on the server."""
    #TODO: What happens when we delete a pog then get something like movement or a property change for it?
    # Fix with different messages that don't completely change the pog, and only use this for creation.
    pogMap = getmap(mapID)
    # Upload (or check that we already have) the image resource from the client
    rggResource.srm.processFile(user, pogDump['src'])
    if not pogMap:
        return
    # HACK: Relies on the fact that responses are locally synchronous
    if not pogID or pogID not in pogMap.Pogs:
        pogID = pogMap._findUniqueID(pogDump['src'])
    users = allusers()
    users.remove(user)
    respondUpdatePog(users, mapID, pogID, pogDump)

# DRAWING

@serverRPC
def respondLine(x, y, w, h, thickness):
    drawLine(x, y, w, h, thickness)

@clientRPC
def sendLine(user, x, y, w, h, thickness):
    respondLine(allusers(), x, y, w, h, thickness)

@serverRPC
def respondDeleteLine(x, y, w, h):
    deleteLine(x, y, w, h)

@clientRPC
def sendDeleteLine(user, x, y, w, h):
    respondDeleteLine(allusers(), x, y, w, h)

def setThicknessToOne():
    _state.thickness = 1

def setThicknessToTwo():
    _state.thickness = 2

def setThicknessToThree():
    _state.thickness = 3

def clearLines():
    rggSystem.clearLines()

# DICE

def rollDice(dice):
    """Rolls the specified dice."""
    if not rggDice.isRollValid(dice):
        say(translate('views', "Invalid dice roll. See /roll documentation for help."))
    else:
        text = translate('views', "{name} rolls {roll}").format(
            name=linkedName(localuser().username),
            roll=rggDice.roll(dice))
        say(text)
        ICSay(text)
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
    if _state.pogSelection:
        movePogs(displacement)
    elif _state.tilePasting and currentmap():
        pasteTile(mapPosition)

def mouseMove(screenPosition, mapPosition, displacement):
    icon = _state.menu.selectedIcon
    if icon == ICON_MOVE: # moveIcon
        if _state.mouseButton == BUTTON_LEFT:
            setCameraPosition(map(lambda c, d: c - d, cameraPosition(), displacement))
        return
    if icon == ICON_SELECT: #selectIcon
        if _state.mouseButton is None:
            if currentmap() is None:
                return
            tooltipPog = currentmap().findTopPog(mapPosition)
            if _state.pogHover == tooltipPog:
                return
            _state.pogHover = tooltipPog
            if tooltipPog is None:
                return
            displayPosition = map(lambda t, c: t - c, tooltipPog.tooltipPosition(), cameraPosition())
            displayTooltip(tooltipPog.tooltipText(), displayPosition)
        elif _state.mouseButton == BUTTON_LEFT:
            return mouseDrag(screenPosition, mapPosition, displacement)
    elif icon == ICON_DRAW: #drawIcon
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
    
    if currentmap() is None:
        return
    
    icon = _state.menu.selectedIcon
    if icon == ICON_MOVE:
        return
    if icon == ICON_SELECT:
        if button == BUTTON_LEFT or button == BUTTON_LEFT + BUTTON_CONTROL:
            if _state.pogPlacement:
                _state.pogPlacement = False
                infograb = QtGui.QPixmap(_state.pogPath)
                pog = rggPog.Pog(
                    mapPosition,
                    (infograb.width(), infograb.height()),
                    1,
                    _state.pogPath)
                createPog(currentmap(), pog)
                return
            elif _state.tilePasting:
                tile = map(lambda p, s: p // s, mapPosition, _state.currentMap.tilesize)
                currentmap().setTile(tile, _state.tilePastingIndex)
                modifyCurrentMap()
                return
        
        if button == BUTTON_LEFT:
            pog = _state.currentMap.findTopPog(mapPosition)
            if pog not in _state.pogSelection:
                _state.pogSelection = set()
            if not pog:
                return
            _state.pogSelection.add(pog)
        elif button == BUTTON_LEFT + BUTTON_CONTROL:
            pog = currentmap().findTopPog(mapPosition)
            if not pog:
                return
            if pog in _state.pogSelection:
                _state.pogSelection.remove(pog)
            else:
                _state.pogSelection.add(pog)
        #Was this duplicated for a reason? I don't see any.
        #elif button == BUTTON_LEFT + BUTTON_CONTROL:
        #    pog = currentmap().findTopPog(mapPosition)
        #    if not pog:
        #        return
        #    if pog in _state.pogSelection:
        #        _state.pogSelection.remove(pog)
        #    else:
        #        _state.pogSelection.add(pog)
        elif button == BUTTON_RIGHT:
            pog = currentmap().findTopPog(mapPosition)
            if pog is not None:
                selected = showPopupMenuAt(
                    screenPosition,
                    [translate('views', 'Set name'),
                        translate('views', 'Generate name'),
                        translate('views', 'Set Layer')])
                if selected == 0:
                    name = promptString(translate('views', "Enter a name for this pog."))
                    if name is None:
                        return
                    pog.name = name
                    modifyPog(currentmap(), pog)
                elif selected == 1:
                    prompt = translate('views', "Enter a generator command. See /randomname for syntax. Multi-pog compatible.")
                    gentype = promptString(prompt)
                    if gentype is None:
                        return
                    gentype = ''.join(gentype.split()).lower()
                    for selectedPog in set([pog] + list(_state.pogSelection)):
                        selectedPog.name = rggNameGen.getName(gentype)
                        modifyPog(currentmap(), selectedPog)
                elif selected == 2:
                    prompt = translate('views', "Enter a layer. Pogs on higher layers are displayed over those on lower layers. Should be a positive integer. Multi-pog compatible.")
                    newlayer = promptInteger(prompt, min=0, max=65535)
                    if newlayer is None:
                        return
                    for selectedPog in set([pog] + list(_state.pogSelection)):
                        selectedPog.layer = newlayer
                        modifyPog(currentmap(), pog)
            else:
                if not _state.tilePasting:
                    selected = showPopupMenuAt(
                        screenPosition,
                        [translate('views', "Create Pog (Temp Command)"),
                            translate('views', "Begin Tile Pasting (Temp Command)")])
                else:
                    selected = showPopupMenuAt(
                        screenPosition,
                        [translate('views', "Create Pog (Temp Command)"),
                            translate('views', "Cease Tile Pasting (Temp Command)")])
                if selected == 0:
                    src = promptLoadFile(translate('views', "Load Pog"), IMAGE_FILTER)
                    if src is None:
                        return
                    size = promptCoordinates(translate('views', "What is the width of the image?"),
                        translate('views', "What is the height of the image?"))
                    if size is None:
                        return
                    pog = rgg.Pog(mapPosition, size, 1, src)
                    createPog(currentmap(), pog)
                elif selected == 1:
                    if not _state.tilePasting:
                        _state.tilePasting = True
                        tile = map(lambda p, c: p // c, mapPosition, _state.currentMap.tilesize)
                        _state.tilePastingIndex = _state.currentMap.getTile(tile)
                    else:
                        _state.tilePasting = False
        #elif button == BUTTON_MIDDLE: #DEBUG STUFF
        #    Maps[currentMap[0]].debugMorphTile([(x+c.getCamX())/Maps[currentMap[0]].tilesize[0], (y+c.getCamY())/Maps[currentMap[0]].tilesize[1]], c.getTileCountOfImage(Maps[currentMap[0]].tileset))

        #endif icon == ICON_SELECT
    elif icon == ICON_DRAW:
        if button == BUTTON_LEFT:
            _state.previousLinePlacement = mapPosition
    elif icon == ICON_DELETE:
        if button == BUTTON_LEFT:
            _state.previousLinePlacement = mapPosition
                


def mouseRelease(screenPosition, mapPosition, button):
    _state.mouseButton = None

    icon = _state.menu.selectedIcon
    if(icon == ICON_SELECT):
      for pog in _state.pogSelection:
        sendUpdatePog(currentmap().ID, pog.ID, pog.dump())
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

            print '(x, y, w, h) (' + str(x) + ', ' + str(y) + ', ' + str(w) + ', ' + str(h) + ')' 

            sendDeleteLine(x, y, w, h)

            _state.nextLinePlacement = mapPosition

def mouseMoveResponse(x, y):
    #print 'move', x, y
    
    screenPosition = (x, y)
    mapPosition = map(lambda p,c: p + c, screenPosition, cameraPosition())
    displacement = map(lambda p,m: p - m, screenPosition, _state.mousePosition)
    
    mouseMove(screenPosition, mapPosition, displacement)
    
    _state.mousePosition = screenPosition

def mousePressResponse(x, y, t):
    #print 'press', x, y, t
    
    
    screenPosition = (x, y)
    mapPosition = map(lambda p,c: p + c, screenPosition, cameraPosition())
    
    _state.mousePosition = screenPosition
    _state.mouseButton = t
    
    mousePress(screenPosition, mapPosition, t)
    
def mouseReleaseResponse(x, y, t):
    #print 'release', x, y, t
    
    screenPosition = (x, y)
    mapPosition = map(lambda p,c: p + c, screenPosition, cameraPosition())
    
    _state.mousePosition = screenPosition
    _state.mouseButton = t
    
    mouseRelease(screenPosition, mapPosition, t)

