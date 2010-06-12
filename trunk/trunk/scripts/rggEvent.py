import rggViews, rggChat, rggICChat

# Globals

_eaten = False
_mouseMoveListeners = []
_mousePressListeners = []
_mouseReleaseListeners = []
_chatInputListeners = []
_ICChatInputListeners = []
_pogUpdateListeners = []
_pogDeleteListeners = []
_pogSelectionChangedListeners = []
_mapChangedListeners = []

def setEaten():
  global _eaten
  _eaten = True

# Add listener functions

def addMouseMoveListener(listener):
  _mouseMoveListeners.append(listener)

def addMousePressListener(listener):
  _mousePressListeners.append(listener)

def addMouseReleaseListener(listener):
  _mouseReleaseListeners.append(listener)

def addChatInputListener(listener):
  _chatInputListeners.append(listener)

def addICChatInputListener(listener):
  _ICChatInputListeners.append(listener)

def addPogUpdateListener(listener):
  _pogUpdateListeners.append(listener)

def addPogDeleteListener(listener):
  _pogDeleteListeners.append(listener)

def addPogSelectionChangedListener(listener):
  _pogSelectionChangedListeners.append(listener)

def addMapChangedListener(listener):
  _mapChangedListeners.append(listener)

# Event functions

def mouseMoveEvent(x, y):
  global _eaten
  _eaten = False

  for listener in _mouseMoveListeners:
    listener.mouseMoveResponse(x, y)

  if not _eaten:
    rggViews.mouseMoveResponse(x, y)

def mousePressEvent(x, y, t):
  global _eaten
  _eaten = False

  for listener in _mousePressListeners:
    listener.mousePressResponse(x, y, t)

  if not _eaten:
    rggViews.mousePressResponse(x, y, t)

def mouseReleaseEvent(x, y, t):
  global _eaten
  _eaten = False

  for listener in _mouseReleaseListeners:
    listener.mouseReleaseResponse(x, y, t)

  if not _eaten:
    rggViews.mouseReleaseResponse(x, y, t)

def chatInputEvent(st):
  global _eaten
  _eaten = False

  for listener in _chatInputListeners:
    listener.chatInputResponse(st)

  if not _eaten:
    rggChat.chat(st)

def ICChatInputEvent(st, chname, portrait):
  global _eaten
  _eaten = False

  for listener in _ICChatInputListeners:
    listener.ICChatInputResponse(st, chname, portrait)

  if not _eaten:
    rggICChat.chat(st, chname, portrait)

def pogUpdateEvent(pog): #may either add a new pog, or update an existing one. Beware.
  for listener in _pogUpdateListeners:
    listener.pogUpdateResponse(pog)

def pogDeleteEvent(pog):
  for listener in _pogDeleteListeners:
    listener.pogDeleteResponse(pog)

def pogSelectionChangedEvent():
  for listener in _pogSelectionChangedListeners:
    listener.pogSelectionChangedResponse()

def mapChangedEvent(newMap):
  for listener in _mapChangedListeners:
    listener.mapChangedResponse(newMap)
