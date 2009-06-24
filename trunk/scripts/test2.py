import bmainmod, rggNameGen

c = bmainmod.bMain()

def newEvent(str):
    if str[0] == '/':
        words = unicode(str).split()
        if words[0] == '/randomname':
            if len(words) == 1:
                name = ("Syntax: /randomname NAMETYPE. Caps and spaces" +
                        "are ignored. Some valid arguments are " +
                        "JAPANESEFEMALEFULL and DwArF M aLe")
            else:
                name = rggNameGen.getName(''.join(words[1:]).lower())
            print name
            c.insertChatMessage(unicode(name))
    else:
        print unicode(str)
        c.insertChatMessage("Me: " + unicode(str))
        c.sendChatMessageToAll(unicode(str))

def newNetEvent(str, handle):
    print unicode(handle) + ": " + unicode(str)
    c.insertChatMessage(unicode(handle) + ":" + unicode(str))

c.newChatInput.connect(newEvent)
c.newNetMessageSignal.connect(newNetEvent)

c.start()
