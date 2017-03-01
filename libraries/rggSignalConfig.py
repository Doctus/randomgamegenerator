'''
    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''
from libraries.rggEvent import chatInputEvent, ICChatInputEvent, mouseMoveEvent
from libraries.rggEvent import mousePressEvent, mouseReleaseEvent, keyPressEvent, keyReleaseEvent
from libraries.rggRemote import clientConnect, clientDisconnect, clientReceive, clientFileReceive
from libraries.rggRemote import serverConnect, serverDisconnect, serverTransferDisconnect
from libraries.rggRemote import serverKick, serverReceive, serverFileReceive
from libraries.rggState import GlobalState
from libraries.rggViews import rollDice, addMacro, playerOptions, kick, updateBanlist, newMap
from libraries.rggViews import loadMap, promptTimestampFormat, saveMap, closeMap, closeAllMaps
from libraries.rggViews import setThickness, deleteAllPogs, saveChars, loadChars, configureGfx
from libraries.rggViews import configureDrawTimer, hostGame, joinGame, disconnectGame
from libraries.rggViews import createSurvey, promptSendFile, toggleAlerts, setLineColour
from libraries.rggViews import toggleTimestamps, toggleRightclick, toggleGridlock
from libraries.rggViews import setLanguage, setPortraitSize, changeStyle, partialTransferResponse
from libraries.rggViews import transferFileResponse, placePog, setScratchPadLock, unsetScratchPadLock
from libraries.rggViews import updateScratchPad
from libraries.rggViews.session import saveSession, loadSession, clearSession


def connectChatWidgetEvents(widget):
	widget.chatInput.connect(chatInputEvent)

def connectICChatWidgetEvents(widget):
	widget.ICChatInput.connect(ICChatInputEvent)

def connectDiceWidgetEvents(widget):
	widget.rollRequested.connect(rollDice)
	widget.macroRequested.connect(addMacro)

def connectUserListWidgetEvents(widget):
	widget.selectGM.connect(playerOptions)
	widget.kickPlayer.connect(kick)
	widget.requestBanlistUpdate.connect(updateBanlist)

def connectScratchPadEvents(widget):
	widget.getScratchPadLock.connect(setScratchPadLock)
	widget.releaseScratchPadLock.connect(unsetScratchPadLock)
	widget.updateScratchPad.connect(updateScratchPad)

def connectMenuEvents(menu):
	menu.newMapAct.triggered.connect(newMap)
	menu.loadMapAct.triggered.connect(loadMap)
	menu.saveSessAct.triggered.connect(saveSession)
	menu.loadSessAct.triggered.connect(loadSession)
	menu.saveMapAct.triggered.connect(saveMap)
	menu.closeSpecificMapAct.triggered.connect(closeMap)
	menu.closeMapAct.triggered.connect(closeAllMaps)
	menu.clearSessAct.triggered.connect(clearSession)
	menu.deletePogsAct.triggered.connect(deleteAllPogs)
	menu.saveCharsAct.triggered.connect(saveChars)
	menu.loadCharsAct.triggered.connect(loadChars)
	menu.gfxSettingsAct.triggered.connect(configureGfx)
	menu.drawTimerSettingsAct.triggered.connect(configureDrawTimer)
	menu.hostGameAct.triggered.connect(hostGame)
	menu.joinGameAct.triggered.connect(joinGame)
	menu.disconnectAct.triggered.connect(disconnectGame)
	menu.createSurveyAct.triggered.connect(createSurvey)
	menu.sendFileAct.triggered.connect(promptSendFile)
	menu.toggleAlertsAct.triggered.connect(toggleAlerts)
	menu.toggleTimestampsAct.triggered.connect(toggleTimestamps)
	menu.toggleRightclickAct.triggered.connect(toggleRightclick)
	menu.lockToGridAct.triggered.connect(toggleGridlock)
	menu.setTimestampFormatAct.triggered.connect(promptTimestampFormat)
	menu.thicknessMenu.triggered.connect(setThickness)
	menu.colourMenu.triggered.connect(setLineColour)
	menu.langMenu.triggered.connect(setLanguage)
	menu.portraitMenu.triggered.connect(setPortraitSize)
	menu.stylesMenu.triggered.connect(changeStyle)

def connectClientEvents(client):
	client.connected.connect(clientConnect)
	client.disconnected.connect(clientDisconnect)
	client.objectReceived.connect(clientReceive)
	client.fileReceived.connect(clientFileReceive)
	client.fileEvent.connect(transferFileResponse)
	client.partialTransferEvent.connect(partialTransferResponse)

def connectServerEvents(server):
	server.connected.connect(serverConnect)
	server.disconnected.connect(serverDisconnect)
	server.transferDisconnected.connect(serverTransferDisconnect)
	server.kicked.connect(serverKick)
	server.objectReceived.connect(serverReceive)
	server.fileReceived.connect(serverFileReceive)
	server.fileEvent.connect(transferFileResponse)
	server.partialTransferEvent.connect(partialTransferResponse)

def connectGLWidgetEvents(glwidget):
	glwidget.mouseMoveSignal.connect(mouseMoveEvent)
	glwidget.mousePressSignal.connect(mousePressEvent)
	glwidget.mouseReleaseSignal.connect(mouseReleaseEvent)
	glwidget.keyPressSignal.connect(keyPressEvent)
	glwidget.keyReleaseSignal.connect(keyReleaseEvent)
	glwidget.pogPlace.connect(placePog)

def connectEvents(client, server, glWidget):
	connectServerEvents(server)
	connectClientEvents(client)
	connectMenuEvents(GlobalState.menu)
	connectChatWidgetEvents(GlobalState.cwidget)
	connectICChatWidgetEvents(GlobalState.icwidget)
	connectDiceWidgetEvents(GlobalState.dwidget)
	connectUserListWidgetEvents(GlobalState.uwidget)
	connectGLWidgetEvents(glWidget)
	connectScratchPadEvents(GlobalState.scratchPadWidget)
