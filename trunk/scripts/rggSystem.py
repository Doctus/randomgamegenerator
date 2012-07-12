'''
initialization - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Qt and C++ services.

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

import sys, random, math
import os, os.path
from PyQt4 import QtCore, QtGui

class wAction(QtGui.QAction):

    def __init__(self, text, parent, id):
        QtGui.QAction.__init__(self, text, parent)
        self.id = id

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
IMAGE_NAME_FILTER = list(('*{ext}'.format(ext=ext) for ext in IMAGE_EXTENSIONS))
IMAGE_FILTER = fake.translate('system', 'Images ({imageList})').format(
    imageList=','.join('*{ext}'.format(ext=ext) for ext in IMAGE_EXTENSIONS))
TILESET_DIR = 'data/tilesets'
POG_DIR = 'data/pogs'
PORTRAIT_DIR = 'data/portraits'
PLUGINS_DIR = 'plugins'
LOG_DIR = 'save/logs'
MAP_DIR = 'save/maps'
CHAR_DIR = 'save/characters'
MUSIC_DIR = 'data/music'
SAVE_DIR = 'save'
COLOURS = {"White":(1.0, 1.0, 1.0), 
           "Red": (1.0, 0.0, 0.0), 
           "Orange": (1.0, 0.5, 0.0), 
           "Yellow": (1.0, 1.0, 0.0),
           "Green": (0.0, 0.8, 0.2),
           "Blue": (0.0, 0.0, 1.0),
           "Purple": (0.76, 0.0, 1.0),
           "Black": (0.0, 0.0, 0.0)}
VERSION = "1.01"
DEV = True
PING_INTERVAL_SECONDS = 10

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
    global mainWindow

    assert(not mainWindow)

    from rggMain import MainWindow
    mainWindow = MainWindow()
    return mainWindow

def showErrorMessage(message, title=translate('system', "Error", 'default error prompt title')):
    """Pops up an error message to the user."""
    QtGui.QMessageBox.critical(mainWindow, title, message)

def showPopupMenuAt(position, choices):
    popup = QtGui.QMenu(mainWindow)
    idCounter = 0

    for choice in choices:
        popup.addAction(wAction(choice, mainWindow, idCounter))
        idCounter += 1

    realx = position[0] + (mainWindow.x() + mainWindow.glwidget.x())
    realy = position[1] + (mainWindow.y() + mainWindow.glwidget.y())
    selectedAction = popup.exec_(QtCore.QPoint(realx, realy))

    if not selectedAction:
        return -1

    return selectedAction.id

def showPopupMenuAtAbs(position, choices):
    popup = QtGui.QMenu(mainWindow)
    idCounter = 0

    for choice in choices:
        popup.addAction(wAction(choice, mainWindow, idCounter))
        idCounter += 1

    realx = position[0]
    realy = position[1]
    selectedAction = popup.exec_(QtCore.QPoint(realx, realy))

    if not selectedAction:
        return -1

    return selectedAction.id

def promptString(prompt, title=translate('system', "Input", 'default string prompt title'), inittext=None):
    if inittext is not None:
        text, ok = QtGui.QInputDialog.getText(mainWindow, title, prompt, text=inittext)
    else:
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

    if(len(convertedText) == 0):
        return -1

    buttons = []

    from PyQt4.QtGui import QMessageBox
    questionDialog = QMessageBox(mainWindow);
    questionDialog.setText(prompt);

    j = len(convertedText) - 1
    while(j >= 0):
        newButton = questionDialog.addButton(convertedText[j], QMessageBox.AcceptRole);
        buttons.insert(0, newButton);
        if(j == defaultButton):
            questionDialog.setDefaultButton(newButton)
        j -= 1

    questionDialog.exec_()

    i = 0
    for button in buttons:
        if(questionDialog.clickedButton() == button):
            return i
        i += 1

    return -1

def promptYesNo(prompt):
    from PyQt4.QtGui import QMessageBox
    questionDialog = QMessageBox(mainWindow)
    questionDialog.setText(prompt)
    questionDialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return questionDialog.exec_()
    
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
                if os.stat(os.path.join(dirpath, filename))[6] == 0: continue
                files.append(makePortableFilename(name))
    #files.sort()
    return files
    
def cameraPosition():
    return mainWindow.glwidget.camera

def cameraSize():
    return (mainWindow.glwidget.w, mainWindow.glwidget.h)

def setCameraPosition(position):
    mainWindow.glwidget.camera = list(position)

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

def drawSelectionCircle(x, y, splasifarcity, radius):
    mainWindow.glwidget.addSelectionCircle(splasifarcity, x, y, radius)
    
def clearSelectionCircles():
    mainWindow.glwidget.clearSelectionCircles()
    
def drawRectangle(x, y, w, h, r, g, b):
    mainWindow.glwidget.addRectangle(x, y, w, h, r, g, b)
    
def clearRectangles():
    mainWindow.glwidget.clearRectangles()

def drawLine(x, y, w, h, thickness, r, g, b):
    mainWindow.glwidget.addLine(thickness, x, y, w, h, r, g, b)

def deleteLine(x, y, w, h, thickness = -1):
    mainWindow.glwidget.deleteLine(thickness, x, y, w, h)

def clearLines():
    mainWindow.glwidget.clearLines()

def getLinesOfThickness(thickness):
    lines = dict()
    try:
        lines = mainWindow.glwidget.lines[thickness]
    except:
        pass
    return lines

def drawRectangleMadeOfLines(x, y, w, h, colour, thickness):
    drawLine(x, y, w, y, thickness, colour[0], colour[1], colour[2])
    drawLine(w, y, w, h, thickness, colour[0], colour[1], colour[2])
    drawLine(w, h, x, h, thickness, colour[0], colour[1], colour[2])
    drawLine(x, h, x, y, thickness, colour[0], colour[1], colour[2])

def drawCircle(centre, edge, colour, thickness):
    radius = math.hypot(edge[0]-centre[0], edge[1]-centre[1])
    vert = [centre[0]+radius, centre[1], 0, 0]
    for r in range(3, 363, 3):
        vert[2] = centre[0]+math.cos(r*0.01745329)*radius
        vert[3] = centre[1]+math.sin(r*0.01745329)*radius
        drawLine(vert[0], vert[1], vert[2], vert[3], thickness, colour[0], colour[1], colour[2])
        vert[0] = vert[2]
        vert[1] = vert[3]
        
    
def drawRegularPolygon(sides, centre, size, colour, thickness, rainbow = False):
    vertices = []
    for i in xrange(sides):
        vertices.append((centre[0]+size*math.cos(2*math.pi*i/sides), centre[1]+size*math.sin(2*math.pi*i/sides)))
    for p in xrange(sides):
        for q in xrange(sides):
            if sides%2 == 1 or p%(sides/2) != q%(sides/2):
                if not rainbow:
                    drawLine(vertices[p][0], vertices[p][1], vertices[q][0], vertices[q][1], thickness, colour[0], colour[1], colour[2])
                else:
                    drawLine(vertices[p][0], vertices[p][1], vertices[q][0], vertices[q][1], thickness, random.random(), random.random(), random.random())    
    
def setZoom(zoom):
    #_main.setZoom(zoom)
    print "unimplemented2"
    return False

def getZoom():
    return mainWindow.glwidget.zoom
    
def getMapPosition(screenCoordinates):
    mapPosition = map(lambda p,c,d: p/d - c/d, screenCoordinates, cameraPosition(), (getZoom(), getZoom()))
    return mapPosition
