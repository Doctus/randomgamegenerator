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
from rggSystem import fake, translate, showErrorMessage, findFiles, IMAGE_EXTENSIONS, TILESET_DIR, makePortableFilename
from rggFields import integerField, stringField, dropDownField, validationError
from rggNet import ConnectionData, localHost
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
        widget.connect(okayButton, QtCore.SIGNAL('pressed()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('pressed()'), widget.reject)
        
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
        
        return dict(
            username=stringField(
                translate('hostDialog', 'Username'),
                value=data.get('username', translate('hostDialog', 'Anonymous'))),
            port=integerField(
                translate('hostDialog', 'Port'),
                min=1, max=65535, value=data.get('port', 6812)))
    
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
        widget.connect(okayButton, QtCore.SIGNAL('pressed()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('pressed()'), widget.reject)
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
        
    def clean(self):
        """Check for errors and return well-formatted data."""
        self.cleanData = self._interpretFields(self.fields)
        return self.cleanData
    
    def save(self):
        """Make a new map and return it."""
        assert(self.cleanData)
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
        
        return dict(
            username=stringField(translate('joinDialog', 'Username'),
                value=data.get('username', translate('joinDialog', 'Anonymous'))),
            host=stringField(translate('joinDialog', 'Host Name'),
                value=data.get('host', localHost())),
            port=integerField(translate('joinDialog', 'Port'),
                min=1, max=65535, value=data.get('port', 6812)))
    
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
        widget.connect(okayButton, QtCore.SIGNAL('pressed()'), okayPressed)
        widget.connect(cancelButton, QtCore.SIGNAL('pressed()'), widget.reject)
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
        
    def clean(self):
        """Check for errors and return well-formatted data."""
        self.cleanData = self._interpretFields(self.fields)
        return self.cleanData
    
    def save(self):
        """Make a new map and return it."""
        assert(self.cleanData)
        return ConnectionData(self.cleanData['host'], self.cleanData['port'],
            self.cleanData['username'])
    
