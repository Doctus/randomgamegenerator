import bmainmod, rggNameGen, rggTileLoader

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
        elif words[0].lower() == '/me' or '/emote':
            if len(words) == 1:
                action = ("Syntax: /me DOES ACTION. Displays '[HANDLE] DOES "
                        "ACTION' in italic font.")
            else:
                action = ''.join(words[1:])
            c.insertChatMessage('<i>' + c.getLocalHandle() + ' ' +
                                unicode(action) + '</i>')
            c.sendNetMessageToAll('T!' + unicode(action))
        elif words[0].lower() == '/w' or '/t' or '/whisper' or '/tell':
            if len(words) == 1:
                mesg = ("Syntax: /whisper HANDLE MESSAGE. Sends a message " +
                        "only to the specified user. Spaces MUST be correct.")
                c.insertChatMessage(unicode(mesg))
            else:
                target = words[1]
                mesg = " ".join(words[2:])
                c.insertChatMessage('To ' + unicode(target) + ': ' +
                                    unicode(mesg))
                if isServer():
                    c.sendNetMessageToHandle('w!' + unicode(mesg), target)
                else:
                    c.sendNetMessageToAll('W! ' + target + ' ' + unicode(mesg))
    else:
        c.insertChatMessage(c.getLocalHandle() + ": " + unicode(str))
        c.sendNetMessageToAll("t!" + unicode(str))

def newNetEvent(str, handle):
    if len(str) > 1:
        if str[1] == '!':
            if str[0] == 't': #Ordinary chat message
                c.insertChatMessage(unicode(handle) + ": " + unicode(str[2:]))
                if isServer():
                    c.sendNetMessageToAllButOne('t!' + unicode(str),
                                                unicode(handle))
            elif str[0] == 'T': #Emote message
                c.insertChatMessage('<i>' + unicode(handle) + " " +
                                    unicode(str[2:]) + '</i>')
                if isServer():
                    c.sendNetMessageToAllButOne('T!' + unicode(str),
                                                unicode(handle))
            elif str[0] == 'w': #Whisper/tell
                c.insertChatMessage('From ' + unicode(handle) + ': ' +
                                    unicode(str[2:]))
            elif str[0] == 'W': #Whisper/tell requiring relay
                words = unicode(str).split()
                c.sendNetMessageToHandle('w!' + unicode(" ".join(words[2:])),
                                         words[1])
            elif str[0] == 'u': #User message
                words = unicode(str).split()
                if words[1] == 'join':
                    c.insertChatMessage('<b>' + unicode(words[2:]) +
                                        " has joined the game" + '</b>')
                elif words[1] == 'leave':
                    c.insertChatMessage('<b>' + unicode(words[2:]) +
                                        " has left the game" + '</b>')
            elif str[0] == 'n': #Map file
                #This isn't useful, just demonstrating principle
                loadedmappe = rggTileLoader.loadFromString(str[2:])
            else:
                print 'Malformed or unrecognised data received.'
        else:
            print 'Malformed data received.'
    else:
        print 'Malformed data received.'

def newConnection(handle):
    c.insertChatMessage(unicode(handle) + " has joined")
    c.sendNetMessageToAll('u!' + ' join ' + unicode(handle))

def disConnection(handle):
    c.insertChatMessage(unicode(handle) + " has left the game")
    c.sendNetMessageToAll('u!' + ' leave ' + unicode(handle))
    
c.newChatInputSignal.connect(newEvent)
c.newNetMessageSignal.connect(newNetEvent)
c.connectedSignal.connect(newConnection)
c.disconnectedSignal.connect(disConnection)

c.start()
