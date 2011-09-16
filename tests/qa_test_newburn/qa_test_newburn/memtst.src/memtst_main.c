/*
 * Memory Test Utility
 *
 * (c) Copyright VA Linux Systems, Inc. 1993-2001.  All rights reserved.
 *
 * You may redistribute this program under the terms of the General Public
 * License, version 2, or, at your option, any later version.
 *
 * Author: Larry M. Augustin
 * Practically rewritten 6/20/01 by Jason T. Collins.  I doubt Larry would
 * recognize it now.
 *
 * 110199 (jtc):  Adjustable parameter for free VM.  Default is 128 MB.
 *
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>

extern char *optarg;
extern int optind, opterr, optopt;

#include "memtst.h"
#include "memory.h"

/* Function Declarations */
void usage(char *argv0, char *errormsg);
int do_other_processes(int processes, int argc, char **argv, char **env);

int verbose=0; /* see in main() below */


/* do all subprocesses and return results. */
int do_other_processes(int processes, int argc, char **argv, char **env)
{
	char **newargv;
	int newargc;
	int i, pid, status=-1;
	/* If you want more than 9999999999 processes, too damned bad. 
	   Don't worry, I do bounds checking. ;) */
	char p[10];

	/* Three additional parameters */
	newargc = argc + 4;
	newargv = malloc(sizeof(char *) * newargc);

	/* Copy existing argv into newargv */
	for (i=0; i < argc; ++i) {
		newargv[i] = malloc(sizeof(char)*(strlen(argv[i])+1));
		strcpy(newargv[i],argv[i]);
	}

	/* Add parameters for number of processes plus the "fast" mode */
	newargv[i++] = "-n";
	snprintf(p,10,"%d",processes);
	printf("%s more processes to launch\n",p);
	newargv[i++] = p;
	newargv[i++] = "-B";
	newargv[i] = NULL;
	/* Clear out errno in case it has strange values in it */
	errno=0;

	pid = fork();
	if (pid == -1)
		return -1;
	if (pid == 0) {
		/* In client.  Make it so, number one */
		execve(newargv[0],newargv,env);
		exit(127);
	}

	/* pid == client process pid, we're in parent */
	do {
		if(waitpid(pid, &status, 0) == -1) {
			if (errno != EINTR) return 1;
		} else {
			/* if our process exited normally, return that
			   status.  If it died for strange reasons return
			   an error.  */
			if (WIFEXITED(status)) {
				return WEXITSTATUS(status);
			} else return 1;
		}
	} while (1);
}


void usage(char *argv0, char *errormsg) 
{
	if(strlen(errormsg))fprintf(stderr, "Error: %s", errormsg); 
	fprintf(stderr, "usage: %s -12345 -B -c [ceiling] -f [free_vm] -n [processes] -v\n", argv0);
	fprintf(stderr, "Pattern 1:    Larry's traditional test\n");
	fprintf(stderr, "Pattern 2-4:  Simple variations on Larry's test\n");
	fprintf(stderr, "Pattern 5:    the 0FA5 rotating pattern\n");
	fprintf(stderr, "You must specify at least one pattern with -1, -2, et. al\n");
	exit(2);
}


/* Velcome to my memory test.  */
int main(int argc, char **argv, char **env) 
{
	/* int verbose=0;  */  /* currently a global, see memtst.h */
	/* Amount of memory (MB) to leave free by default.  This makes
	   memtst have utility as a standalone program. */
	int free_vm=128;

	/* Maximum amount of memory (MB) to never exceed in this
	   process by default.  This is probably not a really useable
	   default, I'm not sure what would be reasonable here. */
	int ceiling=2047;

	/* Number of processes to spawn.  We will fork this many times
	   and test the largest block size on each. */
	int processes=1;

	/* You'll have to modify code for good results less than 6
	   unless you use 0 (use one long block)*/
	int block_table_size=14;

	/* Block size table */
	int *block_table;

	/* Number of patterns on the command line */
	int patterns=0;

	int retval = 0;

	/* Some would argue that what I do with these obviates the
	   need for struct tests.  They'd probably be right.  But I
	   think it looks clearer this way.  */
	void *testfunctions_write[NUMOFTESTS];
	void *testfunctions_check[NUMOFTESTS];
	char *descriptions[NUMOFTESTS];

	/* The Buffer, and How Big It Is */
	char *buf;
	unsigned long nint;

	tests *memtests;
	
	while (1) {
		int c;
		c = getopt(argc,argv,"12345Bc:f:vn:");
		if (c==-1) break;
		switch (c) {
		case '1':
			testfunctions_write[patterns]=&larry_write;
			testfunctions_check[patterns]=&larry_check;
			descriptions[patterns]="larry";
			++patterns;
			break;
		case '2':
			testfunctions_write[patterns]=&larry_bkwds_write;
			testfunctions_check[patterns]=&larry_bkwds_check;
			descriptions[patterns]="larry_bkwds";
			++patterns;
			break;
		case '3':
			testfunctions_write[patterns]=&larry_top_write;
			testfunctions_check[patterns]=&larry_top_check;
			descriptions[patterns]="larry_top";
			++patterns;
			break;
		case '4':
			testfunctions_write[patterns]=&larry_bottom_write;
			testfunctions_check[patterns]=&larry_bottom_check;
			descriptions[patterns]="larry_bottom";
			++patterns;
			break;
		case '5':
			testfunctions_write[patterns]=&bitpatts_write;
			testfunctions_check[patterns]=&bitpatts_check;
			descriptions[patterns]="bitpatts";
			++patterns;
			break;
		case 'B':
			block_table_size=0;
			break;
		case 'c':
			/* remember, usage never returns */
			if ((ceiling = strtol(optarg,NULL,0)) <= 0)
				usage(argv[0],"Need a ceiling with -c\n");
			break;
		case 'f':
			if ((free_vm = strtol(optarg,NULL,0)) <= 0)
				usage(argv[0],"Need free vm value with -f\n");
			break;
		case 'v':
			verbose=1;
			break;
		case 'n':
			if ((processes = strtol(optarg,NULL,0)) <= 0)
				usage(argv[0],"Please specify a number of processes with -n.\n");
			break;
		case '?':
		default:
			usage(argv[0],"");
		}
	}
	if (patterns == 0) {
		usage(argv[0],"Must specify a pattern to test.\n");
	}

	memtests=test_setup(patterns,
			    testfunctions_write,
			    testfunctions_check,
			    descriptions);

	nint = compute_nint(free_vm, ceiling);

	/* be warned, get_buf can/will modify nint here.  Sorry, it ain't
	   a perfect world. */
	buf = get_buf(&nint);

	block_table = generate_block_table(nint,&block_table_size);

	/* If we fail the test, just exit. */
	if(memtst(memtests,buf,block_table,block_table_size)) {
		exit(1);
	}

	--processes;
	if(processes == 0) exit(0);

	/* Most types of programs would free the buffer here, since
	   we don't use it and wait.  But I want to sit on the memory
	   to convince the kernel that I might use it, so hopefully
	   it will remain mapped for a while so the other test processes
	   can get different areas of memory.  This was the motivation
	   for the rewrite, so on machines with > 2 GB of RAM I'm a lot
	   closer to guaranteeing full coverage with the test. */
	retval=do_other_processes(processes, argc, argv, env);

	printf("Returning: %d\n", retval);
	return (retval);
}
