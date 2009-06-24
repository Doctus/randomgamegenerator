import bmainmod

c = bmainmod.bMain()

def newEvent(str):
    print unicode(str)
    c.insertChatMessage("Me: " + unicode(str))
    c.sendChatMessageToAll(unicode(str))

def newNetEvent(str, handle):
    print unicode(handle) + ": " + unicode(str)
    c.insertChatMessage(unicode(handle) + ":" + unicode(str))

c.newChatInput.connect(newEvent)
c.newNetMessageSignal.connect(newNetEvent)

c.start()
