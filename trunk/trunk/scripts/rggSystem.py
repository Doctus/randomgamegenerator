'''
initialization - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Qt and C++ servces.

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

import sys, random
import os, os.path
from PyQt4 import QtCore, QtGui

class fake(object):
    """Fake translation tools."""
    
    @staticmethod
    def translate(context, key, *args):
        """Fake translate to mark strings before they are used."""
        if args:
            raise RuntimeError("Fake translation of {context} failed. "
                "Comment arguments will not be preserved.".format(context=context))
        assert(not args)
        return key

# Real translation
def translate(*args):
    return unicode(QtCore.QCoreApplication.translate(*args))

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".ppm", ".xbm", ".xpm")
IMAGE_FILTER = fake.translate('system', 'Images ({imageList})').format(
    imageList=','.join('*{ext}'.format(ext=ext) for ext in IMAGE_EXTENSIONS))
TILESET_DIR = 'data/tilesets'
POG_DIR = 'data/pogs'
PORTRAIT_DIR = 'data/portraits'
PLUGINS_DIR = 'plugins'
LOG_DIR = 'logs'
MAP_DIR = 'maps'

_main = None
mainWindow = None

def signal(*args, **kwargs):
    """Creates a signal."""
    
    # Figure out parameters
    parameters = args
    for parm in parameters:
        if not isinstance(parm, type):
            raise TypeError("Parameters to the signal constructor must be types.")
    doc = kwargs.get('doc')
    
    # A unique key
    key = object()
    
    def get(self):
        if not hasattr(self, '_signals'):
            self._signals = {}
        if key not in self._signals:
            self._signals[key] = signalStorage(parameters)
        return self._signals[key]
    
    return property(get, doc=doc)

class signalStorage(object):
    """A signal mechanism similar to Qt's signals.
    
    Would have used Qt's if they supported python better.
    
    """
    
    def __init__(self, parameters):
        """Initializes the signal.
        
        args -- the parameters used to trigger the signal
        
        """
        self.callbacks = set()
        self.parameters = parameters
    
    def emit(self, *args):
        """Emit this signal to all connected slots."""
        if len(args) != len(self.parameters):
            raise TypeError("Too few parameters to signal.")
        for parm, arg in zip(self.parameters, args):
            if not isinstance(arg, parm):
                raise TypeError("Invalid parameter to signal: expected {0} to be {1}.".format(repr(arg), parm))
        for callback in self.callbacks:
            try:
                callback(*args)
            except Exception as e:
                import traceback
                print "ERROR encountered in signal handler {handler}:".format(handler=repr(callback))
                traceback.print_exc()
    
    def connect(self, callable):
        """Connect this signal to a slot. (Python callable.)"""
        self.callbacks.add(callable)
        
    def disconnect(self, callable=None):
        """Disconnect this signal from a specified slot,
        or all slots if no parameter is specified.
        
        """
        if callable is None:
            self.callbacks = set()
        else:
            self.callbacks.remove(callable)

def injectMain():
    """Injects and returns the main C++ interface object."""
    import _bmainmod
    
    global _main
    global mainWindow
    
    assert(not _main)
    assert(not mainWindow)
    
    _main = _bmainmod.bMain()
    mainWindow = _main.getMainWindow()
    return _main

def showErrorMessage(message, title=translate('system', "Error", 'default error prompt title')):
    """Pops up an error message to the user."""
    QtGui.QMessageBox.critical(mainWindow, title, message)

def displayTooltip(text, position):
    return _main.displayTooltip(text, position[0], position[1])

def showPopupMenuAt(position, choices):
    return _main.showPopupMenuAt(position[0], position[1], choices)

def showPopupMenuAtAbs(position, choices):
    return _main.showPopupMenuAtAbs(position[0], position[1], choices)

def promptString(prompt, title=translate('system', "Input", 'default string prompt title')):
    text, ok = QtGui.QInputDialog.getText(mainWindow, title, prompt)
    if not ok:
        return None
    return unicode(text)

def promptInteger(prompt, title=translate('system', "Input", 'default integer prompt title'),
        min=-sys.maxint, max=sys.maxint, default=0, step=1):
    value, ok = QtGui.QInputDialog.getInt(mainWindow, title, prompt, default, min, max, step)
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

def promptLoadFile(title, filter, dir=''):
    filename = QtGui.QFileDialog.getOpenFileName(mainWindow,
        title,
        dir,
        filter)
    if not filename:
        return None
    return makePortableFilename(unicode(filename))

def promptSaveFile(title, filter, dir=''):
    filename = QtGui.QFileDialog.getSaveFileName(mainWindow,
        title,
        dir,
        filter)
    if not filename:
        return None
    return makePortableFilename(unicode(filename))

def promptButtonSelection(prompt, text=[], defaultButton = 0):
    convertedText = ()
    if text is not tuple: #lists/dictionaries make this function a sad panda :(
        convertedText = (text)
    else:
        convertedText = text
    return _main.displayUserDialogChoice(prompt, convertedText, defaultButton)

def findFiles(dir, extensions):
    """Get the list of files with one of the given extensions."""
    files = []
    for dirpath, dirnames, filenames in os.walk(dir):
        if ".svn" in dirpath:
            continue
        #filenames.sort()
        for filename in filenames:
            if os.path.splitext(filename)[1] in extensions:
                name = os.path.join(dirpath, filename)[len(dir) + 1:]
                #print "found file:", name, makePortableFilename(name)
                files.append(makePortableFilename(name))
    #files.sort()
    return files
    
def cameraPosition():
    return (_main.getCamX(), _main.getCamY())

def cameraSize():
    return (_main.getCamW(), _main.getCamH())

def setCameraPosition(position):
    _main.setCam(position[0], position[1])

def findRandomAppend():
    """Gives a random character to append to string to make it random."""
    # Can't spell swear words without vowels
    # Left out l and v because they look enough like i and u
    letters = '256789bcdfghjkmnpqrstwxz'
    return random.choice(letters)


def makeLocalFilename(filename):
    """Converts a portable path to a complete path."""
    # TODO: Implement filename conversion
    return filename

def makePortableFilename(filename):
    """Attempts to convert a local path to a portable, relative, unique path."""
    # TODO: Implement filename conversion
    return filename.replace('\\', '/')

def drawLine(x, y, w, h, thickness):
    _main.addLine(x, y, w, h, thickness)

def deleteLine(x, y, w, h, thickness = -1):
    _main.deleteLine(x, y, w, h, thickness)

def clearLines():
    _main.clearLines()

def getLinesOfThickness(thickness):
    return _main.getLineOfThickness(thickness)

def reloadImage(filename, tilewidth, tileheight):
    """Reloads the specified image file."""
    return _main.changeImage(filename, filename, tilewidth, tileheight)

def setZoom(zoom):
    _main.setZoom(zoom)

def getZoom():
    return _main.getZoom()
