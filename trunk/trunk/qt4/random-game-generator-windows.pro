# -------------------------------------------------
# Project created by Oipo 2009-05-22
# -------------------------------------------------
QT += opengl gui core
TARGET = random-name-generator
TEMPLATE = app
LIBS = -L../libs -lconfig++
INCPATH = ../include
DEFINES = WINDOWS
SOURCES += ../src/main.cpp \
    ../src/cTilesetManager.cpp \
    ../src/cTileset.cpp \
    ../src/cTileManager.cpp \
    ../src/cTile.cpp \
    ../src/cMap.cpp \
    ../src/cGame.cpp \
    ../src/cCamera.cpp \
    ../src/Widgets/GLWidget.cpp \
    ../src/cEventManager.cpp
HEADERS += ../src/cTilesetManager.h \
    ../src/cTileset.h \
    ../src/cTileManager.h \
    ../src/cTile.h \
    ../src/cMap.h \
    ../src/cGame.h \
    ../src/cCamera.h \
    ../src/Widgets/GLWidget.h \
    ../src/cEventManager.h
FORMS +=
