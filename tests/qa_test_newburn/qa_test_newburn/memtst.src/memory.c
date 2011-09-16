#include <stdio.h>
#include <stdlib.h>
#include "memory.h"

#define LINESIZE 1024

void meminfo( struct memory *m ) {
  FILE *f;
  char line[LINESIZE];
  int got_total_mem = 0;
  int got_total_swap = 0;

  f = fopen("/proc/meminfo", "r");

  while (fgets(line, LINESIZE-1, f) != NULL) {
	  unsigned long tmp;

	  if (sscanf(line, "MemTotal: %lu", &tmp) == 1) {
		  m->total_mem = tmp * 1024;
		  got_total_mem = 1;
	  } else if (sscanf(line, "SwapTotal: %lu", &tmp) == 1) {
		  m->total_swap = tmp * 1024;
		  got_total_swap = 1;
	  }
  }
  fclose(f);

  if (!got_total_mem || !got_total_swap) {
	  fprintf(stderr, "failed to get meminfo\n");
	  exit(1);
  }

  printf("mem: %lu swap:%lu\n", m->total_mem, m->total_swap);
}

