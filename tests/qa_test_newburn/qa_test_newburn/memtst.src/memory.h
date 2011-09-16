#ifndef MEMORY_H
#define MEMORY_H

struct memory {
	unsigned long total_mem;
	
	unsigned long total_swap;
};

void meminfo( struct memory * );

#endif
