import bmainmod, rggNameGen, rggTileLoader, rggDice, rggTile
from PyQt4 import QtCore

c = bmainmod.bMain()
testMappe = rggTileLoader.Map()

#testimage = rggTile.tile(0, 0, 32, 32, 0, "../data/town.png")

def _linkedName(inp):
    return str('<a href="/tell ' + inp + '" title="' + inp + '">' + inp + '</a>')

def newEvent(st):
    if (len(st) <= 0) or ('title=' in st):
        return
    if st[0] == '/':
        words = unicode(st).split()
        if words[0].lower() == '/test':
            #testimage.setTile(testimage.getTile() + 1)
            testMappe.DEBUGSaveToFile()
            testMappe.DEBUGLoadFromFile()
        if words[0].lower() == '/test2':
            c.sendNetMessageToAll(testMappe.stringform)
        if words[0].lower() == '/help' or words[0].lower() == '/h':
            c.insertChatMessage("Command Help:<br> Typing ordinary text and pressing 'enter' " +
                                "will display to all players. Other commands may be invoked " +
                                "with '/' plus the name of the command plus any arguments." +
                                "<br>Commands<br>/randomname<br>/techname<br>/roll<br>/troll"+
                                "<br>/emote<br>/tell")
        elif words[0].lower() == '/randomname':
            if len(words) == 1:
                name = ("Syntax: /randomname NAMETYPE. Caps and spaces " +
                        "are ignored. Some valid arguments are " +
                        "JAPANESEFEMALEFULL and DwArF M aLe")
            else:
                name = rggNameGen.getName(''.join(words[1:]).lower())
            c.insertChatMessage(unicode(name))
        elif words[0].lower() == '/techname' or words[0].lower() == '/techniquename':
            if len(words) == 1:
                c.insertChatMessage(rggNameGen.getTechniqueName())
            else: #it's a pain but doing it this way ensures order doesn't need to be memorised...
                argCompilation = ['rand', 'rand', 'rand', -1, False]
                parse = str(st) #Needs to be done for find() to be invoked
                if parse.find("martial") != -1:
                    argCompilation[0] = 'martial'
                elif parse.find("magic") != -1:
                    argCompilation[0] = 'magic'
                if parse.find("fire") != -1:
                    argCompilation[1] = 'fire'
                elif parse.find("ice") != -1:
                    argCompilation[1] = 'ice'
                elif parse.find("darkness") != -1:
                    argCompilation[1] = 'darkness'
                elif parse.find("light") != -1:
                    argCompilation[1] = 'light'
                elif parse.find("psionic") != -1:
                    argCompilation[1] = 'psionic'
                elif parse.find("violent") != -1:
                    argCompilation[1] = 'violent'
                if parse.find("good") != -1:
                    argCompilation[2] = 'good'
                elif parse.find("neutral") != -1:
                    argCompilation[2] = 'neutral'
                elif parse.find("evil") != -1:
                    argCompilation[2] = 'evil'
                if parse.find("simple") != -1:
                    argCompilation[3] = 2
                elif parse.find("moderate") != -1:
                    argCompilation[3] = 3
                elif parse.find("complex") != -1:
                    argCompilation[3] = 4
                if parse.find("awesome") != -1 or parse.find("hotblood") != -1 or parse.find("cool") != -1:
                    argCompilation[4] = True
                c.insertChatMessage(rggNameGen.getTechniqueName(argCompilation[0], argCompilation[1], argCompilation[2],
                                                                argCompilation[3], argCompilation[4]))
        elif words[0].lower() == '/roll':
            if len(words) == 1:
                c.insertChatMessage("Syntax: /roll DICE. Dice can be " +
                                    "like '3d4 - 2 + 1d20' or '5k3' or" +
                                    " other variants depending on " +
                                    "development. See also /troll")
            else:
                rolltext = (_linkedName(c.getLocalHandle()) + " rolls " +
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
            c.insertChatMessage('<i>' + _linkedName(c.getLocalHandle()) + ' ' +
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
        c.insertChatMessage(_linkedName(c.getLocalHandle()) + ": " + st)
        c.sendNetMessageToAll("t!" + st)

def newNetEvent(st, handle):
    #c.insertChatMessage("DEBUG: " + str)
    if len(st) > 1:
        if st[1] == '!':
            if st[0] == 't': #Ordinary chat message
                c.insertChatMessage(_linkedName(unicode(handle)) + ": " + st[2:])
                if c.isServer():
                    c.sendNetMessageToAllButOne('s!' + ' ' + handle +
                                                ' ' + st[2:],
                                                handle)
            elif st[0] == 'T': #Emote message
                c.insertChatMessage('<i>' + _linkedName(unicode(handle)) + " " +
                                    st[2:] + '</i>')
                if c.isServer():
                    c.sendNetMessageToAllButOne('S!' + ' ' + handle +
                                                ' ' + st[2:],
                                                handle)
            elif st[0] == 's': #Spoofed talk
                words = unicode(st).split()
                c.insertChatMessage(_linkedName(words[1]) + ": " +
                                    " ".join(words[2:]))
            elif st[0] == 'S': #Spoofed emote
                words = unicode(st).split()
                c.insertChatMessage('<i>' + _linkedName(words[1]) + " " +
                                    " ".join(words[2:]) + '</i>')
            elif st[0] == 'w': #Whisper/tell
                words = unicode(st).split()
                c.insertChatMessage('From ' + _linkedName(words[1]) + ': ' +
                                    " ".join(words[2:]))
            elif st[0] == 'W': #Whisper/tell requiring relay
                words = unicode(st).split()
                if words[1] == c.getLocalHandle():
                    c.insertChatMessage('From ' + _linkedName(handle) + ': ' +
                                        " ".join(words[2:]))
                else:
                    c.sendNetMessageToHandle('w!' + " " + handle + " " +
                                             " ".join(words[2:]), words[1])
            elif st[0] == 'r': #Die roll
                c.insertChatMessage(st[2:])
                if c.isServer():
                    c.sendNetMessageToAllButOne(st, handle)
            elif st[0] == 'u': #User message
                words = unicode(st).split()
                if words[1] == 'join':
                    c.insertChatMessage('<b>' + " ".join(words[2:]) +
                                        " has joined the game" + '</b>')
                elif words[1] == 'leave':
                    c.insertChatMessage('<b>' + " ".join(words[2:]) +
                                        " has left the game" + '</b>')
            elif st[0] == 'n': #Map file
                #This isn't useful, just demonstrating principle
                testMappe.loadFromString(str(st).split())
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

def loadMap(filename):
    print c.displayUserDialogChoice("Test!", ["One", "Two", "Three"], 2)
    #testMappe.LoadFromFile(filename)
    
QtCore.QObject.connect(c, QtCore.SIGNAL("newNetMessageSignal(QString, QString)"), newNetEvent)
QtCore.QObject.connect(c, QtCore.SIGNAL("connectedSignal(QString)"), newConnection)
QtCore.QObject.connect(c, QtCore.SIGNAL("disconnectedSignal(QString)"), disConnection)
QtCore.QObject.connect(c, QtCore.SIGNAL("newChatInputSignal(QString)"), newEvent)
QtCore.QObject.connect(c, QtCore.SIGNAL("loadMapSignal(QString)"), loadMap)

c.start()
