'''
initialization - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Interface among main singleton widgets.

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

import _bmainmod, sys
import os, os.path
from PyQt4 import QtCore, QtGui

_c = _bmainmod.bMain()

mainWindow = _c.getMainWindow()


def connectSignal(signal, func):
    QtCore.QObject.connect(_c, QtCore.SIGNAL(signal), func)

def connectChat(func):
    global _dwidget, _pwidget, _cwidget
    
    from rggDockWidget import diceRoller, pogPalette, chatWidget
    _dwidget = diceRoller(mainWindow)
    _pwidget = pogPalette(mainWindow)
    #_mwidget = mapEditor(mainWindow)
    _cwidget = chatWidget(mainWindow)
    
    QtCore.QObject.connect(_dwidget, QtCore.SIGNAL("newChatInputSignal(QString)"), func)
    QtCore.QObject.connect(_pwidget, QtCore.SIGNAL("newChatInputSignal(QString)"), func)
    QtCore.QObject.connect(_cwidget, QtCore.SIGNAL("newChatInputSignal(QString)"), func)

class fake(object):
    """Fake translation tools."""
    
    @staticmethod
    def translate(context, key, *args):
        """Fake translate to mark strings before they are used."""
        return key

# Real translation
def translate(*args):
    return unicode(QtCore.QCoreApplication.translate(*args))

def start():
    return _c.start()

def addDiceMacro(dice, name):
    _dwidget.addMacro(dice, name)

def showErrorMessage(message, title=translate('system', "Error", 'default error prompt title')):
    """Pops up an error message to the user."""
    QtGui.QMessageBox.critical(mainWindow, title, message)

def say(message):
    """Say an IC message."""
    _cwidget.insertMessage(message)

def announce(message):
    """Say an OOC message."""
    _cwidget.insertMessage(message)

def displayTooltip(text, position):
    return _c.displayTooltip(text, position[0], position[1])

def showPopupMenuAt(position, choices):
    return _c.showPopupMenuAt(position[0], position[1], choices)

def promptString(prompt, title=translate('system', "Input", 'default string prompt title')):
    text, ok = QtGui.QInputDialog.getText(mainWindow, title, prompt)
    if not ok:
        return None
    return unicode(text)

def promptInteger(prompt, title=translate('system', "Input", 'default integer prompt title'),
        min=-sys.maxint, max=sys.maxint, step=1):
    value, ok = QtGui.QInputDialog.getInt(mainWindow, title, prompt, 0, min, max, step)
    if not ok:
        return None
    return int(value)
    
def promptCoordinates(prompt1, prompt2, title=translate('system', "Input", 'default coordinate prompt title'),
        min=-sys.maxint, max=sys.maxint, step=1):
    value1 = promptInteger(prompt1, title, min, max, step)
    if value1 is None:
        return None
    value2 = promptInteger(prompt2, title, min, max, step)
    if value2 is None:
        return None
    return (value1, value2)

def promptLoadFile(title, filter):
    filename = QtGui.QFileDialog.getOpenFileName(mainWindow,
        title,
        '',
        filter)
    if not filename:
        return None
    return unicode(filename)

def promptSaveFile(title, filter):
    filename = QtGui.QFileDialog.getSaveFileName(mainWindow,
        title,
        '',
        filter)
    if not filename:
        return None
    return unicode(filename)

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".ppm", ".xbm", ".xpm")
IMAGE_FILTER = translate('system', 'Images ({imageList})').format(
    imageList=','.join('*{ext}'.format(ext=ext) for ext in IMAGE_EXTENSIONS))
TILESET_DIR = 'data/tilesets'
POG_DIR = 'data/pogs'

def findFiles(dir, extensions):
    """Get the list of tileset files."""
    files = []
    for dirpath, dirnames, filenames in os.walk(dir):
        if ".svn" in dirpath:
            continue
        #filenames.sort()
        for filename in filenames:
            if os.path.splitext(filename)[1] in extensions:
                files.append(os.path.join(dirpath, filename)[len(dir) + 1:])
    #files.sort()
    return files
    
def localHandle():
    return 'you'

def linkedName(name):
    return translate('system', '<a href="/tell {name}" title="{name}">{name}</a>').format(name=name)

def linkedHandle():
    return linkedName(localHandle())

def cameraPosition():
    return (_c.getCamX(), _c.getCamY())

def setCameraPosition(position):
    _c.setCam(position[0], position[1])


