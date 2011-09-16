#ifndef MEMTST_H
#define MEMTST_H

#include "sizeofint.h"

/* This structure represents a test pattern, essentially a pointer to
   functions for looping through test arrays either writing, or checking.
   The functions should have parameters as below
       void function_write(int *buf, int block_size, int plus);
       int function_check(int *buf, int block_size, int *error);
   function_write should simply write the test pattern to the buffer.
   The plus parameter should be interpreted as if you were writing inside
   a bigger buffer, i.e. your buffer is (plus) offset the beginning of
   a bigger buffer.  Right now, it's just used for the expect/actual
   part of the reporting.
   function_check needs to check the buffer.  If function_check finds
   an error, set *error to non-zero and return the offset, otherwise
   leave *error alone and return whatever you want.  See memtst.c for
   examples. */

typedef struct {
	void *testfunction_write;
	void *testfunction_check;
	char *desc;
} test_pattern;


/* Here is our test structure. */
typedef struct {
	int numoftests;
	test_pattern **patterns;
} tests;
   
#if SIZEOF_INT == 4
#define HEX_AS 0xaaaaaaaa
#endif
#if SIZEOF_INT == 8
#define HEX_AS 0xaaaaaaaaaaaaaaaa
#endif
#ifndef HEX_AS
#error "Unsupported architecture, only 32 and 64 bit systems supported"
#endif

/* Test Functions */
/* How many of these buggers do we have to be prepared for */
#define NUMOFTESTS 5

void larry_write(int *nbuf, int block_size, int plus);
int larry_check(int *nbuf, int block_size, int *error);

void larry_bkwds_write(int *nbuf, int block_size, int plus);
int larry_bkwds_check(int *nbuf, int block_size, int *error);

void larry_top_write(int *nbuf, int block_size, int plus);
int larry_top_check(int *nbuf, int block_size, int *error);

void larry_bottom_write(int *nbuf, int block_size, int plus);
int larry_bottom_check(int *nbuf, int block_size, int *error);

void bitpatts_write(int *nbuf, int block_size, int plus);
int bitpatts_check(int *nbuf, int block_size, int *error);


/* Main memtst functions */

unsigned long compute_nint(unsigned long free_vm, unsigned long ceiling);
void display_failure (int *nbuf, int align, int block_size, int offset, int test_function_write());
int *generate_block_table(unsigned long nint, int *block_table_size);
char *get_buf(unsigned long *nint);
void kmemscan (int *nbuf, int block_size, int offset);
int test_block (char *buf, int align, int block_size, 
		int test_function_write(), int test_function_check());
tests *test_setup (int num_tests, void **testfunctions_write, 
		   void **testfunctions_check, char **descriptions );



int memtst(tests *memtests, char *buf, int *block_table, int block_table_size);

#endif
