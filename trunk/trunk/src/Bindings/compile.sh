echo "removing previously created files"
rm -f moc_bMain.cpp sip* *.o

if [ -f /usr/bin/moc-qt4 ]
then
	moc-qt4 bMain.h -o moc_bMain.cpp
else
	moc bMain.h -o moc_bMain.cpp
fi

echo "creating new files"
python configure.py

DEFINES="-DQT_NO_DEBUG -DNDEBUG -W -D_REENTRANT -DQT_CORE_LIB -DQT_GUI_LIB"
CFLAGS="-pipe -fPIC -O2 -Wall -march=native -fomit-frame-pointer"
FILES="*.cpp"
for file in $FILES; do
  output=`echo $file | sed 's/.cpp/.o/'`
  echo "compiling $file into $output"
  g++ -c $CFLAGS $DEFINES -I. -I/usr/include/python2.6 `pkg-config --cflags QtGui` `pkg-config --cflags gl` $file -o $output
done

g++ -shared $CFLAGS $DEFINES -lpython2.6 `pkg-config --libs QtGui` `pkg-config --libs gl` ../../qt4/librandom-game-generator.so *.o -o _bmainmod.so
