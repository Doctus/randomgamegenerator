'''
rggNet - for the Random Game Generator project
By Doctus (kirikayuumura.noir@gmail.com)

Handling of network connections.

    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''
from re import compile as recompile
from os import path, stat, makedirs, remove
from getpass import getuser

from libraries.rggQt import QTimer, QFile, QTcpServer, QHostAddress, QHostInfo
from libraries.rggSocket import statefulSocket, generateChecksum, fileData
from libraries.rggSystem import translate, mainWindow, signal, makeLocalFilename, findRandomAppend
from libraries.rggConstants import UNICODE_STRING, BASE_STRING, NETWORK_VERSION, COMPATIBLE_NETWORK_VERSIONS

MESSAGE_IDENTIFY = "IDENTIFY" # Identify this client
MESSAGE_ACTIVATE = "ACTIVATE" # Assign username
MESSAGE_GET = "GET" # Request file transfer
MESSAGE_PUT = "PUT" # Transfer file data
MESSAGE_IGNORE = "IGNORE" # Requested file was ignored
MESSAGE_ACCEPT = "ACCEPT" # Accept the specified file
MESSAGE_REJECT = "REJECT" # Reject the specified file

PROTOCOL_OBJECT = "OBJECT" # Object-based protocol
PROTOCOL_TRANSFER = "TRANSFER" # Transfer-based protocol

VALID_USERNAME = recompile('^[\w\-]+$')

class ConnectionData(object):
	"""Data used to create a network connection."""

	def __init__(self, host=None, port=6812, username=translate('net', 'Anonymous', 'default connection username'), passw=''):
		self.host = host or localUser() or localHost()
		self.port = port
		self.username = username
		self.password = passw

class BaseClient(object):
	"""Base class for local and remote clients."""

	def __init__(self):
		"""Initializes the client."""
		# Sockets/server
		self.obj = None
		self.xfer = None
		self.server = None
		self.hostname = None
		self.port = None
		self.password = None

		# File transfer lists
		self.sendList = set()
		self.getList = set()
		self.sentfile = None
		self.receivedfile = None
		# Doesn't need translation
		self.username = UNICODE_STRING(localUser()) or 'localhost'
		assert(self.username)

		self.timer = QTimer()
		self.timer.timeout.connect(self._updatetransfer)
		self.timer.start(1000)

		#self.timer = QTimer()
		#self.timer.timeout.connect(self.transferHack)
		#self.timer.start(3600000)

	@property
	def ready(self):
		return bool(self.obj) and self.obj.ready

	def close(self):
		"""Disconnect all network activity."""
		self.sendList = set()
		self.getList = set()
		self.hostname = None
		self.port = None
		if self.obj:
			x = self.obj
			self.obj = None
			x.connected.disconnect()
			x.disconnected.disconnect()
			x.objectReceived.disconnect()
			x.commandReceived.disconnect()
			x.close()
		self._closeXfer()

	def _openXfer(self, socket):
		"""Open the transfer socket."""
		assert(self.ready)
		self._closeXfer()
		self.xfer = socket
		socket.connected.connect(self._socketConnected)
		socket.disconnected.connect(self._socketDisconnected)
		socket.objectReceived.connect(self._socketObject)
		socket.commandReceived.connect(self._socketCommand)
		socket.fileSent.connect(self._fileSent)
		socket.fileReceived.connect(self._fileReceived)
		socket.filePartlySent.connect(self._filePartlySent)
		socket.filePartlyReceived.connect(self._filePartlyReceived)

	def _closeXfer(self):
		"""Disconnect the transfer socket."""
		if self.xfer:
			if self.sentfile:
				x = self.sentfile
				self.sentfile = None
				x.file.close()
			self.receivedfile = None

			x = self.xfer
			self.xfer = None
			x.connected.disconnect()
			x.disconnected.disconnect()
			x.objectReceived.disconnect()
			x.commandReceived.disconnect()
			x.fileSent.disconnect()
			x.fileReceived.disconnect()
			x.close()

	def _filePartlySent(self, filename, size, processed):
		self.partialTransferEvent.emit(self, filename, size, processed)

	def _filePartlyReceived(self, filename, size, processed):
		self.partialTransferEvent.emit(self, filename, size, processed)

	def send(self, data):
		"""Call to send an object over the wire."""
		self.server.receive(self.username, data)

	def receive(self, obj):
		"""Make the client receive some data."""
		pass

	def requestFile(self, filename):
		if filename in self.getList:
			# NOTE: could update checksum here (for refreshing the file when updated locally)
			return False
		try:
			file = QFile(makeLocalFilename(filename))
			if not file.open(QFile.ReadWrite):
				try:
					makedirs(path.dirname(filename))
				except:
					pass
				if not file.open(QFile.ReadWrite):
					return False
			try:
				size = file.size()
				digest = generateChecksum(file)
				filedata = fileData(file, filename, size, digest)
			finally:
				file.close()
		except IOError:
			return False
		if stat(filename).st_size == 0:
			remove(filename)
		self.getList.add(filename)
		self.obj.sendMessage(MESSAGE_GET,
			filename=filedata.filename,
			size=filedata.size,
			checksum=filedata.digest)
		message = "[{0}] Requested transfer of {filename} [{size} {checksum}]"
		print(message.format(self.obj.context, filename=filedata.filename, size=filedata.size,checksum=filedata.digest))
		self.fileEvent.emit(self, filename, "Requested")
		self._updatetransfer()
		return True

	def _updateSendReceive(self):
		"""Determines the order of updates to prioritize server GETs."""
		raise NotImplementedError("Must override.")

	def _updateSend(self):
		"""Updates the transfers to send."""

		while self.sendList and not self.sentfile:
			self.fileEvent.emit(self, "", "SENDING: "+str(len(self.sendList))+ " QUEUED")
			filedata = next(iter(self.sendList))
			self.sendList.remove(filedata)
			if self._shouldSendFile(filedata):
				self.sentfile = filedata
				self.xfer.sendMessage(MESSAGE_PUT,
					filename=filedata.filename,
					size=filedata.size,
					digest=filedata.digest)
				socket = self.xfer
				message = "[{0}] Offering transfer of {filename} [{size} {checksum}]"
			else:
				self.obj.sendMessage(MESSAGE_IGNORE, filename=filedata.filename)
				socket = self.obj
				message = "[{0}] Ignored transfer of {filename} [{size} {checksum}]"
			print(message.format(socket.context, filename=filedata.filename, size=filedata.size,checksum=filedata.digest))
		if self.sentfile: self.fileEvent.emit(self, "", "EXITED SEND LOOP DUE TO SENTFILE  ("+str(len(self.sendList))+ " FILES REMAIN QUEUED)")

	def _updateReceive(self):
		"""Updates the transfers to receive."""

		# Did the server want to send us something?
		if self.receivedfile:
			filename = self.receivedfile.filename
			if self._shouldReceiveFile(self.receivedfile):
				message = "[{0}] Accepted transfer of {filename} [{size} {checksum}]"
				print(message.format(self.xfer.context, filename=filename, size=self.receivedfile.size, checksum=self.receivedfile.digest))
				self.xfer.sendMessage(MESSAGE_ACCEPT, filename=filename)
				self.xfer.receiveFile(self.receivedfile)
			else:
				message = "[{0}] Rejected transfer of {filename} [{size} {checksum}]"
				print(message.format(self.xfer.context, filename=filename, size=self.receivedfile.size, checksum=self.receivedfile.digest))
				self._fileFailed(filename)
				self.xfer.sendMessage(MESSAGE_REJECT, filename=filename)
			self.getList.discard(filename)
			self.receivedfile = None

	def _updatetransfer(self):
		"""Opens or updates the transfer socket."""
		if not self.ready:
			self.fileEvent.emit(self, "", "NOT READY")
			return
		if not self.getList and not self.sendList:
			self.fileEvent.emit(self, "", "NO SEND LIST")
			return
		if not self.xfer:
			self.fileEvent.emit(self, "", "NO XFER SOCKET")
			self._openXfer()
			return

		self._updateSendReceive()

	def preemptivelyOpenTransferSocket(self):
		if not self.ready:
			return
		if not self.xfer:
			self._openXfer()
			return

	def transferHack(self):
		'''Kiiiind of crazy...'''
		if self.ready and not self.getList and not self.sendList and not self.xfer.busy:
			self._openXfer()

	def allowSend(client, filename, size, checksum):
		"""Replacable hook for determining which files should be sent."""
		return True

	def allowReceipt(client, filename, size, checksum):
		"""Replacable hook for determining which files should be accepted."""
		return True

	def _shouldSendFile(self, fileData):
		"""Check if we should send a file. Does extra mutating work."""
		filename = fileData.filename
		try:
			# Can we open the file?
			if not fileData.file.open(QFile.ReadOnly):
				self.fileEvent.emit(self, filename, "SENDFILE Could not open")
				print("SENDFILE Could not open")
				return False
			try:
				file = fileData.file
				# Do we already have an identical copy?
				size = fileData.file.size()
				digest = generateChecksum(file)
				if fileData.size is not None and fileData.digest is not None:
					if size == fileData.size and digest == fileData.digest:
						self.fileEvent.emit(self, filename, "SENDFILE Size and digest match")
						print("SENDFILE Size and digest match")
						return False

				fileData.size = file.size()
				fileData.digest = digest

				# User hook
				if not self.allowSend(fileData.filename,
						fileData.size, fileData.digest):
					self.fileEvent.emit(self, filename, "SENDFILE User hook")
					print("SENDFILE User hook")
					return False

				file = None
				self.fileEvent.emit(self, filename, "SENDFILE Success")
				print("SENDFILE Success")
				return True
			finally:
				if file:
					file.close()
		except IOError:
			pass
		return False

	def _shouldReceiveFile(self, fileData):
		"""Check if we should receive a file. Does extra mutating work."""
		file, filename = fileData.file, fileData.filename

		# Did we ask for the file?
		if not filename in self.getList:
			self.fileEvent.emit(self, filename, "RECVFILE Duplicate")
			print("RECVFILE Duplicate")
			return False
		try:
			# Can we open the file?
			if not file.open(QFile.ReadWrite):
				self.fileEvent.emit(self, filename, "RECVFILE Could not open")
				print("RECVFILE Could not open")
				return False
			try:
				# Do we already have an identical copy?
				if file.size() == fileData.size:
					if generateChecksum(file) == fileData.digest:
						self.fileEvent.emit(self, filename, "RECVFILE Size and digest match")
						print("RECVFILE Size and digest match")
						return False

				# User hook
				if not self.allowReceipt(fileData.filename,
						fileData.size, fileData.digest):
					self.fileEvent.emit(self, filename, "RECVFILE User hook")
					print("RECVFILE User hook")
					return False

				file = None
				self.fileEvent.emit(self, filename, "RECVFILE Success")
				print("RECVFILE Success")
				return True
			finally:
				if file:
					file.close()
		except IOError:
			pass
		return False

	# SIGNAL RESPONSES

	def _socketConnected(self, socket):
		"""Called when a socket is connected."""
		pass

	def _socketDisconnected(self, socket, errorMessage):
		"""Called when a socket disconnects."""
		if socket == self.obj:
			self.close()
		elif socket == self.xfer:
			self._closeXfer()
			self._updatetransfer()

	def _socketObject(self, socket, data):
		"""Called when an object is received on a socket."""
		if socket == self.obj:
			self.receive(data)

	def _socketCommand(self, socket, command, kwargs):
		"""Responds to socket commands."""
		if socket == self.obj:
			if command not in (MESSAGE_ACTIVATE, MESSAGE_GET, MESSAGE_IGNORE):
				message = "[{0}] Unexpected object command {command}"
				print(message.format(socket.context, command=command))
				return
		elif socket == self.xfer:
			if command not in (MESSAGE_ACTIVATE, MESSAGE_PUT, MESSAGE_ACCEPT, MESSAGE_REJECT):
				message = "[{0}] Unexpected transfer command {command}"
				print(message.format(socket.context, command=command))
				return
		else:
			return
		if ((command == MESSAGE_ACTIVATE) == socket.ready):
			message = "[{0}] Unexpected command {command}"
			print(message.format(socket.context, command=command))
			return
		try:
			kwargs = dict((str(key), val) for key, val in list(kwargs.items()))
			if command == MESSAGE_ACTIVATE:
				self._activateSocket(socket, **kwargs)
			elif command == MESSAGE_GET:
				self._getFile(socket, **kwargs)
			elif command == MESSAGE_PUT:
				self._putFile(socket, **kwargs)
			elif command == MESSAGE_IGNORE:
				self._ignoreFile(socket, **kwargs)
			elif command == MESSAGE_ACCEPT:
				self._acceptFile(socket, **kwargs)
			elif command == MESSAGE_REJECT:
				self._rejectFile(socket, **kwargs)
		except TypeError as e:
			message = "[{0}] Invalid parameters to remote command {command}: {parms}; {err}"
			import traceback
			print(message.format(socket.context, command=command, parms=repr(kwargs), err=e))
			traceback.print_exc()

	def _activateSocket(self, socket, username):
		"""Activates the socket."""
		pass

	def _getFile(self, socket, filename, size, checksum):
		"""Responds to a file request."""
		self.fileEvent.emit(self, filename, "Requested by client")
		self.sendList.add(fileData(QFile(makeLocalFilename(filename)), filename, size, checksum))
		self._updatetransfer()

	def _putFile(self, socket, filename, size, digest):
		"""Checks whether to accept a sent file."""

		if self.receivedfile is not None:
			message = "[{0}] Remote duplicate PUT; ignoring {filename}"
			print(message.format(socket.context, filename=self.receivedfile.filename))

		self.receivedfile = fileData(QFile(makeLocalFilename(filename)), filename, size, digest)
		self._updatetransfer()

	def _ignoreFile(self, socket, filename):
		"""Responds to a file request."""
		message = "[{0}] Remote refused to send {filename}"
		print(message.format(socket.context, filename=filename))
		self.fileEvent.emit(self, filename, "Remote refused to send")
		if filename in self.getList:
			self.getList.remove(filename)
			self._fileFailed(filename)
		self._updatetransfer()

	def _acceptFile(self, socket, filename):
		"""Starts sending the specified file."""
		if not self.sentfile or self.sentfile.filename != filename:
			message = "[{0}] Attempt to accept unexpected file {filename}"
			print(message.format(socket.context, filename=filename))
			socket._disconnectWithPrejudice()
			return
		socket.sendFile(self.sentfile)
		self.sentfile = None

	def _rejectFile(self, socket, filename):
		"""Cancels sending the specified file."""
		if not self.sentfile or self.sentfile.filename != filename:
			message = "[{0}] Attempt to reject unexpected file {filename}"
			print(message.format(socket.context, filename=filename))
			return
		self.sendList.remove(filename)
		self.sentfile.file.close()
		self.sentfile = None

	def _fileSent(self, socket, filename):
		"""Look for more stuff to send."""
		self._updatetransfer()

	def _fileReceived(self, socket, filename):
		"""Look more stuff to send."""
		self._updatetransfer()

	def _fileFailed(self, filename):
		"""Notify that the socket did not send the specified file."""
		pass

	fileEvent = signal(object, BASE_STRING, BASE_STRING, doc=
		"""Called when something happens relating to a file.

		client -- this client
		filename -- the filename of the file received
		event -- a description of the event

		"""
	)

	partialTransferEvent = signal(object, BASE_STRING, BASE_STRING, BASE_STRING, doc=
		"""Called when part of a transfer occurs.

		client -- this client
		filename -- the filename of the file involved
		size -- total size of the file
		processed -- amount of the file transferred so far

		"""
	)


class JsonClient(BaseClient):
	"""A client that communicates with a server."""

	# CONNECTION

	@property
	def isHosting(self):
		return self.server.isConnected

	@property
	def isConnected(self):
		return self.obj or self.server.isConnected

	def host(self, port):
		"""Starts the network as a server."""
		if self.isConnected:
			raise RuntimeError("Already connected.")
		assert(self.username)
		result = self.server._listen(port)
		if result:
			self.port = port
		return result

	def join(self, hostname, port):
		"""Starts the network as a client."""
		if self.isConnected:
			raise RuntimeError("Already connected.")
		self.obj = statefulSocket(name="C-OBJ", hostname=hostname, port=port)
		self.hostname = hostname
		self.port = port
		self.obj.connected.connect(self._socketConnected)
		self.obj.disconnected.connect(self._socketDisconnected)
		self.obj.objectReceived.connect(self._socketObject)
		self.obj.commandReceived.connect(self._socketCommand)
		assert(self.username)

	def close(self):
		"""Closes the server as well as this client."""
		super(JsonClient, self).close()
		if self.server.isConnected:
			self.server.close()

	def _openXfer(self):
		"""Open the transfer socket."""
		BaseClient._openXfer(self, statefulSocket(name="C-XFR", hostname=self.hostname, port=self.port))

	def send(self, data):
		"""Call to send an object over the wire."""
		if self.ready:
			self.obj.sendObject(data)
		else:
			self.server.receive(self.username, data)

	def requestFile(self, filename):
		if self.ready:
			return BaseClient.requestFile(self, filename)
		else:
			return False

	def receive(self, obj):
		"""Make the client receive some data."""
		self.objectReceived.emit(self, obj)

	def _updateSendReceive(self):
		"""Determines the order of updates to avoid deadlock."""

		self.fileEvent.emit(self, "", "CHECKING SEND/RECEIVE")

		# Even if there's a transfer waiting, prioritize sending stuff first
		self._updateSend()

		# This check ensures the client priortizes sending over receiving
		if self.sentfile:
			self.fileEvent.emit(self, "", "SENT FILE")
			return
		self._updateReceive()

	# SIGNALS

	connected = signal(object, BASE_STRING, doc=
		"""Called when the client is ready to start sending;
		when isConnected becomes True.

		Never called when hosting; can send immediately in that case.

		client -- this client
		username -- the username the server is using

		"""
	)

	disconnected = signal(object, BASE_STRING, doc=
		"""Called when the client disconnects or fails to connect.

		Not called when disconnected manually (through close()).

		Never called when hosting; you will never be disconnected automatically.

		client -- this client
		errorMessage -- the untranslated reason the connection failed

		"""
	)

	transferDisconnected = signal(object, BASE_STRING, doc=
		"""Called when the transfer socket disconnects or fails to connect.

		Not called when disconnected manually (through close()).

		Never called when hosting; you will never be disconnected automatically.

		client -- this client
		errorMessage -- the untranslated reason the connection failed

		"""
	)

	objectReceived = signal(object, dict, doc=
		"""Called when an object is received over the wire.

		client -- this client
		data -- the data received

		"""
	)

	fileReceived = signal(object, BASE_STRING, doc=
		"""Called when a file is received over the wire.

		client -- this client
		filename -- the filename of the file received

		"""
	)

	fileFailed = signal(object, BASE_STRING, doc=
		"""Called when a file fails to come over the wire.

		client -- this client
		filename -- the filename of the file received

		"""
	)


	def setPassword(self, new):
		self.password = new

	# SIGNAL RESPONSES

	def _socketConnected(self, socket):
		"""Called when a socket is connected."""
		if socket == self.obj:
			self.obj.sendMessage(MESSAGE_IDENTIFY, protocol=PROTOCOL_OBJECT, username=self.username, passw=self.password, networkVersion=NETWORK_VERSION)
		elif socket == self.xfer:
			self.xfer.sendMessage(MESSAGE_IDENTIFY, protocol=PROTOCOL_TRANSFER, username=self.username)

	def _socketDisconnected(self, socket, errorMessage):
		"""Called when a socket disconnects."""
		if socket == self.obj:
			self.disconnected.emit(self, errorMessage)
		if socket == self.xfer:
			self.transferDisconnected.emit(self, errorMessage)
		super(JsonClient, self)._socketDisconnected(socket, errorMessage)

	def _activateSocket(self, socket, username):
		"""Activates the socket."""
		if socket == self.xfer:
			socket.activate()
			self._updatetransfer()
		elif socket == self.obj:
			socket.activate()
			self.connected.emit(self, username)
			self._updatetransfer()
			super(JsonClient, self)._activateSocket(socket, username)

	def _fileReceived(self, socket, filename):
		"""Emit and look for more stuff to send."""
		if socket == self.xfer:
			self.fileReceived.emit(self, filename)
		super(JsonClient, self)._fileReceived(socket, filename)

	def _fileFailed(self, filename):
		"""Notify that the socket did not send the specified file."""
		self.fileFailed.emit(self, filename)

class RemoteClient(BaseClient):
	"""A client on a different computer."""

	# CONNECTION

	def __init__(self, username, server, obj):
		super(RemoteClient, self).__init__()
		assert(obj.ready)
		self.obj = obj
		self.server = server

		self.obj.disconnected.connect(self._socketDisconnected)
		self.obj.objectReceived.connect(self._socketObject)
		self.obj.commandReceived.connect(self._socketCommand)
		self.username = username

	@property
	def isConnected(self):
		return bool(self.obj)

	# HACK: Bugfix.
	def _openXfer(self, socket=None):
		"""A true hack to fix an edge case."""
		if socket is not None:
			BaseClient._openXfer(self, socket)

	# send/receive are reversed for ducking
	def receive(self, data):
		"""Call to send an object over the wire."""
		assert(self.ready)
		self.obj.sendObject(data)

	def _updateSendReceive(self):
		"""Determines the order of updates to avoid deadlock."""

		# Even if there's a send pending, prioritize receiving stuff first
		self._updateReceive()
		if self.xfer.busy:
			return
		self._updateSend()

	def allowSend(self, filename, size, checksum):
		"""Overridden to defer to server."""
		return self.server.allowSend(self.username, filename, size, checksum)

	def allowReceipt(self, filename, size, checksum):
		"""Overridden to defer to server."""
		return self.server.allowReceipt(self.username, filename, size, checksum)

	# SIGNAL RESPONSES

	def _socketDisconnected(self, socket, errorMessage):
		"""Called when a socket disconnects."""
		if socket == self.obj:
			self.server._dropClient(self.username, errorMessage)
		elif socket == self.xfer:
			self.server._respondXferDisconnect(self.username, errorMessage)
		super(RemoteClient, self)._socketDisconnected(socket, errorMessage)

	def _socketObject(self, socket, data):
		"""Called when an object is received on a socket."""
		if socket == self.obj:
			self.send(data)

	def _fileReceived(self, socket, filename):
		"""Emit and look for more stuff to send."""
		if socket == self.xfer:
			self.server.fileReceived.emit(self.server, self.username, filename)
		super(RemoteClient, self)._fileReceived(socket, filename)

	def _fileFailed(self, filename):
		"""Notify that the socket did not send the specified file."""
		self.server.fileFailed.emit(self.server, self.username, filename)

class JsonServer(object):
	"""A server that processes JSON messages."""

	def __init__(self, client):
		self.clients = {}
		self._addClient(client)
		self.unknown = set()
		self.client = client
		client.server = self
		self.tcp = None
		# Banlist can be manipulated manually;
		# just add ips
		self.banlist = set()
		self.password = None

	@property
	def isConnected(self):
		return bool(self.tcp)

	def _listen(self, port):
		"""Starts the server. Returns True on success, else False."""
		if self.isConnected:
			raise RuntimeError("Already connected.")

		self.clients = {}
		self._addClient(self.client)

		tcp = QTcpServer(mainWindow)
		tcp.newConnection.connect(self._newConnection)

		result = tcp.listen(QHostAddress("0.0.0.0"), port)
		if result:
			print("[SERVER] Listening on {0}:{1}".format(tcp.serverAddress().toString(), tcp.serverPort()))
			self.tcp = tcp
		else:
			print("[SERVER] Error on listen attempt; {0}".format(tcp.errorString()))
			# TODO: Should we delete the server here?
			tcp.deleteLater()

		#TODO: Better error reporting?
		return result

	def close(self):
		self.clients = {}
		self._addClient(self.client)
		if self.isConnected:
			tcp = self.tcp
			self.tcp = None
			for client in list(self.clients.values()):
				client.close()
			for socket in self.unknown:
				socket.close()
			self.unknown = set()
			tcp.close()
			# TODO: Should we delete the server here?
			tcp.deleteLater()
			print("[SERVER] No longer listening.")

	def send(self, username, data):
		"""Call to send an object over the wire."""
		if not self.userExists(username):
			raise RuntimeError("Invalid username {0}".format(username))
		client = self.clients[self._processUsername(username)]
		client.receive(data)

	def broadcast(self, data, users=None):
		"""Call to send an object over the wire.

		users -- users to send to; default is all
		"""
		if users:
			users = set(self._processUsername(username) for username in users)
		else:
			users = list(self.clients.keys())
		for shortname in users:
			assert(shortname in self.clients)
			self.clients[shortname].receive(data)

	def requestFile(self, username, filename):
		"""Requests a file from the specified user."""
		if not self.userExists(username):
			raise RuntimeError("Invalid username {0}".format(username))
		client = self.clients[self._processUsername(username)]
		return client.requestFile(filename)

	def receive(self, username, data):
		"""Receive the specified data."""
		return self.objectReceived.emit(self, username, data)

	def allowSend(server, username, filename, size, checksum):
		"""Replacable hook for determining which files should be sent."""
		return True

	def allowReceipt(server, username, filename, size, checksum):
		"""Replacable hook for determining which files should be accepted."""
		return True

	def _processUsername(self, username):
		"""Processes a username to lowercase."""
		return UNICODE_STRING(username).lower()

	def _addClient(self, client):
		"""Adds a client to the list."""
		assert(not self.userExists(client.username))
		self.clients[self._processUsername(client.username)] = client

	def userExists(self, username):
		"""Checks whether the given username is taken."""
		return (self._processUsername(username) in self.clients)

	def fullname(self, username):
		"""Returns the correctly capitalized version of the username."""
		assert(self.userExists(username))
		return self.clients[self._processUsername(username)].username

	def allowPassword(self, passw):
		if passw == self.password:
			return True
		return False

	def addBan(self, IP):
		"""Adds the given IP to the banlist."""
		self.banlist.add(str(IP))

	def clearBanlist(self):
		"""Clears all entries from the banlist."""
		self.banlist = set()

	@property
	def users(self):
		"""Returns the list of usernames."""
		return list(self.clients.keys())

	def userIP(self, username):
		"""Gets the IP of an existing client."""
		if not self.userExists(username):
			raise RuntimeError("Invalid username {0}".format(username))
		if self.clients[self._processUsername(username)] == self.client:
			return "127.0.0.1"
		return UNICODE_STRING(self.clients[self._processUsername(username)].obj.socket.peerAddress())

	def baseUsername(server):
		"""Replaceable hook for the base 'guest' username."""
		# NOTE: should not localize
		return 'guest'

	def allowUsername(server, username):
		"""Replacable hook for determining whether a username is OK.

		Does not need to determine uniqueness, but the name may
		be altered to something in the form of '{original}-[A-Za-z0-9]+'

		"""
		return bool(VALID_USERNAME.match(username))

	def _fixUsername(self, username=None):
		"""Fixes a username so that it's unique."""
		if not username:
			username = self.baseUsername()
		if self.userExists(username):
			username = username + ('-' + findRandomAppend())
			while self.userExists(username):
				username += findRandomAppend()
		return str(username)

	def setPassword(self, new):
		self.password = new

	def rename(self, oldname, newname):
		"""Renames a user to the specified name.

		Does some quick validity checking.
		Raises if not accepted;
		pre: not userExists(newname) and allowUsername(newname) and oldname != newname

		NOTE: Might cause file transfer to be declined, but
			will just reconnect.

		Only renames on this side; you must coordinate it manually.

		"""
		oldname = self._processUsername(oldname)
		newproc = self._processUsername(newname)

		assert(self.userExists(oldname))
		client = self.clients[oldname]
		assert(self.allowUsername(newname))
		assert(client.username != newname)
		assert(not self.userExists(newname) or newproc == oldname)

		del self.clients[oldname]
		client.username = newname
		self._addClient(client)

	def kick(self, username):
		"""Kicks a user."""
		if not self.isConnected:
			return
		username = self._processUsername(username)
		assert(username in self.clients)
		client = self.clients[username]
		assert(client != self.client)
		client.close()
		del self.clients[username]
		self.kicked.emit(self, client.username)

	def _dropClient(self, username, errorMessage):
		"""Disconnect a remote client."""
		if not self.isConnected:
			return
		username = self._processUsername(username)
		assert(self.userExists(username))
		assert(username in self.clients)
		client = self.clients[username]
		assert(client != self.client)
		client.close()
		assert(username in self.clients)
		del self.clients[username]
		self.disconnected.emit(self, client.username, errorMessage)

	def _respondXferDisconnect(self, username, errorMessage):
		"""Attempt to reestablish a lost transfer socket connection."""
		assert(self.userExists(username))
		assert(username.lower() in self.clients)
		client = self.clients[username.lower()]
		assert(client != self.client)
		self.transferDisconnected.emit(self, client.username, errorMessage)

	connected = signal(object, BASE_STRING, doc=
	"""Called when a client connects to the server.

	server -- this server
	username -- the username of the client

	"""
	)

	disconnected = signal(object, BASE_STRING, BASE_STRING, doc=
		"""Called when a client disconnects from the server.

		Not called when disconnected manually (through close()).

		Never called when hosting; you will never be disconnected automatically.

		server -- this server
		username -- the username of the client
		errorMessage -- the untranslated reason the connection failed

		"""
	)

	transferDisconnected = signal(object, BASE_STRING, BASE_STRING, doc=
		"""Called when a client transfer socket disconnects from the server.

		Not called when disconnected manually (through close()).

		Never called when hosting; you will never be disconnected automatically.

		server -- this server
		username -- the username of the client
		errorMessage -- the untranslated reason the connection failed

		"""
	)

	kicked = signal(object, BASE_STRING, doc=
		"""Called when a client is kicked from the server.

		server -- this server
		username -- the username of the client

		"""
	)

	objectReceived = signal(object, BASE_STRING, dict, doc=
		"""Called when an object is received from the client over the wire.

		server -- this server
		username -- the username of the client
		data -- the data received

		"""
	)

	fileReceived = signal(object, BASE_STRING, BASE_STRING, doc=
		"""Called when a file is received over the wire.

		server -- this server
		username -- the username of the client
		filename -- the filename of the file received

		"""
	)

	fileFailed = signal(object, BASE_STRING, BASE_STRING, doc=
		"""Called when a file fails to come over the wire.

		server -- this server
		username -- the username of the client
		filename -- the filename of the file received

		"""
	)

	fileEvent = signal(object, BASE_STRING, BASE_STRING, doc=
		"""Called when a file fails to come over the wire.

		username -- the username of the client
		filename -- the filename of the file received
		event -- a description of the event

		"""
	)

	partialTransferEvent = signal(object, BASE_STRING, BASE_STRING, BASE_STRING, doc=
		"""Called when part of a transfer occurs.

		username -- the username of the client
		filename -- the filename of the file involved
		size -- total size of the file
		processed -- amount of the file transferred so far

		"""
	)

	def passFileEvent(self, clientName, filename, eventDescription):
		self.fileEvent.emit(clientName, filename, eventDescription)

	def passPartialTransferEvent(self, clientName, filename, size, processed):
		self.partialTransferEvent.emit(clientName, filename, size, processed)

	def _newConnection(self):
		"""Responds to a new connection occurring."""
		if not self.tcp:
			return
		while self.tcp.hasPendingConnections():
			socket = self.tcp.nextPendingConnection()
			if str(socket.peerAddress().toString()) in self.banlist:
				socket.close()
				print("[SERVER] Banned client attempted to connect: {1}:{2}".format(
					socket.peerName(), socket.peerAddress().toString(), socket.peerPort()))
				return
			assert(socket)
			print("[SERVER] New client connected: {1}:{2}".format(
					socket.peerName(), socket.peerAddress().toString(), socket.peerPort()))
			socket = statefulSocket(socket=socket)
			self.unknown.add(socket)
			socket.disconnected.connect(self._socketDisconnected)
			socket.commandReceived.connect(self._socketCommand)
			socket.objectReceived.connect(self._socketObject)
			print("Connections successful for ", str(socket))

	def _detachUnknown(self, socket):
		self.unknown.discard(socket)
		socket.disconnected.disconnect()
		socket.commandReceived.disconnect()
		socket.objectReceived.disconnect()

	def _socketDisconnected(self, socket, reason):
		message = "Socket closed before identification: {reason}"
		message = message.format(reason=reason)
		self._forbidSocket(socket, message)

	def _forbidSocket(self, socket, text):
		message = "[{0}] {1}"
		print(message.format(socket.context, text))
		self._detachUnknown(socket)
		socket.close()

	def _socketObject(self, socket, obj):
		message = "Disallowed object data received"
		self._forbidSocket(socket, message)
		return

	def _socketCommand(self, socket, command, kwargs):
		if command != MESSAGE_IDENTIFY:
			message = "Disallowed initial remote command {command}"
			message = message.format(command=command)
			self._forbidSocket(socket, message)
			return
		try:
			kwargs = dict((str(key), val) for key, val in list(kwargs.items()))
			self._socketIdentified(socket, **kwargs)
		except TypeError as e:
			message = "Invalid parameters to initial remote command {command}: {parms}; {err}"
			message = message.format(command=command, parms=repr(kwargs), err=e)
			self._forbidSocket(socket, message)

	def _socketIdentified(self, socket, protocol, username, passw = None, networkVersion = "1"):
		"""Socket identifies itself with protocol and username."""
		if protocol not in (PROTOCOL_OBJECT, PROTOCOL_TRANSFER):
			message = "Disallowed protocol identified {protocol} ({username})"
			message = message.format(protocol=protocol, username=username)
			self._forbidSocket(socket, message)
			return
		if networkVersion not in COMPATIBLE_NETWORK_VERSIONS:
			message = "Incompatible network version (client should update RGG): {networkVersion} ({username})"
			message = message.format(networkVersion=networkVersion, username=username)
			self._forbidSocket(socket, message)
			return
		self._detachUnknown(socket)
		if protocol == PROTOCOL_OBJECT:
			# Make it unique and valid

			if not self.allowUsername(username):
				username = None
			username = self._fixUsername(username)

			assert(not self.userExists(username))

			if self.password is not None and len(self.password) > 0:
				if not self.allowPassword(passw):
					message = "Password error {protocol} ({username})"
					message = message.format(protocol=protocol, username=username)
					self._forbidSocket(socket, message)
					return

			socket.imbueName("S-OBJ")
			socket.activate()
			client = RemoteClient(username, self, socket)
			self._addClient(client)
			client.fileEvent.connect(self.passFileEvent)
			client.partialTransferEvent.connect(self.passPartialTransferEvent)
			socket.sendMessage(MESSAGE_ACTIVATE, username=username)
			self.connected.emit(self, username)
		else:
			# Make sure identities match
			username = self._processUsername(username)
			if username not in self.clients:
				message = "Transfer protocol username does not match {username}"
				message = message.format(username=username)
				self._forbidSocket(socket, message)
				return
			client = self.clients[username]
			if client == self.client:
				message = "Transfer protocol attempt to match server user."
				message = message.format(username=username)
				self._forbidSocket(socket, message)
				return
			assert(client.ready)
			if client.obj.socket.peerAddress() != socket.socket.peerAddress():
				message = "Transfer protocol attempt to match user from different IP."
				message = message.format(username=username)
				self._forbidSocket(socket, message)
				return
			socket.activate()
			socket.imbueName("S-XFR")
			client._openXfer(socket)
			socket.sendMessage(MESSAGE_ACTIVATE, username=username)
			message = "[{0}:{1}] Transfer socket connected to {username}"
			print(message.format(socket.context, client.obj.context, username=username))
			client._updatetransfer()

def localHost():
	"""Gets the name of the local machine."""
	return UNICODE_STRING(QHostInfo.localHostName())

def localUser():
	"""Gets the name of the local user."""
	return UNICODE_STRING(getuser())

