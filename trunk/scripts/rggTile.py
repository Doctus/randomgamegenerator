import _bmainmod
from PyQt4 import QtCore

class tile(_bmainmod.bImage):

    #x, y, width, height, tile, layer, filename
    def __init__(self, position, texturedimensions, drawdimensions, tile, layer, filename):
        x, y = position
        w, h = texturedimensions
        dw, dh = drawdimensions
        #for i in xrange(len(filename)):
        #    if filename[i] == '\\':
        #        filename = filename[:i] + '/' + filename[i+1:]
        #print (int(x), int(y), int(w),
        #                                      int(h), int(tile), int(layer), str(filename))
        super(_bmainmod.bImage, self).__init__(int(x), int(y), int(w),
                                               int(h), int(dw), int(dh),
                                               int(tile), int(layer), str(filename))
        #print 'pyimage created'

    def destroy(self):
        self.DELETEME()
