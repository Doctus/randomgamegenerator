'''
rggDialogs - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Design inspired by Django Forms.

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

import os, os.path
import rggMap
from rggSystem import fake, translate, showErrorMessage, findFiles, IMAGE_EXTENSIONS, TILESET_DIR, PORTRAIT_DIR, SAVE_DIR, makePortableFilename
from rggFields import integerField, floatField, stringField, dropDownField, validationError
from rggNet import ConnectionData, localHost
from rggJson import *
from PyQt4 import QtGui, QtCore

class dialog(object):
    """A base class for dialogs.
    
    """
    
    def __init__(self):
        """Initializes the dialog, with optional parameters."""
        self.cleanData = None
        self._error = None
    
    def clean(self):
        """Check for errors and return well-formatted data."""
        raise NotImplementedError()
    
    @property
    def error(self):
        """Access any errors on this dialog."""
        self.is_valid()
        return self._error
    
    def is_valid(self):
        """Return true if the data is valid and complete."""
        try:
            self.clean()
            assert(self.cleanData is not None)
            return True
        except validationError as e:
            self.cleanData = None
            if len(e.args) > 0:
                self._error = e.args[0]
            else:
                # Catch-all shouldn't be seen by end-users
                self._error = translate('dialog', "There is an error in your input.")
    
    def save(self):
        """Utilize validated data to make changes."""
        raise NotImplementedError()

class newMapDialog(dialog):
    """A dialog used to create a new map."""
    
    def __init__(self, **kwargs):
        """Initializes the dialog data."""
        super(newMapDialog, self).__init__()
        self.fields = self._createFields(kwargs)
    
    def _createFields(self, data):
        """Create the fields used by this dialog."""
        
        tilesets = findFiles(TILESET_DIR, IMAGE_EXTENSIONS)
        if len(tilesets) <= 0:
            raise RuntimeError(translate('newMapDialog',
                'Cannot create a map when no tilesets are available.'))
        
        return dict(
            mapName=stringField(translate('newMapDialog', 'Map Name'),
                value=data.get('mapName', translate('newMapDialog', 'Generic Map'))),
            authName=stringField(translate('newMapDialog', 'Author Name'),
                value=data.get('authName', translate('newMapDialog', 'Anonymous'))),
            tileset=dropDownField(translate('newMapDialog', 'Tileset'), tilesets,
                value=data.get('tileset', tilesets[0])),
            mapWidth=integerField(translate('newMapDialog', 'Map Width'),
                min=1, max=65535, value=data.get('mapWidth', 25)),
            mapHeight=integerField(translate('newMapDialog', 'Map Height'),
                min=1, max=65535, value=data.get('mapHeight', 25)),
            tileWidth=integerField(translate('newMapDialog', 'Per-Tile Width'),
                min=1, max=65535, value=data.get('tileWidth', 32)),
            tileHeight=integerField(translate('newMapDialog', 'Per-Tile Height'),
                min=1, max=65535, value=data.get('tileHeight', 32)))
    
    def _interpretFields(self, fields):
        """Interpret the fields into a dictionary of clean items."""
        return dict((key, field.clean()) for key, field in fields.items())
    
    def exec_(self, parent, accept):
        """Executes this dialog as modal, ensuring OK is only hit with valid data.
        
        parent -- the parent object of this dialog
        accept() -- Acceptance function;
            return True to accept data, False to continue (you should show an error)
        
        returns: True if the OK button is hit and the acceptance function passes.
        
        """
        
        widget = QtGui.QDialog(parent)
        
        # Buttons
        okayButton = QtGui.QPushButton(translate('newMapDialog', "Create Map"))
        okayButton.setDefault(True)
        cancelButton = QtGui.QPushButton(translate('newMapDialog', "Cancel"))
        
        # Add fields
        formLayout = QtGui.QFormLayout()
        for id in ('mapName', 'authName', 'mapWidth', 'mapHeight', 'tileset', 'tileWidth', 'tileHeight'):
            field = self.fields[id]
            formLayout.addRow(translate('newMapDialog', '{0}: ', 'Row layout').format(field.name), field.widget(widget))
        
        # Add buttons
        theLesserOrFalseBox = QtGui.QBoxLayout(0)
        theLesserOrFalseBox.addWidget(okayButton)
        theLesserOrFalseBox.addWidget(cancelButton)
        
        # Position both
        grandBox = QtGui.QBoxLayout(2)
        grandBox.addLayout(formLayout)
        grandBox.addLayout(theLesserOrFalseBox)
        
        # Set up the widget
        widget.setLayout(grandBox)
        widget.setModal(True)
        widget.setWindowTitle(translate('newMapDialog', "New Map"))
        
        # Allow user to specify validation
        def okayPressed():
            if accept():
                widget.accept()
        
        # Signals
        widget.connect(okayButton, QtCore.SIGNAL('clicked()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('clicked()'), widget.reject)
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
        
    def clean(self):
        """Check for errors and return well-formatted data."""
        self.cleanData = self._interpretFields(self.fields)
        return self.cleanData
    
    def save(self):
        """Make a new map and return it."""
        assert(self.cleanData)
        return rggMap.Map(
            self.cleanData['mapName'],
            self.cleanData['authName'],
            (self.cleanData['mapWidth'], self.cleanData['mapHeight']),
            makePortableFilename(os.path.join('data/tilesets', self.cleanData['tileset'])),
            (self.cleanData['tileWidth'], self.cleanData['tileHeight']))
    
class hostDialog(dialog):
    """A dialog used to specify parameters to game hosting."""
    
    def __init__(self, **kwargs):
        """Initializes the dialog data."""
        super(hostDialog, self).__init__()
        self.fields = self._createFields(kwargs)
    
    def _createFields(self, data):
        """Create the fields used by this dialog."""
        
        self.fieldtemp = [6812, translate('hostDialog', 'Anonymous')]
        
        try:
            js = jsonload(os.path.join(SAVE_DIR, "net_server.rgs"))
            self.fieldtemp[0] = int(loadString('hostDialog.port', js.get('port')))
            self.fieldtemp[1] = loadString('hostDialog.username', js.get('username'))
        except:
            pass
        
        return dict(
            username=stringField(
                translate('hostDialog', 'Username'),
                value=data.get('username', self.fieldtemp[1])),
            port=integerField(
                translate('hostDialog', 'Port'),
                min=1, max=65535, value=data.get('port', self.fieldtemp[0])))
    
    def _interpretFields(self, fields):
        """Interpret the fields into a dictionary of clean items."""
        return dict((key, field.clean()) for key, field in fields.items())
    
    def exec_(self, parent, accept):
        """Executes this dialog as modal, ensuring OK is only hit with valid data.
        
        parent -- the parent object of this dialog
        accept() -- Acceptance function;
            return True to accept data, False to continue (you should show an error)
        
        returns: True if the OK button is hit and the acceptance function passes.
        
        """
        
        widget = QtGui.QDialog(parent)
        
        # Buttons
        okayButton = QtGui.QPushButton(translate('hostDialog', "Host"))
        okayButton.setDefault(True)
        cancelButton = QtGui.QPushButton(translate('hostDialog', "Cancel"))
        
        # Add fields
        formLayout = QtGui.QFormLayout()
        for id in ('port', 'username'):
            field = self.fields[id]
            formLayout.addRow(
                translate('hostDialog', '{0}: ', 'Row layout').format(field.name),
                field.widget(widget))
        
        # Add buttons
        theLesserOrFalseBox = QtGui.QBoxLayout(0)
        theLesserOrFalseBox.addWidget(okayButton)
        theLesserOrFalseBox.addWidget(cancelButton)
        
        # Position both
        grandBox = QtGui.QBoxLayout(2)
        grandBox.addLayout(formLayout)
        grandBox.addLayout(theLesserOrFalseBox)
        
        # Set up the widget
        widget.setLayout(grandBox)
        widget.setModal(True)
        widget.setWindowTitle(translate('hostDialog', "Host Game"))
        
        # Allow user to specify validation
        def okayPressed():
            if accept():
                widget.accept()
        
        # Signals
        widget.connect(okayButton, QtCore.SIGNAL('clicked()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('clicked()'), widget.reject)
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
    
    def dump(self):
        return dict(username=self.cleanData['username'],
                    port=str(self.cleanData['port']))
        
    def clean(self):
        """Check for errors and return well-formatted data."""
        self.cleanData = self._interpretFields(self.fields)
        return self.cleanData
    
    def save(self):
        """Make a new map and return it."""
        assert(self.cleanData)
        try:
            jsondump(self.dump(), os.path.join(SAVE_DIR, "net_server.rgs"))
        except:
            pass
        return ConnectionData(localHost(), self.cleanData['port'],
            self.cleanData['username'])
    
class joinDialog(dialog):
    """A dialog used to specify parameters to game joining."""
    
    def __init__(self, **kwargs):
        """Initializes the dialog data."""
        super(joinDialog, self).__init__()
        self.fields = self._createFields(kwargs)
    
    def _createFields(self, data):
        """Create the fields used by this dialog."""
        
        self.fieldtemp = [localHost(), 6812, translate('joinDialog', 'Anonymous')]
        
        try:
            js = jsonload(os.path.join(SAVE_DIR, "net_settings.rgs"))
            self.fieldtemp[0] = loadString('joinDialog.host', js.get('host'))
            self.fieldtemp[1] = int(loadString('joinDialog.port', js.get('port')))
            self.fieldtemp[2] = loadString('joinDialog.username', js.get('username'))
        except:
            pass
        
        return dict(
            username=stringField(translate('joinDialog', 'Username'),
                value=data.get('username', self.fieldtemp[2])),
            host=stringField(translate('joinDialog', 'Host Name (IP)'),
                value=data.get('host', self.fieldtemp[0])),
            port=integerField(translate('joinDialog', 'Port'),
                min=1, max=65535, value=data.get('port', self.fieldtemp[1])))
    
    def _interpretFields(self, fields):
        """Interpret the fields into a dictionary of clean items."""
        return dict((key, field.clean()) for key, field in fields.items())
    
    def exec_(self, parent, accept):
        """Executes this dialog as modal, ensuring OK is only hit with valid data.
        
        parent -- the parent object of this dialog
        accept() -- Acceptance function;
            return True to accept data, False to continue (you should show an error)
        
        returns: True if the OK button is hit and the acceptance function passes.
        
        """
        
        widget = QtGui.QDialog(parent)
        
        # Buttons
        okayButton = QtGui.QPushButton(translate('joinDialog', "Join"))
        okayButton.setDefault(True)
        cancelButton = QtGui.QPushButton(translate('joinDialog', "Cancel"))
        
        # Add fields
        formLayout = QtGui.QFormLayout()
        for id in ('host', 'port', 'username'):
            field = self.fields[id]
            formLayout.addRow(
                translate('joinDialog', '{0}: ', 'Row layout').format(field.name),
                field.widget(widget))
        
        # Add buttons
        theLesserOrFalseBox = QtGui.QBoxLayout(0)
        theLesserOrFalseBox.addWidget(okayButton)
        theLesserOrFalseBox.addWidget(cancelButton)
        
        # Position both
        grandBox = QtGui.QBoxLayout(2)
        grandBox.addLayout(formLayout)
        grandBox.addLayout(theLesserOrFalseBox)
        
        # Set up the widget
        widget.setLayout(grandBox)
        widget.setModal(True)
        widget.setWindowTitle(translate('joinDialog', "Join Game"))
        
        # Allow user to specify validation
        def okayPressed():
            if accept():
                widget.accept()
        
        # Signals
        widget.connect(okayButton, QtCore.SIGNAL('clicked()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('clicked()'), widget.reject)
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
        
    def clean(self):
        """Check for errors and return well-formatted data."""
        self.cleanData = self._interpretFields(self.fields)
        return self.cleanData
    
    def dump(self):
        return dict(host=self.cleanData['host'],
                    port=str(self.cleanData['port']),
                    username=str(self.cleanData['username']))
    
    def save(self):
        """Make a new map and return it."""
        assert(self.cleanData)
        try:
            jsondump(self.dump(), os.path.join(SAVE_DIR, "net_settings.rgs"))
        except:
            pass
        return ConnectionData(self.cleanData['host'], self.cleanData['port'],
            self.cleanData['username'])
    
class newCharacterDialog(dialog):
    """A dialog used to create a new character for in-character chat."""
    
    def __init__(self, **kwargs):
        """Initializes the dialog data."""
        super(newCharacterDialog, self).__init__()
        self.fields = self._createFields(kwargs)
    
    def _createFields(self, data):
        """Create the fields used by this dialog."""
        
        return dict(
            listid=stringField(
                translate('newCharacterDialog', 'List ID'),
                value=data.get('listid', translate('newCharacterDialog', 'New Character'))),
            charactername=stringField(
                translate('newCharacterDialog', 'Character Name'),
                value=data.get('charactername', translate('newCharacterDialog', ' '))),
            portrait=stringField(
                translate('newCharacterDialog', 'Portrait'),
                value=data.get('portrait', translate('newCharacterDialog', 'default_portrait_1.png'))))
    
    def _interpretFields(self, fields):
        """Interpret the fields into a dictionary of clean items."""
        return dict((key, field.clean()) for key, field in fields.items())
    
    def exec_(self, parent, accept):
        """Executes this dialog as modal, ensuring OK is only hit with valid data.
        
        parent -- the parent object of this dialog
        accept() -- Acceptance function;
            return True to accept data, False to continue (you should show an error)
        
        returns: True if the OK button is hit and the acceptance function passes.
        
        """
        
        widget = QtGui.QDialog(parent)
        
        # Buttons
        okayButton = QtGui.QPushButton(translate('newCharacterDialog', "Create"))
        okayButton.setDefault(True)
        cancelButton = QtGui.QPushButton(translate('newCharacterDialog', "Cancel"))
        self.portraitArea = QtGui.QListWidget(parent)
        
        # Add fields
        formLayout = QtGui.QFormLayout()
        for id in ('listid', 'charactername', 'portrait'):
            field = self.fields[id]
            formLayout.addRow(
                translate('newCharacterDialog', '{0}: ', 'Row layout').format(field.name),
                field.widget(widget))
        
        # Add buttons
        theLesserOrFalseBox = QtGui.QBoxLayout(0)
        theLesserOrFalseBox.addWidget(okayButton)
        theLesserOrFalseBox.addWidget(cancelButton)
        
        # Position both
        grandBox = QtGui.QBoxLayout(2)
        grandBox.addLayout(formLayout)
        grandBox.addLayout(theLesserOrFalseBox)
        
        evilBox = QtGui.QBoxLayout(0)
        evilBox.addWidget(self.portraitArea)
        evilBox.addLayout(grandBox)
        
        self.portraitArea.currentItemChanged.connect(self.changePort)
        
        # Set up the widget
        widget.setLayout(evilBox)
        widget.setModal(True)
        widget.setWindowTitle(translate('newCharacterDialog', "Create Character"))
        
        # Allow user to specify validation
        def okayPressed():
            if accept():
                widget.accept()
        
        # Signals
        widget.connect(okayButton, QtCore.SIGNAL('clicked()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('clicked()'), widget.reject)
        
        portraits = findFiles(PORTRAIT_DIR, IMAGE_EXTENSIONS)
        portraits.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
        for greatJustice in portraits:
            icon = QtGui.QIcon(QtGui.QIcon(os.path.join(PORTRAIT_DIR, greatJustice)).pixmap(QtCore.QSize(32, 32)))
            self.portraitArea.addItem(QtGui.QListWidgetItem(icon, greatJustice))
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
    
    def changePort(self, portrait, previous):
        self.fields['portrait'].widgett.setText(unicode(portrait.text()))
        
    def clean(self):
        """Check for errors and return well-formatted data."""
        self.cleanData = self._interpretFields(self.fields)
        return self.cleanData
    
    def save(self):
        """Make a new character and return it."""
        assert(self.cleanData)
        return([self.cleanData['listid'], 
                self.cleanData['charactername'], 
                self.cleanData['portrait']])

class gfxSettingsDialog(dialog):
    """A dialog used to create a new map."""
    
    def __init__(self, **kwargs):
        """Initializes the dialog data."""
        super(gfxSettingsDialog, self).__init__()
        self.fields = self._createFields(kwargs)
    
    def _createFields(self, data):
        """Create the fields used by this dialog."""
        self.fieldtemp = ["GL_COMPRESSED_RG_RGTC2", 1.0, "GL_NEAREST", "GL_NEAREST", "GL_NEAREST_MIPMAP_NEAREST", 1, 1]

        try:
            js = jsonload(os.path.join(SAVE_DIR, "gfx_settings.rgs"))
            self.fieldtemp[0] = loadString('gfx.compress', js.get('compress'))
            self.fieldtemp[1] = loadFloat('gfx.anifilt', js.get('anifilt'))
            self.fieldtemp[2] = loadString('gfx.minfilter', js.get('minfilter'))
            self.fieldtemp[3] = loadString('gfx.magfilter', js.get('magfilter'))
            self.fieldtemp[4] = loadString('gfx.mipminfilter', js.get('mipminfilter'))
            self.fieldtemp[5] = loadString('gfx.FSAA', js.get('FSAA'))
            self.fieldtemp[6] = loadString('gfx.VBO', js.get('VBO'))
        except:
            print "no settings detected"
            pass

        normFilters = ["GL_NEAREST", "GL_LINEAR"]
        mipFilters = ["Off", "GL_NEAREST_MIPMAP_NEAREST", "GL_NEAREST_MIPMAP_LINEAR", "GL_LINEAR_MIPMAP_NEAREST", "GL_LINEAR_MIPMAP_LINEAR"]

        return dict(
            compress=dropDownField(translate('gfxSettingsDialog', 'Compress'), ["None", "GL_COMPRESSED_RG_RGTC2"],
                value=data.get('compress', self.fieldtemp[0])),
            anifilt=floatField(translate('gfxSettingsDialog', 'Anifilt'),
                min=1.0, max=16.0, decimals=1, value=data.get('Anifilt', self.fieldtemp[1])),
            minfilter=dropDownField(translate('gfxSettingsDialog', 'minfilter'), normFilters,
                value=data.get('minfilter', self.fieldtemp[2])),
            magfilter=dropDownField(translate('gfxSettingsDialog', 'magfilter'), normFilters,
                value=data.get('magfilter', self.fieldtemp[3])),
            mipminfilter=dropDownField(translate('gfxSettingsDialog', 'mipminfilter'), mipFilters,
                value=data.get('mipminfilter', self.fieldtemp[4])),
            FSAA=dropDownField(translate('gfxSettingsDialog', 'FSAA'), ["Off", "On"],
                value=data.get('FSAA', self.fieldtemp[5])),
            VBO=dropDownField(translate('gfxSettingsDialog', 'VBO'), ["Off", "On"],
                value=data.get('VBO', self.fieldtemp[6])))
    
    def _interpretFields(self, fields):
        """Interpret the fields into a dictionary of clean items."""
        return dict((key, field.clean()) for key, field in fields.items())
    
    def exec_(self, parent, accept):
        """Executes this dialog as modal, ensuring OK is only hit with valid data.
        
        parent -- the parent object of this dialog
        accept() -- Acceptance function;
            return True to accept data, False to continue (you should show an error)
        
        returns: True if the OK button is hit and the acceptance function passes.
        
        """
        
        widget = QtGui.QDialog(parent)
        
        # Buttons
        okayButton = QtGui.QPushButton(translate('gfxSettingsDialog', "Save"))
        okayButton.setDefault(True)
        cancelButton = QtGui.QPushButton(translate('gfxSettingsDialog', "Cancel"))
        
        # Add fields
        formLayout = QtGui.QFormLayout()
        for id in ('compress', 'anifilt', 'minfilter', 'magfilter', 'mipminfilter', 'FSAA', 'VBO'):
            field = self.fields[id]
            formLayout.addRow(translate('gfxSettingsDialog', '{0}: ', 'Row layout').format(field.name), field.widget(widget))
        
        # Add buttons
        theLesserOrFalseBox = QtGui.QBoxLayout(0)
        theLesserOrFalseBox.addWidget(okayButton)
        theLesserOrFalseBox.addWidget(cancelButton)
        
        # Position both
        grandBox = QtGui.QBoxLayout(2)
        grandBox.addLayout(formLayout)
        grandBox.addLayout(theLesserOrFalseBox)
        
        # Set up the widget
        widget.setLayout(grandBox)
        widget.setModal(True)
        widget.setWindowTitle(translate('gfxSettingsDialog', "Configure Graphics"))
        
        # Allow user to specify validation
        def okayPressed():
            if accept():
                widget.accept()
        
        # Signals
        widget.connect(okayButton, QtCore.SIGNAL('clicked()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('clicked()'), widget.reject)
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
        
    def clean(self):
        """Check for errors and return well-formatted data."""
        self.cleanData = self._interpretFields(self.fields)
        return self.cleanData
    
    def save(self):
        """Make a new map and return it."""
        assert(self.cleanData)
        return self._interpretFields(self.fields)
