'''
rggEvent - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Handling of signal/slot system for user input and network event response.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

# Globals

_mouseMoveListeners = []
_mousePressListeners = []
_mouseReleaseListeners = []
_keyPressListeners = []
_keyReleaseListeners = []
_chatInputListeners = []
_ICChatInputListeners = []
_pogUpdateListeners = []
_pogDeleteListeners = []
_pogSelectionChangedListeners = []
_mapChangedListeners = []

# Add listener functions
# Priority value should normally be a *_RESPONSE_LEVEL from rggConstants

def addMouseMoveListener(listener, priority):
    _mouseMoveListeners.append((listener, priority))
    _mouseMoveListeners.sort(key=lambda item: item[1])

def addMousePressListener(listener, priority):
    _mousePressListeners.append((listener, priority))
    _mousePressListeners.sort(key=lambda item: item[1])

def addMouseReleaseListener(listener, priority):
    _mouseReleaseListeners.append((listener, priority))
    _mouseReleaseListeners.sort(key=lambda item: item[1])
  
def addKeyPressListener(listener, priority):
    _keyPressListeners.append((listener, priority))
    _keyPressListeners.sort(key=lambda item: item[1])
  
def addKeyReleaseListener(listener, priority):
    _keyReleaseListeners.append((listener, priority))
    _keyReleaseListeners.sort(key=lambda item: item[1])

def addChatInputListener(listener, priority):
    _chatInputListeners.append((listener, priority))
    _chatInputListeners.sort(key=lambda item: item[1])

def addICChatInputListener(listener, priority):
    _ICChatInputListeners.append((listener, priority))
    _ICChatInputListeners.sort(key=lambda item: item[1])

def addPogUpdateListener(listener, priority):
    _pogUpdateListeners.append((listener, priority))
    _pogUpdateListeners.sort(key=lambda item: item[1])

def addPogDeleteListener(listener, priority):
    _pogDeleteListeners.append((listener, priority))
    _pogDeleteListeners.sort(key=lambda item: item[1])

def addPogSelectionChangedListener(listener, priority):
    _pogSelectionChangedListeners.append((listener, priority))
    _pogSelectionChangedListeners.sort(key=lambda item: item[1])

def addMapChangedListener(listener, priority):
    _mapChangedListeners.append((listener, priority))
    _mapChangedListeners.sort(key=lambda item: item[1])

# Event functions

def mouseMoveEvent(x, y):

    for listener, priority in _mouseMoveListeners:
        if listener(x, y):
            return

def mousePressEvent(x, y, t):

    for listener, priority in _mousePressListeners:
        if listener(x, y, t):
            return

def mouseReleaseEvent(x, y, t):

    for listener, priority in _mouseReleaseListeners:
        if listener(x, y, t):
            return
    
def keyPressEvent(k):

    for listener, priority in _keyPressListeners:
        if listener(k):
            return
    
def keyReleaseEvent(k):

    for listener, priority in _keyReleaseListeners:
        if listener(k):
            return

def chatInputEvent(st):

    for listener, priority in _chatInputListeners:
        if listener(st):
            return

def ICChatInputEvent(st, chname, portrait):

    for listener, priority in _ICChatInputListeners:
        if listener(st, chname, portrait):
            return

def pogUpdateEvent(pog): #may either add a new pog, or update an existing one. Beware.

    for listener, priority in _pogUpdateListeners:
        if listener.pogUpdateResponse(pog):
            return

def pogDeleteEvent(pog):

    for listener, priority in _pogDeleteListeners:
        if listener.pogDeleteResponse(pog):
            return

def pogSelectionChangedEvent():

    for listener, priority in _pogSelectionChangedListeners:
        if listener():
            return

def mapChangedEvent(newMap):

    for listener, priority in _mapChangedListeners:
        if listener(newMap):
            return
