# -------------------------------------------------
# Project created by QtCreator 2009-04-30T16:15:26
# -------------------------------------------------
QT += core
#QT =
TARGET = bmainmod
TEMPLATE = lib
DEFINES = _WINDOWS
CONFIG += release dll

INCLUDEPATH += C:\Python26\lib\site-packages\PyQt4\include \
C:\Python26\include \
F:\Programming\randomgamegenerator\trunk\src\Bindings \

QMAKE_LIBDIR += C:\Python26\libs \
F:\Programming\randomgamegenerator\trunk\qt4\release

LIBS += -lrandom-game-generator \
-lpython26

SOURCES +=  ../src/Bindings/bMain.cpp \
../src/Bindings/bImage.cpp \
../src/Bindings/sipbmainmodbImage.cpp \
../src/Bindings/sipbmainmodbMain.cpp \
../src/Bindings/sipbmainmodcmodule.cpp

HEADERS += ../src/Bindings/bMain.h \
../src/Bindings/bImage.h \
../src/Bindings/sipAPIbmainmod.h
