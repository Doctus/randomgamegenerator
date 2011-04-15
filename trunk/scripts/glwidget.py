# -*- coding: utf-8 -*-
#
#glWidget - Takes care of drawing images, with optionally glmod to speed things up
#
#By Oipo (kingoipo@gmail.com)

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.extensions import hasGLExtension
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.arrays import ArrayDatatype as ADT

#Only set these when creating non-development code
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *

mod = False
try:
    print "Loading GLMod"
    import glmod
    mod = True
except:
    print "Failed!"
    pass

from rggTile import *

def nextPowerOfTwo(val):
    val -= 1
    val = (val >> 1) | val
    val = (val >> 2) | val
    val = (val >> 4) | val
    val = (val >> 8) | val
    val = (val >> 16) | val
    val += 1
    return val

class GLWidget(QGLWidget):
    '''
    Widget for drawing everything, and for catching mouse presses and similar
    '''

    mousePressSignal = pyqtSignal(int, int, int) #x, y, button
    mouseReleaseSignal = pyqtSignal(int, int, int) #x, y, button
    mouseMoveSignal = pyqtSignal(int, int) #x, y
    
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        self.w = 640
        self.h = 480
        self.images = dict()
        self.lastMousePos = [0, 0]
        self.camera = [0, 0]
        self.layers = []
        self.zoom = 1
        self.VBO = None
        self.vbos = False
        self.VBOBuffer = 0
        self.offset = 0
        self.ctrl = False
        self.shift = False
        self.qimages = {}
        self.texext = GL_TEXTURE_2D
        self.npot = 3
        self.lines = dict()
        self.error = False
        self.texts = []
        self.textid = 0
        self.vertByteCount = ADT.arrayByteCount(numpy.zeros((8, 2), 'f'))
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True) #this may be the fix for a weird problem with leaveevents

    #GL functions
    def paintGL(self):
        '''
        Drawing routine
        '''

        glClear(GL_COLOR_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(self.camera[0], self.camera[1], 0)
        glScaled(self.zoom, self.zoom, 1)

        if self.vbos:
            glmod.drawVBO()
        else:
            for layer in self.layers:
                for img in self.images[layer]:
                    self.drawImage(img)

        if mod:
            glmod.drawLines(self.lines)
        else:
            for layer in self.lines:
                glLineWidth(layer)
                glBegin(GL_LINES)
                for line in self.lines[layer]:
                    glVertex2f(line[0], line[1])
                    glVertex2f(line[2], line[3])
                glEnd()

        for text in self.texts:
            split = text[1].split("\n")
            if len(split[0]) == 0:
                split.pop(0)
            pos = -16 * (len(split) - 1)
            for t in split:
                if len(t) == 0:
                    continue
                
                self.renderText(float(text[2][0]), float(text[2][1])+pos, 0, t)
                pos += 16

        glScaled(1/self.zoom, 1/self.zoom, 1)
        glTranslatef(-self.camera[0], -self.camera[1], 0)
        glPopMatrix()
        
    def addLine(self, thickness, x, y, w, h):
        if not thickness in self.lines:
            self.lines[thickness] = []
            
        self.lines[thickness].append((float(x), float(y), float(w), float(h)))
        
    def deleteLine(self, thickness, x, y, w, h):
        if thickness == -1:
            for layer in self.lines:
                for line in self.lines[layer]:
                    if self.pointIntersectRect((line[0], line[1]), (x, y, w, h)) \
                       and self.pointIntersectRect((line[0] + line[2], line[1] + line[3]), (x, y, w, h)):
                        self.lines[layer].remove(line)
                        
    def clearLines(self):
        self.lines.clear()
                    
    def pointIntersectRect(self, point, rect): 
    #point: (x, y)
    #rect:  (x, y, w, h)
        if point[0] < rect[0] or point[0] > rect[0] + rect[2]:
            return False
        if point[1] < rect[1] or point[1] > rect[1] + rect[3]:
            return False
        return True

    def resizeGL(self, w, h):
        '''
        Resize the GL window 
        '''

        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_FASTEST)
        self.w = w
        self.h = h

    def initializeGL(self):
        '''
        Initialize GL
        '''
        global mod
        
        if not hasGLExtension("GL_ARB_framebuffer_object"):
            print "GL_ARB_framebuffer_object not supported, switching to GL_GENERATE_MIPMAP"
            self.npot = 2
        version = glGetString(GL_VERSION)
        if int(version[0]) == 1 and int(version[2]) < 4: #no opengl 1.4 support
            print "GL_GENERATE_MIPMAP not supported, not using mipmapping"
            self.npot = 1
        if not hasGLExtension("GL_ARB_texture_non_power_of_two"):
            print "GL_ARB_texture_non_power_of_two not supported, switching to GL_ARB_texture_rectangle"
            self.texext = GL_TEXTURE_RECTANGLE_ARB
            self.npot = 1
        if not hasGLExtension("GL_ARB_texture_rectangle"):
            print "GL_TEXTURE_RECTANGLE_ARB not supported, switching to GL_TEXTURE_2D"
            self.texext = GL_TEXTURE_2D
            self.npot = 0

        glEnable(self.texext)
        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, self.width(), self.height())
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_FASTEST)

        initok = False
        if mod:
            ret = glmod.init(self.texext)
            if ret == -1:
                print "Something terrible went wrong in initializing glmod"
                mod = False
            elif ret == -2:
                print "using gl module without VBO support"
            else:
                initok = True
                print "using gl module with VBO support"

        if mod and initok:
            if glInitVertexBufferObjectARB() and bool(glBindBufferARB):
                self.vbos = True
                print "VBO support initialised succesfully"
                self.VBO = int(glGenBuffersARB(1))
                glmod.initVBO(self.VBO, ADT.arrayByteCount(numpy.zeros((2, 2), 'f')))
            else:
                print "VBO support initialisation failed, continuing without"

    #util functions
    def createImage(self, qimagepath, layer, textureRect, drawRect, hidden = False, dynamicity = GL_STATIC_DRAW_ARB):
        '''
        Creates an rggTile instance, uploads the correct image to GPU if not in cache, and some other helpful things.
        '''
        #print "requested to create", qimagepath, layer, textureRect, drawRect, hidden
        layer = int(layer)
        texture = None
        found = False

        if qimagepath in self.qimages:
            qimg = self.qimages[qimagepath][0]
            if self.qimages[qimagepath][2] > 0:
                texture = self.qimages[qimagepath][1]
                found = True
        else:
            qimg = QImage(qimagepath)
            print "created", qimagepath

        if textureRect[2] == -1:
            textureRect[2] = qimg.width() - 1

        if textureRect[3] == -1:
            textureRect[3] = qimg.height() - 1

        if drawRect[2] == -1:
            drawRect[2] = qimg.width()

        if drawRect[3] == -1:
            drawRect[3] = qimg.height()

        image = tile(qimagepath, qimg, textureRect, drawRect, layer, hidden, dynamicity, self)

        if found == False:
            if self.npot == 0:
                w = nextPowerOfTwo(qimg.width())
                h = nextPowerOfTwo(qimg.height())
                if w != qimg.width() or h != qimg.height():
                    qimg = qimg.scaled(w, h)
     
            img = self.convertToGLFormat(qimg)
            texture = glGenTextures(1)
            imgdata = img.bits().asstring(img.numBytes())

            glBindTexture(self.texext, texture)
            
            if self.npot == 3:
                glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
                glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            elif self.npot == 2:
                glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
                glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(self.texext, GL_GENERATE_MIPMAP, GL_TRUE)
            else:
                glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

            glTexImage2D(self.texext, 0, GL_RGBA, img.width(), img.height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imgdata);

            if self.npot == 3:
                glEnable(GL_TEXTURE_2D)
                glGenerateMipmap(GL_TEXTURE_2D)
            
            self.qimages[qimagepath] = [qimg, texture, 1] #texture, reference count
        else:
            self.qimages[qimagepath][2] += 1

        image.textureId = texture

        if layer not in self.images:
            self.images[layer] = []
            self.layers = self.images.keys()
            self.layers.sort()
            image.createLayer = True

        self.images[layer].append(image)

        if self.vbos:
            image.VBO = self.VBO
            self.fillBuffers(image)
            self.calculateVBOList(image)

        return image

    def reloadImage(self, qimagepath):
        '''
        reload a texture
        '''

        qimg = None
        texture = 0

        if qimagepath in self.qimages:
            qimg = self.qimages[qimagepath][0]
            if self.qimages[qimagepath][2] > 0:
                texture = self.qimages[qimagepath][1]
            else:
                print "no texture for", qimagepath
                return
        else:
            print "couldn't find", qimagepath
            return

        if self.npot == 0:
            w = nextPowerOfTwo(qimg.width())
            h = nextPowerOfTwo(qimg.height())
            if w != qimg.width() or h != qimg.height():
                qimg = qimg.scaled(w, h)
 
        img = self.convertToGLFormat(qimg)
        texture = glGenTextures(1)
        imgdata = img.bits().asstring(img.numBytes())

        glBindTexture(self.texext, texture)
        
        if self.npot == 3:
            glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
            glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        elif self.npot == 2:
            glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
            glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(self.texext, GL_GENERATE_MIPMAP, GL_TRUE)
        else:
            glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage2D(self.texext, 0, GL_RGBA, img.width(), img.height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imgdata);

        if self.npot == 3:
            glEnable(GL_TEXTURE_2D)
            glGenerateMipmap(GL_TEXTURE_2D)

        print "reloaded", qimagepath

    def reserveVBOSize(self, size):
        '''
        Reserves a VBO with the specified size as the amount of VBO entries, and re-assigns all images with the new data.
        '''
        if self.vbos and size > self.VBOBuffer:
            self.VBOBuffer = nextPowerOfTwo(size+1)
            print "reserving size", self.VBOBuffer

            self.fillBuffers(None, False)
            self.calculateVBOList()

    def fillBuffers(self, image = None, resize = True):
        '''
        if image == None, this function requests a new BO from the GPU with a calculated size
        if image != None, this function adds the VBO data from image to the BO in the GPU, if there is enough space.
        '''
        size = 0

        for layer in self.layers:
            size += len(self.images[layer])

        glBindBufferARB(GL_ARRAY_BUFFER_ARB, self.VBO)

        if self.VBOBuffer <= size or image == None:
            if resize and self.VBOBuffer <= size:
                print "resizing from", size, "to", nextPowerOfTwo(size+1)
                self.VBOBuffer = nextPowerOfTwo(size+1)

            glBufferDataARB(GL_ARRAY_BUFFER_ARB, self.VBOBuffer*self.vertByteCount, None, GL_STATIC_DRAW_ARB)

            self.offset = 0

            for layer in self.layers:
                for img in self.images[layer]:
                    img.offset = int(float(self.offset)/self.vertByteCount*4)
                    VBOData = img.getVBOData()

                    glBufferSubDataARB(GL_ARRAY_BUFFER_ARB, self.offset, self.vertByteCount, VBOData)
                    self.offset += self.vertByteCount
            
            self.calculateVBOList()

        else:
            image.offset = int(float(self.offset)/self.vertByteCount*4)
            VBOData = image.getVBOData()

            glBufferSubDataARB(GL_ARRAY_BUFFER_ARB, self.offset, self.vertByteCount, VBOData)
            self.offset += self.vertByteCount

        glBindBuffer(GL_ARRAY_BUFFER_ARB, 0)

    def deleteImage(self, image):
        '''
        Decreases the reference count of the texture by one, and deletes it if nothing is using it anymore
        '''

        self.qimages[image.imagepath][2] -= 1

        if self.qimages[image.imagepath][2] <= 0:
            glDeleteTextures(image.textureId)

        self.images[image.layer].remove(image)

        if self.vbos:
            self.calculateVBOList(image, True)

    def drawImage(self, image):
        global mod

        if image.hidden:
            return

        x, y, w, h = image.textureRect
        dx, dy, dw, dh = image.drawRect

        cx, cy = self.camera

        # Culling
        if (dx * self.zoom > self.w - cx) or (dy * self.zoom > self.h - cy) or ((dx + dw) * self.zoom < 0-cx) or ((dy + dh) * self.zoom < 0-cy):
            return

        if mod:
            glmod.drawTexture(image.textureId, dx, dy, dw, dh, x, y, w, h)
        else:
            self.drawTexture(image.textureId, dx, dy, dw, dh, x, y, w, h)

    def drawTexture(self, texture, dx, dy, dw, dh, x, y, w, h):
        '''
        texture is an int
        textureRect is a list of size 4, determines which square to take from the texture
        drawRect is a list of size 4, is used to determine the drawing size
        '''

        glBindTexture(self.texext, texture)

        glBegin(GL_QUADS)
        #Top-left vertex (corner)
        glTexCoord2f(x, y+h) #image/texture
        glVertex3f(dx, dy, 0) #screen coordinates

        #Bottom-left vertex (corner)
        glTexCoord2f(x+w, y+h)
        glVertex3f((dx+dw), dy, 0)

        #Bottom-right vertex (corner)
        glTexCoord2f(x+w, y)
        glVertex3f((dx+dw), (dy+dh), 0)

        #Top-right vertex (corner)
        glTexCoord2f(x, y)
        glVertex3f(dx, (dy+dh), 0)
        glEnd()
        
    def calculateVBOList(self, image = None, delete = False):
        '''
        Create the VBO list to be passed on to the module for drawing
        or if the change is only one image, modify it.
        '''
        if len(self.layers) > 0 and image != None:
            if delete:
                #print "setLayer"
                temp = [self.layers.index(image.layer)]
                for img in self.images[image.layer]:
                    if img.hidden or img == image:
                        continue
                    temp.append(int(img.textureId))
                    temp.append(img.offset)
                glmod.setVBOlayer(tuple(temp))
            elif image.createLayer:
                layer = self.layers.index(image.layer)
                glmod.insertVBOlayer((layer, int(image.textureId), image.offset))
                #print "addLayer", (layer, image.textureId, image.offset)
                image.createLayer = False
            else:
                layer = self.layers.index(image.layer)
                #print "addEntry", (layer, image.textureId, image.offset)
                glmod.addVBOentry((layer, int(image.textureId), image.offset))
            return

        vbolist = []
        for layer in self.layers:
            temp = []
            for img in self.images[layer]:
                if img.hidden:
                    continue
                temp.append(img.textureId)
                temp.append(img.offset)
            vbolist.append(tuple(temp))

        if len(vbolist) > 2:
            #print "setVBO", vbolist
            glmod.setVBO(tuple(vbolist))

    def hideImage(self, image, hide):
        '''
        This function should only be called from image.py
        Use Image.hide() instead.
        '''
        if self.vbos:
            self.calculateVBOList(image, hide)
            
    def setLayer(self, image, newLayer):
        '''
        This function should only be called from image.py
        Use Image.layer instead.
        '''
        if self.vbos:
            self.calculateVBOList(image, True)
            image._layer = newLayer
            if newLayer not in self.images:
                self.images[newLayer] = []
                self.layers = self.images.keys()
                self.layers.sort()
                image.createLayer = True
            self.calculateVBOList(image)
            
    def getImageSize(self, image):
    
        qimg = None
        if image in self.qimages:
            qimg = self.qimages[image][0]
        else:
            qimg = QImage(qimagepath)
        
        return qimg.size()
        
    def addText(self, text, pos):
        self.texts.append([self.textid, text, pos])
        self.textid += 1
        return self.textid - 1
        
    def removeText(self, id):
        i = 0
        for t in self.texts:
            if t[0] == id:
                self.texts.pop(i)
                return
            i += 1
            
    def setTextPos(self, id, pos):
        for t in self.texts:
            if t[0] == id:
                t[2] = pos

    def mouseMoveEvent(self, mouse):
        self.mouseMoveSignal.emit(mouse.pos().x(), mouse.pos().y())
        
        mouse.accept()

    def mousePressEvent(self, mouse):
        button = 0
        
        if self.ctrl:
            print "ctrl pressed1"
            button += 3
        if self.shift:
            button += 6

        if mouse.button() == Qt.LeftButton:
            button += 0
        elif mouse.button() == Qt.RightButton:
            button += 2
        elif mouse.button() == Qt.MidButton:
            button += 1
        self.mousePressSignal.emit(mouse.pos().x(), mouse.pos().y(), button)

        mouse.accept()
        
    def mouseReleaseEvent(self, mouse):
        button = 0
        
        if self.ctrl:
            button += 3
        if self.shift:
            button += 6

        if mouse.button() == Qt.LeftButton:
            button += 0
        elif mouse.button() == Qt.RightButton:
            button += 2
        elif mouse.button() == Qt.MidButton:
            button += 1
        self.mouseReleaseSignal.emit(mouse.pos().x(), mouse.pos().y(), button)

        mouse.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl = True
        if event.key() == Qt.Key_Shift:
            self.shift = True
            
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.ctrl = False
        if event.key() == Qt.Key_Shift:
            self.shift = False

    def wheelEvent(self, mouse):
        oldCoord = [mouse.pos().x(), mouse.pos().y()]
        oldCoord[0] *= float(1)/self.zoom
        oldCoord[1] *= float(1)/self.zoom

        oldCoord2 = self.camera
        oldCoord2[0] *= float(1)/self.zoom
        oldCoord2[1] *= float(1)/self.zoom

        if mouse.delta() < 0:
            self.zoom -= 0.15
        elif mouse.delta() > 0:
            self.zoom += 0.15

        if self.zoom < 0.30:
            self.zoom = 0.30
        elif self.zoom > 4:
            self.zoom = 4

        self.camera[0] = oldCoord2[0] * self.zoom - ((oldCoord[0]*self.zoom)-mouse.pos().x())
        self.camera[1] = oldCoord2[1] * self.zoom - ((oldCoord[1]*self.zoom)-mouse.pos().y())


        mouse.accept()
        
    def leaveEvent(self, event):
        self.ctrl = False
        self.shift = False
