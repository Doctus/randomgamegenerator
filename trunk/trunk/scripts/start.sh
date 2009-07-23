OLD_LD=$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=.
cp ../qt4/librandom-game-generator.so.1 ./
cp ../src/Bindings/_bmainmod.so ./
#python test3.py &
#python test3.py &
python test3.py
export LD_LIBRARY_PATH=$OLD_LD
