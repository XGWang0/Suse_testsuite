all: simple

simple.o: simple.c
	gcc -c simple.c

simple: simple.o
	gcc -o simple simple.o

clean:
	rm -f simple.o

distclean: clean
	rm -f simple

install: all
	cp simple ../../data/file-access-acl/

