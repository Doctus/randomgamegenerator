
if __name__ == '__main__':
    from rggSystem import injectMain
    main = injectMain()
    
    import rggSystem, rggRPC, rggChat, rggViews, rggRemote
    
    # Initialize view state.
    s = rggViews._state
    s.initialize()
    
    # EVENT WIRING
    # amounts to configuration
    
    # mouse events
    main.mouseMoveSignal.connect(rggViews.mouseMoveResponse)
    main.mousePressSignal.connect(rggViews.mousePressResponse)
    main.mouseReleaseSignal.connect(rggViews.mouseReleaseResponse)
    
    # chat widget
    s.cwidget.chatInput.connect(rggChat.chat)
    
    # dice widget
    s.dwidget.rollRequested.connect(rggViews.rollDice)
    s.dwidget.macroRequested.connect(rggViews.addMacro)
    
    # pog widget
    s.pwidget.pogPlaced.connect(rggViews.placePog)
    
    # menu items
    s.menu.newMapAct.triggered.connect(rggViews.newMap)
    s.menu.loadMapAct.triggered.connect(rggViews.loadMap)
    s.menu.saveMapAct.triggered.connect(rggViews.saveMap)
    s.menu.hostGameAct.triggered.connect(rggViews.hostGame)
    s.menu.joinGameAct.triggered.connect(rggViews.joinGame)
    s.menu.disconnectAct.triggered.connect(rggViews.disconnectGame)
    
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
        main.start()
    finally:
        client.close()
