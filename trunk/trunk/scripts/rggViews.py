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
import rggNameGen, rggDice, rggMap, rggTile, rggPog, rggDockWidget, rggDialogs, rggMenuBar
from rggRPC import server, client
from rggJson import jsondump, jsonload
from rggMenuBar import ICON_SELECT, ICON_MOVE
from rggSystem import cameraPosition, setCameraPosition, mainWindow
from rggSystem import translate, showErrorMessage, displayTooltip
from rggSystem import showPopupMenuAt, IMAGE_FILTER
from rggSystem import promptString, promptInteger, promptCoordinates, promptSaveFile, promptLoadFile
from rggDialogs import newMapDialog, hostDialog, joinDialog
from PyQt4 import QtCore, QtGui

# Button enum
BUTTON_LEFT = 0
BUTTON_MIDDLE = 1
BUTTON_RIGHT = 2
BUTTON_CONTROL = 3
BUTTON_SHIFT = 6

# Table of active users on the server
class User(object):
    """User representation on the server."""
    
    def __init__(self, id):
        self.id = id
        self.username = '[unnamed #{0}]'.format(id)
        self.unnamed = True

class state(object):
    """A state class build to avoid all these global statements."""
    
    Maps = []
    currentMap = None
    
    pogSelection = set()
    pogHover = None
    
    mouseButton = None
    mousePosition = (0, 0)
    
    tilePasting = False
    tilePastingIndex = 0
    
    pogPlacement = False
    pogPath = "path"
    
    @staticmethod
    def initialize():
        state.menu = rggMenuBar.menuBar()
        
        state.dwidget = rggDockWidget.diceRoller(mainWindow)
        state.pwidget = rggDockWidget.pogPalette(mainWindow)
        state.cwidget = rggDockWidget.chatWidget(mainWindow)
        
        state.localuser = User(0)
        # remain unnamed, but give a default
        state.localuser.username = 'localplayer'
        
        state.users = { state.localuser.id: state.localuser }
        state.usernames = {}

# MESSAGES

def say(message):
    """Say an IC message."""
    state.cwidget.insertMessage(message)

def announce(message):
    """Say an OOC message."""
    state.cwidget.insertMessage(message)

def linkedName(name):
    return translate('views', '<a href="/tell {name}" title="{name}">{name}</a>').format(name=name)

# NETWORK

def allusers():
    """Get a list of all users."""
    return state.users.values()

def allusersbut(idOrNameOrUser):
    user = getuser(idOrNameOrUser)
    if not user:
        raise RuntimeError("No user named {user}.".format(user=idOrNameOrUser))
    all = allusers()
    assert(user in all)
    all.remove(user)
    return all

def getuser(idOrName):
    """Returns a user given an id or name, or None if not valid."""
    if isinstance(idOrName, User):
        assert(idOrName in allusers())
        return idOrName
    if isinstance(idOrName, basestring):
        idOrName = idOrName.lower()
        if idOrName in state.usernames:
            return state.usernames[idOrName]
    try:
        return state.users[int(idOrName)]
    except:
        pass
    return None

def usernames():
    """Returns all the usernames."""
    return state.usernames.keys()

def changeName(user, name):
    assert(name not in state.usernames)
    if user.unnamed:
        user.unnamed = False
    if user.username in state.usernames:
        del state.usernames[user.username]
    state.usernames[name] = user
    user.username = name

def createUsername(basename=None):
    if not basename:
        basename = 'guest'
    while basename in state.usernames:
        # HACK: should move static out to system
        basename += rggMap.Map._findRandomAppend()
    return basename

def localuser():
    """The user for the local player."""
    return state.localuser

def localhandle():
    return localuser().username

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
        if client.host(connection):
            say(translate('views', 'Now listening on port {port}.').format(port=connection.port))
            import rggRemote
            rggRemote.changeUsername(client.username)
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
        client.join(connection)
        say(translate('views', 'Connecting to {host}:{port}...').format(host=connection.host, port=connection.port))

def disconnectGame():
    """Allows the user to disconnect from the internet."""
    if not client.isConnected:
        say(translate('views', "You are not connected."))
        return
    
    client.close()
    state.users = {0: localuser()}
    state.usernames = {}
    localuser().unnamed = True
    say(translate('views', "Disconnected."))

# MAPS

def switchMap(map):
    """Switches to the specified map."""
    if state.currentMap:
        state.currentMap.hide()
    state.currentMap = map
    if state.currentMap:
        state.currentMap.show()

def addMap(map):
    """Adds a map to the list and marks it current."""
    assert(not map in state.Maps)
    state.Maps.append(map)
    switchMap(map)
    # broadcast map
    #c.sendNetMessageToAll(Maps[currentMap[0]].stringform)

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
        addMap(map)

def loadMap():
    """Allows the user to load a new map."""
    filename = promptLoadFile(translate('views', 'Open Map'),
        translate('views', 'Random Game Map files (*.rgm)'))
    if not filename:
        return
    try:
        obj = jsonload(filename)
    except Exception as e:
        showErrorMessage(translate('views', "Unable to read {0}."))
        return
    map = rggMap.Map.load(obj)
    addMap(map)

def saveMap():
    """Allows the user to save the current map."""
    
    map = state.currentMap
    if state.currentMap is None:
        return
    # TODO: Probably better handled in a Map Properties dialog.
    #if promptChoice("Edit map info?", ['Yes', 'No'], 1) == 0:
    #    map.mapname = unicode(promptString("What is the name of this map?")) or map.mapname
    #    map.authorname = unicode(promptString("Who is the author of this map?")) or map.authorname
    
    filename = promptSaveFile(translate('views', 'Save Map'),
        translate('views', 'Random Game Map files (*.rgm)'))
    if not filename:
        return
    
    dumpjson(map.dump(), filename)

# DICE

def rollDice(dice):
    """Rolls the specified dice."""
    if not rggDice.isRollValid(dice):
        say(translate('views', "Invalid dice roll. See /roll documentation for help."))
    else:
        text = translate('views', "{name} rolls {roll}").format(
            name=linkedHandle(),
            roll=rggDice.roll(dice))
        say(text)
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
        state.dwidget.addMacro(dice, name)
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


def placePog(pogpath):
    """Places a pog on the map."""
    if state.currentMap is None:
        return
    state.pogPlacement = True
    state.pogPath = pogpath

# MOUSE ACTIONS

def mouseDrag(screenPosition, mapPosition, displacement):
    if state.pogSelection:
        for pog in state.pogSelection:
            pog.displace(displacement)
        # Send net message
        #c.sendNetMessageToAll('p! m ' + str(manipulatedPogs[0].ID) + ' ' + str(manipulatedPogs[0].x) + ' '
        #                              + str(manipulatedPogs[0].y))
    elif state.tilePasting:
        tile = map(lambda p, d: p // d, mapPosition, state.currentMap.tilesize)
        state.currentMap.setTile(tile, state.tilePastingIndex)

def mouseMove(screenPosition, mapPosition, displacement):
    icon = state.menu.selectedIcon
    if icon == ICON_MOVE: # moveIcon
        if state.mouseButton == BUTTON_LEFT:
            setCameraPosition(map(lambda c, d: c - d, cameraPosition(), displacement))
        return
    elif icon != ICON_SELECT: #selectIcon
        return
    
    if state.mouseButton is None:
        if state.currentMap is None:
            return
        tooltipPog = state.currentMap.findTopPog(mapPosition)
        if state.pogHover == tooltipPog:
            return
        state.pogHover = tooltipPog
        if tooltipPog is None:
            return
        displayPosition = map(lambda t, c: t - c, tooltipPog.tooltipPosition(), cameraPosition())
        displayTooltip(tooltipPog.tooltipText(), displayPosition)
    elif state.mouseButton == BUTTON_LEFT:
        return mouseDrag(screenPosition, mapPosition, displacement)

def mousePress(screenPosition, mapPosition, button):
    
    if state.currentMap is None:
        return
    
    icon = state.menu.selectedIcon
    if icon == ICON_MOVE:
        return
    elif icon != ICON_SELECT:
        return
    
    if button == BUTTON_LEFT or button == BUTTON_LEFT + BUTTON_CONTROL:
        if state.pogPlacement:
            state.pogPlacement = False
            infograb = QtGui.QPixmap(state.pogPath)
            state.currentMap.addPog(rggPog.Pog(
                mapPosition,
                (infograb.width(), infograb.height()),
                1,
                state.pogPath))
            #c.sendNetMessageToAll('p! c ' + " ".join([str(x+c.getCamX()), str(y+c.getCamY()), str(infograb.width()), str(infograb.height()), placingPog[1]]))
            return
        elif state.tilePasting:
            tile = map(lambda p, s: p // s, mapPosition, state.currentMap.tilesize)
            state.currentMap.setTile(tile, state.tilePastingIndex)
            return
    
    if button == BUTTON_LEFT:
        pog = state.currentMap.findTopPog(mapPosition)
        if pog not in state.pogSelection:
            state.pogSelection = set()
        if not pog:
            return
        state.pogSelection.add(pog)
    elif button == BUTTON_LEFT + BUTTON_CONTROL:
        pog = state.currentMap.findTopPog(mapPosition)
        if not pog:
            return
        if pog in state.pogSelection:
            state.pogSelection.remove(pog)
        else:
            state.pogSelection.add(pog)
    elif button == BUTTON_RIGHT:
        pog = state.currentMap.findTopPog(mapPosition)
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
                #c.sendNetMessageToAll('p! n ' + str(manipulatedPogs[1].ID) + ' ' + unicode(manipulatedPogs[1].name))
            elif selected == 1:
                prompt = translate('views', "Enter a generator command. See /randomname for syntax. Multi-pog compatible.")
                gentype = promptString(prompt)
                if gentype is None:
                    return
                gentype = ''.join(gentype.split()).lower()
                for selectedPog in set([pog] + list(state.pogSelection)):
                    selectedPog.name = rggNameGen.getName(gentype)
                    #c.sendNetMessageToAll('p! n ' + str(manipulatedPogs[1].ID) + ' ' + unicode(manipulatedPogs[1].name))
            elif selected == 2:
                prompt = translate('views', "Enter a layer. Pogs on higher layers are displayed over those on lower layers. Should be a positive integer. Multi-pog compatible.")
                newlayer = promptInteger(prompt, min=0, max=65535)
                if newlayer is None:
                    return
                for selectedPog in set([pog] + list(state.pogSelection)):
                    selectedPog.layer = newlayer
                    #c.sendNetMessageToAll('p! l ' + str(manipulatedPogs[1].ID) + ' ' + str(manipulatedPogs[1].layer))
        else:
            if not state.tilePasting:
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
                state.currentMap.addPog(pog)
                #c.sendNetMessageToAll('p! c ' + " ".join([str(x), str(y), str(pogsizeW), str(pogsizeH), pogsrc]))
            elif selected == 1:
                if not state.tilePasting:
                    state.tilePasting = True
                    tile = map(lambda p, c: p // c, mapPosition, state.currentMap.tilesize)
                    state.tilePastingIndex = state.currentMap.getTile(tile)
                else:
                    state.tilePasting = False
    #elif button == BUTTON_MIDDLE: #DEBUG STUFF
    #    Maps[currentMap[0]].debugMorphTile([(x+c.getCamX())/Maps[currentMap[0]].tilesize[0], (y+c.getCamY())/Maps[currentMap[0]].tilesize[1]], c.getTileCountOfImage(Maps[currentMap[0]].tileset))


def mouseRelease(screenPosition, mapPosition, button):
    state.mouseButton = None

def mouseMoveResponse(x, y):
    #print 'move', x, y
    
    screenPosition = (x, y)
    mapPosition = map(lambda p,c: p + c, screenPosition, cameraPosition())
    displacement = map(lambda p,m: p - m, screenPosition, state.mousePosition)
    
    mouseMove(screenPosition, mapPosition, displacement)
    
    state.mousePosition = screenPosition

def mousePressResponse(x, y, t):
    #print 'press', x, y, t
    
    
    screenPosition = (x, y)
    mapPosition = map(lambda p,c: p + c, screenPosition, cameraPosition())
    
    state.mousePosition = screenPosition
    state.mouseButton = t
    
    mousePress(screenPosition, mapPosition, t)
    
def mouseReleaseResponse(x, y, t):
    #print 'release', x, y, t
    
    screenPosition = (x, y)
    mapPosition = map(lambda p,c: p + c, screenPosition, cameraPosition())
    
    state.mousePosition = screenPosition
    state.mouseButton = t
    
    mouseRelease(screenPosition, mapPosition, t)

