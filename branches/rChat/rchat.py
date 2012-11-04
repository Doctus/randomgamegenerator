if __name__ == '__main__':
    from rggSystem import injectMain, SAVE_DIR
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4.QtOpenGL import *

    from rggJson import loadString, jsonload
    import os, sys
    
    fieldtemp = ["English"]
    app = QApplication(['RChat'])

    try:
        js = jsonload(os.path.join(SAVE_DIR, "lang_settings.rgs"))
        fieldtemp[0] = loadString('lang.language', js.get('language'))
    except:
        print "no language settings detected"
        pass

    if fieldtemp[0] != "English":
        transfile = ""
        if fieldtemp[0] == "Japanese":
            transfile = "rgg_py_ja"
        if fieldtemp[0] == "Dutch":
            transfile = "rgg_py_nl"
        if fieldtemp[0] == "German":
            transfile = "rgg_py_de"

        trans = QTranslator()
        if not trans.load(transfile):
            print transfile + "not found"
        app.installTranslator(trans)

    main = injectMain()
    
    import rggSystem, rggRPC, rggChat, rggICChat, rggViews, rggRemote, rggEvent
    
    # Initialize view state.
    s = rggViews._state
    s.initialize(app)
    
    # EVENT WIRING
    # amounts to configuration
    
    # chat widget
    s.cwidget.chatInput.connect(rggEvent.chatInputEvent)
    #s.icwidget.ICChatInput.connect(rggEvent.ICChatInputEvent)
    
    # dice widget
    s.dwidget.rollRequested.connect(rggViews.rollDice)
    s.dwidget.macroRequested.connect(rggViews.addMacro)
    
    # user list widget
    s.uwidget.kickPlayer.connect(rggViews.kick)
    s.uwidget.requestBanlistUpdate.connect(rggViews.updateBanlist)
    
    # menu items
    s.menu.hostGameAct.triggered.connect(rggViews.hostGame)
    s.menu.joinGameAct.triggered.connect(rggViews.joinGame)
    s.menu.disconnectAct.triggered.connect(rggViews.disconnectGame)
    s.menu.toggleAlertsAct.triggered.connect(rggViews.toggleAlerts)
    s.menu.toggleTimestampsAct.triggered.connect(rggViews.toggleTimestamps)
    s.menu.setTimestampFormatAct.triggered.connect(rggViews.promptTimestampFormat)
    s.menu.langMenu.triggered.connect(rggViews.setLanguage)
    
    server = rggRPC.server
    client = rggRPC.client
    
    client.connected.connect(rggRemote.clientConnect)
    client.disconnected.connect(rggRemote.clientDisconnect)
    client.objectReceived.connect(rggRemote.clientReceive)
    client.fileReceived.connect(rggRemote.clientFileReceive)
    server.connected.connect(rggRemote.serverConnect)
    server.disconnected.connect(rggRemote.serverDisconnect)
    server.kicked.connect(rggRemote.serverKick)
    server.objectReceived.connect(rggRemote.serverReceive)
    server.fileReceived.connect(rggRemote.serverFileReceive)
    
    # Start execution
    try:
        main.show()
        app.exec_()
    finally:
        client.close()