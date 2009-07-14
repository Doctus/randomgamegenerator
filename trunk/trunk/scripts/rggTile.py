import bmainmod
from PyQt4 import QtCore

class tile(bmainmod.bImage):

    #x, y, width, height, tile, layer, filename
    def __init__(self, x, y, w, h, t, l, filename):
        super(bmainmod.bImage, self).__init__(x, y, w, h, t, l, filename)

