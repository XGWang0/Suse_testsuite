all:
	gcc -D_FILE_OFFSET_BITS=64 -DVERSION=\"3.1p0\" -Dstrlcpy=strncpy -Darc4random=rand -O2 src/iogen.c -o iogen
	nroff -mandoc -Tascii src/iogen.8 > iogen.cat8
clean:
	rm -rf iogen.cat8 iogen
install:
	cp iogen /usr/bin/
	@echo "you figure out where the man page goes"
uninstall:
	rm -rf /usr/bin/iogen
