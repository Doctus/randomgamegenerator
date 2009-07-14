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

class Pog:
    def __init__(self, initx, inity, width, height, layer, srcfile):
        self.x = initx
        self.y = inity
        self.w = width
        self.h = height
        self.layer = layer
        self.src = srcfile
        self.tile = rggTile.tile(self.x, self.y, self.w, self.h, 0, layer, self.src)

    def updateLoc(self):
        self.tile = rggTile.tile(self.x, self.y, self.w, self.h, 0, self.src)

    def absoluteMove(self, newx, newy):
        print "Moving Yue to " + str(newx) + str(newy)
        self.x = newx
        self.y = newy
        self.updateLoc()

    def relativeMove(self, changex, changey):
        self.x += changex
        self.y += changey
        self.updateLoc()
