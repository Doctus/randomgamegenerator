'''
rggJson - for the Random Game Generator project
By Doctus (kirikayuumura.noir@gmail.com)

Loading of JSON data.

    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''

from json import dump, dumps, load, loads
from gzip import open as gzipopen
from .rggFields import validationError
from .rggSystem import makeLocalFilename
from .rggConstants import BASE_STRING, JSON_MODE

def jsondumps(obj):
	"""Dumps the object into a string. Contains no newlines."""
	# compact version
	#serial = dumps(obj, separators=(',',':'))
	# pretty print
	serial = dumps(obj, sort_keys=True)
	assert(isinstance(serial, BASE_STRING))
	assert('\n' not in serial)
	return serial

def jsondump(obj, filename):
	"""Dump object to file."""
	with gzipopen(makeLocalFilename(filename), 'w'+JSON_MODE) as file:
		dump(obj, file, sort_keys=True, indent=4)

def jsonloads(str):
	"""Loads the object from a string. May throw."""
	obj = loads(str)
	assert(isinstance(obj, list) or isinstance(obj, dict))
	return obj

def jsonload(filename):
	"""Loads the object from a file. May throw."""
	try:
		with gzipopen(makeLocalFilename(filename), 'r'+JSON_MODE) as file:
			obj = load(file)
	except: #might be an old uncompressed save
		with open(makeLocalFilename(filename), 'r'+JSON_MODE) as file:
			obj = load(file)
	assert(isinstance(obj, list) or isinstance(obj, dict))
	return obj

def jsonappend(obj, filename):
	"""Dump object to file. Merges with existing file if present."""
	try:
		dat = jsonload(filename)
	except:
		jsondump(obj, filename)
		return
	dat.update(obj)
	jsondump(dat, filename)

def loadString(name, value, allowEmpty=False):
	if allowEmpty and value is None:
		return ''
	if isinstance(value, BASE_STRING):
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

def loadFloat(name, value, min=None, max=None):
	try:
		value = float(value)
	except:
		raise validationError('Validation expected {0} to be an float, found {1}.'.format(name, value))
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
				value[i], min=min, max=max) for i in range(len(value)))
	raise validationError(
		'Validation expected {0} to be an array of coordinates, found {1}.'.
			format(name, value))

