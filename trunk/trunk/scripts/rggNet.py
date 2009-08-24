'''
rggNet - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Handling of network connections.

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
from rggJson import jsondumps, jsonloads
from rggSystem import translate, mainWindow, signal
from PyQt4 import QtCore, QtNetwork

WHITESPACE = re.compile('^\s*$')

class ConnectionData(object):
    """Data used to create a network connection."""
    
    def __init__(self, host=None, port=6812, username=translate('net', 'Anonymous', 'default connection name')):
        self.host = host or localHost()
        self.port = port
        self.username = username

class JsonClient(object):
    """A client that communicates with a server."""
    
    def __init__(self):
        self.debugcounter = 0
        self.debugname = 'CD'
        self.socket = None
        self.server = None
        self.username = None
        self.state = QtNetwork.QAbstractSocket.UnconnectedState
        self.id = 0
    
    def _setDebugName(self):
        """Sets the debug name."""
        self.debugname = 'C{0}:{1}'.format(self.id, self.debugcounter)
        self.debugcounter += 1
    
    @property
    def isConnected(self):
        return bool(self.isClient or self.server)
    
    @property
    def isClient(self):
        return self.state == QtNetwork.QAbstractSocket.ConnectedState
    
    def host(self, connectionData):
        """Starts the network as a server."""
        if self.isConnected:
            raise RuntimeError("Already connected.")
        self._setDebugName()
        self.username = connectionData.username
        self.server = self._server
        result = self.server.listen(connectionData)
        if not result:
            self.close()
        return result
        
    def join(self, connectionData):
        """Starts the network as a client."""
        if self.isConnected:
            raise RuntimeError("Already connected.")
        self.id = 0
        self._setDebugName()
        self.username = connectionData.username
        socket = QtNetwork.QTcpSocket(mainWindow)
        context = self.debugname
        socket.error.connect(lambda err: self._error(context, socket, err))
        socket.hostFound.connect(lambda: self._hostFound(context, socket))
        socket.connected.connect(lambda: self._connected(context, socket))
        socket.disconnected.connect(lambda: self._disconnected(context, socket))
        socket.stateChanged.connect(lambda state: self._stateChanged(context, socket, state))
        socket.readyRead.connect(lambda: self._readyRead(context, socket))
        
        self.socket = socket
        socket.connectToHost(connectionData.host, connectionData.port)
    
    def close(self):
        """Disconnect all network activity."""
        self.state = QtNetwork.QAbstractSocket.UnconnectedState
        self.debugname = 'CD'
        if self.socket:
            socket = self.socket
            self.socket = None
            socket.disconnectFromHost()
            print "[{0}] Closed connection.".format(self.debugname)
        elif self.server:
            server = self.server
            self.server = None
            server.close()
        
    def send(self, data):
        """Call to send an object over the wire."""
        if self.isClient:
            dumpMessage(self.debugname, self.socket, data)
        else:
            self._server._receive(self.id, data)
    
    connected = signal(object, doc=
        """Called when the client is ready to start sending;
        when isConnected becomes True.
        
        Never called when hosting; can send immediately in that case.
        
        client -- this client
        
        """
    )
    
    disconnected = signal(object, basestring, doc=
        """Called when the client disconnects or fails to connect.
        
        Not called when disconnected manually (through close()).
        
        Never called when hosting; you will never be disconnected automatically.
        
        client -- this client
        errorMessage -- the reason the connection failed
        
        """
    )
    
    received = signal(object, dict, doc=
        """Called when an object is received over the wire.
        
        client -- this client
        data -- the data received
        
        """
    )
    
    def _receive(self, data):
        """Call to make the client receive data."""
        self.received.emit(self, data)
    
    def _readyRead(self, context, socket):
        """Called when data is ready."""
        if socket is not self.socket:
            return
        while True:
            data = loadMessage(self.debugname, socket)
            if data is None:
                return
            self._receive(data)
    
    def _connected(self, context, socket):
        """Called when connected to the server."""
        if socket is not self.socket:
            return
    
    def _disconnected(self, context, socket):
        """Called when disconnected from the server."""
        print "[{0}] Disconnected.".format(context)
        # TODO: Should we delete the socket here?
        #socket.deleteLater()
        
    def _stateChanged(self, context, socket, newState):
        """Detects connection changes."""
        if socket is not self.socket:
            return
        
        oldState = self.state
        self.state = newState
        if oldState == newState:
            return
        
        s = QtNetwork.QAbstractSocket
        
        if newState == s.HostLookupState:
            print "[{0}] Looking up host...".format(context)
            return
        elif newState == s.ConnectingState:
            print "[{0}] Connecting...".format(context)
            return
        elif newState == s.ConnectedState:
            print "[{0}] Connected.".format(context)
            self.connected.emit(self)
            return
        elif oldState not in (s.HostLookupState, s.ConnectingState, s.ConnectedState):
            return
        
        # Closing connection, unconnected, or some weird state hit; assume a disconnect
        # Discover disconnection reason
        print "[{0}] Disconnected: {1} {2} {reason}".format(
            context, oldState, newState, reason=socket.errorString())
        
        err = socket.error()
        
        # Messages for what happens when we weren't yet connected
        if oldState != s.ConnectedState:
            # ConnectionRefusedError could mean either refused or timed out
            # SocketTimeoutError is probably not relevant here
            if err == s.ConnectionRefusedError or err == s.SocketTimeoutError:
                message = translate('net', 'The connection was refused or timed out.')
            # Couldn't look up the IP or url that the user specified (didn't reach DNS)
            elif err == s.HostNotFoundError:
                message = translate('net', 'The system could not find the specified host address.')
            # Local firewall or privileges denied access to sockets
            elif err == s.SocketAccessError:
                message = translate('net', 'The program was denied access to network hardware.')
            # Lot of stuff that probably won't apply; SSL, Proxies, etc
            # Mostly they mean there's a cable unplugged or something
            else:
                message = translate('net', 'The program could not find the specified host.')
        
        # Messages for when we were connected
        else:
            # Server quit gracefully or kicked you out
            if err == s.RemoteHostClosedError:
                message = translate('net', 'The server closed the connection.')
            # Server died without saying anything
            elif err == s.SocketTimeoutError:
                message = translate('net', 'The connection timed out.')
            # Something random happened
            else:
                message = translate('net', 'You have been disconnected.')
        self.disconnected.emit(self, message)
    
    def _hostFound(self, context, socket):
        """Responds to host name being resolved. (DNS)"""
        if socket is not self.socket:
            return
        # Apparently it's still not available
        #print "[{0}] Host found: {1} resolved to {2}:{3}".format(
        #    context, socket.peerName(), socket.peerAddress().toString(), socket.peerPort())
    
    def _error(self, context, socket, err):
        """Writes errors to the console."""
        print "[{context}] ERROR {message}".format(
            context=context, message=socket.errorString()) 

class RemoteClient(object):
    """A client on a different computer."""
    
    def __init__(self, server, socket):
        """Initializes the client."""
        self.socket = socket
        self.server = server
        self.id = -1
        self.state = self.socket.state()
        socket.readyRead.connect(self._readyRead)
        socket.stateChanged.connect(self._stateChanged)
        socket.disconnected.connect(self._disconnected)
        socket.error.connect(self._error)
    
    @property
    def isConnected(self):
        return self.state == QtNetwork.QAbstractSocket.ConnectedState
    
    # NOTE: These are reversed for ducking.
    def send(self, data):
        """Called when data is sent from the client."""
        self.server._receive(self.id, data)
    
    def _receive(self, data):
        """Called to make the client receive data."""
        if not self.isConnected:
            raise RuntimeError("Not connected.")
        dumpMessage("C{0}".format(self.id), self.socket, data)
    
    def close(self):
        """Close the connection."""
        if self.isConnected:
            self.socket.close()
    
    def _readyRead(self):
        """Called when data is ready."""
        while True:
            data = loadMessage('C{0}'.format(self.id), self.socket)
            if data is None:
                return
            self.send(data)
    
    def _disconnected(self, context, socket):
        """Called when disconnected from the server."""
        print "[C{0}] Disconnected.".format(self.id)
        # TODO: Should we delete the socket here?
        #socket.deleteLater()
        
    def _stateChanged(self, newState):
        """Detects connection changes."""
        
        oldState = self.state
        self.state = newState
        if oldState == newState:
            return
        
        s = QtNetwork.QAbstractSocket
        
        # Closing connection, unconnected, or some weird state hit; assume a disconnect
        # Discover disconnection reason
        print "[C{0}] Disconnected: {1} {2} {reason}".format(
            self.id, oldState, newState, reason=socket.errorString())
        
        err = self.socket.error()
        
        # Client gracefully quit
        if err == s.RemoteHostClosedError:
            message = translate('net', 'The client closed the connection.')
        # Client died without saying anything
        elif err == s.SocketTimeoutError:
            message = translate('net', 'The connection timed out.')
        # Something random happened
        else:
            message = translate('net', 'The client was disconnected.')
        
        self.server._disconnect(self.id, message)
    
    def _error(self, err):
        """Writes errors to the console."""
        print "[C{context}] ERROR {message}".format(
            context=self.id, message=self.socket.errorString()) 
    

class JsonServer(object):
    """A server that processes JSON messages."""
    
    def __init__(self, client):
        self.server = None
        self.clients = {0: client}
        self.id = 1
        self._client = client
        client._server = self
    
    @property
    def isConnected(self):
        return bool(self.server)
    
    def addClient(self, client):
        """Adds a client to the list."""
        assert(not client in self.clients.values())
        client.id = self.id
        self.id += 1
        self.clients[client.id] = client
    
    def listen(self, connectionData):
        """Starts the server. Returns True on success, else False."""
        if self.isConnected:
            raise RuntimeError("Already connected.")
        
        server = QtNetwork.QTcpServer(mainWindow)
        server.newConnection.connect(self._newConnection)
        
        result = server.listen(QtNetwork.QHostAddress(), connectionData.port)
        if result:
            print "[Server] Listening on {0}:{1}".format(server.serverAddress().toString(), server.serverPort())
            self.server = server
        else:
            print "[Server] Error on listen attempt; {0}".format(server.errorString())
            # TODO: Should we delete the server here?
            #server.deleteLater()
            
        return result
    
    def close(self):
        if self.isConnected:
            server = self.server
            self.server = None
            for client in self.clients:
                client.close()
            self.clients = {0: self._client}
            self.id = 1
            server.close()
            # TODO: Should we delete the server here?
            #server.deleteLater()
    
    def idExists(self, id):
        """Check whether the id exists."""
        return id in self.clients
    
    def send(self, id, data):
        """Call to send an object over the wire."""
        if not self.idExists(id):
            raise RuntimeError("Invalid id {0}".format(id))
        client = self.clients[id]
        client._receive(data)
    
    def broadcast(self, data, exclude=None):
        """Call to send an object over the wire.
        
        exclude -- exclude a list of ids
        """
        for client in self.clients:
            if exclude and client.id in exclude:
                continue
            client._receive(data)
    
    def _disconnect(self, id, errorMessage):
        """Receive the specified data."""
        assert(id != 0)
        del self.clients[id]
        return self.disconnected.emit(self, id, errorMessage)
    
    def _receive(self, id, data):
        """Receive the specified data."""
        return self.received.emit(self, id, data)
    
    connected = signal(object, int, doc=
        """Called when a client connects to the server.
        
        server -- this server
        id -- the id of the client
        
        """
    )
    
    disconnected = signal(object, int, basestring, doc=
        """Called when a client disconnects from the server.
        
        Not called when disconnected manually (through close()).
        
        Never called when hosting; you will never be disconnected automatically.
        
        server -- this server
        id -- the id of the client
        errorMessage -- the reason the connection failed
        
        """
    )
    
    received = signal(object, int, dict, doc=
        """Called when an object is received from a client over the wire.
        
        server -- this server
        id -- the id of the client
        data -- the data received
        
        """
    )
    
    def _newConnection(self):
        """Responds to a new connection occurring."""
        if not self.server:
            return
        while self.server.hasPendingConnections():
            socket = self.server.nextPendingConnection()
            assert(socket)
            client = RemoteClient(self, socket)
            self.addClient(client)
            print "[Server] Client connected: {1}:{2}".format(
                socket.peerName(), socket.peerAddress().toString(), socket.peerPort())
            self.connected.emit(self, client.id)

def localHost():
    """Gets the name of the local machine."""
    return unicode(QtNetwork.QHostInfo.localHostName())

ERROR_LENGTH = 12
def sampleError(text):
    if len(text) < ERROR_LENGTH:
        return text
    return text[:ERROR_LENGTH]

# Simple one-item identity-based cache to avoid generating JSON on identical requests
# Will not work if contents are altered
memoizeKey = None
memoizeData = None

def dumpMessage(context, socket, data):
    """Attempts to dump the specified data into the socket."""
    global memoizeKey
    global memoizeData
    if memoizeKey is data:
        # NOTE: Could be expensive; can remove for speed
        #assert(hash(data) == hash(memoizeKey))
        serial = memoizeData
    else:
        serial = jsondumps(data)
        serial = QtCore.QByteArray('\n' + serial + '\n')
        memoizeKey = data
        memoizeData = serial
    result = socket.write(serial)
    if result == len(serial):
        #print "Socket write: [{context}] {0}".format(sampleError(serial), context=context)
        socket.flush()
        return
    sample = sampleError(serial)
    if result == -1:
        print "Socket write error: {context} could not send data '{1}' length {0}.".format(len(serial), sample, context=context)
    else:
        print "Socket write error: {context} sent partial message '{1}' length {0}.".format(len(serial), sample, context=context)
    
def loadMessage(context, socket):
    """Attempts to load a JSON object or array from the socket.
    
    returns None if not ready
    """
    serial = ""
    while WHITESPACE.match(serial):
        if not socket.canReadLine():
            return None
        serial = socket.readLine(0)
        #print "Socket read: [{context}] {0}".format(sampleError(serial), context=context)
        if not serial:
            print "Socket read error: {context} unexpectedly could not read line".format(context=context)
            return None
        assert(len(serial) > 0 and serial[-1] == '\n')
    try:
        #print unicode(serial)
        obj = jsonloads(unicode(serial))
        #print repr(obj)
    except:
        sample = sampleError(serial)
        print "Socket read error: {context} read invalid JSON '{1}' length {0}".format(len(serial), sample, context=context)
        return loadMessage(socket) # Don't want to report None if there's more to read
    return obj

