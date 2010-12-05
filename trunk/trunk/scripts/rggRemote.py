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

import re, os
import rggViews, rggRPC, rggResource
from rggSystem import translate, fake, makePortableFilename, PORTRAIT_DIR
from rggViews import say, ICSay, announce, linkedName, currentmap, getmap, allmaps
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
def respondDice(username, message):
    say(translate('remote', '{sayText}').format(
        sayText=message))
    ICSay(translate('remote', '{sayText}').format(                                                       
        sayText=message))
        
@clientRPC
def sendDice(user, message):
    respondDice(allusers(), user.username, message)

@serverRPC
def respondSay(username, message):
    say(translate('remote', '{name}: {sayText}').format(
        name=linkedName(username),
        sayText=message))

@clientRPC
def sendSay(user, message):
    respondSay(allusers(), user.username, message)
    
@serverRPC
def respondICSay(chname, message, portrait):
    if len(portrait) > 1:
        portfile = rggResource.crm.translateFile(makePortableFilename(os.path.join(PORTRAIT_DIR, portrait)), rggResource.RESOURCE_IMAGE)
        ICSay(translate('remote', '<table><tr><td><img src="{port}" width="64" height="64"></td><td>{name}: {sayText}</td></tr></table><br />').format(
            port=portfile,                                                        
            name=linkedName(chname),
            sayText=message))
    else:
        ICSay(translate('remote', '{name}: {sayText}</p>').format(                                                       
        name=linkedName(chname),
        sayText=message))

@clientRPC
def sendICSay(user, message, chname, portrait):
    rggResource.crm.listen(portrait, rggResource.RESOURCE_IMAGE, rggResource.crm, None)
    respondICSay(allusers(), chname, message, portrait)

@serverRPC
def respondEmote(username, message):
    say(translate('remote', '<i>{name} {emote}</i>').format(
        name=linkedName(username),
        emote=message))

@clientRPC
def sendEmote(user, message):
    respondEmote(allusers(), user.username, message)

@serverRPC
def respondICEmote(chname, message, portrait):
    if len(portrait) > 1:
        portfile = makePortableFilename(os.path.join(PORTRAIT_DIR, portrait))
        ICSay(translate('remote', '<table><tr><td><img src="{port}" width="64" height="64"></td><td><i>{name} {emote}</i></td></tr></table><br />').format(
            port=portfile,                                                                      
            name=linkedName(chname),
            emote=message))
    else:
        ICSay(translate('remote', '<i>{name} {emote}</i>').format(                                                                    
            name=linkedName(chname),
            emote=message))
        

@clientRPC
def sendICEmote(user, message, chname, portrait):
    respondICEmote(allusers(), chname, message, portrait)

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

@serverRPC
def respondUserJoin(username):
    say(translate('remote', "{name} has joined!").format(name=username))

# LOW-LEVEL NETWORKING

def clientConnect(client, username):
    """Occurs when the client is ready to start sending data."""
    #print "Client connected."
    rggViews.renameuser(localhandle(), username)
    rggViews.closeAllMaps()
    say(translate('remote', "Welcome, {name}!").format(name=username))

def clientDisconnect(client, errorMessage):
    """Occurs when the client connection disconnects without being told to.
    
    errorMessage -- a human-readable error message for why the connection failed
    
    """
    #print "Client disconnected."
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
    #print "Server found user."
    user = User(username)
    rggViews.adduser(user)
    respondUserJoin(allusersbut(user), username)
    for ID, map in allmaps():
        rggViews.respondMapCreate(user, ID, map.dump())

@serverRPC
def disconnectionMessage(message, error, *args, **kwargs):
    """Special translation for a disconnection message."""
    #print "Server dropped user."
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

