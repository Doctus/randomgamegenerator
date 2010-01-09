rm moc_bMain.cpp sip*

if [ -f /usr/bin/moc-qt4 ]
then
	moc-qt4 bMain.h -o moc_bMain.cpp
else
	moc bMain.h -o moc_bMain.cpp
fi

python configure.py
#g++ -shared -pipe -fPIC -O2 -Wall -g3 -ggdb -W -D_REENTRANT -DQT_CORE_LIB -DQT_GUI_LIB -I. -I/usr/include/python2.6 -lpython2.6 `pkg-config --cflags --libs QtGui` `pkg-config --cflags gl` ../../qt4/librandom-game-generator.so *.cpp -o _bmainmod.so
g++ -shared -pipe -fPIC -O2 -Wall  -DQT_NO_DEBUG -DNDEBUG -W -D_REENTRANT -DQT_CORE_LIB -DQT_GUI_LIB -I. -I/usr/include/python2.6 -lpython2.6 `pkg-config --cflags --libs QtGui` `pkg-config --cflags gl` ../../qt4/librandom-game-generator.so *.cpp -o _bmainmod.so
