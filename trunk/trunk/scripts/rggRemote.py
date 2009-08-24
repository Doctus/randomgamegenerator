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

import rggViews, rggRPC
from rggSystem import translate
from rggViews import say, announce, linkedName, getuser, allusers, User
from rggRPC import clientRPC, serverRPC

@serverRPC
def receiveSay(username, message):
    say(translate('remote', '{name}: {sayText}').format(
        name=linkedName(username),
        sayText=message))

@clientRPC
def sendSay(user, message):
    receiveSay(allusers(), user.username, message)

def sendEmote(message):
    action = translate('views', '<i>{name} {emote}</i>').format(
        name=linkedHandle(),
        emote=message)
    say(action)
    #c.sendNetMessageToAll('T!' + unicode(action))

def sendWhisper(name, message):
    pass
    #if c.isServer():
        #if not c.sendNetMessageToHandle('w! ' + c.getLocalHandle() +
        #                         ' ' + unicode(mesg), target):
        #    cwidget.insertMessage("Error: could not find that handle.")
        #else:
        #    cwidget.insertMessage('To ' + unicode(target) + ': ' +
        #                unicode(mesg))
    #else:
    #    cwidget.insertMessage('To ' + unicode(target) + ': ' +
    #                    unicode(mesg))
        #c.sendNetMessageToAll('W! ' + target + ' ' + unicode(mesg))

# LOW-LEVEL NETWORKING

def clientConnect(client):
    """Occurs when the client is ready to start sending data."""
    say(translate('remote', "Connected!"))
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


