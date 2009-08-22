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
import rggTile
from rggJson import loadString, loadInteger, loadObject, loadArray, loadCoordinates

class Pog(object):
    def __init__(self, position, dimensions, layer, srcfile):
        self.ID = None
        self._position = position
        self.dimensions = dimensions
        self._layer = layer
        self.src = srcfile
        self.name = None
        self.tile = None
        self.show()
    
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
        self.tile = None

    def show(self):
        if self.hidden:
            self.tile = rggTile.tile(self.position, self.dimensions, 0, self.layer, self.src)
    
    @property
    def layer(self):
        return self._layer
    
    @layer.setter
    def layer(self, layer):
        self._layer = layer
        if not self.hidden:
            self.tile.setLayer(int(layer))
    
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
                             str(self.layer), str(self.src)]
        if self.name is not None:
            self.tmp.append(str(self.name))
        return " ".join(self.tmp)
    
    def dump(self):
        """Serialize to an object valid for JSON dumping."""
        assert(self.ID is not None)
        return dict(
            id=self.ID,
            position=self.position,
            dimensions=self.dimensions,
            layer=self.layer,
            src=self.src,
            name=self.name)
    
    @staticmethod
    def load(obj):
        """Deserialize a new map from a dictionary."""
        pog = Pog(
            loadCoordinates('Pog.position', obj.get('position')),
            loadCoordinates('Pog.dimensions', obj.get('dimensions')),
            loadInteger('Pog.layer', obj.get('layer'), min=0, max=65535),
            loadString('Pog.src', obj.get('src')))
        pog.name = loadString('Pog.name', obj.get('name'), allowEmpty=True)
        pog.ID=loadString('Pog.id', obj.get('id'))
        return pog
