# -------------------------------------------------
# Project created by QtCreator 2009-04-30T16:15:26
# -------------------------------------------------
QT += core
#QT =
TARGET = bmainmod
TEMPLATE = lib
CONFIG += release dll

INCLUDEPATH += C:\Python26\lib\site-packages\PyQt4\include \
C:\Python26\include \
F:\Programming\randomgamegenerator\trunk\src\Bindings \

QMAKE_LIBDIR += C:\Python26\libs2 \
F:\Programming\randomgamegenerator\trunk\qt4\release \
C:\Python26\DLLs

LIBS += -lrandom-game-generator \
-lpython26

SOURCES +=  ../src/Bindings/bMain.cpp \
../src/Bindings/bImage.cpp \
../src/Bindings/sip_bmainmodbImage.cpp \
../src/Bindings/sip_bmainmodbMain.cpp \
../src/Bindings/sip_bmainmodcmodule.cpp \
../src/Bindings/sip_bmainmodQVector.cpp

HEADERS += ../src/Bindings/bMain.h \
../src/Bindings/bImage.h \
../src/Bindings/sipAPI_bmainmod.h
