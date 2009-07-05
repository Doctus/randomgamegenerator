export LD_LIBRARY_PATH=.
cp ../qt4/librandom-game-generator.so.1 ./
cp ../src/Bindings/bmainmod.so ./
#python test3.py &
#python test3.py &
python test3.py
unset LD_LIBRARY_PATH
