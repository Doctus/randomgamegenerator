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
import rggTile, rggPog, rggSystem, rggResource, random
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
        
        self.Pogs = {}
        self.lines = []
        self.linesDict = {}
        self.tileindexes = [0 for i in xrange(mapsize[0] * mapsize[1])]
        self.hidden = False
        self.tiles = None
        self._drawOffset = drawOffset

        self._createTiles()

        rggResource.crm.listen(tileset, rggResource.RESOURCE_IMAGE, self, self._updateSrc)

    def addPog(self, pog, dumpmode=False):
        """Adds a pog to the map, assigning it a unique id."""
        assert(pog.ID is not None)
        import rggEvent
        self.Pogs[pog.ID] = pog
        if self.hidden:
            pog._realHide(True)
        if dumpmode: return
        pog._tile = pog._makeTile()
        if pog.hidden:
            pog._realHide(True)
        rggEvent.pogUpdateEvent(pog)

    def removePog(self, pog):
        assert(pog.ID is not None)
        import rggEvent
        rggEvent.pogDeleteEvent(self.Pogs[pog.ID])
        self.Pogs[pog.ID]._tile.destroy()
        del self.Pogs[pog.ID]

    def _findUniqueID(self, src):
        """Get a unique id for a pog."""
        id = src or rggSystem.findRandomAppend()
        while id in self.Pogs:
            id += rggSystem.findRandomAppend()
        return id
        
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
        
        #if not self.hidden:
        for t in self.tiles:
            t.displaceDrawRect(displacement)
    
    def hide(self, hidden=True, includeTiles=True, includePogs=True, includeLines=True):
        """Hide or show all pogs and tiles."""
        if hidden == self.hidden:
            return
        self.hidden = hidden
        if includePogs:
            if hidden:
                for pog in self.Pogs.values():
                    pog._realHide(True)
            else:
                for pog in self.Pogs.values():
                    if not pog.hidden:
                        pog._realHide(False)
        if includeTiles:
            if hidden:
                self._hideTiles()
            else:
                self._showTiles()
        if includeLines:
            if hidden:
                self.storeLines()
            else:
                self.restoreLines()
                
    def refreshPogs(self):
        for pog in self.Pogs.values():
            pog.forceUpdate()
    
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
        for tile in self.tiles:
            tile.destroy()
        self.tiles = None
    
    def _createTiles(self):
        """Show all the tiles of this map."""
        if self.tiles != None:
            for y in xrange(0, self.mapsize[1]):
                for x in xrange(0, self.mapsize[0]):
                    self.tiles[x+y*self.mapsize[0]].destroy()
        
        print "deleted tiles"
        
        src = rggResource.crm.translateFile(self.tileset, rggResource.RESOURCE_IMAGE)
        self.tiles = [None]*self.mapsize[0]*self.mapsize[1]
        mainWindow.glwidget.reserveVBOSize(self.mapsize[0] * self.mapsize[1])
        
        print "creating tiles"

        for y in xrange(0, self.mapsize[1]):
            for x in xrange(0, self.mapsize[0]):
                textureRect = (0, 0, self.tilesize[0], self.tilesize[1])
                drawRect = (x * self.tilesize[0] + self.drawOffset[0], y * self.tilesize[1] + self.drawOffset[1], self.tilesize[0], self.tilesize[1])
                temptile = mainWindow.glwidget.createImage(src, 0, textureRect, drawRect, self.hidden)
                self.tiles[x+y*self.mapsize[0]] = temptile
                
        print "created tiles"

    def _updateSrc(self, crm, filename, translation):
        if filename == self.tileset and crm._status[filename] == rggResource.STATE_READY:
            self._createTiles()
    
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
        return
        if len(indexes) != len(self.tileindexes):
            return
        self.tileindexes[:] = indexes[:]
        
        imgsize = mainWindow.glwidget.getImageSize(rggResource.crm.translateFile(self.tileset, rggResource.RESOURCE_IMAGE))
        
        for i in xrange(len(indexes)):
            #self.tiles[i].setTile(self.tileindexes[i])
            #print self.tileindexes[i], self.tiles[i].getTile()
            x = self.tileindexes[t]%(imgsize.width()/self.tilesize[0])*self.tilesize[0]
            y = int((index*self.tilesize[0])/imgsize.width())*self.tilesize[1]
            self.tiles[i].setTextureRect((x, y, self.tilesize[0], self.tilesize[1]))
    
    def findTopPog(self, position):
        """Returns the top pog at a given position, or None."""
        layer = -sys.maxint
        top = None
        for pog in self.Pogs.values():
            if layer >= pog.layer:
                continue
            if pog.pointCollides(position):
                top = pog
                layer = top.layer
        return top

    def storeLines(self):
        self.lines = []
        
        for item in self.linesDict.items():
            self.lines.extend( [item[1][0], item[1][1], item[1][1], item[1][1], item[0]] )

    def restoreLines(self):
        for line in self.lines:
            rggSystem.drawLine(line[0], line[1], line[2], line[3], line[4])
    
    def dump(self):
        """Serialize to an object valid for JSON dumping."""

        self.storeLines()

        return dict(
            mapname=self.mapname,
            authorname=self.authorname,
            mapsize=self.mapsize,
            tileset=self.tileset,
            tilesize=self.tilesize,
            pogs=dict([(pog.ID, pog.dump()) for pog in self.Pogs.values()]),
            tiles=self.tileindexes,
            lines=self.lines)
    
    @staticmethod
    def load(obj, dumpmode=False):
        """Deserialize a new map from a dictionary."""
        map = Map(
            loadString('Map.mapname', obj.get('mapname')),
            loadString('Map.authorname', obj.get('authorname')),
            loadCoordinates('Map.mapsize', obj.get('mapsize'), length=2, min=1, max=65535),
            loadString('Map.tileset', obj.get('tileset')),
            loadCoordinates('Map.tilesize', obj.get('tilesize'), length=2, min=1, max=65535))
        
        pogs = loadObject('Map.pogs', obj.get('pogs'))
        for ID, pog in pogs.items():
            loaded = rggPog.Pog.load(pog)
            loaded.ID = ID
            map.addPog(loaded, dumpmode)

        lines = loadArray('Map.lines', obj.get('lines'))
        map.lines = []
        for line in lines:
            map.lines.append(loadCoordinates('Map.lines[]', line))
        
        # HACK: Looks like coordinates; saves work.
        tiles = loadCoordinates('Map.tiles', obj.get('tiles'), length=len(map.tileindexes), min=0, max=65535)
        map._setIndexes(tiles)
        return map
        
    def __unicode__(self):
        return "{0} {1}".format(self.mapname, self.ID)
    
    def __str__(self):
        return self.__unicode__()
