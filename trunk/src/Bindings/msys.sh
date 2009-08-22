
# Contents will change a lot if versions are changed

/c/Qt/2009.03/qt/bin/moc bMain.h -o moc_bMain.cpp
/c/Python26/python.exe configure.py
echo 'compiling...'
g++ -shared -O2 -Wall -DQT_NO_DEBUG -DNDEBUG -W -D_REENTRANT -DQT_CORE_LIB -DQT_GUI_LIB -DQT_SHARED -I. -L/c/Python26/libs -L/c/Qt/2009.03/qt/lib -I/c/Python26 -I/c/Qt/2009.03/qt/include -I/c/Qt/2009.03/qt/include/qt -I/c/Qt/2009.03/qt/include/QtCore -I/c/Python26/include -I/c/Python26/Lib/site-packages/PyQt4/include *.cpp ../../qt4/release/librandom-game-generator.a -lpython26 -lQtCore4 -lQtGui4 -o _bmainmod.pyd
