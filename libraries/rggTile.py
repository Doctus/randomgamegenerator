# -*- coding: utf-8 -*-
#
#Image convenience class
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

from OpenGL.GL import GL_TEXTURE_2D

from libraries.rggConstants import UNICODE_STRING

class tile(object):
	'''
	Class for storing image data, position and some opengl stuff
	'''

	def __init__(self, imagepath, textureRect, drawRect, layer, hidden, dynamicity, glwidget):
		self.imagepath = imagepath
		self.drawRect = drawRect
		self.textureRect = textureRect
		self._layer = layer
		self.dynamicity = dynamicity
		self.textureId = None
		self.offset = None
		self._hidden = hidden
		self.glwidget = glwidget
		self.createLayer = False
		self.destroyed = False
		self.origtextrect = textureRect
		self.rotation = 0.0

		if self.glwidget.texext == GL_TEXTURE_2D:
			origsize = self.glwidget.getImageSize(self.imagepath)
			x = float(textureRect[0])/float(origsize.width())
			y = float(textureRect[1])/float(origsize.height())
			w = float(textureRect[2])/float(origsize.width())
			h = float(textureRect[3])/float(origsize.height())
			self.textureRect = [x, y, w, h]

	def destroy(self):
		if not self.destroyed:
			self.glwidget.deleteImage(self)
			self.destroyed = True
		else:
			print("attempted to destroy an image twice")

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
		if self._layer != newlayer:
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

	def setDrawW(self, w):
		drawRect = list(self.drawRect)
		drawRect[2] = w
		self.setDrawRect(drawRect)

	def setDrawH(self, h):
		drawRect = list(self.drawRect)
		drawRect[3] = h
		self.setDrawRect(drawRect)

	def getW(self):
		return self.drawRect[2]

	def getH(self):
		return self.drawRect[3]

	def width(self):
		return self.drawRect[2]

	def height(self):
		return self.drawRect[3]

	def setRotation(self, rotation):
		self.rotation = rotation

	def setDrawRect(self, drawRect):
		self.drawRect = drawRect

	def displaceDrawRect(self, displacement):
		self.drawRect = list(self.drawRect)
		self.drawRect[0] = self.drawRect[0] + displacement[0]
		self.drawRect[1] = self.drawRect[1] + displacement[1]
		self.setDrawRect(self.drawRect)

	def setTextureRect(self, textureRect):
		self.textureRect = textureRect
		if self.glwidget.texext == GL_TEXTURE_2D:
			origsize = self.glwidget.getImageSize(self.imagepath)
			x = float(textureRect[0])/float(origsize.width())
			y = float(textureRect[1])/float(origsize.height())
			w = float(textureRect[2])/float(origsize.width())
			h = float(textureRect[3])/float(origsize.height())
			self.textureRect = [x, y, w, h]

	def displaceTextureRect(self, displacement):
		if self.glwidget.texext == GL_TEXTURE_2D:
			origsize = self.glwidget.getImageSize(self.imagepath)
			x = float(self.origtextrect[0] + displacement[0])/float(origsize.width())
			y = float(self.origtextrect[1] + displacement[1])/float(origsize.height())
			w = float(self.origtextrect[2])/float(origsize.width())
			h = float(self.origtextrect[3])/float(origsize.height())
			self.textureRect = [x, y, w, h]
		else:
			self.textureRect[0] += displacement[0]
			self.textureRect[1] += displacement[1]

	def __str__(self):
		text = "Image(", self.imagepath, self.drawRect, self.textureRect, self.layer, self.offset, self.textureId, self._hidden, ")"
		return UNICODE_STRING(text)
