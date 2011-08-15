if __name__ == '__main__':
    from rggSystem import injectMain, SAVE_DIR
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4.QtOpenGL import *

    from rggJson import loadString, jsonload
    import os
    
    fieldtemp = ["English"]
    app = QApplication(['RGG in Space'])

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

    qgf = QGLFormat.defaultFormat()
    qgf.setSampleBuffers(True)
    QGLFormat.setDefaultFormat(qgf)

    main = injectMain()
    
    import rggSystem, rggRPC, rggChat, rggICChat, rggViews, rggRemote, rggEvent
    
    # Initialize view state.
    s = rggViews._state
    s.initialize(app)
    
    # EVENT WIRING
    # amounts to configuration
    
    # mouse events
    main.glwidget.mouseMoveSignal.connect(rggEvent.mouseMoveEvent)
    main.glwidget.mousePressSignal.connect(rggEvent.mousePressEvent)
    main.glwidget.mouseReleaseSignal.connect(rggEvent.mouseReleaseEvent)
    
    # chat widget
    s.cwidget.chatInput.connect(rggEvent.chatInputEvent)
    s.icwidget.ICChatInput.connect(rggEvent.ICChatInputEvent)
    
    # dice widget
    s.dwidget.rollRequested.connect(rggViews.rollDice)
    s.dwidget.macroRequested.connect(rggViews.addMacro)
    
    # pog widget
    s.pwidget.pogPlaced.connect(rggViews.placePog)
    
    # user list widget
    s.uwidget.selectGM.connect(rggViews.selectGM)
    
    # menu items
    s.menu.newMapAct.triggered.connect(rggViews.newMap)
    s.menu.loadMapAct.triggered.connect(rggViews.loadMap)
    s.menu.saveSessAct.triggered.connect(rggViews.saveSession)
    s.menu.loadSessAct.triggered.connect(rggViews.loadSession)
    s.menu.saveMapAct.triggered.connect(rggViews.saveMap)
    s.menu.closeMapAct.triggered.connect(rggViews.closeAllMaps)
    s.menu.saveCharsAct.triggered.connect(rggViews.saveChars)
    s.menu.loadCharsAct.triggered.connect(rggViews.loadChars)
    s.menu.gfxSettingsAct.triggered.connect(rggViews.configureGfx)
    s.menu.hostGameAct.triggered.connect(rggViews.hostGame)
    s.menu.joinGameAct.triggered.connect(rggViews.joinGame)
    s.menu.disconnectAct.triggered.connect(rggViews.disconnectGame)
    s.menu.toggleAlertsAct.triggered.connect(rggViews.toggleAlerts)
    s.menu.toggleTimestampsAct.triggered.connect(rggViews.toggleTimestamps)
    s.menu.setTimestampFormatAct.triggered.connect(rggViews.promptTimestampFormat)
    s.menu.thicknessMenu.triggered.connect(rggViews.setThickness)
    s.menu.colourMenu.triggered.connect(rggViews.setLineColour)
    s.menu.langMenu.triggered.connect(rggViews.setLanguage)
    
    server = rggRPC.server
    client = rggRPC.client
    
    client.connected.connect(rggRemote.clientConnect)
    client.disconnected.connect(rggRemote.clientDisconnect)
    client.objectReceived.connect(rggRemote.clientReceive)
    client.fileReceived.connect(rggRemote.clientFileReceive)
    server.connected.connect(rggRemote.serverConnect)
    server.disconnected.connect(rggRemote.serverDisconnect)
    server.objectReceived.connect(rggRemote.serverReceive)
    server.fileReceived.connect(rggRemote.serverFileReceive)
    
    # Start execution
    try:
        main.show()
        app.exec_()
    finally:
        client.close()
