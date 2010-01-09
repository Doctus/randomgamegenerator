
import re, hashlib
from rggJson import jsondumps, jsonloads
from rggSystem import fake, translate, mainWindow, signal
from PyQt4 import QtCore, QtNetwork

# Major protocols used by the socket
PROTOCOL_UNKNOWN = 'RGG_UNKNOWN' # unidentified protocol
PROTOCOL_USER = 'RGG_USER' # RPC protocol
PROTOCOL_TRANSFER = 'RGG_TRANSFER' # file transfer protocol

PROTOCOLS = (PROTOCOL_UNKNOWN, PROTOCOL_USER, PROTOCOL_TRANSFER)

# Sent in 4kb chunks
CHUNK_SIZE = 4 * 1024
EMPTY_REGEX = re.compile('^\s*$')

PARM_COMMAND = '-command'
PARM_INTERNAL = '-internal'
PARM_ARGS = '-args'

def generateChecksum(file):
    seeked = file.seek(0)
    if not seeked or file.pos() != 0:
        raise IOError("Unable to make file seek.")
    
    hash = hashlib.md5()
    MD5_CHUNK_SIZE = 4096
    totalsize = 0
    size = file.size()
    while True:
        chunk = file.read(MD5_CHUNK_SIZE)
        totalsize += len(chunk)
        hash.update(chunk)
        if len(chunk) < MD5_CHUNK_SIZE:
            break
    
    if totalsize < size:
        raise IOError("Error reading file while calculating md5 sum.")
    
    return hash.hexdigest()

class fileData(object):
    """Some data about a file."""
    
    def __init__(self, file, filename, size, digest):
        assert(not file.isSequential())
        self.file = file
        self.filename = filename
        self.size = size
        self.digest = digest
        self.processed = 0
        self.checkHash = hashlib.md5()
    
    def generateDigest(self):
        return generateChecksum(self.file)
    
    def read(self, context):
        """Read a chunk of the file."""
        data = self.file.read(CHUNK_SIZE)
        self.processed += len(data)
        if len(data) == 0:
            message = "[{0}] Error reading sent file {filename}."
            print message.format(context, filename=self.filename)
            return None
        if self.processed > self.size:
            message = "[{0}] Sent file {filename} has too many bytes."
            print message.format(context, filename=self.filename)
            return None
        if self.file.atEnd():
            if self.processed != self.size:
                message = "[{0}] Sent file {filename} has too few bytes."
                print message.format(context, filename=self.filename)
                return None
        return data
    
    def write(self, context, chunk):
        """Write a chunk to the file."""
        self.processed += len(chunk)
        assert(len(chunk) > 0)
        assert(self.processed <= self.size)
        self.checkHash.update(chunk)
        result = self.file.write(chunk)
        
        if result != len(chunk):
            message = "[{0}] Error writing received file data {filename}."
            print message.format(context, filename=self.filename)
            return False
        
        if self.size == self.processed and self.digest != self.checkHash.hexdigest():
            message = "[{0}] Received file checksum does not match; {filename} '{sum1}' vs '{sum2}'"
            print message.format(context, filename=self.filename, sum1=self.digest, sum2=self.checkHash.hexdigest())
            return False
        
        return True
    
    def seekToBeginning(self):
        """Seeks to the beginning of the file or raises an error."""
        seeked = self.file.seek(0)
        if not seeked or self.file.pos() != 0:
            raise IOError("Unable to make file seek.")
 
class statefulSocket(object):
    """A socket wrapper that manages its connection state."""
    
    _debugcounter = 0
    
    def __init__(self, name="S-UNK", socket=None, hostname=None, port=None):
        """Initializes the socket, connecting or wrapping a connection."""
        
        self.clientside = bool(hostname)
        self.state = QtNetwork.QAbstractSocket.UnconnectedState
        self.debugid = statefulSocket._debugcounter
        statefulSocket._debugcounter += 1
        self.imbueName(name)
        self.active = False
            
        self.ready = False
        
        self.sentfile = None
        self.receivedfile = None
        
        if self.clientside:
            assert(hostname and port)
            assert(not socket)
            
            self.socket = QtNetwork.QTcpSocket(mainWindow)
        
        else:
            assert(not hostname and not port)
            assert(socket)
            assert(socket.state() == QtNetwork.QAbstractSocket.ConnectedState)
            
            self.socket = socket
            self.state = QtNetwork.QAbstractSocket.ConnectedState
            
        # Attach signals
        self.socket.error.connect(self._error)
        self.socket.hostFound.connect(self._hostFound)
        self.socket.disconnected.connect(self._disconnected)
        self.socket.stateChanged.connect(self._stateChanged)
        self.socket.readyRead.connect(self._readyRead)
        self.socket.bytesWritten.connect(self._bytesWritten)
        
        # Connect client
        if self.clientside:
            self.socket.connectToHost(hostname, port)
    
    def imbueName(self, name):
        """Changes the name of this object."""
        self.context = "{0}-{1}".format(name, self.debugid)
        
    def activate(self):
        """Activates this socket."""
        assert(not self.ready)
        self.ready = True
        self.active = True
        print "[{0}] Activated!".format(self.context)
    
    @property
    def busy(self):
        """Whether the socket is busy sending data already."""
        return (not self.ready or self.sentfile is not None or self.receivedfile is not None)
    
    @property
    def closed(self):
        """Whether the socket is already closed."""
        return (self.state == QtNetwork.QAbstractSocket.UnconnectedState)
    
    def close(self):
        """Disconnect all network activity."""
        if not self.closed:
            self.ready = False
            self.state = QtNetwork.QAbstractSocket.UnconnectedState
            if self.sentfile:
                self.sentfile.file.close()
                self.sentfile = None
            if self.receivedfile:
                self.receivedfile.file.close()
                self.receivedfile = None
            if self.clientside:
                self.socket.disconnectFromHost()
            else:
                self.socket.close()
            print "[{0}] Closed connection.".format(self.context)
    
    def _closeWithPrejudice(self):
        """Close the socket, reporting a disconnection message if not already closed."""
        if self.closed:
            return
        oldState = self.state
        self.close()
        self.disconnected.emit(self, self.disconnectionError(oldState, self.socket.error()))
    
    def _respondToSocketError(self, header, result, length=0, text=None):
        """Responds to a read or write error.
        
        header -- "Read Error" or "Write Error"
        result -- the number of bytes read or negative to indicate error
        length -- the length of the text if text is not provided
        text -- if human-readable, the message text
        
        """
        if text:
            length = len(text)
            ERROR_LENGTH = 12
            if len(text) > ERROR_LENGTH:
                text = text[:ERROR_LENGTH]
            text = "'{0}' ".format(text)
        else:
            text = ''
        
        assert(length > 0)
        assert(length != result)
        
        if result < 0:
            message = "[{context}] {header}: could not process message {sample}length {length}"
        else:
            message = "[{context}] {header}: partial message {sample}length {partial}/{length}"
        sample = statefulSocket._sampleText(serial)
        print message.format(context=self.context, sample=text, length=len(serial), partial=result)
        
        self._closeWithPrejudice()
        
    def disconnectionError(self, previousState, err):
        """Find a human-readable error message for when the connection fails."""
        
        s = QtNetwork.QAbstractSocket
        
        # Messages for what happens when we weren't yet connected
        if self.clientside:
            if previousState != s.ConnectedState:
                # ConnectionRefusedError could mean either refused or timed out
                # SocketTimeoutError is probably not relevant here
                if err == s.ConnectionRefusedError or err == s.SocketTimeoutError:
                    return fake.translate('socket', 'The connection was refused or timed out.')
                # Couldn't look up the IP or url that the user specified (didn't reach DNS)
                if err == s.HostNotFoundError:
                    return fake.translate('socket', 'The system could not find the specified host address.')
                # Local firewall or privileges denied access to sockets
                if err == s.SocketAccessError:
                    return fake.translate('socket', 'The program was denied access to network hardware.')
                # Lot of stuff that probably won't apply; SSL, Proxies, etc
                # Mostly they mean there's a cable unplugged or something
                return fake.translate('socket', 'The program could not find the specified host.')
            # Connected but not ready
            if not self.active:
                return fake.translate('socket', 'The server refused the connection.')
        
        # Client gracefully quit
        if err == s.RemoteHostClosedError:
            if self.clientside:
                return fake.translate('socket', 'The server closed the connection.')
            return fake.translate('socket', 'The client closed the connection.')
        # Client died without saying anything
        if err == s.SocketTimeoutError:
            return fake.translate('socket', 'The connection timed out.')
        
        # Something random happened
        if self.clientside:
            return fake.translate('socket', 'You have been disconnected.')
        return fake.translate('socket', 'The client was disconnected.')
    
    # SENDING
    
    # Memoization of previously sent value because
    # server data is often sent to multiple destinations
    _memoizeKey = None
    _memoizeData = None
    
    @staticmethod
    def _serialize(data):
        """Serialize an object to a message that can be sent."""
        serial = jsondumps(data)
        return QtCore.QByteArray(serial + '\n')
    
    def _rawsend(self, serial):
        """Sends serialized data."""
        result = self.socket.write(serial)
        if result == len(serial):
            # I guess flush forces synchronous sending.
            #self.socket.flush()
            return True
            
        self._respondToSocketError("Write Error", result, text=serial)
        return False
    
    def _rawreadline(self):
        """Reads a line from the socket."""
        assert(self.socket.canReadLine())
        data = self.socket.readLine()
        if len(data) > 0:
            assert(data[-1] == '\n')
            return data
        
        self._respondToSocketError("Line read Error", -1, length=0)
        return None
    
    def _rawread(self, length):
        """Reads a line from the socket."""
        assert(length > 0)
        data = self.socket.read(length)
        if len(data) == length:
            return data
        
        self._respondToSocketError("Read Error", -1, length=length)
        return None
    
    def sendObject(self, data):
        """Sends a JSON object over the wire.
        
        Precondition: self.ready
        
        """
        assert(not self.busy or not self.ready)
        
        if statefulSocket._memoizeKey is data:
            serial = statefulSocket._memoizeData
            # TODO: This check negates the memoization
            # should uncomment for release.
            assert(self._serialize(data) == serial)
        else:
            serial = statefulSocket._serialize(data)
            statefulSocket._memoizeKey = data
            statefulSocket._memoizeData = serial
        
        self._rawsend(serial)
    
    def sendMessage(self, command, **kwargs):
        """Sends a message across the wire."""
        assert(command is not None)
        obj = {
            PARM_COMMAND: command,
            PARM_INTERNAL: True,
        }
        for key, arg in kwargs.items():
            obj[key] = arg
        self.sendObject(obj)
    
    def sendFile(self, filedata):
        """Begins sending file data directly over the wire.
        
        filedata -- an open filedata object
        
        """
        assert(self.ready)
        assert(not self.busy)
        
        filedata.seekToBeginning()
        self.sentfile = filedata
        self.updateSend()
    
    def updateSend(self):
        """Continues sending the current send file."""
        if not self.sentfile:
            return
        
        while self.socket.bytesToWrite() < CHUNK_SIZE:
            data = self.sentfile.read(self.context)
            if data is None:
                self._closeWithPrejudice()
                return
            if not self._rawsend(data):
                return
            if self.sentfile.file.atEnd():
                sentfile = self.sentfile
                self.sentfile = None
                sentfile.file.close()
                self.fileSent.emit(self, sentfile.filename)
                return
    
    # RECEIVING
    
    def receiveFile(self, filedata):
        """Writes the next size bytes to the specified file."""
        
        filedata.seekToBeginning()
        self.receivedfile = filedata
        self.updateReceive()
    
    def updateReceive(self):
        """Parses incoming data into messages or objects."""
        
        while True:
            if self.receivedfile is not None:
                length = min(CHUNK_SIZE, self.receivedfile.size - self.receivedfile.processed)
                if self.socket.bytesAvailable() < length:
                    return
                data = self._rawread(length)
                if data is None:
                    return
                if not self.receivedfile.write(self.context, data):
                    self._closeWithPrejudice()
                    return
                if self.receivedfile.size == self.receivedfile.processed:
                    receivedfile = self.receivedfile
                    self.receivedfile = None
                    receivedfile.file.close()
                    self.fileReceived.emit(self, receivedfile.filename)
                    # May be more available
                    continue
            else:
                if not self.socket.canReadLine():
                    return
                serial = self._rawreadline()
                if serial is None:
                    return
                # Allow empty lines
                if EMPTY_REGEX.match(serial):
                    continue
                try:
                    obj = jsonloads(unicode(serial))
                except:
                    self._respondToSocketError("JSON Error", result, text=serial)
                    return
                self.receiveObject(obj)
    
    def receiveObject(self, obj):
        """Look for internal commands or pass directly to object handler."""
        if obj.get(PARM_INTERNAL) == True:
            command = obj.get(PARM_COMMAND)
            if command is not None:
                del obj[PARM_COMMAND]
            del obj[PARM_INTERNAL]
            self.commandReceived.emit(self, command, obj)
        else:
            self.objectReceived.emit(self, obj)
    
    # SIGNALS
    
    connected = signal(object, doc=
        """Called when the socket becomes ready to start sending;
        when ready becomes True.
        
        Happens when a remote socket identifies itself as a user or
        a local socket receives a connection notification from the server.
        
        socket -- this socket
        
        """
    )
    
    disconnected = signal(object, basestring, doc=
        """Called when the socket disconnects or fails to connect.
        
        Not called when disconnected manually (through close()).
        
        socket -- this socket
        errorMessage -- the untranslated reason the connection failed
        
        """
    )
    
    objectReceived = signal(object, dict, doc=
        """Called when data is received over the wire.
        
        socket -- this socket
        data -- the data received
        
        """
    )
    
    commandReceived = signal(object, basestring, dict, doc=
        """Called when data is received over the wire.
        
        socket -- this socket
        command -- the command to carry out
        arguments -- the keyword arguments
        
        """
    )
    
    fileSent = signal(object, basestring, doc=
        """Called when a file is done sending.
        
        socket -- this socket
        name -- the name of the file
        
        """
    )
    
    fileReceived = signal(object, basestring, doc=
        """Called when a file is done receiving.
        
        socket -- this socket
        name -- the name of the file
        
        """
    )
    
    def _receive(self):
        """Call to make the client receive data."""
        self.updateReceive()
    
    def _readyRead(self):
        """Called when data is ready."""
        self.updateReceive()
    
    def _bytesWritten(self, bytes):
        """Occurs when some data is eaten out of the buffer."""
        self.updateSend()
    
    def _disconnected(self):
        """Called when disconnected from the server."""
        print "[{0}] Disconnected.".format(self.context)
        # TODO: Should we delete the socket here?
        self.socket.deleteLater()
    
    def _stateChanged(self, newState):
        """Detects connection changes."""
        oldState = self.state
        self.state = newState
        #print "State: {0} {1}".format(oldState, newState)
        if oldState == newState:
            return
        
        s = QtNetwork.QAbstractSocket
        
        if self.clientside:
            if newState == s.HostLookupState:
                print "[{0}] Looking up host...".format(self.context)
                return
            if newState == s.ConnectingState:
                print "[{0}] Connecting...".format(self.context)
                return
            if newState == s.ConnectedState:
                print "[{0}] Connected. Awaiting activation...".format(self.context)
                self.connected.emit(self)
                return
        
        if oldState not in (s.HostLookupState, s.ConnectingState, s.ConnectedState):
            return
        
        if oldState == s.UnconnectedState:
            return
        print "[{context}] Closing error #{id} {message}".format(
            context=self.context, id=self.socket.error(), message=self.socket.errorString()) 
        self.state = s.ConnectedState
        self.close()
        self.disconnected.emit(self, self.disconnectionError(oldState, self.socket.error()))
    
    def _hostFound(self):
        """Responds to host name being resolved. (DNS)"""
        # Apparently the resolved host is still not available
        #print "[{0}] Host found: {1} resolved to {2}:{3}".format(
        #    self.context, self.socket.peerName(), self.socket.peerAddress().toString(), self.socket.peerPort())
    
    def _error(self, err):
        """Writes errors to the console."""
        print "[{context}] ERROR #{id} {message}".format(
            context=self.context, id=self.socket.error(), message=self.socket.errorString()) 
