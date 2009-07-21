import _bmainmod
from PyQt4 import QtCore

class tile(_bmainmod.bImage):

    #x, y, width, height, tile, layer, filename
    def __init__(self, x, y, w, h, t, l, filename):
        print "loading " + filename + " at " + x + " " + y
        super(_bmainmod.bImage, self).__init__(int(x), int(y), int(w),
                                              int(h), int(t), int(l), str(filename))

