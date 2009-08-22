'''
rggFields - for the Random Game Generator project            
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

from PyQt4 import QtGui, QtCore
from rggSystem import translate, showErrorMessage

class validationError(Exception):
    """Error which occurs during input validation."""
    pass

class dialogField(object):
    """A field/widget pairing that self-validates and can be used in a GUI."""
    
    def __init__(self, name, value=None):
        self.value = value
        self.name = name
        self._widget = None
    
    def _cleanValue(self, value):
        """Cleans a given value."""
        raise NotImplementedError()
    
    def _createWidget(self, parent):
        """Return a new widget."""
        raise NotImplementedError()
    
    def _getWidgetValue(self, widget):
        """Get the value of the specified widget."""
        raise NotImplementedError()
        
    def widget(self, parent):
        """Creates a corresponding QT widget to use. Only call once."""
        assert(not self._widget)
        self._widget = self._createWidget(parent)
        return self._widget
    
    def clean(self):
        """Clean the field's value, returning a valid one, or throwing an error."""
        value = self.value
        if self._widget:
            value = self._getWidgetValue(self._widget)
        return self._cleanValue(value)
    
class integerField(dialogField):
    """An integer field with optional limits and suffix."""
    
    def __init__(self, name, value=None, min=None, max=None, suffix=None):
        """Initializes the field.
        
        name -- the name of the field
        value -- the initial value to store
        min -- the lower limit to allow
        max -- the upper limit to allow
        suffix -- the units to append to the input
        
        """
        super(integerField, self).__init__(name, value)
        self.min, self.max, self.suffix = min, max, suffix
    
    def _cleanValue(self, value):
        try:
            value = int(value)
        except:
            raise validationError(translate('integerField', 'You must enter a number for the {0} field.').format(self.name))
        if self.min is None or self.min <= value:
            if self.max is None or self.max >= value:
                return value
        raise validationError(
            translate('integerField', 'You must enter a number for {0} between {1} and {2}.').
                format(self.name,
                    self.min or translate('integerField', 'negative infinity'),
                    self.max or translate('integerField', 'infinity')))
    
    def _createWidget(self, parent):
        widget = QtGui.QSpinBox(parent)
        if self.min is not None:
            widget.setMinimum(self.min)
        if self.max is not None:
            widget.setMaximum(self.max)
        if self.suffix is not None:
            widget.setSuffix(self.suffix)
        try:
            if self.value is not None:
                widget.setValue(self._cleanValue(self.value))
        except:
            pass
        
        return widget
    
    def _getWidgetValue(self, widget):
        return int(widget.value())

class stringField(dialogField):
    """A basic string field."""
    
    def __init__(self, name, value=None, allowEmpty=False):
        """Initializes the field.
        
        name -- the name of the field
        value -- the initial value to store
        allowEmpty -- whether empty strings are allowed
        
        """
        super(stringField, self).__init__(name, value)
        self.allowEmpty = allowEmpty
    
    def _cleanValue(self, value):
        if value is None and self.allowEmpty:
            return ''
        if isinstance(value, basestring):
            if self.allowEmpty or len(value) > 0:
                return value
        raise validationError(translate('stringField', 'You must enter text into the {0} field.').format(self.name))
    
    def _createWidget(self, parent):
        value = ''
        try:
            value = self._cleanValue(self.value)
        except:
            pass
        widget = QtGui.QLineEdit(value, parent)
        return widget
    
    def _getWidgetValue(self, widget):
        return unicode(widget.text())

class dropDownField(dialogField):
    """A field made up of several independent choices."""
    
    def __init__(self, name, choices, value=None):
        """Initializes the field.
        
        name -- the name of the field
        choices -- the list of choices allowed
        value -- the initial value to store
        
        """
        super(dropDownField, self).__init__(name, value)
        self.choices = choices
    
    def _cleanValue(self, value):
        if len(self.choices) <= 0:
            return ''
        if value in self.choices:
            return value
        raise validationError(translate('dropDownField', 'You must enter a valid choice for the {0} field.').format(self.name))
    
    def _createWidget(self, parent):
        index = -1
        widget = QtGui.QComboBox(parent)
        for choice in self.choices:
            if choice == self.value:
                index = widget.count()
            widget.addItem(choice)
        if index >= 0:
            widget.setCurrentIndex(index)
        return widget
    
    def _getWidgetValue(self, widget):
        return unicode(widget.currentText())

