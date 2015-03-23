from . import rggRemote, rggViews, rggEvent

def connectChatWidgetEvents(widget):
	widget.chatInput.connect(rggEvent.chatInputEvent)

def connectICChatWidgetEvents(widget):
	widget.ICChatInput.connect(rggEvent.ICChatInputEvent)

def connectDiceWidgetEvents(widget):
	widget.rollRequested.connect(rggViews.rollDice)
	widget.macroRequested.connect(rggViews.addMacro)

def connectUserListWidgetEvents(widget):
	widget.selectGM.connect(rggViews.playerOptions)
	widget.kickPlayer.connect(rggViews.kick)
	widget.requestBanlistUpdate.connect(rggViews.updateBanlist)

def connectMenuEvents(menu):
	menu.newMapAct.triggered.connect(rggViews.newMap)
	menu.loadMapAct.triggered.connect(rggViews.loadMap)
	menu.saveSessAct.triggered.connect(rggViews.saveSession)
	menu.loadSessAct.triggered.connect(rggViews.loadSession)
	menu.saveMapAct.triggered.connect(rggViews.saveMap)
	menu.closeSpecificMapAct.triggered.connect(rggViews.closeMap)
	menu.closeMapAct.triggered.connect(rggViews.closeAllMaps)
	menu.clearSessAct.triggered.connect(rggViews.clearSession)
	menu.deletePogsAct.triggered.connect(rggViews.deleteAllPogs)
	menu.saveCharsAct.triggered.connect(rggViews.saveChars)
	menu.loadCharsAct.triggered.connect(rggViews.loadChars)
	menu.gfxSettingsAct.triggered.connect(rggViews.configureGfx)
	menu.drawTimerSettingsAct.triggered.connect(rggViews.configureDrawTimer)
	menu.hostGameAct.triggered.connect(rggViews.hostGame)
	menu.joinGameAct.triggered.connect(rggViews.joinGame)
	menu.disconnectAct.triggered.connect(rggViews.disconnectGame)
	menu.createSurveyAct.triggered.connect(rggViews.createSurvey)
	menu.sendFileAct.triggered.connect(rggViews.promptSendFile)
	menu.toggleAlertsAct.triggered.connect(rggViews.toggleAlerts)
	menu.toggleTimestampsAct.triggered.connect(rggViews.toggleTimestamps)
	menu.setTimestampFormatAct.triggered.connect(rggViews.promptTimestampFormat)
	menu.thicknessMenu.triggered.connect(rggViews.setThickness)
	menu.colourMenu.triggered.connect(rggViews.setLineColour)
	menu.langMenu.triggered.connect(rggViews.setLanguage)
	menu.portraitMenu.triggered.connect(rggViews.setPortraitSize)
	menu.stylesMenu.triggered.connect(rggViews.changeStyle)

def connectClientEvents(client):
	client.connected.connect(rggRemote.clientConnect)
	client.disconnected.connect(rggRemote.clientDisconnect)
	client.objectReceived.connect(rggRemote.clientReceive)
	client.fileReceived.connect(rggRemote.clientFileReceive)
	client.fileEvent.connect(rggViews.transferFileResponse)
	client.partialTransferEvent.connect(rggViews.partialTransferResponse)

def connectServerEvents(server):
	server.connected.connect(rggRemote.serverConnect)
	server.disconnected.connect(rggRemote.serverDisconnect)
	server.transferDisconnected.connect(rggRemote.serverTransferDisconnect)
	server.kicked.connect(rggRemote.serverKick)
	server.objectReceived.connect(rggRemote.serverReceive)
	server.fileReceived.connect(rggRemote.serverFileReceive)
	server.fileEvent.connect(rggViews.transferFileResponse)
	server.partialTransferEvent.connect(rggViews.partialTransferResponse)

def connectGLWidgetEvents(glwidget):
	glwidget.mouseMoveSignal.connect(rggEvent.mouseMoveEvent)
	glwidget.mousePressSignal.connect(rggEvent.mousePressEvent)
	glwidget.mouseReleaseSignal.connect(rggEvent.mouseReleaseEvent)
	glwidget.keyPressSignal.connect(rggEvent.keyPressEvent)
	glwidget.keyReleaseSignal.connect(rggEvent.keyReleaseEvent)
	glwidget.pogPlace.connect(rggViews.placePog)

def connectEvents(client, server, menu, chatWidget, ICChatWidget, diceWidget, userListWidget, glWidget):
	connectServerEvents(server)
	connectClientEvents(client)
	connectMenuEvents(menu)
	connectChatWidgetEvents(chatWidget)
	connectICChatWidgetEvents(ICChatWidget)
	connectDiceWidgetEvents(diceWidget)
	connectUserListWidgetEvents(userListWidget)
	connectGLWidgetEvents(glWidget)
