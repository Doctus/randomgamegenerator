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
import time, random, os, base64, sys
import rggNameGen, rggDice, rggDockWidget, rggDialogs, rggMenuBar, rggResource, rggSystem
from rggRPC import server, client, serverRPC, clientRPC
from rggJson import jsondump, jsonload, jsonappend
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
    
    alert = True
    
    mouseButton = None
    mousePosition = (0, 0)
    
    @staticmethod
    def initialize(mainApp):
        _state.menu = rggMenuBar.menuBar()
        
        #_state.twidget = rggDockWidget.debugConsoleWidget(mainWindow)
        #sys.stdout = _state.twidget
        #sys.stderr = _state.twidget
        
        _state.dwidget = rggDockWidget.diceRoller(mainWindow)
        _state.cwidget = rggDockWidget.chatWidget(mainWindow)
        #_state.icwidget = rggDockWidget.ICChatWidget(mainWindow)
        _state.uwidget = rggDockWidget.userListWidget(mainWindow)
        _state.users = {}
        _state.localuser = User(client.username)
        _state.users[client.username] = _state.localuser
        _state.keepalive = 4
        
        _state.pingTimer = QtCore.QTimer()
        _state.pingTimer.timeout.connect(keepAlive)
        _state.pingTimer.start(rggSystem.PING_INTERVAL_SECONDS*1000)
        
        _state.App = mainApp
    
def addUserToList(name, host=False):
    _state.uwidget.addUser(name, host)
    
def toggleAlerts(newValue=None):
    """Toggles messages containing the user's handle causing an alert."""
    if newValue is None:
        _state.alert = not _state.alert
    else:
        _state.alert = newValue

def toggleTimestamps(newValue=None):
    if newValue is None:
        _state.cwidget.timestamp = not _state.cwidget.timestamp
    else:
        _state.cwidget.timestamp = newValue
    if _state.cwidget.timestamp:
        jsonappend({'timestamp':'On'}, os.path.join(SAVE_DIR, "ui_settings.rgs"))
    else:
        jsonappend({'timestamp':'Off'}, os.path.join(SAVE_DIR, "ui_settings.rgs"))

def setTimestampFormat(newFormat):
    _state.cwidget.timestampformat = newFormat
    jsonappend({'timestampformat':newFormat}, os.path.join(SAVE_DIR, "ui_settings.rgs"))

def promptTimestampFormat():
    prompt = translate("views", "Please enter a new timestamp format; the default is [%H:%M:%S]")
    newFormat = promptString(prompt, inittext = _state.cwidget.timestampformat)
    if newFormat is None:
        return
    setTimestampFormat(newFormat)

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
    
def setUwidgetLocal():
    _state.uwidget.localname = localhandle()

@serverRPC    
def respondPing():
    _state.keepalive = 4
    
@clientRPC
def sendPing(user):
    respondPing(user)
    
def keepAlive():
    _state.keepalive -= 1
    if _state.keepalive == 1:
        say(translate('views', '<font color="red">Warning:</font> Connection may have been lost.'))
    if _state.keepalive == 0:
        respondPossibleDisconnect()
    sendPing()

def respondPossibleDisconnect():
    say(translate('views', '<font color="red">Connection appears to have been lost.</font>'))
    disconnectGame()
    
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
        server.setPassword(connection.password)
        updateBanlist()
        renameuser(localhandle(), connection.username)
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
        obj = jsonload(os.path.join(SAVE_DIR, "banlist.rgs"))
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
    users = {localhandle(): localuser()}
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

def saveChars():
    
    filename = promptSaveFile(translate('views', 'Save Characters'),
        translate('views', 'Random Game Character files (*.rgc)'),
        rggSystem.CHAR_DIR)
    if not filename:
        return
    
    jsondump(_state.icwidget.dump(), checkFileExtension(filename, ".rgc"))
    
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

def setLanguage(new):
    jsondump(dict(language=str(new.iconText())), os.path.join(SAVE_DIR, "lang_settings.rgs"))
    #This should ideally be translated into the newly selected language, but I have no idea how to accomplish that.
    info = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Language Changed", "".join(('Your new language setting "', str(new.iconText()), '" will take effect the next time you start RGG.')), QtGui.QMessageBox.Ok)
    info.exec_()
    
@serverRPC
def respondUserList(list):
    for item in list:
        addUserToList(item[0], item[1])
        
@serverRPC
def respondUserRemove(name):
    _state.uwidget.removeUser(name)
    
def clearUserList():
    _state.uwidget.clearUserList()

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

def generateName(generator, args):
    """Generates a random name of the specified type."""
    say(rggNameGen.getName(generator, args))