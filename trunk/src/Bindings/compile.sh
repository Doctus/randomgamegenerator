moc bMain.h -o moc_bMain.cpp
python configure.py
g++ -shared -pipe -fPIC -O2 -Wall -g3 -ggdb -W -D_REENTRANT -DNDEBUG -DQT_NO_DEBUG -DQT_CORE_LIB -DQT_GUI_LIB -I. -I/usr/include/python2.6 -lpython2.6 `pkg-config --cflags --libs QtGui` `pkg-config --cflags gl` ../../qt4/librandom-game-generator.so *.cpp -o bmainmod.so
