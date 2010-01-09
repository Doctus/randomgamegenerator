'''
rggJson - for the Random Game Generator project            
By Doctus (kirikayuumura.noir@gmail.com)

Loading of JSON data.

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

from rggFields import validationError
from rggSystem import makeLocalFilename
import json

def jsondumps(obj):
    """Dumps the object into a string. Contains no newlines."""
    # compact version
    #serial = json.dumps(obj, separators=(',',':'))
    # pretty print
    serial = json.dumps(obj, sort_keys=True)
    assert(isinstance(serial, basestring))
    assert('\n' not in serial and u'\n' not in serial)
    return serial

def jsondump(obj, filename):
    """Dump object to file."""
    file = open(makeLocalFilename(filename), 'wb')
    # compact version
    #json.dump(obj, file, separators=(',',':'))
    # pretty print
    json.dump(obj, file, sort_keys=True, indent=4)
    file.close()

def jsonloads(str):
    """Loads the object from a string. May throw."""
    obj = json.loads(str)
    assert(isinstance(obj, list) or isinstance(obj, dict))
    return obj

def jsonload(filename):
    """Loads the object from a file. May throw."""
    file = open(makeLocalFilename(filename), 'rb')
    obj = json.load(file)
    file.close()
    assert(isinstance(obj, list) or isinstance(obj, dict))
    return obj

def loadString(name, value, allowEmpty=False):
    if allowEmpty and value is None:
        return ''
    if isinstance(value, basestring):
        if allowEmpty or len(value) > 0:
            return value
    raise validationError('Validation expected {0} to be a string, found {1}.'.format(name, value))

def loadInteger(name, value, min=None, max=None):
    try:
        value = int(value)
    except:
        raise validationError('Validation expected {0} to be an integer, found {1}.'.format(name, value))
    if min is None or min <= value:
        if max is None or max >= value:
            return value
    raise validationError(
        'Validation expected {0} to be a number between {1} and {2}, found {3}.'.
            format(name, min or 'negative infinity', max or 'infinity', value))

def loadObject(name, value):
    if isinstance(value, dict):
        return value
    raise validationError(
        'Validation expected {0} to be an object, found {1}.'.
            format(name, value))
    
def loadArray(name, value, length=None):
    if isinstance(value, list):
        if length is None or len(value) == length:
            return value
    raise validationError(
        'Validation expected {0} to be an array, found {1}.'.
            format(name, value))
    
def loadCoordinates(name, value, length=None, min=None, max=None):
    if isinstance(value, list) or isinstance(value, tuple):
        if length is None or len(value) == length:
            return tuple(loadInteger('{name}[{coord}]'.format(name=name, coord=i),
                value[i], min=min, max=max) for i in xrange(len(value)))
    raise validationError(
        'Validation expected {0} to be an array of coordinates, found {1}.'.
            format(name, value))

