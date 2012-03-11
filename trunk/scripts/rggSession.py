'''
rggSession - for the Random Game Generator project            

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
import rggTile, rggPog, rggMap, rggSystem, rggResource, random, sys
from rggJson import loadString, loadInteger, loadObject, loadArray, loadCoordinates
from rggSystem import mainWindow, clearLines

class Session(object):
    
    def __init__(self):
        self.maps = {}
        self.pogs = {}
        
        self.lines = []
        self.linesDict = {}
        
        self.maphack = 0
        
    def _addMap(self, mappe):
        assert(mappe.ID is not None)
        if mappe.drawOffset == [0, 0]:
            pos = self.maphack
            mappe.drawOffset = (pos, 0)
        self.maps[mappe.ID] = mappe
        self.maphack += mappe.pixelSize[0] + 25
        
    def _addPog(self, pog):
        assert(pog.ID is not None)
        self.pogs[pog.ID] = pog
        
    def _findUniqueMapID(self, src):
        """Get a unique id for a map."""
        id = src or rggSystem.findRandomAppend()
        while id in self.maps.keys():
            id += rggSystem.findRandomAppend()
        return id
    
    def _findUniquePogID(self, src):
        """Get a unique id for a pog."""
        id = src or rggSystem.findRandomAppend()
        while id in self.pogs.keys():
            id += rggSystem.findRandomAppend()
        return id
    
    def addPog(self, pog):
        assert(pog.ID is not None)
        #rggResource.srm.processFile(localuser(), pog._src)
        import rggEvent
        self.pogs[pog.ID] = pog
        if pog.hidden:
            pog._realHide(True)
        rggEvent.pogUpdateEvent(pog)
    
    def removePog(self, pog):
        assert(pog.ID is not None)
        import rggEvent
        rggEvent.pogDeleteEvent(self.pogs[pog.ID])
        self.pogs[pog.ID].destroy()
        del self.pogs[pog.ID]
        
    def addMap(self, mappe):
        if mappe.drawOffset == [0, 0]:
            pos = self.maphack
            mappe.drawOffset = (pos, 0)
        self.maphack += mappe.pixelSize[0] + 25
    
        ID = self._findUniqueMapID(mappe.mapname)
        mappe.ID = ID
        
        #rggResource.srm.processFile(localuser(), map.tileset)
        
        self.maps[ID] = mappe
        
    def addDumpedMap(self, dump, ID):
        mappe = rggMap.Map.load(dump)
        mappe.ID = ID
        self._addMap(mappe)
        
    def getMapExists(self, ID):
        return ID in self.maps.keys()
        
    def getMap(self, ID):
        return self.maps[ID]
        
    def findTopMap(self, mapPosition):
        for mappe in self.maps.values():
            size = mappe.pixelSize
            if mapPosition[0] >= mappe.drawOffset[0] and mapPosition[0] <= mappe.drawOffset[0] + size[0]:
                if mapPosition[1] >= mappe.drawOffset[1] and mapPosition[1] <= mappe.drawOffset[1] + size[1]:
                    return mappe
        return None
        
    def closeMap(self, ID):
        self.maps[ID]._deleteTiles()
        del self.maps[ID]
    
    def closeAllMaps(self):
        self.maphack = 0
        for mappe in self.maps.values():
            mappe._deleteTiles()
        self.maps = {}
    
    def findTopPog(self, position):
        """Returns the top pog at a given position, or None."""
        layer = -sys.maxint
        top = None
        for pog in self.pogs.values():
            if layer >= pog.layer:
                continue
            if pog.pointCollides(position):
                top = pog
                layer = top.layer
        return top
    
    def refreshPogs(self):
        for pog in self.pogs.values():
            pog.forceUpdate()
    
    def storeLines(self):
        self.lines = []
        
        for thickness, lines in self.linesDict.items():
            for item in lines:
                self.lines.extend( [item[0], item[1], item[2], item[3], thickness, item[4], item[5], item[6]] )

    def restoreLines(self):
        for thickness, lines in self.linesDict.items():
            for item in lines:
                rggSystem.drawLine(item[0], item[1], item[2], item[3], thickness, item[4], item[5], item[6])
                
    def pointIntersectRect(self, point, rect):
        if point[0] < rect[0] or point[0] > rect[0] + rect[2]: return False
        if point[1] < rect[1] or point[1] > rect[1] + rect[3]: return False
        return True
                
    def deleteLine(self, x, y, w, h):
        for thickness, lines in self.linesDict.items():
            dellist = []
            for line in lines:
                if self.pointIntersectRect((line[0], line[1]), (x, y, w, h)) or self.pointIntersectRect((line[2], line[3]), (x, y, w, h)):
                    dellist.append(line)
            for index in dellist:
                lines.remove(index)
            
    def addLine(self, line):
        if not line[4] in self.linesDict:
            self.linesDict[line[4]] = []
        self.linesDict[line[4]].append([line[0], line[1], line[2], line[3], line[5], line[6], line[7]])
        
    def clear(self):
        """Clear all session data to prepare for loading a new one."""
        for map in self.maps.values():
            map._deleteTiles()
        for pog in self.pogs.values():
            pog.destroy()
        clearLines()
        self.maps = {}
        self.pogs = {}
        self.lines = []
        self.linesDict = {}
    
    def dump(self):
        """Serialize to an object valid for JSON dumping."""

        self.storeLines()

        return dict(
            pogs=dict([(pog.ID, pog.dump()) for pog in self.pogs.values()]),
            maps=dict([(mappe.ID, mappe.dump()) for mappe in self.maps.values()]),
            lines=self.lines,
            maphack=self.maphack)
    
    @staticmethod
    def load(obj):
        """Deserialize a new map from a dictionary."""
        sess = Session()
        
        pogs = loadObject('Session.pogs', obj.get('pogs'))
        for ID, pog in pogs.items():
            loaded = rggPog.Pog.load(pog)
            loaded.ID = ID
            sess._addPog(loaded)
            
        maps = loadObject('Session.maps', obj.get('maps'))
        for ID, mappe in maps.items():
            loaded = rggMap.Map.load(mappe)
            loaded.ID = ID
            sess._addMap(loaded)

        linez = obj.get('lines')
        brk = lambda x,y: [x[i:i+y] for i in range(0,len(x),y)]
        for line in brk(linez, 8):
            sess.addLine(line)
            
        sess.restoreLines()
        
        try:
            mh = obj.get('maphack')
            sess.maphack = int(mh)
        except:
            print "Loading old session - map placement may be wrong"
        
        return sess
