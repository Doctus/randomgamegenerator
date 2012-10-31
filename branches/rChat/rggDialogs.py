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
from rggSystem import fake, translate, showErrorMessage, findFiles, IMAGE_EXTENSIONS, IMAGE_NAME_FILTER, TILESET_DIR, PORTRAIT_DIR, SAVE_DIR, makePortableFilename
from rggFields import integerField, floatField, stringField, dropDownField, sliderField, validationError
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

class banDialog(QtGui.QDialog):
    """A dialog used to manage the server banlist."""

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("Banlist")
        
        self.list = QtGui.QListWidget(self)
        for item in self.loadList():
            self.list.addItem(QtGui.QListWidgetItem(item))
            
        self.inputBox = QtGui.QLineEdit(self)
        
        self.addButton = QtGui.QPushButton("Add")
        self.deleteButton = QtGui.QPushButton("Delete")
        self.okButton = QtGui.QPushButton("Ok")
        self.cancelButton = QtGui.QPushButton("Cancel")
        
        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.list, 0, 0, 1, 2)
        self.layout.addWidget(self.inputBox, 1, 0, 1, 2)
        self.layout.addWidget(self.addButton, 2, 0)
        self.layout.addWidget(self.deleteButton, 2, 1)
        self.layout.addWidget(self.okButton, 3, 0)
        self.layout.addWidget(self.cancelButton, 3, 1)

        self.addButton.clicked.connect(self.add)
        self.deleteButton.clicked.connect(self.delete)
        self.okButton.clicked.connect(self.okPressed)
        self.cancelButton.clicked.connect(self.cancelPressed)
        
        self.setLayout(self.layout)
        
    def loadList(self):
        """Returns the currently saved bans, or a blank list if
           file access fails for any reason."""
        try:
            obj = jsonload(os.path.join(SAVE_DIR, "banlist.rgs"))
            return obj["IPs"]
        except:
            return []
        
    def saveList(self):
        ips = []
        for i in xrange(self.list.count()):
            ips.append(str(self.list.item(i).text()))
        iplist = {"IPs":ips}
        jsondump(iplist, os.path.join(SAVE_DIR, "banlist.rgs"))
        
    def add(self):
        self.list.addItem(self.inputBox.text())
        self.inputBox.clear()
        
    def delete(self):
        self.list.takeItem(self.list.currentRow())
        
    def okPressed(self, checked):
        self.saveList()
        self.done(1)

    def cancelPressed(self, checked):
        self.done(0)
    
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
                min=1, max=65535, value=data.get('port', self.fieldtemp[0])),
            password=stringField(
                translate('hostDialog', 'Password'),
                value=data.get('password', ''),
                allowEmpty=True))
    
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
        checkIPButton = QtGui.QPushButton(translate('hostDialog', "Check IP"))
        self.checkIPLabel = QtGui.QLineEdit()
        self.checkIPLabel.setReadOnly(True)
        self.wordIPLabel = QtGui.QLineEdit()
        self.wordIPLabel.setReadOnly(True)
        
        # Add fields
        formLayout = QtGui.QFormLayout()
        for id in ('port', 'username', 'password'):
            field = self.fields[id]
            formLayout.addRow(
                translate('hostDialog', '{0}: ', 'Row layout').format(field.name),
                field.widget(widget))
        
        # Set up layout
        grandBox = QtGui.QGridLayout()
        grandBox.addLayout(formLayout, 0, 0, 1, 2)
        grandBox.addWidget(checkIPButton, 1, 0)
        grandBox.addWidget(self.checkIPLabel, 1, 1)
        grandBox.addWidget(self.wordIPLabel, 2, 0, 1, 2)
        grandBox.addWidget(okayButton, 3, 0)
        grandBox.addWidget(cancelButton, 3, 1)
        
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
        widget.connect(checkIPButton, QtCore.SIGNAL('clicked()'), self.checkIP)
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)

    def checkIP(self):
        import urllib2
        ip = str(urllib2.urlopen('http://automation.whatismyip.com/n09230945.asp').read())
        
        with open("2of12inf.txt", "r") as f:
            dat = f.readlines()
            ipdat = ip.split(".")
            vals = ((int(ipdat[0])*256+int(ipdat[1])),(int(ipdat[2])*256+int(ipdat[3])))
            wordresult = " ".join((dat[vals[0]][:-1], dat[vals[1]][:-1]))
            
        self.checkIPLabel.setText(ip)
        self.wordIPLabel.setText(wordresult)
    
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
            self.cleanData['username'], self.cleanData['password'])
    
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
                min=1, max=65535, value=data.get('port', self.fieldtemp[1])),
            password=stringField(
                translate('joinDialog', 'Password'),
                value=data.get('password', ''),
                allowEmpty=True))
    
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
        
        warningLabel1 = QtGui.QLabel(translate('joinDialog', "Warning: open maps or other session"))
        warningLabel2 = QtGui.QLabel(translate('joinDialog', "data will be replaced upon joining."))
        
        # Add fields
        formLayout = QtGui.QFormLayout()
        for id in ('host', 'port', 'username', 'password'):
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
        grandBox.addWidget(warningLabel1)
        grandBox.addWidget(warningLabel2)
        
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
        if len(self.cleanData['host'].split()) == 2:
            with open("2of12inf.txt", "r") as f:
                inp = self.cleanData['host'].split()
                _dat = f.readlines()
                dat = map(lambda d: d.strip(), _dat)
                wordindex = [dat.index(inp[0]), dat.index(inp[1])]
                ipextract = unicode(".".join((str(wordindex[0]//256), str(wordindex[0]%256), str(wordindex[1]//256), str(wordindex[1]%256))))
                self.cleanData['host'] = ipextract
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
            self.cleanData['username'], self.cleanData['password'])
    
class PortraitFileSystemModel(QtGui.QFileSystemModel):

    def __init__(self):
        super(QtGui.QFileSystemModel, self).__init__()
        self.setRootPath(PORTRAIT_DIR)
        self.setNameFilters(IMAGE_NAME_FILTER)
        self.setNameFilterDisables(False)
        self.absRoot = os.path.abspath(unicode(PORTRAIT_DIR))
        
    def data(self, index, role):
        basedata = QtGui.QFileSystemModel.data(self, index, role)
        if basedata.canConvert(69):
            nodes = [index,]
            while nodes[0].parent().isValid():
                nodes.insert(0, nodes[0].parent())
            paths = []
            for node in nodes:
                paths.append(unicode(self.data(node, 0).toString()))
            if len(os.path.splitdrive(os.getcwd())[0]) > 0:
                paths[0] = os.path.splitdrive(os.getcwd())[0]+"\\"
            path = os.path.join(*paths)
            if os.path.isfile(path):
                return QtGui.QIcon(path)
        return basedata

class PortraitTreeView(QtGui.QTreeView):

    def setParent(self, parent):
        self.call = parent

    def selectionChanged(self, selected, deselected):
        super(QtGui.QTreeView, self).selectionChanged(selected, deselected)
        self.call.changePort(selected)
        
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
                value=data.get('portrait', translate('newCharacterDialog', ' '))))
    
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
        self.portraitModel = PortraitFileSystemModel()
        self.ROOT_LEN = len(self.portraitModel.absRoot)+1
        self.portraitArea = PortraitTreeView(parent)
        self.portraitArea.setParent(self)
        self.portraitArea.setModel(self.portraitModel)
        self.portraitArea.setRootIndex(self.portraitModel.index(PORTRAIT_DIR))
        self.portraitArea.setColumnHidden(1, True)
        self.portraitArea.setColumnHidden(2, True)
        self.portraitArea.setColumnHidden(3, True)
        self.portraitPreview = QtGui.QLabel(" ")
        
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
        grandBox.addWidget(self.portraitPreview)
        grandBox.addLayout(theLesserOrFalseBox)
        
        evilBox = QtGui.QBoxLayout(0)
        evilBox.addWidget(self.portraitArea)
        evilBox.addLayout(grandBox)
        
        #self.portraitArea.pressed.connect(self.changePort)
        
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
        
        #portraits = findFiles(PORTRAIT_DIR, IMAGE_EXTENSIONS)
        #portraits.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
        #for greatJustice in portraits:
        #    icon = QtGui.QIcon(os.path.join(PORTRAIT_DIR, greatJustice))
        #    self.portraitArea.addItem(QtGui.QListWidgetItem(icon, greatJustice))
        
        # Show to user
        return (widget.exec_() == QtGui.QDialog.Accepted)
    
    def changePort(self, selection):
        for i in selection.indexes():
            portrait = i
        self.fields['portrait'].widgett.setText(unicode(self.portraitModel.filePath(portrait))[self.ROOT_LEN:])
        preview = QtGui.QPixmap(self.portraitModel.filePath(portrait))
        if preview.isNull():
            #Typically, this means a folder has been selected.
            self.fields['portrait'].widgett.setText(unicode(" "))
            self.portraitPreview.clear()
            return
        preview = preview.scaled(min(preview.width(), 64), min(preview.height(), 64))
        self.portraitPreview.setPixmap(preview)
        
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
  