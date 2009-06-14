# -------------------------------------------------
# Project created by QtCreator 2009-04-30T16:15:26
# -------------------------------------------------
QT += opengl \
    network
TARGET = random-game-generator
TEMPLATE = app
LIBS = -lconfig++ \
    -lconfuse
SOURCES += ../src/main.cpp \
    ../src/cTilesetManager.cpp \
    ../src/cTileset.cpp \
    ../src/cTileManager.cpp \
    ../src/cTile.cpp \
    ../src/cMap.cpp \
    ../src/cGame.cpp \
    ../src/cCamera.cpp \
    ../src/Widgets/wGLWidget.cpp \
    ../src/Widgets/wMenuBar.cpp \
    ../src/Widgets/wDockWidgets.cpp \
    ../src/Network/nConnection.cpp \
    ../src/Network/nConnectionManager.cpp
HEADERS += ../src/cTilesetManager.h \
    ../src/cTileset.h \
    ../src/cTileManager.h \
    ../src/cTile.h \
    ../src/cMap.h \
    ../src/cGame.h \
    ../src/cCamera.h \
    ../src/Widgets/wGLWidget.h \
    ../src/Widgets/wMenuBar.h \
    ../src/Widgets/wDockWidgets.h \
    ../src/Network/nConnection.h \
    ../src/Network/nConnectionManager.h
FORMS += 
