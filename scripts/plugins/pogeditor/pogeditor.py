from PyQt4 import QtCore, QtGui
from PIL import Image as im
from PIL import ImageQt as imqt
from rggSystem import promptSaveFile, promptLoadFile, promptInteger, promptCoordinates, POG_DIR, PORTRAIT_DIR
import cStringIO

class pogEditScrollArea(QtGui.QScrollArea):
    
    def __init__(self, mainWindow, parentt):
        super(QtGui.QScrollArea, self).__init__(mainWindow)
        self.first = None
        self.parentt = parentt
        
    def mousePressEvent(self, event):
        if self.first is None:
            self.first = (event.x()+self.horizontalScrollBar().value(), event.y()+self.verticalScrollBar().value())
        
    def mouseReleaseEvent(self, event):
        if self.first is not None:
            self.parentt.externalCrop(self.first, (event.x()+self.horizontalScrollBar().value(), event.y()+self.verticalScrollBar().value()))
            self.first = None

class pogEditorWidget(QtGui.QDockWidget):

    def __init__(self, mainWindow):
        super(QtGui.QDockWidget, self).__init__(mainWindow)

        self.setWindowTitle("Pog Editor")
        self.setObjectName("Pog Editor")

        self.currentImage = None
        self.editedImage = None
        
        self.validBorderSizes = [(64, 64), (128, 128)]

        self.scrollarea = pogEditScrollArea(mainWindow, self)

        self.openButton = QtGui.QPushButton("Open File", mainWindow)
        self.connect(self.openButton, QtCore.SIGNAL('clicked()'), self.promptOpenFile)
        self.saveButton = QtGui.QPushButton("Save Pog", mainWindow)
        self.connect(self.saveButton, QtCore.SIGNAL('clicked()'), self.promptSaveFile)
        self.savePortraitButton = QtGui.QPushButton("Save Portrait", mainWindow)
        self.connect(self.savePortraitButton, QtCore.SIGNAL('clicked()'), self.promptSavePortrait)
        self.resetButton = QtGui.QPushButton("Reset Changes", mainWindow)
        self.connect(self.resetButton, QtCore.SIGNAL('clicked()'), self.resetImage)
        self.borderButton = QtGui.QPushButton("Add Pog Border", mainWindow)
        self.connect(self.borderButton, QtCore.SIGNAL('clicked()'), self.addPogBorder)
        self.resizeButton = QtGui.QPushButton("Resize...", mainWindow)
        self.connect(self.resizeButton, QtCore.SIGNAL('clicked()'), self.debugResize)
        #self.cropButton = QtGui.QPushButton("Crop...", mainWindow)
        #self.connect(self.cropButton, QtCore.SIGNAL('clicked()'), self.debugCropPrompt)

        self.layout = QtGui.QGridLayout()
        self.layout.addWidget(self.scrollarea, 0, 0, 1, 3)
        self.layout.addWidget(self.openButton, 1, 0)
        self.layout.addWidget(self.borderButton, 1, 1)
        self.layout.addWidget(self.resizeButton, 1, 2)
        self.layout.addWidget(self.resetButton, 2, 0)
        self.layout.addWidget(self.saveButton, 2, 1)
        self.layout.addWidget(self.savePortraitButton, 2, 2)
        
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.layout)
        self.setAcceptDrops(True)
        self.setWidget(self.widget)
        
        mainWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasImage():
            dat = event.mimeData().imageData()
            img = QtGui.QImage(dat)
            imgbuf = QtCore.QBuffer()
            imgbuf.open(QtCore.QIODevice.ReadWrite)
            img.save(imgbuf, "PNG")
            stringio = cStringIO.StringIO()
            stringio.write(imgbuf.data())
            imgbuf.close()
            stringio.seek(0)
            final = self.openImage(stringio)
            self.newImage(final)
            event.acceptProposedAction()

    def saveImage(self, image, filename):
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
        converted = QtGui.QPixmap.fromImage(converted)
        label = QtGui.QLabel()
        label.setPixmap(converted)
        self.scrollarea.setWidget(label)
        if (converted.height(), converted.width()) not in self.validBorderSizes:
            self.borderButton.setEnabled(False)
        else:
            self.borderButton.setEnabled(True)

    def update(self):
        self.displayImage(self.editedImage)

    #TODO: Implement better editing functionality than these debug functions

    def debugResize(self):
        size = promptCoordinates("Please enter desired image width.", "Please enter desired image height.", 
                                 "Resize", 1, 4096)
        self.editedImage = self.resizeImage(self.editedImage, size)
        self.update()

    def debugCropPrompt(self):
        x = promptInteger("Please enter the left bound of the desired crop area.", "Crop Image", 0, self.editedImage.size[0]-2)
        if x is None: return
        y = promptInteger("Please enter the top bound of the desired crop area.", "Crop Image", 0, self.editedImage.size[1]-2)
        if y is None: return
        w = promptInteger("Please enter the right bound of the desired crop area.", "Crop Image", x+1, self.editedImage.size[0])
        if w is None: return
        h = promptInteger("Please enter the bottom bound of the desired crop area.", "Crop Image", y+1, self.editedImage.size[1])
        if h is None: return
        self.editedImage = self.cropImage(self.editedImage, (x, y, w, h))
        self.update()

def hajimaru(mainwindow):
    widget = pogEditorWidget(mainwindow)
