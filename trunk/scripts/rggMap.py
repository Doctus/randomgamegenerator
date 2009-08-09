#rggMap - for the Random Game Generator project            
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
import rggTile, rggPog, random

class Map:
  def __init__(self):
    self.Pogs = []
    self.pogsByID = {}

  def addPog(self, pog):
    self.Pogs.append(pog)
    if self.pogsByID.has_key(pog.ID):
      self.tmpint = 1
      while self.pogsByID.has_key(self.tmpint):
        self.tmpint = self.tmpint + 1
      pog.ID = self.tmpint
      self.pogsByID[pog.ID] = pog
    else:
      self.pogsByID[pog.ID] = pog

  def loadFromString(self, s):
    if len(s) != len("".join(s)): #An amusing way to do it since it must
      self.stringform = " ".join(s) #contain at least one two-character value
    else:
      self.stringform = s
    self.mapname = " ".join(s[s.index('n!')+1:s.index('!n')])
    self.authorname = " ".join(s[s.index('a!')+1:s.index('!a')])
    self.mapsize = [int(s[s.index('m!')+1]), int(s[s.index('m!')+2])]
    self.tileset = s[s.index('t!')+1]
    self.tilesize = [int(s[s.index('s!')+1]), int(s[s.index('s!')+2])]
    self.tileindexes = []
    self.itlim = len(s)
    if 'p!' in s:
      self.itlim = s.index('p!')
    for itertile in range(s.index('s!')+3, self.itlim):
      if '~' in s[itertile]:
        for x in range(0, int(s[itertile][s[itertile].index('~')+1:])):
          self.tileindexes.append(int(s[itertile][0:s[itertile].index('~')]))
      else: self.tileindexes.append(int(s[itertile]))
    while len(self.tileindexes) < self.mapsize[0]*self.mapsize[1]:
      self.tileindexes.append(1)
    self.tiles = []
    for x in range(0, self.mapsize[0]):
      self.tiles.append([])
      for y in range(0, self.mapsize[1]):
        self.tiles[x].append(rggTile.tile(x*self.tilesize[0], y*self.tilesize[1],
                                          self.tilesize[0], self.tilesize[1],
                                          self.tileindexes[x+(y*self.mapsize[0])],
                                          0,
                                          self.tileset))
    if 'p!' in s:
      self.tmppogseg = s[s.index('p!'):]
      while len(self.tmppogseg) > 0:
          self.addPog(rggPog.Pog(*self.tmppogseg[1:8]))
          self.tmppogseg = self.tmppogseg[8:]

  def encodeIndexes(self, ind):
    self.fullform = []
    self.output = []
    self.counthack = 1
    for item in ind:
      if (item+0!=item) and ('~' in item):
        for x in range(0, int(item[item.index('~')+1:])):
          self.fullform.append(item[0:item.index('~')])
      else:
        self.fullform.append(item)
    for index in range(0, len(self.fullform)-1):
      if self.fullform[index] == self.fullform[index+1]:
        self.counthack += 1
      else:
        if self.counthack == 1: self.output.append(str(self.fullform[index]))
        else: self.output.append(str(str(self.fullform[index]) + '~' + str(self.counthack)))
        self.counthack = 1
    return self.output

  def deriveStringForm(self, mname, aname, msize, tset, tsize, tindexes, pogz):
    #Best to do this "backwards" so we keep track of the indexes for insertion.
    self.result = ['n!', '!n', 'a!', '!a', 'm!', 't!', 's!']
    self.result.extend(self.encodeIndexes(tindexes))
    self.result.insert(7, str(tsize[1]))
    self.result.insert(7, str(tsize[0]))
    self.result.insert(6, str(tset))
    self.result.insert(5, str(msize[1]))
    self.result.insert(5, str(msize[0]))
    #Have to take several lines here because someone decided reverse()
    #should alter the string instead of returning the new version...
    tmpname = aname.split()
    tmpname.reverse()
    for portion in tmpname:
      self.result.insert(3, portion)
    tmpname = mname.split()
    tmpname.reverse()
    for portion in tmpname:
      self.result.insert(1, portion)
    #Now for the horror of the pogs.
    for pog in pogz:
      self.result.append("p! " + pog.deriveStringForm())
    return " ".join(self.result)

  def updateStringForm(self):
    self.stringform = self.deriveStringForm(self.mapname, self.authorname,
                                            self.mapsize, self.tileset,
                                            self.tilesize, self.tileindexes,
                                            self.Pogs)

  def debugMorphTile(self, coord, maxtiles):
    self.tileindexes[coord[0]+(coord[1]*self.mapsize[0])] = (self.tileindexes[coord[0]+(coord[1]*self.mapsize[0])] + 1)%maxtiles
    self.tiles[coord[0]][coord[1]] = rggTile.tile(coord[0]*self.tilesize[0], coord[1]*self.tilesize[1],
                                          self.tilesize[0], self.tilesize[1],
                                          self.tileindexes[coord[0]+(coord[1]*self.mapsize[0])], 0,
                                          self.tileset)
    self.updateStringForm()

  def debugGetTile(self, coord):
    return self.tileindexes[coord[0]+(coord[1]*self.mapsize[0])]

  def debugSetTile(self, coord, ind):
    self.tileindexes[coord[0]+(coord[1]*self.mapsize[0])] = ind
    self.tiles[coord[0]][coord[1]] = rggTile.tile(coord[0]*self.tilesize[0], coord[1]*self.tilesize[1],
                                          self.tilesize[0], self.tilesize[1],
                                          self.tileindexes[coord[0]+(coord[1]*self.mapsize[0])], 0,
                                          self.tileset)
    self.updateStringForm()

  def LoadFromFile(self, filename):
    f = open(filename, 'r')
    tmp = f.read().split()
    f.close()
    self.loadFromString(tmp)

  def reloadTiles(self, imgpath, includePogs=True):
    for x in range(0, self.mapsize[0]):
      self.tiles.append([])
      for y in range(0, self.mapsize[1]):
        self.tiles[x].append(rggTile.tile(x*self.tilesize[0], y*self.tilesize[1],
                                          self.tilesize[0], self.tilesize[1],
                                          self.tileindexes[x+(y*self.mapsize[0])],
                                          0,
                                          self.tileset))
    if includePogs:
      for pog in self.Pogs:
        pog.reloadTile(imgpath)

  def checkPogImages(self):
    uniqueImages = set()
    for pog in self.Pogs:
      uniqueImages.add(pog.src)
    return uniqueImages

  def hide(self):
    self.tiles = []

  def show(self):
    self.tiles = []
    for x in range(0, self.mapsize[0]):
      self.tiles.append([])
      for y in range(0, self.mapsize[1]):
        self.tiles[x].append(rggTile.tile(x*self.tilesize[0], y*self.tilesize[1],
                                          self.tilesize[0], self.tilesize[1],
                                          self.tileindexes[x+(y*self.mapsize[0])],
                                          0,
                                          self.tileset))
