g++ -O2 -fomit-frame-pointer -shared -fPIC `pkg-config --cflags --libs-only-L x11 python gl` glmod.c  -o glmod.so
