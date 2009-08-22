import _bmainmod
from PyQt4 import QtCore

class tile(_bmainmod.bImage):

    #x, y, width, height, tile, layer, filename
    def __init__(self, position, dimensions, tile, layer, filename):
        x, y = position
        w, h = dimensions
        super(_bmainmod.bImage, self).__init__(int(x), int(y), int(w),
                                              int(h), int(tile), int(layer), str(filename))
        #print 'pyimage created'

