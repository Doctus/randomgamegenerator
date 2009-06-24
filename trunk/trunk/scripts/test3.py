import bmainmod, rggNameGen, rggTileLoader

c = bmainmod.bMain()

def newEvent(str):
    if str[0] == '/':
        words = unicode(str).split()
        if words[0] == '/randomname':
            if len(words) == 1:
                name = ("Syntax: /randomname NAMETYPE. Caps and spaces " +
                        "are ignored. Some valid arguments are " +
                        "JAPANESEFEMALEFULL and DwArF M aLe")
            else:
                name = rggNameGen.getName(''.join(words[1:]).lower())
            c.insertChatMessage(unicode(name))
        elif words[0] == '/me' or words[0] == '/emote':
            if len(words) == 1:
                action = ("Syntax: /me DOES ACTION. Displays '[HANDLE] DOES "
                        "ACTION' in italic font.")
            else:
                action = ''.join(words[1:])
            c.insertChatMessage('<i>' + c.getLocalHandle() + ' ' +
                                unicode(action) + '</i>')
            c.sendChatMessageToAll('T!' + unicode(action))
    else:
        c.insertChatMessage(c.getLocalHandle() + ": " + unicode(str))
        c.sendChatMessageToAll("t!" + unicode(str))

def newNetEvent(str, handle):
    if len(str) > 1:
        if str[1] == '!':
            if str[0] == 't': #Ordinary chat message
                c.insertChatMessage(unicode(handle) + ":" + unicode(str[2:]))
            elif str[0] == 'T': #Emote message
                c.insertChatMessage('<i>' + unicode(handle) +
                                    unicode(str[2:]) + '</i>')
            elif str[0] == 'n': #Map file
                #This isn't useful, just demonstrating principle
                loadedmappe = rggTileLoader.loadFromString(str[2:])
            else:
                print 'Malformed or unrecognised data received.'
        else:
            print 'Malformed data received.'
    else:
        print 'Malformed data received.'
    
c.newChatInput.connect(newEvent)
c.newNetMessageSignal.connect(newNetEvent)

c.start()
