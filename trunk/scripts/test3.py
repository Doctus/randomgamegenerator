import bmainmod, rggNameGen, rggTileLoader, rggDice
from PyQt4 import QtCore

c = bmainmod.bMain()

def newEvent(str):
    if str[0] == '/':
        words = unicode(str).split()
        if words[0].lower() == '/randomname':
            if len(words) == 1:
                name = ("Syntax: /randomname NAMETYPE. Caps and spaces " +
                        "are ignored. Some valid arguments are " +
                        "JAPANESEFEMALEFULL and DwArF M aLe")
            else:
                name = rggNameGen.getName(''.join(words[1:]).lower())
            c.insertChatMessage(unicode(name))
        elif words[0].lower() == '/roll':
            if len(words) == 1:
                c.insertChatMessage("Syntax: /roll DICE. Dice can be " +
                                    "like '3d4 - 2 + 1d20' or '5k3' or" +
                                    " other variants depending on " +
                                    "development. See also /troll")
            else:
                rolltext = (c.getLocalHandle() + " rolls " +
                            rggDice.roll(" ".join(words[1:])))
                c.insertChatMessage(rolltext)
                c.sendNetMessageToAll('r!' + rolltext)
        elif words[0].lower() == '/troll':
            rolltext = (c.getLocalHandle() + " rolls " + rggDice.roll('2d6'))
            c.insertChatMessage(rolltext)
            c.sendNetMessageToAll('r!' + rolltext)
        elif words[0].lower() == '/me' or words[0].lower() == '/emote':
            if len(words) == 1:
                action = ("Syntax: /me DOES ACTION. Displays '[HANDLE] DOES "
                        "ACTION' in italic font.")
            else:
                action = ' '.join(words[1:])
            c.insertChatMessage('<i>' + c.getLocalHandle() + ' ' +
                                unicode(action) + '</i>')
            c.sendNetMessageToAll('T!' + unicode(action))
        elif words[0].lower() == '/w' or words[0].lower() == '/t' or words[0].lower() == '/whisper' or words[0].lower() == '/tell':
            if len(words) == 1:
                mesg = ("Syntax: /whisper HANDLE MESSAGE. Sends a message " +
                        "only to the specified user. Spaces MUST be correct." +
                        " Handle may be caps-sensitive.")
                c.insertChatMessage(unicode(mesg))
            else:
                target = words[1]
                mesg = " ".join(words[2:])
                if c.isServer():
                    if not c.sendNetMessageToHandle('w! ' + c.getLocalHandle() +
                                             ' ' + unicode(mesg), target):
                        c.insertChatMessage("Error: could not find that handle.")
                    else:
                        c.insertChatMessage('To ' + unicode(target) + ': ' +
                                    unicode(mesg))
                else:
                    c.insertChatMessage('To ' + unicode(target) + ': ' +
                                    unicode(mesg))
                    c.sendNetMessageToAll('W! ' + target + ' ' + unicode(mesg))
    else:
        c.insertChatMessage(c.getLocalHandle() + ": " + str)
        c.sendNetMessageToAll("t!" + str)

def newNetEvent(str, handle):
    #c.insertChatMessage("DEBUG: " + str)
    if len(str) > 1:
        if str[1] == '!':
            if str[0] == 't': #Ordinary chat message
                c.insertChatMessage(unicode(handle) + ": " + str[2:])
                if c.isServer():
                    c.sendNetMessageToAllButOne('s!' + ' ' + handle +
                                                ' ' + str[2:],
                                                handle)
            elif str[0] == 'T': #Emote message
                c.insertChatMessage('<i>' + unicode(handle) + " " +
                                    str[2:] + '</i>')
                if c.isServer():
                    c.sendNetMessageToAllButOne('S!' + ' ' + handle +
                                                ' ' + str[2:],
                                                handle)
            elif str[0] == 's': #Spoofed talk
                words = unicode(str).split()
                c.insertChatMessage(words[1] + ": " +
                                    " ".join(words[2:]))
            elif str[0] == 'S': #Spoofed emote
                words = unicode(str).split()
                c.insertChatMessage('<i>' + words[1] + " " +
                                    " ".join(words[2:]) + '</i>')
            elif str[0] == 'w': #Whisper/tell
                words = unicode(str).split()
                c.insertChatMessage('From ' + words[1] + ': ' +
                                    " ".join(words[2:]))
            elif str[0] == 'W': #Whisper/tell requiring relay
                words = unicode(str).split()
                if words[1] == c.getLocalHandle():
                    c.insertChatMessage('From ' + handle + ': ' +
                                        " ".join(words[2:]))
                else:
                    c.sendNetMessageToHandle('w!' + " " + handle + " " +
                                             " ".join(words[2:]), words[1])
            elif str[0] == 'r': #Die roll
                c.insertChatMessage(str[2:])
                if c.isServer():
                    c.sendNetMessageToAllButOne(str, handle)
            elif str[0] == 'u': #User message
                words = unicode(str).split()
                if words[1] == 'join':
                    c.insertChatMessage('<b>' + " ".join(words[2:]) +
                                        " has joined the game" + '</b>')
                elif words[1] == 'leave':
                    c.insertChatMessage('<b>' + " ".join(words[2:]) +
                                        " has left the game" + '</b>')
            elif str[0] == 'n': #Map file
                #This isn't useful, just demonstrating principle
                loadedmappe = rggTileLoader.loadFromString(str[2:])
            else:
                print 'Malformed or unrecognised data received.'
        else:
            print 'Malformed data received.'
    else:
        print 'Badly malformed data received.'

def newConnection(handle):
    c.insertChatMessage("<b>" + handle + " has joined" + "</b>")
    if c.isServer():
        c.sendNetMessageToAllButOne('u!' + ' join ' + handle, handle)

def disConnection(handle):
    c.insertChatMessage("<b>" + handle + " has left the game" + "</b>")
    if c.isServer():
        c.sendNetMessageToAllButOne('u!' + ' leave ' + handle, handle)
    
QtCore.QObject.connect(c, QtCore.SIGNAL("newNetMessageSignal(QString, QString)"), newNetEvent)
QtCore.QObject.connect(c, QtCore.SIGNAL("connectedSignal(QString)"), newConnection)
QtCore.QObject.connect(c, QtCore.SIGNAL("disconnectedSignal(QString)"), disConnection)
QtCore.QObject.connect(c, QtCore.SIGNAL("newChatInputSignal(QString)"), newEvent)

c.start()
