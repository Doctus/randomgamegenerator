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
    def __init__(self, ID, initx, inity, width, height, layer, srcfile):
        self.ID = int(ID)
        self.x = int(initx)
        self.y = int(inity)
        self.w = int(width)
        self.h = int(height)
        self.layer = int(layer)
        self.src = unicode(srcfile)
        self.tile = rggTile.tile(self.x, self.y, self.w, self.h, 0, self.layer, self.src)
        self.name = None
        self.hidden = False

    def getPointCollides(self, point):
        if self.hidden: return False
        if (self.x > point[0] or self.x+self.w < point[0] or
            self.y > point[1] or self.y+self.h < point[1]):
            return False
        return True

    def updateLoc(self):
        self.tile.setX(self.x)
        self.tile.setY(self.y)

    def absoluteMove(self, newx, newy):
        #print "Moving Yue to " + str(newx) + str(newy)
        self.x = newx
        self.y = newy
        self.updateLoc()

    def relativeMove(self, changex, changey):
        self.x += changex
        self.y += changey
        self.updateLoc()

    def hide(self):
        self.tile = None
        self.hidden = True

    def show(self):
        self.tile = rggTile.tile(self.x, self.y, self.w, self.h, 0, self.layer, self.src)
        self.hidden = False

    def reloadTile(self, srcfile):
        if not self.hidden and self.src == srcfile:
            self.show()

    def getPrintableAttributes(self):
        self.atttmp = []
        if self.name is not None: self.atttmp.append(unicode(self.name))
        if self.atttmp is not []:
            return " ".join(self.atttmp)
        return None

    def getOverheadTooltipLoc(self):
        return [self.x, self.y-20]

    def deriveStringForm(self):
        self.tmp = [str(self.ID), str(self.x), str(self.y), str(self.w), str(self.h),
                             str(self.layer), str(self.src)]
        if self.name is not None:
            self.tmp.append(str(self.name))
        return " ".join(self.tmp)
