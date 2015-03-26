'''
rggConstants - for the Random Game Generator project
By Doctus (kirikayuumura.noir@gmail.com)

Configuration values for internal constants.

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

import sys

# Version

VERSION = "1.04"
DEV = True
REPOSITORY_LINK = "https://github.com/Doctus/randomgamegenerator"

# Graphical settings

COLOURS = {"White":(1.0, 1.0, 1.0),
		   "Red": (1.0, 0.0, 0.0),
		   "Orange": (1.0, 0.5, 0.0),
		   "Yellow": (1.0, 1.0, 0.0),
		   "Green": (0.0, 0.8, 0.2),
		   "Blue": (0.0, 0.0, 1.0),
		   "Purple": (0.76, 0.0, 1.0),
		   "Black": (0.0, 0.0, 0.0)}

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".ppm", ".xbm", ".xpm")
IMAGE_NAME_FILTER = list(('*{ext}'.format(ext=ext) for ext in IMAGE_EXTENSIONS))
IMAGE_FILTER = 'Images ({imageList})'.format(imageList=','.join('*{ext}'.format(ext=ext) for ext in IMAGE_EXTENSIONS))

# Network settings

PING_INTERVAL_SECONDS = 10
IP_CACHE_TIME = 900 #15 minutes

# Directory structure

TILESET_DIR = 'data/tilesets'
POG_DIR = 'data/pogs'
PORTRAIT_DIR = 'data/portraits'
PLUGINS_DIR = 'plugins'
LOG_DIR = 'save/logs'
MAP_DIR = 'save/maps'
CHAR_DIR = 'save/characters'
CHARSHEETS_DIR = 'save/sheets'
MUSIC_DIR = 'data/music'
SAVE_DIR = 'save'

# Priority values for event handling

LATE_RESPONSE_LEVEL = 10
NORMAL_RESPONSE_LEVEL = 5
EARLY_RESPONSE_LEVEL = 0

# Save data strings

GFX_SETTINGS_FILE = "gfx_settings.rgs"

GFX_PREFIX = "gfx."

ANI_FILTER_STRING = "anifilt"
MIN_FILTER_STRING = "minfilter"
MAG_FILTER_STRING = "magfilter"
MIPMIN_FILTER_STRING = "mipminfilter"
FSAA_SETTING_STRING = "FSAA"
VBO_SETTING_STRING = "VBO"
MAGIC_SETTING_STRING = "Magic"
ON_OFF_OPTIONS = ["Off", "On"]
STANDARD_FILTER_OPTIONS = ["GL_NEAREST", "GL_LINEAR"]
MIP_FILTER_OPTIONS = ["Off", "GL_NEAREST_MIPMAP_NEAREST", "GL_NEAREST_MIPMAP_LINEAR", "GL_LINEAR_MIPMAP_NEAREST", "GL_LINEAR_MIPMAP_LINEAR"]

# Python 2 / 3 compatibility constants

if sys.version_info >= (3,):
	BASE_STRING = str
	UNICODE_STRING = str
else:
	BASE_STRING = basestring
	UNICODE_STRING = unicode
