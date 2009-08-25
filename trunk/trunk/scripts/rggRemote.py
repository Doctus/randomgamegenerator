'''
rggRemote - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Remote views.

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

import re
import rggViews, rggRPC
from rggSystem import translate, fake
from rggViews import say, announce, linkedName
from rggViews import localuser, getuser, allusers, allusersbut, usernames, User
from rggRPC import clientRPC, serverRPC

VALID_USERNAME = re.compile('^\w+$')

@serverRPC
def respondError(message, *args, **kwargs):
    """Responds as an error message.
    
    message -- the error message to send
        should be fake translated so it is
        done on the client instead of the server.
    
    Extra arguments are passed to format the translated string.
    
    """
    say(translate('remote', message).format(*args, **kwargs))

@serverRPC
def respondNewUser(username):
    say(translate('remote', '{name} has joined.').format(name=username))

@serverRPC
def respondArrival(username):
    localuser().username = username
    say(translate('remote', 'Welcome, {name}.').format(name=username))

@serverRPC
def respondUsernameChange(oldname, newname):
    say(translate('remote', '{oldname} is now known as {newname}.').format(oldname=oldname, newname=newname))

@serverRPC
def respondSenderUsernameChange(oldname, newname):
    say(translate('remote', 'You are now known as {newname}.').format(oldname=oldname, newname=newname))

@clientRPC
def changeUsername(user, username):
    username = username.lower()
    
    # Make sure there are at least no spaces
    if not VALID_USERNAME.match(username):
        respondError(user, fake.translate('remote', '{username} contains invalid characters.'), username=username)
        if not user.unnamed:
            return
        username = rggViews.createUsername()
    if user.username == username:
        respondError(user, fake.translate('remote', 'You are already known as {username}.'), username=username)
        return
    #print username, usernames(), username in usernames()
    if username in usernames():
        respondError(user, fake.translate('remote', '{username} is already taken.'), username=username)
        if not user.unnamed:
            return
        username = rggViews.createUsername(username)
    
    oldName = user.username
    unnamed = user.unnamed
    rggViews.changeName(user, username)
    if unnamed:
        respondNewUser(allusersbut(user), username)
        if user != localuser():
            respondArrival(user, username)
    else:
        del state.usernames[oldName]
        respondUsernameChange(allusersbut(user), oldName, username)
        if user != localuser():
            respondSenderUsernameChange(user, oldName, username)

@serverRPC
def respondSay(username, message):
    say(translate('remote', '{name}: {sayText}').format(
        name=linkedName(username),
        sayText=message))

@clientRPC
def sendSay(user, message):
    respondSay(allusers(), user.username, message)

@serverRPC
def respondEmote(username, message):
    say(translate('remote', '<i>{name} {emote}</i>').format(
        name=linkedName(username),
        emote=message))

@clientRPC
def sendEmote(user, message):
    respondEmote(allusers(), user.username, message)

@serverRPC
def respondWhisperSender(target, message):
    say(translate('remote', 'To {username}: {message}').format(
        username=linkedName(target),
        message=message))

@serverRPC
def respondWhisperTarget(sender, message):
    say(translate('remote', '{username} whispers: {message}').format(
        username=linkedName(sender),
        message=message))

@clientRPC
def sendWhisper(user, target, message):
    target = target.lower()
    targetuser = getuser(target)
    if not targetuser:
        respondError(user, fake.translate('remote', '{target} does not exist.'), target=target)
    else:
        respondWhisperSender(user, targetuser.username, message)
        respondWhisperTarget(targetuser, user.username, message)
    
# LOW-LEVEL NETWORKING

def clientConnect(client):
    """Occurs when the client is ready to start sending data."""
    say(translate('remote', "Connected!"))
    changeUsername(client.username)
    #TODO change username to client.username

def clientDisconnect(client, errorMessage):
    """Occurs when the client connection disconnects without being told to.
    
    errorMessage -- a human-readable error message for why the connection failed
    
    """
    say(translate('remote', "Disconnected. {0}").format(errorMessage))

def clientReceive(client, data):
    """Occurs when the client receives data.
    
    data -- a dictionary or list of serialized data
    
    """
    #print "client received"
    rggRPC.receiveClientRPC(client, data)

def serverConnect(server, id):
    """Occurs when a new client joins.
    
    id -- a numeric id for the client
    
    """
    if id in rggViews.state.users:
        print "Server: duplicate id ({0}) connected.".format(id)
        return
    rggViews.state.users[id] = User(id)
    # TODO: Something here?

def serverDisconnect(server, id, errorMessage):
    """Occurs when a client disconnects without being kicked.
    
    id -- a numeric id for the client
    errorMessage -- a human-readable error message for why the connection failed
    
    """
    if id not in rggViews.state.users:
        print "Server: unknown id ({0}) disconnected: {1}".format(id, errorMessage)
        return
    # TODO: Something here?
    del rggViews.state.users[id]

def serverReceive(server, id, data):
    """Occurs when the server receives data.
    
    id -- a numeric id for the client
    data - a dictionary or list of serialized data
    
    """
    if id not in rggViews.state.users:
        print "Server: Data for unknown id ({0}) received: {1}".format(id, repr(data))
        return
    #print "server received"
    rggRPC.receiveServerRPC(rggViews.state.users[id], data)


