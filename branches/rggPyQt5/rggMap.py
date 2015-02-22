'''
rggMap - for the Random Game Generator project            

By Doctus (kirikayuumura.noir@gmail.com)

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
import rggTile, rggSystem, rggResource, random
from rggJson import loadString, loadInteger, loadObject, loadArray, loadCoordinates
from rggSystem import mainWindow

class Map(object):
    
    def __init__(self, mapname, authorname, mapsize, tileset, tilesize, drawOffset = [0, 0]):
        """Initializes a new map."""
        
        self.ID = None
        self.mapname = mapname
        self.authorname = authorname
        self.mapsize = mapsize
        self.tileset = tileset
        self.tilesize = tilesize

        self.tileindexes = [0 for i in range(mapsize[0] * mapsize[1])]
        self.hidden = False
        self.tiles = None
        self.initted = False
        self._drawOffset = drawOffset

        #self._createTiles()

        rggResource.crm.listen(tileset, rggResource.RESOURCE_IMAGE, self, self._updateSrc)
        
    @property
    def pixelSize(self):
        size = [self.mapsize[0], self.mapsize[1]]
        size[0] *= self.tilesize[0]
        size[1] *= self.tilesize[1]
        return size

    @property
    def drawOffset(self):
        return self._drawOffset
        
    @drawOffset.setter
    def drawOffset(self, drawOffset):
        displacement = [0, 0]
        displacement[0] = drawOffset[0] - self._drawOffset[0]
        displacement[1] = drawOffset[1] - self._drawOffset[1]
        self._drawOffset = drawOffset
        print("drawOffset:", drawOffset)
        
        if self.tiles != None:
            for t in self.tiles:
                t.displaceDrawRect(displacement)
    
    def hide(self, hidden=True):
        """Hide or show all tiles."""
        if hidden == self.hidden:
            return
        self.hidden = hidden
        if hidden:
            self._hideTiles()
        else:
            self._showTiles()
    
    def show(self):
        return self.hide(False)

    def _hideTiles(self):
        for tile in self.tiles:
            tile.setHidden(True)

    def _showTiles(self):
        if self.tiles == None:
            return
        for tile in self.tiles:
            tile.setHidden(False)
    
    def _deleteTiles(self):
        mainWindow.glwidget.deleteImages(self.tiles)
        self.tiles = None
        rggResource.crm.destroy(self)
    
    def _createTiles(self):
        """Show all the tiles of this map."""
        src = rggResource.crm.translateFile(self.tileset, rggResource.RESOURCE_IMAGE)
        imgsize = mainWindow.glwidget.getImageSize(rggResource.crm.translateFile(src, rggResource.RESOURCE_IMAGE))

        if self.tiles != None:
            mainWindow.glwidget.deleteImages(self.tiles)

        print("deleted tiles")

        self.tiles = [None]*self.mapsize[0]*self.mapsize[1]
        mainWindow.glwidget.reserveVBOSize(self.mapsize[0] * self.mapsize[1])

        for y in range(0, self.mapsize[1]):
            for x in range(0, self.mapsize[0]):
                texx = self.tileindexes[x+self.mapsize[0]*y]%(imgsize.width()/self.tilesize[0])*self.tilesize[0]
                texy = int((self.tileindexes[x+self.mapsize[0]*y]*self.tilesize[0])/imgsize.width())*self.tilesize[1]
                textureRect = (texx, texy, self.tilesize[0], self.tilesize[1])
                drawRect = (x * self.tilesize[0] + self.drawOffset[0], y * self.tilesize[1] + self.drawOffset[1], self.tilesize[0], self.tilesize[1])
                temptile = mainWindow.glwidget.createImage(src, 0, textureRect, drawRect, self.hidden)
                self.tiles[x+y*self.mapsize[0]] = temptile
                
        print("created tiles")

    def _updateSrc(self, crm, filename, translation):
        if filename == self.tileset and crm._status[filename] == rggResource.STATE_DONE:
            self._createTiles()
        print("update src", self.ID, filename, self.tileset, crm._status[filename])
    
    def getTile(self, tile):
        """Change the specified tile."""
        x, y = tile
        assert(0 <= x <= self.mapsize[0])
        assert(0 <= y <= self.mapsize[1])
        t = x + self.mapsize[0] * y
        return self.tileindexes[int(t)]
    
    def setTile(self, tile, index):
        """Change the specified tile."""
        x, y = tile
        assert(0 <= x <= self.mapsize[0])
        assert(0 <= y <= self.mapsize[1])
        t = x + self.mapsize[0] * y
        self.tileindexes[t] = index
        imgsize = mainWindow.glwidget.getImageSize(rggResource.crm.translateFile(self.tileset, rggResource.RESOURCE_IMAGE))
        
        x = index%(imgsize.width()/self.tilesize[0])*self.tilesize[0]
        y = int((index*self.tilesize[0])/imgsize.width())*self.tilesize[1]
        self.tiles[t].setTextureRect((x, y, self.tilesize[0], self.tilesize[1]))

    def tilePosExists(self, tilepos):
        x, y = tilepos
        return ((0 <= x < self.mapsize[0]) and (0 <= y < self.mapsize[1]))
    
    def _setIndexes(self, indexes):
        if len(indexes) != len(self.tileindexes):
            return
        self.tileindexes[:] = indexes[:]
    
    def dump(self):
        """Serialize to an object valid for JSON dumping."""

        return dict(
            mapname=self.mapname,
            authorname=self.authorname,
            mapsize=self.mapsize,
            tileset=self.tileset,
            tilesize=self.tilesize,
            tiles=self.tileindexes,
            drawoffset=self._drawOffset)
    
    @staticmethod
    def load(obj, dumpmode=False):
        """Deserialize a new map from a dictionary."""
        map = Map(
            loadString('Map.mapname', obj.get('mapname')),
            loadString('Map.authorname', obj.get('authorname')),
            loadCoordinates('Map.mapsize', obj.get('mapsize'), length=2, min=1, max=65535),
            loadString('Map.tileset', obj.get('tileset')),
            loadCoordinates('Map.tilesize', obj.get('tilesize'), length=2, min=1, max=65535),
            loadCoordinates('Map.drawoffset', obj.get('drawoffset'), length=2))
        
        # HACK: Looks like coordinates; saves work.
        tiles = loadCoordinates('Map.tiles', obj.get('tiles'), length=len(map.tileindexes), min=0, max=65535)
        map._setIndexes(tiles)
        map._createTiles()
        return map
        
    def __unicode__(self):
        return "{0} {1}".format(self.mapname, self.ID)
    
    def __str__(self):
        return self.__unicode__()
