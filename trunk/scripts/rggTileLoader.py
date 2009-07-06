#rggTileLoader - for the Random Game Generator project
# v. 0.01  >> THIS IS MERELY A DEMONSTRATION INTENDED
#             FOR FUTURE REFERENCE AND WILL NOT
#             FUNCTION CORRECTLY AS-IS.
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

class Map:
  def __init__(self):
    pass

  def loadFromString(self, s):
    self.stringform = " ".join(s)
    self.mapname = " ".join(s[s.index('n!')+1:s.index('!n')])
    self.authorname = " ".join(s[s.index('a!')+1:s.index('!a')])
    self.mapsize = [int(s[s.index('m!')+1]), int(s[s.index('m!')+2])]
    self.tileset = s[s.index('t!')+1]
    self.tilesize = [int(s[s.index('s!')+1]), int(s[s.index('s!')+2])]
    self.tileindexes = []
    for itertile in range(s.index('s!')+3, len(s)):
      if '~' in s[itertile]:
        for x in range(0, int(s[itertile][s[itertile].index('~')+1:])):
          self.tileindexes.append(int(s[itertile][0:s[itertile].index('~')]))
      else: self.tileindexes.append(int(s[itertile]))
    #print 'list generation done'
    while len(self.tileindexes) < self.mapsize[0]*self.mapsize[1]:
      self.tileindexes.append(1)
    #print self.mapname
    #print self.authorname
    #print self.tiles
    self.tiles = []
    for x in range(0, self.mapsize[0]):
      self.tiles.append([])
      for y in range(0, self.mapsize[1]):
        self.tiles[x].append(rggTile.tile(x*self.tilesize[0], y*self.tilesize[1],
                                          self.tilesize[0], self.tilesize[1],
                                          self.tileindexes[x+(y*self.mapsize[0])],
                                          self.tileset))
        
  def DEBUGLoadFromFile(self):
    f = open('test.txt', 'r')
    tmp = f.read().split()
    f.close()
    self.loadFromString(tmp)

  def DEBUGSaveToFile(self):
    #The proper version of saving should basically take the various
    #inputs, format them properly, and write to a specified file.
    #It will of course be important to implement the same RLE.
    f = open('test.txt', 'w')
    f.write('n! Example Map !n a! Doctus !a m! 20 20 t! ../data/town.png s! '+
            '32 32 3~4 1~15 7 5 3 4 6~5 3~30 4 5 4 7 9 2 3')
    f.close()

  def LoadFromFile(self, filename):
    f = open(filename, 'r')
    tmp = f.read().split()
    f.close()
    self.loadFromString(tmp)
