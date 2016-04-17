try:
	from PIL import Image as im
	from PIL import ImageQt as imqt
	AVAILABLE = True
except:
	im = None
	imqt = None
	AVAILABLE = False
from libraries.rggConstants import POG_DIR, PORTRAIT_DIR
from libraries.rggQt import QScrollArea, QDockWidget, QPushButton, QGridLayout, SIGNAL, QImage
from libraries.rggQt import QBuffer, Qt, QWidget, QIODevice, QPixmap, QLabel, QPoint, QMenu, QAction
from libraries.rggSystem import promptSaveFile, promptLoadFile, promptInteger, promptCoordinates
import cStringIO

class pogEditScrollArea(QScrollArea):

	def __init__(self, mainWindow, parentt):
		super(QScrollArea, self).__init__(mainWindow)
		self.first = None
		self.parentt = parentt

	def mousePressEvent(self, event):
		if self.first is None:
			self.first = (event.x()+self.horizontalScrollBar().value(), event.y()+self.verticalScrollBar().value())

	def mouseReleaseEvent(self, event):
		if self.first is not None:
			self.parentt.externalCrop(self.first, (event.x()+self.horizontalScrollBar().value(), event.y()+self.verticalScrollBar().value()))
			self.first = None

class pogEditorWidget(QDockWidget):

	def __init__(self, mainWindow):
		super(QDockWidget, self).__init__(mainWindow)

		self.setWindowTitle("Pog Editor")
		self.setObjectName("Pog Editor")

		self.currentImage = None
		self.editedImage = None

		self.validBorderSizes = [(64, 64), (128, 128), (256, 256)]

		self.scrollarea = pogEditScrollArea(mainWindow, self)

		self.openButton = QPushButton("Open File", mainWindow)
		self.connect(self.openButton, SIGNAL('clicked()'), self.promptOpenFile)
		self.saveButton = QPushButton("Save Pog", mainWindow)
		self.connect(self.saveButton, SIGNAL('clicked()'), self.promptSaveFile)
		self.savePortraitButton = QPushButton("Save Portrait", mainWindow)
		self.connect(self.savePortraitButton, SIGNAL('clicked()'), self.promptSavePortrait)
		self.resetButton = QPushButton("Reset Changes", mainWindow)
		self.connect(self.resetButton, SIGNAL('clicked()'), self.resetImage)
		self.borderButton = QPushButton("Add Pog Border", mainWindow)
		self.connect(self.borderButton, SIGNAL('clicked()'), self.addPogBorder)
		self.resizeButton = QPushButton("Resize...", mainWindow)
		self.connect(self.resizeButton, SIGNAL('clicked()'), self.promptResize)

		self.layout = QGridLayout()
		self.layout.addWidget(self.scrollarea, 0, 0, 1, 3)
		self.layout.addWidget(self.openButton, 1, 0)
		self.layout.addWidget(self.borderButton, 1, 1)
		self.layout.addWidget(self.resizeButton, 1, 2)
		self.layout.addWidget(self.resetButton, 2, 0)
		self.layout.addWidget(self.saveButton, 2, 1)
		self.layout.addWidget(self.savePortraitButton, 2, 2)

		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.setAcceptDrops(True)
		self.setWidget(self.widget)

		mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)

	def dragEnterEvent(self, event):
		if event.mimeData().hasImage():
			event.acceptProposedAction()

	def dropEvent(self, event):
		if event.mimeData().hasImage():
			dat = event.mimeData().imageData()
			img = QImage(dat)
			imgbuf = QBuffer()
			imgbuf.open(QIODevice.ReadWrite)
			img.save(imgbuf, "PNG")
			stringio = cStringIO.StringIO()
			stringio.write(imgbuf.data())
			imgbuf.close()
			stringio.seek(0)
			final = self.openImage(stringio)
			self.newImage(final)
			event.acceptProposedAction()

	def saveImage(self, image, filename):
		if ".png" not in filename: #Linux issue workaround
			image.save(filename+'.png', "PNG", transparency=((254, 0, 254)))
		else:
			image.save(filename, "PNG", transparency=((254, 0, 254)))

	def openImage(self, path):
		image = im.open(path)
		image = image.convert("RGB")
		return image

	def poggifyImage(self, image):
		if image.size == (64, 64):
			overlay = im.open("data/pog_circle_64.png")
		elif image.size == (128, 128):
			overlay = im.open("data/pog_circle_128.png")
		elif image.size == (256, 256):
			overlay = im.open("data/pog_circle_256.png")
		else:
			raise NotImplementedError("Cannot create pogs of size " + str(image.size))

		image.paste(overlay, None, overlay)

		olddat = image.getdata()
		newdat = []
		for pixel in olddat:
			if pixel[0:3] == (254, 0, 254):
				newdat.append((254, 0, 254, 255))
			else:
				newdat.append(pixel)
		image.putdata(newdat)

		return image

	def resizeImage(self, image, newsize):
		return image.resize(newsize, im.ANTIALIAS)

	def addPogBorder(self):
		self.editedImage = self.poggifyImage(self.editedImage)
		self.update()

	def cropImage(self, image, bounds):
		return image.crop(bounds)

	def externalCrop(self, boundA, boundB):
		if self.editedImage is None:
			return
		bounds = (min(boundA[0], boundB[0]), min(boundA[1], boundB[1]),
						 max(boundA[0], boundB[0]), max(boundA[1], boundB[1]))
		self.editedImage = self.cropImage(self.editedImage, bounds)
		self.update()

	def resetImage(self):
		self.editedImage = self.currentImage
		self.update()

	def newImage(self, image):
		self.currentImage = image
		self.editedImage = self.currentImage
		self.update()

	def promptOpenFile(self):
		filename = promptLoadFile('Open Image', 'Image files (*.png *.jpg *.jpeg *.bmp *.gif *.tga)', POG_DIR)
		if filename is not None:
			image = self.openImage(filename)
			self.newImage(image)

	def promptSaveFile(self):
		filename = promptSaveFile('Save Pog', 'Pog files (*.png)', POG_DIR)
		if filename is not None:
			self.saveImage(self.editedImage, filename)

	def promptSavePortrait(self):
		filename = promptSaveFile('Save Portrait', 'Portrait files (*.png)', PORTRAIT_DIR)
		if filename is not None:
			self.saveImage(self.editedImage, filename)

	def displayImage(self, image):
		converted = imqt.ImageQt(image)
		converted = converted.copy()
		converted = QPixmap.fromImage(converted)
		label = QLabel()
		label.setPixmap(converted)
		self.scrollarea.setWidget(label)
		if (converted.height(), converted.width()) not in self.validBorderSizes:
			self.borderButton.setEnabled(False)
		else:
			self.borderButton.setEnabled(True)

	def update(self):
		self.displayImage(self.editedImage)

	def promptResize(self):
		sizesMenu = QMenu()
		sizeResults = {}
		for size in self.validBorderSizes:
			action = QAction("%s x %s"%(size[0], size[1]), self)
			sizeResults[action.text()] = size
			sizesMenu.addAction(action)
		result = sizesMenu.exec_(self.resizeButton.mapToGlobal(QPoint(0,0)))
		if result:
			size = sizeResults[result.text()]
			self.editedImage = self.resizeImage(self.editedImage, size)
			self.update()
