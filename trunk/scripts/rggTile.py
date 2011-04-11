#import _bmainmod
#from PyQt4 import QtCore

'''class tile(_bmainmod.bImage):

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
        self.DELETEME()'''

        
# -*- coding: utf-8 -*-
#
#Image convenience class
#
#By Oipo (kingoipo@gmail.com)

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.arrays import ArrayDatatype as ADT

import numpy

class tile(object):
    '''
    Class for storing image data, position and some opengl stuff
    '''

    def __init__(self, imagepath, qimg, textureRect, drawRect, layer, hidden, dynamicity, glwidget):
        self.imagepath = imagepath
        self.drawRect = drawRect
        self.textureRect = textureRect
        self._layer = layer
        self.dynamicity = dynamicity
        self.textureId = None
        self.offset = None
        self.VBO = None
        self._hidden = hidden
        self.qimg = qimg
        self.glwidget = glwidget
        self.createLayer = False

        if self.glwidget.texext == GL_TEXTURE_2D:
            x = float(textureRect[0])/float(qimg.width()-1)
            y = float(textureRect[1])/float(qimg.height()-1)
            w = float(textureRect[2])/float(qimg.width()-1)
            h = float(textureRect[3])/float(qimg.height()-1)
            self.textureRect = [x, y, w, h]

    #def __del__(self):
        #self.glwidget.deleteImage(self)
            
    def destroy(self):
        self.glwidget.deleteImage(self)

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, hide):
        if self._hidden != hide:
            self._hidden = hide
            self.glwidget.hideImage(self, hide)
            
    @property
    def layer(self):
        return self._layer
        
    @layer.setter
    def layer(self, newlayer):
        self.glwidget.setLayer(self, newlayer)
        self._layer = newlayer
            
    def setHidden(self, hide):
        if self._hidden != hide:
            self._hidden = hide
            self.glwidget.hideImage(self, hide)
            
    def setX(self, x):
        drawRect = list(self.drawRect)
        drawRect[0] = x
        self.setDrawRect(drawRect)
        
    def setY(self, y):
        drawRect = list(self.drawRect)
        drawRect[1] = y
        self.setDrawRect(drawRect)
        
    def getW(self):
        return self.drawRect[2]
        
    def getH(self):
        return self.drawRect[3]

    def width(self):
        return self.drawRect[2]

    def height(self):
        return self.drawRect[3]

    def setDrawRect(self, drawRect):
        self.drawRect = drawRect

        if self.glwidget.vbos:
            VBOData = self.getVBOData()
            vertByteCount = ADT.arrayByteCount(VBOData)

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBO)
            glBufferSubData(GL_ARRAY_BUFFER_ARB, int(self.offset*vertByteCount/4), vertByteCount, VBOData)

    def setTextureRect(self, textureRect):
        self.textureRect = textureRect
        if self.glwidget.texext == GL_TEXTURE_2D:
            x = float(textureRect[0])/float(self.qimg.width())
            y = float(textureRect[1])/float(self.qimg.height())
            w = float(textureRect[2])/float(self.qimg.width())
            h = float(textureRect[3])/float(self.qimg.height())
            self.textureRect = [x, y, w, h]
            
        if self.glwidget.vbos:
            VBOData = self.getVBOData()
            vertByteCount = ADT.arrayByteCount(VBOData)

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBO)
            glBufferSubData(GL_ARRAY_BUFFER_ARB, int(self.offset*vertByteCount/4), vertByteCount, VBOData)

    def getVBOData(self):
        x, y, w, h = self.textureRect
        dx, dy, dw, dh = self.drawRect

        VBOData = numpy.zeros((8, 2), 'f')

        VBOData[0, 0] = x #tex
        VBOData[0, 1] = y+h

        VBOData[1, 0] = dx #vert
        VBOData[1, 1] = dy

        VBOData[2, 0] = x+w #tex
        VBOData[2, 1] = y+h

        VBOData[3, 0] = dx+dw #vert
        VBOData[3, 1] = dy

        VBOData[4, 0] = x+w
        VBOData[4, 1] = y

        VBOData[5, 0] = dx+dw
        VBOData[5, 1] = dy+dh

        VBOData[6, 0] = x
        VBOData[6, 1] = y

        VBOData[7, 0] = dx
        VBOData[7, 1] = dy+dh

        return VBOData
