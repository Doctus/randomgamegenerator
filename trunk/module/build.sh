g++ -O2 -fomit-frame-pointer -shared -fPIC -I /usr/include/python2.6/ `pkg-config --cflags --libs-only-L x11` glmod.c -lpython2.6 -lGL -o glmod.so
