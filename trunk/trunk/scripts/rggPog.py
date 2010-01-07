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
import rggTile, rggResource
from rggJson import loadString, loadInteger, loadObject, loadArray, loadCoordinates

class Pog(object):
    def __init__(self, position, dimensions, layer, srcfile):
        self.ID = None
        self._position = position
        self.dimensions = dimensions
        self._layer = layer
        self._src = srcfile
        self.name = None
        self.tile = None
        self.show()
        rggResource.crm.listen(srcfile, rggResource.RESOURCE_IMAGE, self, self._updateSrc)
    
    @property
    def hidden(self):
        return not self.tile
    
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        if not self.hidden:
            x, y = position
            self.tile.setX(x)
            self.tile.setY(y)
    
    def displace(self, displacement):
        self.position = map(lambda p,d: p + d, self.position, displacement)
        return self.position

    def hide(self):
        if self.tile:
            self.tile.destroy()
            self.tile = None

    def show(self):
        if self.hidden:
            self.tile = self._makeTile()
    
    @property
    def layer(self):
        return self._layer
    
    @layer.setter
    def layer(self, layer):
        self._layer = layer
        if not self.hidden:
            self.tile.setLayer(int(layer))
    
    @property
    def src(self):
        return self._src
    
    def pointCollides(self, point):
        if self.hidden: return False
        x, y = point
        sx, sy = self.position
        sw, sh = self.dimensions
        if (sx > x or sx + sw < x or
            sy > y or sy + sh < y):
            return False
        return True

    def tooltipPosition(self):
        return self.position[0], self.position[1] - 20
    
    def tooltipText(self):
        self.atttmp = []
        if self.name is not None: self.atttmp.append(unicode(self.name))
        if self.atttmp is not []:
            return " ".join(self.atttmp)
        return None

    def deriveStringForm(self):
        self.tmp = [str(self.ID), str(self.x), str(self.y), str(self.w), str(self.h),
                             str(self.layer), str(self._src)]
        if self.name is not None:
            self.tmp.append(str(self.name))
        return " ".join(self.tmp)
    
    def _makeTile(self):
        src = rggResource.crm.translateFile(self._src, rggResource.RESOURCE_IMAGE)
        return rggTile.tile(self.position, self.dimensions, 0, self.layer, src)
    
    def _updateSrc(self, crm, filename, translation):
        if filename == self._src and self.tile:
            self.tile.destroy()
            self.tile = self._makeTile()
    
    def dump(self):
        """Serialize to an object valid for JSON dumping."""
        return dict(
            position=self.position,
            dimensions=self.dimensions,
            layer=self.layer,
            src=self._src,
            name=self.name)
    
    @staticmethod
    def load(obj):
        """Deserialize a new map from a dictionary."""
        pog = Pog(
            loadCoordinates('Pog.position', obj.get('position'), length=2),
            loadCoordinates('Pog.dimensions', obj.get('dimensions'), length=2, min=1, max=65535),
            loadInteger('Pog.layer', obj.get('layer'), min=0, max=65535),
            loadString('Pog.src', obj.get('src')))
        pog.name = loadString('Pog.name', obj.get('name'), allowEmpty=True)
        return pog
