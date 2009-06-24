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

def loadFromString(s):
  mapname = " ".join(s[s.index('n!')+1:s.index('!n')])
  authorname = " ".join(s[s.index('a!')+1:s.index('!a')])
  mapsize = [int(s[s.index('m!')+1]), int(s[s.index('m!')+2])]
  tileset = s[s.index('t!')+1]
  #tileset = imageManager.load(s[s.index('t!')+1]) //see below
  tilesize = [int(s[s.index('s!')+1]), int(s[s.index('s!')+2])]
  tiles = []
  for tile in range(s.index('s!')+3, len(s)):
    if '~' in s[tile]:
      for x in range(0, int(s[tile][s[tile].index('~')+1:])):
        tiles.append(int(s[tile][0:s[tile].index('~')]))
    else: tiles.append(int(s[tile]))
  #print 'list generation done'
  while len(tiles) < mapsize[0]*mapsize[1]:
    tiles.append(1)
  #image.drawClippedAt(x, y, rect_clip) //not sure how interaction will
  #                                    work; should the ID/tileset be
  #                                    passed or the xywh of the tile or?
  print mapname
  print authorname
  print tiles

def DEBUGLoadFromFile():
  f = open('test.txt', 'r')
  tmp = f.read().split()
  f.close()
  _loadFromString(tmp)

def DEBUGSaveToFile():
  #The proper version of saving should basically take the various
  #inputs, format them properly, and write to a specified file.
  #It will of course be important to implement the same RLE.
  f = open('test.txt', 'w')
  f.write('n! Example Map !n a! Doctus !a m! 5 5 t! town.png s! '+
          '32 32 5 1~15 12 5 8 9 6~5')
  f.close()
