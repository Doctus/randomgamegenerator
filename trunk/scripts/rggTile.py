import bmainmod
from PyQt4 import QtCore

class tile(bmainmod.bImage):

    def __init__(self, x, y, w, h, t, filename):
        super(bmainmod.bImage, self).__init__(x, y, w, h, t, filename)

