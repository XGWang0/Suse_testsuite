/* maxalloc.c: print maximum number of megabytes we can allocate. */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>
#include <math.h>
#include <malloc.h>
#include "memory.h"

void maxalloc(int ceiling, int attempts) {
	unsigned nint;
	int *buf;
	int a;
	unsigned nint_search;
	nint=(ceiling*(1024*1024 / sizeof(int)));
	nint_search = nint * 0.5;
	a=attempts;

	/* while we've not reached maximum attempts and while the attempts
	   aren't yet pointless */
	while((--a) > 0 && nint_search > (1000 / sizeof(int) / 2)) {
		if ((buf = (int *) malloc(nint*sizeof(int))) != NULL) {
			free(buf);
			if (a == attempts - 1) {
				break;
			}
			if (a > 1 && nint_search * .5 > (1000/sizeof(int)/2)) {
				nint = nint + nint_search;
			}
		} else {
			if (nint_search > nint) {
				nint=0;
			} else {
				nint = nint - nint_search;
			}
		}
		nint_search = nint_search * .5;
	}
	printf("%d\n", (int) (sizeof(int) * (nint / (1024*1024))));
}

int main(int argc, char **argv) {
        if (argc > 1) {
                maxalloc((int) strtol(argv[1],NULL,0), 30);
	} else {
		maxalloc(4000,30);
        }
        return 0;
}
