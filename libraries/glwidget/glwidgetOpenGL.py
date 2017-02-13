# -*- coding: utf-8 -*-
#
#glWidget - Takes care of drawing images
#
#By Oipo (kingoipo@gmail.com)
'''
    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''

from OpenGL.GL import GL_TEXTURE_2D, GL_NEAREST, GL_NEAREST_MIPMAP_NEAREST, glClear, GL_COLOR_BUFFER_BIT
from OpenGL.GL import glPushMatrix, glTranslatef, glScaled, glColor4f, glDisable, glLineWidth
from OpenGL.GL import glBegin, GL_LINES, glColor3f, glVertex2f, glEnd, glVertex2d, glPopMatrix
from OpenGL.GL import glViewport, glMatrixMode, GL_PROJECTION, glLoadIdentity, glOrtho, GL_MODELVIEW
from OpenGL.GL import glHint, GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST, GL_LINEAR, GL_NEAREST_MIPMAP_LINEAR
from OpenGL.GL import GL_LINEAR_MIPMAP_NEAREST, GL_LINEAR_MIPMAP_LINEAR, glGetString, GL_VERSION
from OpenGL.GL import OpenGL, GL_LINE_LOOP, glEnable, GL_MULTISAMPLE, GL_TRUE
from OpenGL.GL import GL_BLEND, GL_DEPTH_TEST, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from OpenGL.GL import glClearColor, glGenTextures, glBindTexture, glTexParameterf
from OpenGL.GL import GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_WRAP_S
from OpenGL.GL import GL_GENERATE_MIPMAP, GL_CLAMP_TO_EDGE, GL_TEXTURE_WRAP_R, GL_TEXTURE_WRAP_T, GL_RGBA
from OpenGL.GL import GL_UNSIGNED_BYTE, GL_QUADS, glVertex3f, glTexCoord2f, glTexParameteri
from OpenGL.GL import glTexImage2D, glGenerateMipmap, glDeleteTextures, glRotatef
from OpenGL.GL.EXT.texture_filter_anisotropic import GL_TEXTURE_MAX_ANISOTROPY_EXT
from OpenGL.extensions import hasGLExtension
from OpenGL.GL.ARB.vertex_buffer_object import GL_STATIC_DRAW_ARB

#Only set these when creating non-development code
OpenGL.ERROR_CHECKING = False
OpenGL.ERROR_LOGGING = False

from math import cos, sin
from os import path
from sys import _getframe

from libraries.rggQt import QGLWidget, pyqtSignal, Qt, QImage
from libraries.rggTile import tile
from libraries.rggSystem import promptSaveFile, signal
from libraries.rggJson import loadString, loadFloat, jsonload
from libraries.rggConstants import BASE_STRING, POG_DIR, SAVE_DIR

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
	keyPressSignal = pyqtSignal(int) #key
	keyReleaseSignal = pyqtSignal(int) #key

	def __init__(self, parent):
		QGLWidget.__init__(self, parent)

		self.setMinimumSize(320, 240)
		self.w = 640
		self.h = 480
		self.images = dict()
		self.allimgs = []
		self.lastMousePos = [0, 0]
		self.camera = [0, 0]
		self.layers = []
		self.zoom = 1
		self.offset = 0
		self.ctrl = False
		self.shift = False
		self.qimages = {}
		self.texext = GL_TEXTURE_2D
		self.lines = dict()
		self.previewLines = dict()
		self.selectionCircles = dict()
		self.rectangles = {1:[]}
		self.error = False
		self.texts = []
		self.textid = 0
		self.logoon = "Off"

		self.setAcceptDrops(True)

		#settings, as used in SAVE_DIR/gfx_settings.rgs
		self.npot = 3
		self.anifilt = 0
		self.magfilter = GL_NEAREST
		self.mipminfilter = GL_NEAREST_MIPMAP_NEAREST
		self.minfilter = GL_NEAREST

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

		glColor4f(1.0, 1.0, 1.0, 1.0)
		for layer in self.layers:
			for img in self.images[layer]:
				self.drawImage(img)

		glDisable(self.texext)
		for layer in self.lines:
			glLineWidth(layer)
			glBegin(GL_LINES)
			for line in self.lines[layer]:
				glColor3f(line[4], line[5], line[6])
				glVertex2f(line[0], line[1])
				glVertex2f(line[2], line[3])
			glEnd()
		for layer in self.previewLines:
			glLineWidth(layer)
			glBegin(GL_LINES)
			for line in self.previewLines[layer]:
				glColor3f(line[4], line[5], line[6])
				glVertex2f(line[0], line[1])
				glVertex2f(line[2], line[3])
			glEnd()
		if -1 in self.selectionCircles:
			glLineWidth(3)
			glColor3f(0.0, 1.0, 0.0)
			for circle in self.selectionCircles[-1]:
				glBegin(GL_LINE_LOOP)
				for r in range(0, 360, 3):
					glVertex2f(circle[0] + cos(r*0.01745329) * circle[2], circle[1] + sin(r*0.01745329) * circle[2])
				glEnd()
		for rectangle in self.rectangles[1]:
			glLineWidth(2)
			glColor3f(rectangle[4], rectangle[5], rectangle[6])
			glBegin(GL_LINE_LOOP)
			glVertex2d(rectangle[0], rectangle[1])
			glVertex2d(rectangle[2], rectangle[1])
			glVertex2d(rectangle[2], rectangle[3])
			glVertex2d(rectangle[0], rectangle[3])
			glEnd()
		glEnable(self.texext)

		glColor4f(1.0, 1.0, 1.0, 1.0)
		for text in self.texts:
			_split = text[1].split("\n")
			brk = lambda x, n, acc=[]: brk(x[n:], n, acc+[(x[:n])]) if x else acc
			split = []
			for item in _split:
				split.extend(brk(item, 35))
			if len(split[0]) == 0:
				split.pop(0)
			pos = -16 * (len(split) - 1)
			for t in split:
				if len(t) == 0:
					continue

				self.renderText(float(text[2][0]), float(text[2][1])+pos, 0, t)
				pos += 16

		glPopMatrix()

	def addSelectionCircle(self, splasifarcity, x, y, radius):
		if not splasifarcity in self.selectionCircles:
			self.selectionCircles[splasifarcity] = []

		self.selectionCircles[splasifarcity].append((float(x), float(y), float(radius)))

	def clearSelectionCircles(self):
		self.selectionCircles.clear()

	def addLine(self, thickness, x, y, w, h, r, g, b):
		if not thickness in self.lines:
			self.lines[thickness] = []

		self.lines[thickness].append((float(x), float(y), float(w), float(h), float(r), float(g), float(b)))

	def deleteLine(self, thickness, x, y, w, h):
		for thickness in self.lines:
			new_list = []
			for line in self.lines[thickness]:
				if not self.pointIntersectRect((line[0], line[1]), (x, y, w, h)) \
					   and not self.pointIntersectRect((line[2], line[3]), (x, y, w, h)):
				   new_list.append(line)
			self.lines[thickness] = new_list

	def addPreviewLine(self, thickness, x, y, w, h, r, g, b):
		if not thickness in self.previewLines:
			self.previewLines[thickness] = []

		self.previewLines[thickness].append((float(x), float(y), float(w), float(h), float(r), float(g), float(b)))

	def clearLines(self):
		self.lines.clear()

	def clearPreviewLines(self):
		self.previewLines.clear()

	def addRectangle(self, x, y, w, h, r, g, b):
		self.rectangles[1].append((float(x), float(y), float(w), float(h), float(r), float(g), float(b)))

	def clearRectangles(self):
		self.rectangles = {1:[]}

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
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		self.w = w
		self.h = h

		if self.logoon == "On":
			if self.logo[0] and len(self.logo) == 5:
				self.logo[4].setDrawRect([0, 0, w, h])

	#ugly conversion function :(
	def interpretString(self, string):
		if string == "GL_NEAREST":
			return GL_NEAREST
		if string == "GL_LINEAR":
			return GL_LINEAR
		if string == "GL_NEAREST_MIPMAP_NEAREST":
			return GL_NEAREST_MIPMAP_NEAREST
		if string == "GL_NEAREST_MIPMAP_LINEAR":
			return GL_NEAREST_MIPMAP_LINEAR
		if string == "GL_LINEAR_MIPMAP_NEAREST":
			return GL_LINEAR_MIPMAP_NEAREST
		if string == "GL_LINEAR_MIPMAP_LINEAR":
			return GL_LINEAR_MIPMAP_LINEAR
		return string

	def initializeGL(self):
		'''
		Initialize GL
		'''

		self.fieldtemp = [1.0, "GL_NEAREST", "GL_NEAREST", "GL_NEAREST_MIPMAP_NEAREST", "On"]

		try:
			js = jsonload(path.join(SAVE_DIR, "gfx_settings.rgs"))
			self.fieldtemp[0] = loadFloat('gfx.anifilt', js.get('anifilt'))
			self.fieldtemp[1] = loadString('gfx.minfilter', js.get('minfilter'))
			self.fieldtemp[2] = loadString('gfx.magfilter', js.get('magfilter'))
			self.fieldtemp[3] = loadString('gfx.mipminfilter', js.get('mipminfilter'))
			self.fieldtemp[4] = loadString('gfx.FSAA', js.get('FSAA'))
		except:
			#print("no settings detected")
			pass

		#mipmap support and NPOT texture support block
		if not hasGLExtension("GL_ARB_framebuffer_object"):
			#print("GL_ARB_framebuffer_object not supported, switching to GL_GENERATE_MIPMAP")
			self.npot = 2
		version = glGetString(GL_VERSION)
		if int(version[0]) == 1 and int(version[2]) < 4: #no opengl 1.4 support
			#print("GL_GENERATE_MIPMAP not supported, not using mipmapping")
			self.npot = 1
		if not hasGLExtension("GL_ARB_texture_rectangle"):
			#print("GL_TEXTURE_RECTANGLE_ARB not supported, switching to GL_TEXTURE_2D")
			self.texext = GL_TEXTURE_2D
			self.npot = 0

		#assorted settings block
		if hasGLExtension("GL_EXT_texture_filter_anisotropic") and self.fieldtemp[0] > 1.0:
			self.anifilt = self.fieldtemp[0]
			#print("using " + str(self.fieldtemp[0]) + "x anisotropic texture filtering. max: " + str(glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)))
		self.minfilter = self.interpretString(self.fieldtemp[1])
		self.magfilter = self.interpretString(self.fieldtemp[2])
		self.mipminfilter = self.interpretString(self.fieldtemp[3])
		if self.mipminfilter == "Off":
			self.mipminfilter = -1
		if self.format().sampleBuffers() and self.fieldtemp[4] == "On":
			#print("enabling "  + str(self.format().samples()) + "x FSAA")
			glEnable(GL_MULTISAMPLE)
		else:
			pass
			#print("FSAA not supported and/or disabled")

		glEnable(self.texext)
		glEnable(GL_BLEND)
		glDisable(GL_DEPTH_TEST)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glViewport(0, 0, self.width(), self.height())
		glClearColor(0.0, 0.0, 0.0, 0.0)

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
			#print("created", qimagepath)

		if textureRect[2] == -1:
			textureRect[2] = qimg.width()

		if textureRect[3] == -1:
			textureRect[3] = qimg.height()

		if drawRect[2] == -1:
			drawRect[2] = qimg.width()

		if drawRect[3] == -1:
			drawRect[3] = qimg.height()

		image = tile(qimagepath, textureRect, drawRect, layer, hidden, dynamicity, self)

		if found == False:
			img = None
			if self.npot == 0:
				w = nextPowerOfTwo(qimg.width())
				h = nextPowerOfTwo(qimg.height())
				if w != qimg.width() or h != qimg.height():
					img = self.convertToGLFormat(qimg.scaled(w, h))
				else:
					img = self.convertToGLFormat(qimg)
			else:
				img = self.convertToGLFormat(qimg)

			texture = int(glGenTextures(1))
			try:
				imgdata = img.bits().asstring(img.byteCount())
			except Exception as e:
				print(e)
				print("requested to create", qimagepath, layer, textureRect, drawRect, hidden)
				for x in [0, 1, 2, 3]:
					f_code = _getframe(x).f_code #really bad hack to get the filename and number
					print("Doing it wrong in " + f_code.co_filename + ":" + str(f_code.co_firstlineno))
					print("Error: " + e)

			#print("created texture", texture)

			glBindTexture(self.texext, texture)

			if self.anifilt > 1.0:
				glTexParameterf(self.texext, GL_TEXTURE_MAX_ANISOTROPY_EXT, self.anifilt)
			if self.npot == 3 and self.mipminfilter != -1:
				glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, self.mipminfilter)
				glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, self.magfilter)
			elif self.npot == 2 and self.mipminfilter != -1:
				glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, self.mipminfilter)
				glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, self.magfilter)
				glTexParameteri(self.texext, GL_GENERATE_MIPMAP, GL_TRUE)
			else:
				glTexParameteri(self.texext, GL_TEXTURE_MIN_FILTER, self.minfilter)
				glTexParameteri(self.texext, GL_TEXTURE_MAG_FILTER, self.magfilter)

			glTexParameteri(self.texext, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
			glTexParameteri(self.texext, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
			glTexParameteri(self.texext, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

			glTexImage2D(self.texext, 0, GL_RGBA, img.width(), img.height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imgdata);

			if self.npot == 3 and self.mipminfilter != -1:
				glEnable(GL_TEXTURE_2D)
				glGenerateMipmap(GL_TEXTURE_2D)

			self.qimages[qimagepath] = [qimg, texture, 1] #texture, reference count
		else:
			self.qimages[qimagepath][2] += 1

		image.textureId = texture

		if layer not in self.images:
			self.images[layer] = []
			self.layers = list(self.images.keys())
			self.layers.sort()
			image.createLayer = True

		self.images[layer].append(image)
		self.allimgs.append(image)

		return image

	def deleteImage(self, image):
		'''
		Decreases the reference count of the texture by one, and deletes it if nothing is using it anymore
		'''

		self.qimages[image.imagepath][2] -= 1

		if self.qimages[image.imagepath][2] <= 0:
			#print("deleting texture", image.textureId)
			glDeleteTextures(image.textureId)
			del self.qimages[image.imagepath]

		self.images[image.layer].remove(image)
		self.allimgs.remove(image)

		image = None

	def deleteImages(self, imageArray):
		'''
		Decreases the reference count of the texture of each image by one, and deletes it if nothing is using it anymore
		'''

		for image in imageArray:
			self.qimages[image.imagepath][2] -= 1

			if self.qimages[image.imagepath][2] <= 0:
				#print("deleting texture", image.textureId)
				glDeleteTextures(image.textureId)
				del self.qimages[image.imagepath]

			self.images[image.layer].remove(image)
			self.allimgs.remove(image)

	def drawImage(self, image):

		if image.hidden:
			return

		x, y, w, h = image.textureRect
		dx, dy, dw, dh = image.drawRect
		r = float(image.rotation)

		cx, cy = self.camera

		# Culling
		if (dx * self.zoom > self.w - cx) or (dy * self.zoom > self.h - cy) or ((dx + dw) * self.zoom < 0-cx) or ((dy + dh) * self.zoom < 0-cy):
			return

		self.drawTexture(image.textureId, dx, dy, dw, dh, x, y, w, h, r)

	def drawTexture(self, texture, dx, dy, dw, dh, x, y, w, h, r):
		'''
		texture is an int
		textureRect is a list of size 4, determines which square to take from the texture
		drawRect is a list of size 4, is used to determine the drawing size
		'''

		glBindTexture(self.texext, texture)

		glPushMatrix()
		glTranslatef(dx+dw/2, dy+dh/2, 0)
		glRotatef(r, 0, 0, 1.0)
		glTranslatef(-1*(dx+dw/2), -1*(dy+dh/2), 0)

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

		glPopMatrix()

	def hideImage(self, image, hide):
		'''
		This function should only be called from image.py
		Use Image.hide() instead.
		'''
		pass

	def setLayer(self, image, newLayer):
		'''
		This function should only be called from image.py
		Use Image.layer instead.
		'''

		oldLayer = image._layer
		image._layer = newLayer
		if newLayer not in self.images:
			self.images[newLayer] = []
			self.layers = list(self.images.keys())
			self.layers.sort()
			image.createLayer = True

		self.images[oldLayer].remove(image)
		self.images[newLayer].append(image)

	def getImageSize(self, image):
		qimg = None

		if image in self.qimages:
			qimg = self.qimages[image][0]
		else:
			qimg = QImage(image)

		return qimg.size()

	def addText(self, text, pos):
		self.texts.append([self.textid, text, pos])
		self.textid += 1
		return self.textid - 1

	def removeText(self, id):
		for i, t in enumerate(self.texts):
			if t[0] == id:
				self.texts.pop(i)
				return

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
		elif event.key() == Qt.Key_Shift:
			self.shift = True
		elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
			self.zoom += 0.15
			if self.zoom > 4:
				self.zoom = 4
		elif event.key() == Qt.Key_Minus:
			self.zoom -= 0.15
			if self.zoom < 0.30:
				self.zoom = 0.30
		elif event.key() == Qt.Key_0:
			self.zoom = 1
		elif event.key() == Qt.Key_Up:
			self.camera[1] += (50 * self.zoom)
		elif event.key() == Qt.Key_Down:
			self.camera[1] -= (50 * self.zoom)
		elif event.key() == Qt.Key_Left:
			self.camera[0] += (50 * self.zoom)
		elif event.key() == Qt.Key_Right:
			self.camera[0] -= (50 * self.zoom)
		else:
			self.keyPressSignal.emit(event.key())

	def keyReleaseEvent(self, event):
		if event.key() == Qt.Key_Control:
			self.ctrl = False
		elif event.key() == Qt.Key_Shift:
			self.shift = False
		else:
			self.keyReleaseSignal.emit(event.key())

	def wheelEvent(self, mouse):
		oldCoord = [mouse.pos().x(), mouse.pos().y()]
		oldCoord[0] *= float(1)/self.zoom
		oldCoord[1] *= float(1)/self.zoom

		oldCoord2 = self.camera
		oldCoord2[0] *= float(1)/self.zoom
		oldCoord2[1] *= float(1)/self.zoom

		try:
			delta = mouse.angleDelta().y() #let's not worry about 2-dimensional wheels.
		except AttributeError:
			delta = mouse.delta()

		if delta < 0:
			self.zoom -= 0.5
		elif delta > 0:
			self.zoom += 0.5

		if self.zoom < 0.60:
			self.zoom = 0.5
		elif self.zoom > 4:
			self.zoom = 4

		self.camera[0] = oldCoord2[0] * self.zoom - ((oldCoord[0]*self.zoom)-mouse.pos().x())
		self.camera[1] = oldCoord2[1] * self.zoom - ((oldCoord[1]*self.zoom)-mouse.pos().y())


		mouse.accept()

	def leaveEvent(self, event):
		self.ctrl = False
		self.shift = False

	def dragEnterEvent(self, event):
		if event.mimeData().hasImage():
			event.acceptProposedAction()
		elif event.mimeData().hasText():
			event.acceptProposedAction()

	def dropEvent(self, event):
		if event.mimeData().hasImage():
			dat = event.mimeData().imageData()
			img = QImage(dat)
			filename = promptSaveFile('Save Pog', 'Pog files (*.png)', POG_DIR)
			if filename is not None:
				img.save(filename, "PNG")
			event.acceptProposedAction()
		elif event.mimeData().hasText():
			self.pogPlace.emit(event.pos().x(), event.pos().y(), str(event.mimeData().text()))

	pogPlace = signal(int, int, BASE_STRING, doc=
		"""Called to request pog placement on the map."""
	)
