'''
resource mapping - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Qt and C++ servces.

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

import sys, random, weakref
import os, os.path
from collections import defaultdict
from PyQt4 import QtCore, QtGui
from rggRPC import client, server, clientRPC, serverRPC
from rggSystem import reloadImage

RESOURCE_IMAGE = "image"
RESOURCE_SOUND = "sound"

STATE_UNKNOWN = "unknown" # Nobody's asked about this file yet
STATE_READY = "ready" # Ready on the server; currently being requested by client or already gotten
STATE_LOADING = "loading" # Loading on the server; nothing doing on the client
STATE_INVALID = "invalid" # Not present on server; assumed missing by client
VALID_STATES = (STATE_UNKNOWN, STATE_READY, STATE_LOADING, STATE_INVALID)

# DEFAULT MEDIA (feel free to change)
RESOURCE_INVALID = {
    RESOURCE_IMAGE: "invalid.png",
    RESOURCE_SOUND: "silent.wav"
}
RESOURCE_LOADING = {
    RESOURCE_IMAGE: "loading.png",
    RESOURCE_SOUND: "silent.wav"
}

KEEP_ALIVE_FIELD = '_keepWeakReferenceAlive'

class clientResourceMapper(object):
    """Clientside handling of resources."""
    
    def __init__(self, client):
        """Initializes this resource mapper."""
        self._status = defaultdict(lambda: STATE_UNKNOWN)
        self._exists = defaultdict(bool)
        self._listeners = defaultdict(list)
        client.fileReceived.connect(self._onFileReceived)
        client.fileFailed.connect(self._onFileFailed)
        client.connected.connect(lambda client, username: self.refresh())
        client.disconnected.connect(lambda client, reason: self.refresh())
        self._client = client
    
    def translateFile(self, filename, kind):
        """Translates a file of the given type."""
        current = self._status[filename]
        if current == STATE_UNKNOWN:
            self._update(filename, STATE_READY)
            if not self._request(filename):
                self._onFileFailed(None, filename)
        return self._rawtranslate(filename, kind)
    
    def listen(self, filename, kind, root, callback):
        """Listens for updates on the specified file.
        
        filename -- the name of the file to get updates on
        kind -- the kind of file to get updates on
        root -- the listening will go on as long as this object remains alive
        callback -- takes three parameters:
            clientResourceManager -- this manager
            filename -- the original filename requested
            translation -- the new value the filename translates to
        
        """
        # NOTE: Weak references always get me in trouble...
        response = self._makeResponse(kind, callback)
        if not hasattr(root, KEEP_ALIVE_FIELD):
            setattr(root, KEEP_ALIVE_FIELD, [])
        getattr(root, KEEP_ALIVE_FIELD).append(response)
        self._listeners[filename] = [listener for listener in self._listeners[filename] if listener()]
        self._listeners[filename].append(weakref.ref(response))
        #print "LISTEN", len(self._listeners[filename])
    
    def updateStatus(self, filename, status):
        """Responds to a status update sent from the server."""
        current = self._status[filename]
        # Telling us what we already know
        if status == current:
            return
        # Tell everyone about the change
        self._update(filename, status)
        # Ready to download, so let's load it (or verify it)
        if status == STATE_READY:
            if not self._request(filename):
                self._onFileFailed(None, filename)
        
    def refresh(self):
        """Cleans the entire resource map and refreshes all data."""
        # NOTE: There may be some inconsistency since the request is not in sync
        # with the data that comes from the server.
        # Clean out old listeners
        oldlisteners = self._listeners
        self._listeners = defaultdict(list)
        for filename, listeners in oldlisteners.items():
            newlist = [listener for listener in self._listeners if listener()]
            if len(newlist):
                self._listeners[filename] = newlist
        _sendStatusRequest(list(self._listeners.keys()))
    
    def reload(self, statusMapping):
        """Reloads the status of a group of files."""
        self._status = defaultdict(lambda: STATE_UNKNOWN)
        self._exists = defaultdict(bool)
        for filename, status in statusMapping.values():
            if status == STATE_UNKNOWN:
                continue
            self._update(filename, status)
    
    def _request(self, filename):
        """Request a given file from the server."""
        return self._client.requestFile(filename)
    
    def _update(self, filename, status):
        """Signal the change of status in a file."""
        # Avoid the loop unless there's been an actual change
        oldstatus = self._status[filename]
        exists = fileExists(filename)

        #if oldstatus != status or exists != self._exists[filename]:
        self._status[filename] = status
        self._exists[filename] = exists
        
        # Broadcast the changes to all listeners
        needClean = False
        for listener in self._listeners[filename]:
            cb = listener()
            if cb:
                cb(filename)
            else:
                needClean = True
        # Clean up expired weak references
        if needClean:
            self._listeners[filename] = [listener for listener in self._listeners[filename] if listener()]
    
    def _rawtranslate(self, filename, kind):
        """Translates the given filename based on availability."""
        status = self._status[filename]
        if status == STATE_INVALID:
            return RESOURCE_INVALID[kind]
        return filename
    
    def _makeResponse(self, kind, callback):
        # array is replacement for nonlocal keyword
        #last = [None]
        def response(filename):
            current = self._rawtranslate(filename, kind)
            #if last[0] != current:
            #    last[0] = current
            callback(self, filename, current)
        return response
    
    def _onFileReceived(self, client, filename):
        """Responds to a file being successfully transferred."""
        # HACK: Using reload image on not-necessarily-image files
        #reloadImage(filename)
        self._update(filename, STATE_READY)
    
    def _onFileFailed(self, client, filename):
        """Responds to a file that was not transferred."""
        current = self._status[filename]
        if current in (STATE_UNKNOWN, STATE_LOADING, STATE_READY) and fileExists(filename):
            # Could either have verified correctly or failed to transfer
            # Either way, call it present
            status = STATE_READY
        else:
            # Missing on server or failed to transfer
            # Call it missing
            status = STATE_INVALID
        self._update(filename, status)

class serverResourceMapper(object):
    """Fetches server resources."""
    
    def __init__(self, server):
        """Initializes the mapper."""
        self._status = {}
        self._user = defaultdict(set)
        server.fileReceived.connect(self._onFileReceived)
        server.fileFailed.connect(self._onFileFailed)
        server.disconnected.connect(self._onDisconnected)
        self._server = server
    
    def processFile(self, username, filename):
        """Processes a filename before passing on a packet."""
        current = self._status.get(filename, STATE_UNKNOWN)
        # Already loading or invalid, so who cares
        if current not in (STATE_UNKNOWN, STATE_INVALID):
            return
        # If it exists, just mark it ready.
        if fileExists(filename):
            self._update(filename, STATE_READY)
            return
        # Else it doesn't exist, so mark it loading and request it
        self._status[filename] = STATE_LOADING
        # Need to broadcast here so the client knows it's
        # not yet ready
        self._broadcast(filename, STATE_LOADING)
        self._user[username].add(filename)
        if not self._server.requestFile(username, filename):
            self._onFileFailed(None, username, filename)
    
    def getStatus(self, fileList):
        """Gets status on a list of files."""
        return dict([(filename, self._status.get(filename, STATE_UNKNOWN)) for filename in fileList])
    
    def _onFileReceived(self, server, username, filename):
        """Responds to a file being successfully gotten."""
        self._user[username].discard(filename)
        self._update(filename, STATE_READY)
    
    def _onFileFailed(self, server, username, filename):
        """Responds to a file being failedfully gotten."""
        self._user[username].discard(filename)
        # Worth taking a last look
        if fileExists(filename):
            status = STATE_READY
        else:
            status = STATE_INVALID
        self._update(filename, status)
    
    def _onDisconnected(self, server, username, errorMessage):
        """Resets any requests from a disconnected user."""
        for filename in self._user[username]:
            if fileExists(filename):
                status = STATE_READY
            else:
                status = STATE_INVALID
            self._update(filename, status)
        del self._user[username]
    
    def _update(self, filename, status):
        """Updates the status of a file, broadcasting if needed."""
        current = self._status.get(filename, STATE_UNKNOWN)
        if status == current:
            return
        self._status[filename] = status
        if current != STATE_UNKNOWN:
            self._broadcast(filename, STATE_READY)
    
    def _broadcast(self, filename, status):
        """Broadcasts the status of a file."""
        # HACK: inverted import flow
        from rggViews import allusers
        _broadcastStatus(allusers(), filename, status)

crm = clientResourceMapper(client)
srm = serverResourceMapper(server)

@serverRPC
def _broadcastStatus(filename, status):
    """Broadcasts the status of a file to all clients.
    
    filename -- the name of the file to broadcast
    status -- the status to broadcast for the file
    
    """
    crm.updateStatus(filename, status)

@serverRPC
def _respondStatus(statusDict):
    """Replies with the requested status, which is then used to reload all file statuses."""
    crm.reload(statusDict)

@clientRPC
def _sendStatusRequest(user, fileList):
    """Asks for the status on each of the specified files."""
    _respondStatus(user, srm.getStatus(fileList))

def fileExists(filename):
    # TODO: Implement file existence test.
    return True

    
