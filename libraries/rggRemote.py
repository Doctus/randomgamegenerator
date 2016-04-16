'''
rggRemote - for the Random Game Generator project
By Doctus (kirikayuumura.noir@gmail.com)

Remote views.

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
from os import path

from libraries.rggResource import crm, srm, RESOURCE_IMAGE
from libraries.rggSystem import translate, fake, makePortableFilename
from libraries.rggViews import say, ICSay, linkedName, getPortraitSize
from libraries.rggViews import localhandle, getuser, allusers, allusersbut
from libraries.rggViews import User, addUserToList, getNetUserList, respondUserRemove
from libraries.rggViews import clearUserList, reconnectTransferSocket, renameuser
from libraries.rggViews import _closeAllMaps, setUwidgetLocal, adduser, respondSession
from libraries.rggViews import getSession, respondChangeGM, getGM, respondUserList, removeuser
from libraries.rggRPC import clientRPC, serverRPC, receiveClientRPC, receiveServerRPC
from libraries.rggConstants import PORTRAIT_DIR

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
		portfile = makePortableFilename(path.join(PORTRAIT_DIR, portrait))
		IAMTHEDOOMPHANTOM = crm.translateFile(makePortableFilename(path.join(PORTRAIT_DIR, portrait)), RESOURCE_IMAGE)
		#^ Don't remember whether this is still needed for transfer etc.
		ICSay(translate('remote', '<table><tr><td><img src="{port}" width="{size}" height="{size}"></td><td>{name}: {sayText}</td></tr></table><br />').format(
			port=portfile,
			size=getPortraitSize(),
			name=linkedName(chname),
			sayText=message))
	else:
		ICSay(translate('remote', '{name}: {sayText}</p>').format(
		name=linkedName(chname),
		sayText=message))

@clientRPC
def sendICSay(user, message, chname, portrait):
	crm.listen(portrait, RESOURCE_IMAGE, crm, doNothing)
	if len(portrait) > 1:
		srm.processFile(user, makePortableFilename(path.join(PORTRAIT_DIR, portrait)))
	respondICSay(allusers(), chname, message, portrait)

def doNothing(blah, bleh, bloh):
	pass

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
		portfile = makePortableFilename(path.join(PORTRAIT_DIR, portrait))
		ICSay(translate('remote', '<table><tr><td><img src="{port}" width="{size}" height="{size}"></td><td><i>{name} {emote}</i></td></tr></table><br />').format(
			port=portfile,
			size=getPortraitSize(),
			name=linkedName(chname),
			emote=message))
	else:
		ICSay(translate('remote', '<i>{name} {emote}</i>').format(
			name=linkedName(chname),
			emote=message))


@clientRPC
def sendICEmote(user, message, chname, portrait):
	if len(portrait) > 1:
		srm.processFile(user, makePortableFilename(path.join(PORTRAIT_DIR, portrait)))
	respondICEmote(allusers(), chname, message, portrait)

@serverRPC
def respondICWhisperSender(target, message, chname, portrait):
	if len(portrait) > 1:
		portfile = makePortableFilename(path.join(PORTRAIT_DIR, portrait))
		ICSay(translate('remote', '<table><tr><td><img src="{port}" width="{size}" height="{size}"></td><td>To {name}: {message}</td></tr></table><br />').format(
			port=portfile,
			size=getPortraitSize(),
			name=linkedName(target),
			message=message))
	else:
		ICSay(translate('remote', 'To {name}: {message}').format(
			name=linkedName(chname),
			message=message))

@serverRPC
def respondICWhisperTarget(sender, message, chname, portrait):
	if len(portrait) > 1:
		portfile = makePortableFilename(path.join(PORTRAIT_DIR, portrait))
		ICSay(translate('remote', '<table><tr><td><img src="{port}" width="{size}" height="{size}"></td><td>{name} whispers: {message}</td></tr></table><br />').format(
			port=portfile,
			size=getPortraitSize(),
			name=linkedName(chname),
			message=message))
	else:
		ICSay(translate('remote', '{name} whispers: {message}').format(
			name=linkedName(chname),
			message=message))

@clientRPC
def sendICWhisper(user, target, message, chname, portrait):
	target = target.lower()
	targetuser = getuser(target)
	if not targetuser:
		respondError(user, fake.translate('remote', '{target} does not exist.'), target=target)
	else:
		respondICWhisperSender(user, targetuser.username, message, chname, portrait)
		respondICWhisperTarget(targetuser, user.username, message, chname, portrait)

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
	addUserToList(username)

# LOW-LEVEL NETWORKING

def clientConnect(client, username):
	"""Occurs when the client is ready to start sending data."""
	#print "Client connected."
	renameuser(localhandle(), username)
	_closeAllMaps()
	setUwidgetLocal()
	say(translate('remote', "Welcome, {name}!").format(name=username))
	client.preemptivelyOpenTransferSocket()

def clientDisconnect(client, errorMessage):
	"""Occurs when the client connection disconnects without being told to.

	errorMessage -- a human-readable error message for why the connection failed

	"""
	#print "Client disconnected."
	say(translate('remote', "Disconnected. {0}").format(errorMessage))
	clearUserList()

def clientReceive(client, data):
	"""Occurs when the client receives data.

	data -- a dictionary or list of serialized data

	"""
	#print "client received"
	receiveClientRPC(data)

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
	adduser(user)
	respondUserJoin(allusersbut(user), username)
	respondSession(user, getSession().dump())
	respondChangeGM(user, getGM(), localhandle())
	respondUserList(user, getNetUserList())

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
	user = removeuser(username)
	respondError(allusers(),
		fake.translate('remote', '{username} has left the game. {error}'),
			username=user.username, error=errorMessage)
	respondUserRemove(allusers(), username)

def serverTransferDisconnect(server, username, errorMessage):
	"""Occurs when a client's transfer socket disconnects.

	username -- a username for the client
	errorMessage -- a human-readable error message for why the connection failed

	"""
	reconnectTransferSocket(getuser(username))

def serverKick(server, username):
	"""Occurs when a client is kicked.

	username -- a username for the client

	"""
	user = removeuser(username)
	respondError(allusers(),
		fake.translate('remote', '{username} was kicked by the host.'),
			username=user.username)
	respondUserRemove(allusers(), username)

def serverReceive(server, username, data):
	"""Occurs when the server receives data.

	username -- a username for the client
	data - a dictionary or list of serialized data

	"""
	#print username, getuser(username), usernames(), allusers()
	assert(getuser(username))
	#print "server received"
	receiveServerRPC(getuser(username), data)


def serverFileReceive(server, username, filename):
	"""Occurs when the client receives data.

	username -- the name of the sending user
	filename -- the name of the file received

	"""
	pass

