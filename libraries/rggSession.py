'''
rggSession - for the Random Game Generator project

A class representing a savable game state of pogs, lines, and maps.

By Doctus (kirikayuumura.noir@gmail.com)

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
from sys import maxsize

from libraries.rggPog import Pog
from libraries.rggMap import Map
from libraries.rggEvent import pogUpdateEvent, pogDeleteEvent
from libraries.rggJson import loadString, loadInteger, loadObject, loadArray, loadCoordinates
from libraries.rggSystem import mainWindow, clearLines, drawLine, findRandomAppend

class Session(object):

	def __init__(self):
		self.maps = {}
		self.pogs = {}

		self.lines = []
		self.linesDict = {}

		self.maphack = 0

	def _addMap(self, mappe):
		'''Adds a map that is already loaded and has an ID.'''
		assert(mappe.ID is not None)
		if mappe.drawOffset == [0, 0]:
			pos = self.maphack
			mappe.drawOffset = (pos, 0)
		self.maps[mappe.ID] = mappe
		self.maphack += mappe.pixelSize[0] + 25

	def _addPog(self, pog):
		'''Adds a pog to the session without informing rggEvent.'''
		assert(pog.ID is not None)
		self.pogs[pog.ID] = pog

	def _findUniqueMapID(self, src):
		'''Get a unique id for a map.'''
		id = src or findRandomAppend()
		while id in list(self.maps.keys()):
			id += findRandomAppend()
		return id

	def _findUniquePogID(self, src):
		'''Get a unique id for a pog.'''
		id = src or findRandomAppend()
		while id in list(self.pogs.keys()):
			id += findRandomAppend()
		return id

	def addPog(self, pog):
		'''Adds a pog to the session, informing rggEvent of the addition.'''
		assert(pog.ID is not None)
		#rggResource.srm.processFile(localuser(), pog._src)
		self.pogs[pog.ID] = pog
		pogUpdateEvent(pog)
		self.hideAllHiddenPogs()

	def removePog(self, pog):
		'''Deletes a pog.'''
		assert(pog.ID is not None)
		pogDeleteEvent(self.pogs[pog.ID])
		self.pogs[pog.ID].destroy()
		del self.pogs[pog.ID]

	def removeAllPogs(self):
		'''Deletes all pogs in the session.'''
		for pog in list(self.pogs.values()):
			pogDeleteEvent(pog)
			pog.destroy()
		self.pogs = {}

	def addMap(self, mappe):
		'''Creates a new map and assigns it a unique ID.'''
		if mappe.drawOffset == [0, 0]:
			pos = self.maphack
			mappe.drawOffset = (pos, 0)
		self.maphack += mappe.pixelSize[0] + 25

		ID = self._findUniqueMapID(mappe.mapname)
		mappe.ID = ID

		#rggResource.srm.processFile(localuser(), map.tileset)

		self.maps[ID] = mappe

	def addDumpedMap(self, dump, ID):
		'''Adds a map from a JSON dump with the specified ID.'''
		mappe = Map.load(dump)
		mappe.ID = ID
		self._addMap(mappe)

	def getMapExists(self, ID):
		'''Returns whether a map with the given ID exists in this session.'''
		return ID in list(self.maps.keys())

	def getMap(self, ID):
		'''Returns the map with a given ID.'''
		return self.maps[ID]

	def findTopMap(self, mapPosition):
		'''Returns the top map at a given position, or None.'''
		for mappe in list(self.maps.values()):
			size = mappe.pixelSize
			if mapPosition[0] >= mappe.drawOffset[0] and mapPosition[0] <= mappe.drawOffset[0] + size[0]:
				if mapPosition[1] >= mappe.drawOffset[1] and mapPosition[1] <= mappe.drawOffset[1] + size[1]:
					return mappe
		return None

	def closeMap(self, ID):
		'''Deletes a specified map and its tiles.'''
		self.maps[ID]._deleteTiles()
		del self.maps[ID]

	def closeAllMaps(self):
		'''Deletes all maps and their tiles.'''
		self.maphack = 0
		for mappe in list(self.maps.values()):
			mappe._deleteTiles()
		self.maps = {}

	def findTopPog(self, position):
		'''Returns the top pog at a given position, or None.'''
		layer = -maxsize
		locked = True
		top = None
		for pog in list(self.pogs.values()):
			if (layer >= pog.layer and not (locked and not pog._locked)) or (not locked and pog._locked):
				continue
			if pog.pointCollides(position):
				top = pog
				layer = top.layer
				locked = pog._locked
		return top

	def refreshPogs(self):
		'''Forcibly refreshes all pogs in the session.'''
		for pog in list(self.pogs.values()):
			pog.forceUpdate()

	def storeLines(self):
		'''Stores all lines of which the session is aware in a JSON-compatible format in self.lines'''
		self.lines = []

		for thickness, lines in list(self.linesDict.items()):
			for item in lines:
				self.lines.extend( [item[0], item[1], item[2], item[3], thickness, item[4], item[5], item[6]] )

	def restoreLines(self):
		'''Draws all lines of which the session is aware.'''
		for thickness, lines in list(self.linesDict.items()):
			for item in lines:
				drawLine(item[0], item[1], item[2], item[3], thickness, item[4], item[5], item[6])

	def _pointIntersectRect(self, point, rect):
		'''Check used by deleteLine.'''
		if point[0] < rect[0] or point[0] > rect[0] + rect[2]: return False
		if point[1] < rect[1] or point[1] > rect[1] + rect[3]: return False
		return True

	def deleteLine(self, x, y, w, h):
		'''Remove all lines within the x, y, w, h rect from the session's awareness. This does not delete the lines themselves.'''
		for thickness, lines in list(self.linesDict.items()):
			dellist = []
			for line in lines:
				if self._pointIntersectRect((line[0], line[1]), (x, y, w, h)) or self._pointIntersectRect((line[2], line[3]), (x, y, w, h)):
					dellist.append(line)
			for index in dellist:
				lines.remove(index)

	def addLine(self, line):
		'''Add a line to the session's awareness from a tuple of parameters. This does not create a graphical line.'''
		if not line[4] in self.linesDict:
			self.linesDict[line[4]] = []
		self.linesDict[line[4]].append([line[0], line[1], line[2], line[3], line[5], line[6], line[7]])

	def hideAllHiddenPogs(self):
		'''Checks through all pogs to make sure the ones that should be hidden, are. Workaround for a glwidget issue.'''
		for pog in list(self.pogs.values()):
			if pog.hidden:
				pog.hide()

	def clear(self):
		'''Clear all session data to prepare for loading a new one.'''
		for map in list(self.maps.values()):
			map._deleteTiles()
		for pog in list(self.pogs.values()):
			pog.destroy()
		clearLines()
		self.maps = {}
		self.pogs = {}
		self.lines = []
		self.linesDict = {}
		self.maphack = 0

	def hide(self):
		'''Hide all maps, pogs, and lines while retaining their data.'''
		for map in list(self.maps.values()):
			map.hide()
		for pog in list(self.pogs.values()):
			pog._realHide(True)
		clearLines()

	def show(self):
		'''Restores display of maps, pogs, and lines after a hide() call.'''
		for map in list(self.maps.values()):
			map.show()
		for pog in list(self.pogs.values()):
			pog._realHide(False)
		self.restoreLines()

	def dump(self):
		'''Serialize to an object valid for JSON dumping.'''

		self.storeLines()

		return dict(
			pogs=dict([(pog.ID, pog.dump()) for pog in list(self.pogs.values())]),
			maps=dict([(mappe.ID, mappe.dump()) for mappe in list(self.maps.values())]),
			lines=self.lines,
			maphack=self.maphack)

	@staticmethod
	def load(obj):
		"""Deserialize a new map from a dictionary."""
		sess = Session()

		pogs = loadObject('Session.pogs', obj.get('pogs'))
		for ID, pog in list(pogs.items()):
			loaded = Pog.load(pog)
			loaded.ID = ID
			sess._addPog(loaded)

		for pog in list(sess.pogs.values()):
			if pog.hidden:
				pog.hide()

		maps = loadObject('Session.maps', obj.get('maps'))
		for ID, mappe in list(maps.items()):
			loaded = Map.load(mappe)
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
			print("Loading old session - map placement may be wrong")

		return sess
