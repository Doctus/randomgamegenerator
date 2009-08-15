import time, random, os, base64
import _bmainmod, rggNameGen, rggDice, rggMap, rggTile, rggPog, rggDockWidget, rggDialogs
from PyQt4 import QtCore, QtGui

random.seed()

c = _bmainmod.bMain()
Maps = []
currentMap = [0]
manipulatedPogs = [None, None, None, []] #Pog being selected/leftclicked; pog being right-clicked; pog being hovered over; other pogs selected with ctrl
lastMouseLoc = [0, 0]
global tilePasting
global tilePastingIndex
tilePasting = False
placingPog = [False, "path"]

dwidget = rggDockWidget.diceRoller(c.getMainWindow())
pwidget = rggDockWidget.pogPalette(c.getMainWindow())
#mwidget = rggDockWidget.mapEditor(c.getMainWindow())

def _linkedName(inp):
    return str('<a href="/tell ' + inp + '" title="' + inp + '">' + inp + '</a>')

def newEvent(st):
    if (len(st) <= 0) or ('title=' in st):
        return
    if ('<' in st and '>' not in st) or ('<' in st and '>' in st and '<' in str(st)[str(st).rfind('>'):]):
        c.insertChatMessage(c.tr("Please type &#38;#60; if you wish to include &#60; in your message."))
        return
    if st[0] == '/':
        words = unicode(st).split()
        if words[0].lower() == '/cam':
            print 'x: ' + str(c.getCamX()) + '\ny: ' + str(c.getCamY())
        if words[0].lower() == '/swapmap':
            namestemp = []
            for item in Maps:
                namestemp.append(item.mapname)
            for pog in Maps[currentMap[0]].Pogs:
                pog.hide()
            Maps[currentMap[0]].hide()
            currentMap[0] = c.displayUserDialogChoice("Load map:", namestemp)
            Maps[currentMap[0]].show()
            for pog in Maps[currentMap[0]].Pogs:
                pog.show()
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
            c.insertChatMessage(rggNameGen.getTechniqueName(str(st)))
        elif words[0].lower() == '/advice':
            c.insertChatMessage(rggNameGen.getAdvice())
        elif words[0].lower() == '/roll':
            if len(words) == 1:
                c.insertChatMessage("Syntax: /roll DICE. Dice can be " +
                                    "like '3d4 - 2 + 1d20' or '5k3' or" +
                                    " other variants depending on " +
                                    "development. See also /troll")
            else:
                rolltext = (_linkedName(c.getLocalHandle()) + c.tr(" rolls ") +
                            rggDice.roll(" ".join(words[1:])))
                c.insertChatMessage(rolltext)
                c.sendNetMessageToAll('r!' + rolltext)
        elif words[0].lower() == '/troll':
            rolltext = (c.getLocalHandle() + c.tr(" rolls ") + rggDice.roll('2d6'))
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
        elif words[0].lower() == '/addmacro':
            validation = unicode(c.getUserTextInput("What dice should be rolled?"))
            if "error" not in rggDice.roll(validation).lower() and "not yet implemented" not in rggDice.roll(validation).lower():
                dwidget.addMacro(validation, unicode(c.getUserTextInput("What should the macro be called?")))
            else:
                c.insertChatMessage('Malformed macro. Formatting help is available in "/roll" command.')
        elif words[0].lower() == '/placepog' and placingPog[0] == False:
            placingPog[0] = True
            placingPog[1] = " ".join(words[1:])
        elif words[0].lower() == '/newmap':
            newMap = rggMap.Map()
            newMapString = words[1:]
            newMap.loadFromString(newMapString)
            Maps.append(newMap)
            if len(Maps) > 0:
                for pog in Maps[currentMap[0]].Pogs:
                    pog.hide()
                Maps[currentMap[0]].hide()
            currentMap[0] = Maps.index(newMap)
            Maps[currentMap[0]].updateStringForm()
            Maps[currentMap[0]].show()
            c.sendNetMessageToAll(Maps[currentMap[0]].stringform)
    else:
        c.insertChatMessage(_linkedName(c.getLocalHandle()) + ": " + st)
        c.sendNetMessageToAll("t!" + st)

def newNetEvent(st, handle):
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
            elif st[0] == 'p': #Pog edit
                words = unicode(st).split()
                #print words
                if words[1] == 'm': #Pog movement
                    if Maps[currentMap[0]].pogsByID.has_key(int(words[2])):
                        Maps[currentMap[0]].pogsByID[int(words[2])].absoluteMove(int(words[3]), int(words[4]))
                elif words[1] == 'n': #Pog naming
                    if Maps[currentMap[0]].pogsByID.has_key(int(words[2])):
                        Maps[currentMap[0]].pogsByID[int(words[2])].name = " ".join(words[3:])
                elif words[1] == 'c': #Pog creation
                    Maps[currentMap[0]].addPog(rggPog.Pog(1, int(words[2]), int(words[3]), int(words[4]), int(words[5]), 1, " ".join(words[6:])))
                    if not os.path.exists(" ".join(words[6:])):
                        c.sendNetMessageToHandle('I! ' + " ".join(words[6:]), handle)
                elif words[1] == 'l': #Pog layer change
                    if Maps[currentMap[0]].pogsByID.has_key(int(words[2])):
                        Maps[currentMap[0]].pogsByID[int(words[2])].changeLayer(int(words[3]))
                if c.isServer():
                    c.sendNetMessageToAllButOne(st, handle)
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
                #print st
                mapdat = unicode(st).split()
                if not os.path.exists(mapdat[mapdat.index('t!')+1]):
                    c.sendNetMessageToHandle('I! ' + mapdat[mapdat.index('t!')+1], handle)
                newMap = rggMap.Map()
                newMap.loadFromString(mapdat)
                Maps.append(newMap)
                for pog in Maps[currentMap[0]].Pogs:
                    pog.hide()
                currentMap[0] = Maps.index(newMap)
                for pog in Maps[currentMap[0]].Pogs:
                    pog.show()
                for neededImage in Maps[currentMap[0]].checkPogImages():
                    c.sendNetMessageToHandle('I! ' + neededImage, handle)
                if c.isServer():
                    c.sendNetMessageToAllButOne(st, handle)
            elif st[0] == 'i': #Image file
                words = unicode(st).split()
                imgpath = words[1]
                img = base64.b64decode(words[2])
                f = open(unicode(imgpath), 'wb')
                f.write(img)
                f.close()
                c.changeImage(unicode(imgpath), unicode(imgpath))
                for mappe in Maps:
                    mappe.reloadTiles(unicode(imgpath))
            elif st[0] == 'I': #Image request
                words = unicode(st).split()
                imgpath = words[1]
                f = open(imgpath, 'rb')
                imgdat = base64.b64encode(f.read())
                f.close()
                c.sendNetMessageToHandle("i! " + imgpath + " " + imgdat, handle)
            else:
                print 'Malformed or unrecognised data received: ' + unicode(st)
        else:
            print 'Malformed data received: ' + unicode(st)
    else:
        print 'Badly malformed data received: ' + unicode(st)

def newConnection(handle):
    c.insertChatMessage("<b>" + handle + " has joined" + "</b>")
    if not c.isServer():
        global Maps
        Maps = []
    if c.isServer():
        for mappe in Maps:
            mappe.updateStringForm()
            c.sendNetMessageToHandle(mappe.stringform, handle)
        c.sendNetMessageToAllButOne('u!' + ' join ' + handle, handle)

def disConnection(handle):
    c.insertChatMessage("<b>" + handle + " has left the game" + "</b>")
    if c.isServer():
        c.sendNetMessageToAllButOne('u!' + ' leave ' + handle, handle)     

def newMap():
    mdia = rggDialogs.newMapDialog(c.getMainWindow())
    QtCore.QObject.connect(mdia, QtCore.SIGNAL("newChatInputSignal(QString)"), newEvent)

def loadMap(filename):
    f = open(filename, 'r')
    tmp = f.read().split()
    f.close()
    newMap = rggMap.Map()
    newMap.loadFromString(tmp)
    Maps.append(newMap)
    if len(Maps) > 0:
        for pog in Maps[currentMap[0]].Pogs:
            pog.hide()
        Maps[currentMap[0]].hide()
    currentMap[0] = Maps.index(newMap)
    for pog in Maps[currentMap[0]].Pogs:
        pog.show()
    Maps[currentMap[0]].show()
    c.sendNetMessageToAll(Maps[currentMap[0]].stringform)

def saveMap(filename):
    if c.displayUserDialogChoice("Edit map info?", ['Yes', 'No'], 1) == 0:
        Maps[currentMap[0]].mapname = unicode(c.getUserTextInput("What is the name of this map?"))
        Maps[currentMap[0]].authorname = unicode(c.getUserTextInput("Who is the author of this map?"))
    Maps[currentMap[0]].updateStringForm() #Ensure that the saved version is exactly what the user sees at the time of saving.
    f = open(unicode(filename), 'w')
    f.write(Maps[currentMap[0]].stringform)
    f.close()

def mouseDrag(x, y):
    if manipulatedPogs[0] != None:
        manipulatedPogs[0].relativeMove(x-lastMouseLoc[0], y-lastMouseLoc[1])
        c.sendNetMessageToAll('p! m ' + str(manipulatedPogs[0].ID) + ' ' + str(manipulatedPogs[0].x) + ' '
                                      + str(manipulatedPogs[0].y))
        if manipulatedPogs[3] is not []:
            for pog in manipulatedPogs[3]:
                if pog is not manipulatedPogs[0]: #To make sure we don't get double-alteration
                    pog.relativeMove(x-lastMouseLoc[0], y-lastMouseLoc[1])
                    c.sendNetMessageToAll('p! m ' + str(pog.ID) + ' ' + str(pog.x) + ' '
                                          + str(pog.y))
    elif tilePasting:
        global tilePasting
        global tilePastingIndex
        Maps[currentMap[0]].debugSetTile([(x+c.getCamX())/Maps[currentMap[0]].tilesize[0], (y+c.getCamY())/Maps[currentMap[0]].tilesize[1]], tilePastingIndex)
    lastMouseLoc[0] = x
    lastMouseLoc[1] = y

def mouseMove(x, y):
    if len(Maps) <= 0:
         return
    tooltipPogTemp = None
    for pog in Maps[currentMap[0]].Pogs:
        if pog.getPointCollides([x+c.getCamX(), y+c.getCamY()]):
            if tooltipPogTemp == None:
                tooltipPogTemp = pog
            elif pog.layer > tooltipPogTemp.layer:
                tooltipPogTemp = pog
    if manipulatedPogs[2] == tooltipPogTemp:
        return
    manipulatedPogs[2] = tooltipPogTemp
    if manipulatedPogs[2] is not None:
        if manipulatedPogs[2].getPrintableAttributes() is not None:
            displayLoc = manipulatedPogs[2].getOverheadTooltipLoc()
            c.displayTooltip(manipulatedPogs[2].getPrintableAttributes(), displayLoc[0]-c.getCamX(), displayLoc[1]-c.getCamY())

def mouseRelease(x, y, t):
    manipulatedPogs[0] = None
    manipulatedPogs[1] = None

def mousePress(x, y, t):
    #print 'mouse press event ' + str(t) + ' at (' + str(x) + ', ' + str(y) + ')'
    lastMouseLoc[0] = x
    lastMouseLoc[1] = y
    if Maps == []: return
    if t == 0:
        if placingPog[0]:
            placingPog[0] = False
            infograb = QtGui.QPixmap(placingPog[1])
            Maps[currentMap[0]].addPog(rggPog.Pog(1, x+c.getCamX(), y+c.getCamY(), infograb.width(), infograb.height(), 1, placingPog[1]))
            c.sendNetMessageToAll('p! c ' + " ".join([str(x+c.getCamX()), str(y+c.getCamY()), str(infograb.width()), str(infograb.height()), placingPog[1]]))
        elif tilePasting:
            global tilePasting
            global tilePastingIndex
            Maps[currentMap[0]].debugSetTile([(x+c.getCamX())/Maps[currentMap[0]].tilesize[0], (y+c.getCamY())/Maps[currentMap[0]].tilesize[1]], tilePastingIndex)
        else:
            for pog in Maps[currentMap[0]].Pogs:
                if pog.getPointCollides([x+c.getCamX(), y+c.getCamY()]):
                    if manipulatedPogs[0] == None:
                        manipulatedPogs[0] = pog
                    elif pog.layer > manipulatedPogs[0].layer:
                        manipulatedPogs[0] = pog
            if manipulatedPogs[0] not in manipulatedPogs[3]:
                manipulatedPogs[3] = []
    elif t == 2:
        for pog in Maps[currentMap[0]].Pogs:
            if pog.getPointCollides([x+c.getCamX(), y+c.getCamY()]):
                if manipulatedPogs[1] == None:
                    manipulatedPogs[1] = pog
                elif pog.layer > manipulatedPogs[1].layer:
                    manipulatedPogs[1] = pog
        if manipulatedPogs[1] != None:
            selected = c.showPopupMenuAt(x, y, ["Set name", "Generate name", "Set Layer"])
            if selected == 0:
                manipulatedPogs[1].name = c.getUserTextInput("Enter a name for this pog.")
                c.sendNetMessageToAll('p! n ' + str(manipulatedPogs[1].ID) + ' ' + unicode(manipulatedPogs[1].name))
            elif selected == 1:
                gentype = ''.join(unicode(c.getUserTextInput("Enter a generator command. See /randomname for syntax. Multi-pog compatible."))).lower()
                manipulatedPogs[1].name = rggNameGen.getName(gentype)
                c.sendNetMessageToAll('p! n ' + str(manipulatedPogs[1].ID) + ' ' + unicode(manipulatedPogs[1].name))
                if manipulatedPogs[3] is not []:
                    for pog in manipulatedPogs[3]:
                        pog.name = rggNameGen.getName(gentype)
                        c.sendNetMessageToAll('p! n ' + str(pog.ID) + ' ' + unicode(pog.name))
            elif selected == 2:
                newlayer = abs(int(c.getUserTextInput("Enter a layer. Pogs on higher layers are displayed over those on lower layers. Should be a positive integer. Multi-pog compatible.")))
                manipulatedPogs[1].changeLayer(newlayer)
                c.sendNetMessageToAll('p! l ' + str(manipulatedPogs[1].ID) + ' ' + str(manipulatedPogs[1].layer))
                if manipulatedPogs[3] is not []:
                    for pog in manipulatedPogs[3]:
                        pog.changeLayer(newlayer)
                        c.sendNetMessageToAll('p! l ' + str(pog.ID) + ' ' + str(pog.layer))
        else:
            if tilePasting is False:
                selected = c.showPopupMenuAt(x, y, ["Create Pog (Temp Command)", "Begin Tile Pasting (Temp Command)"])
            else:
                selected = c.showPopupMenuAt(x, y, ["Create Pog (Temp Command)", "Cease Tile Pasting (Temp Command)"])
            if selected == 0:
                pogsrc = unicode(c.getUserTextInput("What is the path to the pog image?"))
                pogsizeraw = unicode(c.getUserTextInput("Image height/width separated by space (e.g. '16 32')"))
                pogsizeW = int(pogsizeraw.split()[0])
                pogsizeH = int(pogsizeraw.split()[1])
                Maps[currentMap[0]].addPog(rggPog.Pog(1, x, y, pogsizeW, pogsizeH, 1, pogsrc))
                c.sendNetMessageToAll('p! c ' + " ".join([str(x), str(y), str(pogsizeW), str(pogsizeH), pogsrc]))
            elif selected == 1 and tilePasting is False:
                global tilePasting
                global tilePastingIndex
                tilePasting = True
                tilePastingIndex = Maps[currentMap[0]].debugGetTile([(x+c.getCamX())/Maps[currentMap[0]].tilesize[0], (y+c.getCamY())/Maps[currentMap[0]].tilesize[1]])
            elif selected == 1:
                global tilePasting
                tilePasting = False
    elif t == 3:
        if placingPog[0]:
            infograb = QtGui.QPixmap(placingPog[1])
            Maps[currentMap[0]].addPog(rggPog.Pog(1, x+c.getCamX(), y+c.getCamY(), infograb.width(), infograb.height(), 1, placingPog[1]))
            c.sendNetMessageToAll('p! c ' + " ".join([str(x+c.getCamX()), str(y+c.getCamY()), str(infograb.width()), str(infograb.height()), placingPog[1]]))
        else:
            pogappendtemp = [None]
            for pog in Maps[currentMap[0]].Pogs:
                if pog.getPointCollides([x+c.getCamX(), y+c.getCamY()]):
                    if pogappendtemp[0] == None:
                        pogappendtemp[0] = pog
                    elif pog.layer > pogappendtemp[0].layer:
                        pogappendtemp[0] = pog
            if pogappendtemp[0] is not None and pogappendtemp[0] not in manipulatedPogs[3]:
                manipulatedPogs[3].append(pogappendtemp[0])
            elif pogappendtemp[0] is not None and pogappendtemp[0] in manipulatedPogs[3]:
                manipulatedPogs[3].remove(pogappendtemp[0])
    elif t == 1: #DEBUG STUFF
        Maps[currentMap[0]].debugMorphTile([(x+c.getCamX())/Maps[currentMap[0]].tilesize[0], (y+c.getCamY())/Maps[currentMap[0]].tilesize[1]], c.getTileCountOfImage(Maps[currentMap[0]].tileset))
    
QtCore.QObject.connect(c, QtCore.SIGNAL("newNetMessageSignal(QString, QString)"), newNetEvent)
QtCore.QObject.connect(c, QtCore.SIGNAL("connectedSignal(QString)"), newConnection)
QtCore.QObject.connect(c, QtCore.SIGNAL("disconnectedSignal(QString)"), disConnection)
QtCore.QObject.connect(c, QtCore.SIGNAL("newChatInputSignal(QString)"), newEvent)
QtCore.QObject.connect(c, QtCore.SIGNAL("newMapSignal( )"), newMap)
QtCore.QObject.connect(c, QtCore.SIGNAL("loadMapSignal(QString)"), loadMap)
QtCore.QObject.connect(c, QtCore.SIGNAL("saveMapSignal(QString)"), saveMap)
QtCore.QObject.connect(c, QtCore.SIGNAL("mouseMoveSignal(int, int)"), mouseMove)
QtCore.QObject.connect(c, QtCore.SIGNAL("mouseDragSignal(int, int)"), mouseDrag)
QtCore.QObject.connect(c, QtCore.SIGNAL("mousePressSignal(int, int, int)"), mousePress)
QtCore.QObject.connect(c, QtCore.SIGNAL("mouseReleaseSignal(int, int, int)"), mouseRelease)

QtCore.QObject.connect(dwidget, QtCore.SIGNAL("newChatInputSignal(QString)"), newEvent)
QtCore.QObject.connect(pwidget, QtCore.SIGNAL("newChatInputSignal(QString)"), newEvent)

c.start()
