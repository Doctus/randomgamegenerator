OLD_LD=$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=.
cp ../qt4/librandom-game-generator.so.1 ./
cp ../src/Bindings/_bmainmod.so ./
#python test3.py &> inst3.log &
#python test3.py &> inst2.log &
python rgg.py #&> inst1.log
export LD_LIBRARY_PATH=$OLD_LD
