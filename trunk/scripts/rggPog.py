#rggPog - for the Random Game Generator project            
#
#By Doctus (kirikayuumura.noir@gmail.com)
'''
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
from PyQt4 import QtGui
import rggTile, rggResource, rggSystem, math
from rggJson import loadString, loadInteger, loadObject, loadArray, loadCoordinates

class Pog(object):
    def __init__(self, position, texturedimensions, size, layer, srcfile, status, locked, properties, mapID, alph):
        self.ID = None
        self._position = position
        self.texturedimensions = texturedimensions
        self._size = size
        self._layer = layer
        self._src = srcfile
        self.name = None
        self._tileStore = None
        self._fakeHidden = False
        self._properties = properties
        self._showTooltip = False
        self.tooltipId = -1
        self.mapID = mapID
        self.alpha = alph
        self._locked = locked #locked only works for mouse movements. This means that scripts may actually be able to move the pog.
        rggResource.crm.listen(srcfile, rggResource.RESOURCE_IMAGE, self, self._updateSrc)
        if status > 0:
            self.hide()
    
    def destroy(self):
        if self._tileStore:
            self._tileStore.destroy()
            self._tileStore = None

    @property
    def hidden(self):
        return self._fakeHidden
    
    @property
    def status(self):
        if self._fakeHidden: return 1
        return 0
        
    @property
    def showTooltip(self):
        return self._showTooltip
        
    @showTooltip.setter
    def showTooltip(self, show):
        if self._showTooltip != show:
            if self.tooltipText() == None or len(self.tooltipText()) == 0:
                return
            from rggSystem import mainWindow
            if show:
                self.tooltipId = mainWindow.glwidget.addText(self.tooltipText(), self._position)
            else:
                mainWindow.glwidget.removeText(self.tooltipId)
            self._showTooltip = show
    
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        if not self.hidden:
            x, y = position
            self._tile.setX(x)
            self._tile.setY(y)
            if self._showTooltip:
                from rggSystem import mainWindow
                mainWindow.glwidget.setTextPos(self.tooltipId, position)
    
    @property
    def _tile(self):
        return self._tileStore
    
    @_tile.setter
    def _tile(self, tile):
        if self._tileStore != None:
            self._tileStore.destroy()
        self._tileStore = tile

    @property
    def size(self):
        return self._size
    
    @property
    def properties(self):
        return self._properties

    @size.setter
    def size(self, size):
        self._size = size
        if self._tileStore:
            self._tileStore.setDrawW(size[0])
            self._tileStore.setDrawH(size[1])
            
    def editProperty(self, key, value):
        self._properties[key] = value
        if self._showTooltip:
            from rggSystem import mainWindow
            mainWindow.glwidget.removeText(self.tooltipId)
            self.tooltipId = mainWindow.glwidget.addText(self.tooltipText(), self._position)
    
    def displace(self, displacement):
        if self._locked:
            return self.position

        self.position = map(lambda p,d: p + d, self.position, displacement)
        return self.position

    def hide(self):
        self._fakeHidden = True
        if self._tile:
            self._tile.setHidden(True)

    def show(self):
        self._fakeHidden = False
        if self._tile:
            self._tile.setHidden(False)

    def _realHide(self, hide):
        '''This makes the pog not redraw, but not necessarily hidden in a map.
           If a map hides and consecutively shows, we don't want previously hidden pogs to be shown.
        '''
        if self._tile:
            self._tile.setHidden(hide)
    
    @property
    def layer(self):
        return self._layer
    
    @layer.setter
    def layer(self, layer):
        self._layer = layer
        if not self.hidden:
            self._tile.layer = int(layer)
    
    @property
    def src(self):
        return self._src
    
    def pointCollides(self, point):
        if self.hidden: return False
        x, y = point
        sx, sy = self.position
        sw, sh = self.size
        if (sx > x or sx + sw < x or
            sy > y or sy + sh < y):
            return False
        return True

    def tooltipPosition(self):
        return self.position[0], self.position[1] - 20
    
    def tooltipText(self):
        self.atttmp = []
        if self.name is not None: self.atttmp.append(unicode(self.name))
        for key in self._properties:
            self.atttmp.append(": ".join([key, self._properties[key]])) 
        if self.atttmp is not []:
            return "\n".join(self.atttmp)
        return None

    def deriveStringForm(self):
        self.tmp = [str(self.ID), str(self.x), str(self.y), str(self.w), str(self.h),
                             str(self.layer), str(self._src)]
        if self.name is not None:
            self.tmp.append(str(self.name))
        return " ".join(self.tmp)
    
    def _makeTile(self):
        from rggSystem import mainWindow
        src = rggResource.crm.translateFile(self._src, rggResource.RESOURCE_IMAGE)
        textureRect = (0, 0, self.texturedimensions[0], self.texturedimensions[1])
        drawRect = (self.position[0], self.position[1], self.size[0], self.size[1])
        return mainWindow.glwidget.createImage(src, self.layer, textureRect, drawRect)
    
    def _updateSrc(self, crm, filename, translation):
        if filename == self._src and crm._status[filename] == rggResource.STATE_DONE:
            self._tile = self._makeTile()
            
    def getSelectionCircleData(self):
        if self.alpha:
            return ((self.position[0]+self.size[0]/2, self.position[1]+self.size[1]/2, -1, (max(self.size[0], self.size[1])*1.2)/2))
        else:
            return ((self.position[0]+self.size[0]/2, self.position[1]+self.size[1]/2, -1, math.sqrt((self.size[0]**2)+(self.size[1]**2))/2))
            
    def forceUpdate(self):
        self._tile = self._makeTile()
    
    def dump(self):
        """Serialize to an object valid for JSON dumping."""
        return dict(
            position=self.position,
            texturedimensions=self.texturedimensions,
            size=self.size,
            layer=self.layer,
            src=self._src,
            name=self.name,
            status=self.status,
            locked=self._locked,
            properties=self.properties,
            mapID=self.mapID,
            alpha=self.alpha)
    
    @staticmethod
    def load(obj):
        """Deserialize a new map from a dictionary."""
        pog = Pog(
            loadCoordinates('Pog.position', obj.get('position'), length=2),
            loadCoordinates('Pog.texturedimensions', obj.get('texturedimensions'), length=2, min=1, max=65535),
            loadCoordinates('Pog.size', obj.get('size'), length=2, min=1, max=65535),
            loadInteger('Pog.layer', obj.get('layer'), min=0, max=65535),
            loadString('Pog.src', obj.get('src')),
            loadInteger('Pog.status', obj.get('status')),
            loadInteger('Pog.locked', obj.get('locked')),
            loadObject('Pog.properties', obj.get('properties')),
            loadString('Pog.mapID', obj.get('mapID')),
            loadInteger('Pog.alpha', obj.get('alpha')))
        pog.name = loadString('Pog.name', obj.get('name'), allowEmpty=True)
        return pog
