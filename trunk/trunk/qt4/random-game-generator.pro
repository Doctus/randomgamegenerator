# -------------------------------------------------
# Project created by QtCreator 2009-04-30T16:15:26
# -------------------------------------------------
QT += opengl \
    network
TARGET = random-game-generator
TEMPLATE = lib
CONFIG += release
TRANSLATIONS = rgg_nl.ts \
    rgg_ja.ts
CODECFORTR = UTF-8
CODECFORSRC = UTF-8
SOURCES += ../src/cTilesetManager.cpp \
    ../src/cTileset.cpp \
    ../src/cGame.cpp \
    ../src/cCamera.cpp \
    ../src/cShapeManager.cpp \
    ../src/Widgets/wGLWidget.cpp \
    ../src/Widgets/wAction.cpp
HEADERS += ../src/cTilesetManager.h \
    ../src/cTileset.h \
    ../src/cGame.h \
    ../src/cCamera.h \
    ../src/cShapeManager.h \
    ../src/Widgets/wGLWidget.h \
    ../src/Widgets/wAction.h
