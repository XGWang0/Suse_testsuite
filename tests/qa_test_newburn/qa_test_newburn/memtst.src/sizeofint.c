/* Jason continues to not use autoconf despite the fact he should. */

#include <stdio.h>

main ()
{
	printf("#define SIZEOF_INT %d\n",sizeof(int));
	exit (0);
}
