moc bMain.h -o moc_bMain.cpp
python configure.py
g++ -shared -pipe -fPIC -O2 -Wall -W -D_REENTRANT -DNDEBUG -DQT_NO_DEBUG -DQT_CORE_LIB -DQT_GUI_LIB -I. -I/usr/include/python2.6 -I/opt/qt4/share/mkspecs/default -I/opt/qt4/include/QtCore -I/opt/qt4/include/QtGui -I/opt/qt4/include -I/opt/X11/include -lpython2.6 -L/opt/qt4/lib -lQtCore -lQtGui ../../qt4/librandom-game-generator.so *.cpp -o bmainmod.so
