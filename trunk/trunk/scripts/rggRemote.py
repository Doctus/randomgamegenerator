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
from rggViews import say, announce, linkedName, currentmap, getmap, allmaps
from rggViews import localhandle,localuser, getuser, allusers, allusersbut, usernames, User
from rggRPC import clientRPC, serverRPC

@serverRPC
def respondError(message, *args, **kwargs):
    """Responds as an error message.
    
    message -- the error message to send
        should be fake translated so it is
        done on the client instead of the server.
    
    Extra arguments are passed to format the translated string.
    
    """
    say(translate('error', message).format(*args, **kwargs))

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

def clientConnect(client, username):
    """Occurs when the client is ready to start sending data."""
    rggViews.renameuser(localhandle(), username)
    rggViews.closeAllMaps()
    say(translate('remote', "Welcome, {name}!".format(name=username)))

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
    rggRPC.receiveClientRPC(data)

def clientFileReceive(client, filename):
    """Occurs when the client receives data.
    
    filename -- the name of the file received
    
    """
    pass

def serverConnect(server, username):
    """Occurs when a new client joins.
    
    username -- a username for the client
    
    """
    user = User(username)
    rggViews.adduser(user)
    say(translate('remote', '{name} has joined.').format(name=username))
    for ID, map in allmaps():
        rggViews.respondMapUpdate(user, ID, map.dump())

@serverRPC
def disconnectionMessage(message, error, *args, **kwargs):
    """Special translation for a disconnection message."""
    error = translate('socket', error)
    say(translate('error', message).format(*args, error=disconnect, **kwargs))

def serverDisconnect(server, username, errorMessage):
    """Occurs when a client disconnects without being kicked.
    
    username -- a username for the client
    errorMessage -- a human-readable error message for why the connection failed
    
    """
    user = rggViews.removeuser(username)
    respondError(allusers(),
        fake.translate('remote', '{username} has left the game. {error}'),
            username=user.username, error=errorMessage)

def serverReceive(server, username, data):
    """Occurs when the server receives data.
    
    username -- a username for the client
    data - a dictionary or list of serialized data
    
    """
    #print username, getuser(username), usernames(), allusers()
    assert(getuser(username))
    #print "server received"
    rggRPC.receiveServerRPC(getuser(username), data)


def serverFileReceive(server, username, filename):
    """Occurs when the client receives data.
    
    username -- the name of the sending user
    filename -- the name of the file received
    
    """
    pass

