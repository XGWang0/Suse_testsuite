#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/time.h>
#define KB 1024
#define MB (KB * 1024)
#define GB (MB * 1024)
#define PAGE_SIZE (4 * KB)
#define AREA_SIZE (100 * MB)
/* This limits the max allocated memory to 100 GB */
#define MAX_AREAS 1000

int timeval_sub(struct timeval *start, struct timeval *end, struct timeval *sub)
{
    sub->tv_sec = end->tv_sec - start->tv_sec;
    if ((sub->tv_usec = end->tv_usec - start->tv_usec) < 0) {
        sub->tv_sec--;
        sub->tv_usec += 1000000;
    }
    return 0;
}

char *random_page;
int main(int argc, char **argv)
{
	char **areas;
	long int i, j, k;
	char *p;
	unsigned long num_areas = 0;
	volatile char v;
	int min_compress = 0;
	int max_compress = 100;
	int rng_compress;
    struct timeval start;
    struct timeval end;
    struct timeval sub;
	random_page = malloc(PAGE_SIZE);
	for (i = 0; i < PAGE_SIZE; i++)
		random_page[i] = random();
	if (argc >= 2) {
		num_areas = atoi(argv[1]) / 100;
		printf("Will allocate up to %d MB\n", num_areas * 100);
	}
	if (argc < 2 || num_areas == 0) {
		printf
		    ("Number of megabytes not given or zero, trying up to %d\n",
		     MAX_AREAS * 100);
		num_areas = MAX_AREAS;
	}
	if (argc >= 3)
		min_compress = atoi(argv[2]);
	if (argc >= 4)
		max_compress = atoi(argv[3]);
	printf
	    ("The memory will be compressible to roughly between %d and %d %% of original size\n",
	     min_compress, max_compress);
	rng_compress = ((max_compress - min_compress) * PAGE_SIZE) / 100;
	min_compress = (min_compress * PAGE_SIZE) / 100;
	areas = malloc(num_areas * sizeof(void *));
	if (!areas)
		exit(1);
    gettimeofday(&start, 0);
	for (i = 0; i < num_areas; i++) {
		//printf("Allocated: %d MB\n", i * 100);
		areas[i] =
		    mmap(NULL, AREA_SIZE, PROT_READ | PROT_WRITE,
			 MAP_PRIVATE | MAP_ANONYMOUS | MAP_POPULATE, -1,
			 0);
		if (areas[i] == MAP_FAILED) {
			perror("mmap");
			num_areas = i;
			break;
		}
		for (p = areas[i]; p < areas[i] + AREA_SIZE;
		     p += PAGE_SIZE) {
			j = min_compress;
			if (rng_compress > 0)
				j += (random() % rng_compress);
			j = PAGE_SIZE - j;
			if (j < PAGE_SIZE)
				memcpy(p + j, random_page, PAGE_SIZE - j);
		}
	}
    gettimeofday(&end,0);
    timeval_sub(&start, &end, &sub);
	printf("allocation takes %ld second %ld microsecond\n", sub.tv_sec, sub.tv_usec);
	printf("Total memory allocated: %d MB\n", i * 100);
	printf("Press enter to re-fault the memory randomly\n");
	//getchar();
    gettimeofday(&start, 0);
	for (i = 0; i < num_areas; i++) {
		for (j = 0; j < AREA_SIZE / PAGE_SIZE; j++) {
			k = random() % AREA_SIZE;
			p = areas[random() % num_areas] + k;
			v = *p;
		}
		//printf("Faulted in: %d MB\n", (i + 1) * 100);
	}
    gettimeofday(&end,0);
    timeval_sub(&start, &end, &sub);
	printf("re-fault takes %ld second %ld microsecond\n", sub.tv_sec, sub.tv_usec);
	//printf("Press enter to exit\n");
	//getchar();
}
