#
#
#
MEMTST_CFLAGS=$(CFLAGS) -fno-unroll-loops -fno-unroll-all-loops

all: memtst maxalloc;

memtst_main: memtst;

sizeofint: ;
	$(CC) sizeofint.c -o sizeofint

sizeofint.h: sizeofint ;
	sh -c "./sizeofint > sizeofint.h"

maxalloc: sizeofint.h ;
	$(CC) -Wall maxalloc.c -o maxalloc

memtst: sizeofint.h ;
	$(CC) $(MEMTST_CFLAGS) -c memory.c -o memory.o
	$(CC) $(MEMTST_CFLAGS) -c memtst.c -o memtst.o
	$(CC) $(MEMTST_CFLAGS)  memtst_main.c memory.o memtst.o -o memtst

clean:
	rm -f *.o memtst maxalloc sizeofint.h sizeofint

