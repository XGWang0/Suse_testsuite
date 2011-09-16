
/****************************************************************
**                                                             **
**    Copyright (c) 1996 - 2001 Caldera International, Inc.    **
**                    All Rights Reserved.                     **
**                                                             **
** This program is free software; you can redistribute it      **
** and/or modify it under the terms of the GNU General Public  **
** License as published by the Free Software Foundation;       **
** either version 2 of the License, or (at your option) any    **
** later version.                                              **
**                                                             **
** This program is distributed in the hope that it will be     **
** useful, but WITHOUT ANY WARRANTY; without even the implied  **
** warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR     **
** PURPOSE. See the GNU General Public License for more        **
** details.                                                    **
**                                                             **
** You should have received a copy of the GNU General Public   **
** License along with this program; if not, write to the Free  **
** Software Foundation, Inc., 59 Temple Place, Suite 330,      **
** Boston, MA  02111-1307  USA                                 **
**                                                             **
****************************************************************/
#define _POSIX_SOURCE 1			/* enable POSIX functions */

char *version = "1.1";			/* establish version */
char *release_date = "January 22, 1996";	/* and release */
char *benchmark_name = "AIM Independent Resource Benchmark - Suite IX";	/* and name */
char *logfile_name = "logfile.suite9";	/* log file for output */
char *report_name = "suite9.ss";	/* spreadsheet file */

#include <stdio.h>			/* enable printf(), etc. */
#include <stdlib.h>			/* enable atol(), etc. */
#include <signal.h>			/* enables signal handling */
#include <time.h>			/* enables ctime(), etc. */
#include <errno.h>			/* enable errno, etc.  */
#include <unistd.h>			/* getpid(), etc. */
#ifndef NO_ULIMIT
#include <ulimit.h>			/* enable ulimit(), etc. */
#endif
#include <string.h>			/* enables strcat(), etc. */
#include <sys/types.h>			/* used for setpgid(), etc. */
#include <sys/stat.h>			/* used for creat(), etc. */
#include <fcntl.h>			/* used for creat(), etc. */
#include <sys/times.h>			/* enables times(), etc. */
#include <sys/wait.h>			/* enable wait(), etc. */
#include <sys/param.h>			/* get HZ, etc. */
#include <math.h>

#include "testerr.h"
#include "suite.h"
#include "files.h"			/* declare all local files */

#define S9WORKFILE "s9workfile"		/* lists of test to run */
#define MAXCMDARGS (100)
#define TEST_LEN (50)			/* max strlen of command strings in workfile */
#define IGNORE 0			/* ignore this test */
#define RUN 1				/* run this test */
static Cargs cmdargs[MAXCMDARGS];	/* filled by register_test() */
static Result results;			/* holds return values from test functions */
static int num_cmdargs = 0;

source_file *
benchmark_c()
{
	static source_file s = { " @(#) singleuser.c:1.21 3/21/94 11:43:59",	/* SCCS info */
		__FILE__, __DATE__, __TIME__
	};

	return &s;
}

/*
 * Externally visible variables
 */
int
  verbose,				/* print details at startup */
  no_logfile,				/* do not print logfile */
  disk_iteration_count = 0,		/* number of loops for disk operations */
 *p_i1;					/* used in fun.c */

char
 *progname;				/* program name */

long
  debug,				/* 1 if we are debugging */
 *p_fcount;				/* used in fun.c */

/*
 * ---------------------------------------------------------------------------------
 * ---------------------------Privately visible variables---------------------------
 * ---------------------------------------------------------------------------------
 */
static int
  work = 0,				/* total # of tasks */
  flag,					/* used with SIGALRM */
  test_period;				/* number of seconds to run test */

static char
  path[10000],				/* make it huge enough */
  mname[256],				/* machine name */
  mconfig[256],				/* machine configuration */
 *ldate,				/* date from ctime */
  sdate[25];				/* date again copied from ctime */

static long
  period;				/* calibration timer */

static void
  build_temp_file(),
  rm_temp_file(),
  begin_timing(),			/* before each test */

  end_timing(),				/* after each test */

  run_each_test_with_timing(),
  get_misc_information(),
  read_workfile(),
  update_disk_test_count();

static FILE *logfile, *ss;

int
main(int argc,
     char **argv)
{
	source_file *(*s) ();		/* pointer to function */

	int i;


#ifndef NO_ULIMIT
	(void)ulimit(2, 1L << 20);	/* 1 meg blocks for max file size */
#endif
	system("sync;sync;sync");	/* clean out the cache, boosts performance */
	progname = argv[0];		/* name of this program */
	verbose = 0;			/* turn off verbose (DEFAULT) */
	no_logfile = 0;			/* print logfile (DEFAULT) */
	debug = 0;			/* turn off debug (DEFAULT) */
	while (--argc > 0) {		/* scan the command line */
		if ((*++argv)[0] == '-') {	/* look at first char of next */
			switch ((*argv)[1]) {	/* look at second */
			case 'd':
				debug = atol(&(*argv)[2]);	/* debugging always on */
				if (!debug)
					debug = 1;	/* default to level 1 */
				break;	/* skip */

			case 'v':
				verbose = 1;	/* print details at startup */
				break;	/* skip */

			case 'n':
				if ((*argv)[2] == 'l')
					no_logfile = 1;	/* don't print out the logfile */
				break;	/* skip */

			default:	/* other options */
				(void)fprintf(stderr, "Usage: %s [-t] [-v] [-dn]\n", progname);	/* and more */
				(void)fprintf(stderr, "  -v     verbose\n");	/* and more */
				(void)fprintf(stderr,
					      "  -nl    don't print logfile\n");
				(void)fprintf(stderr, "  -dn    turn on debug level n\n\n");	/* and more */
				exit(1);	/* drop dead here */
				break;	/* make lint happy */
			}		/* end of switch */
		}			/* end of if */
	}				/* end of while */

	(void)printf("\n%s v%s, %s\n", benchmark_name, version, release_date);
	(void)printf
		("Copyright (c) 1996 - 2001 Caldera International, Inc.\n");
	(void)printf("All Rights Reserved\n\n");
	if (verbose)
		(void)printf("This version compiled at %s on %s\n", __TIME__,
			     __DATE__);
#ifdef COUNT
	(void)printf
		("Operation Count enabled -- Timing Results are invalid.\n\n");
#endif
	/*
	 * create Logfile
	 */
	if (!no_logfile) {
		logfile = fopen(logfile_name, "a");	/* create log file */
		if (logfile == NULL) {
			(void)fprintf(stderr,
				      "\nUnable to open log file `%s'.\n",
				      logfile_name);
			exit(1);
		}
	}
	ss = fopen(report_name, "a");
	if (ss == NULL) {
		(void)fprintf(stderr, "\nUnable to open output file `%s'.\n",
			      report_name);
		exit(1);
	}
	if (verbose) {
		if (!no_logfile)
			(void)printf("Logging output to file `%s'.\n",
				     logfile_name);
		(void)printf("Report output to file `%s'.\n", report_name);
	}
	get_misc_information();		/* ask user lots of questions */
	/*
	 * Call initialization routines for each separate file
	 */
	register_test("NOCMD", "NOARGS", (int (*)())0, 0, "This shouldn't happen");	/* register first one */

	if (verbose) {
		printf("\nFile\t\tDate\t\tTime\t\tSCCS\n");
		printf("---------------------------------------------------------\n");
	}
	for (i = 0; i < Members(source_files); i++) {
		source_file *p;

		s = source_files[i];
		p = s();		/* run it */
		if (verbose)
			printf("%-15s\t%s\t%s\t%s\n", p->filename, p->date,
			       p->time, p->sccs);
	}
	/*
	 * Print each registered test's name
	 */
	if (debug)
		for (i = 0; i < num_cmdargs; i++)
			printf("%s\t%s\n", cmdargs[i].name, cmdargs[i].args);
	/*
	 * num_cmdargs has now been set to # of "real" tests registered plus 1 for "NOCMD" 
	 */
	if (verbose) {
		printf("---------------------------------------------------------\n");
		printf("\nA total of %d discrete tests were registered.\n\n",
		       num_cmdargs);
	}

	read_workfile();		/* see which tests to run */
	update_disk_test_count();	/* now update disk tests w/ disk_iteration_count */
	if (!no_logfile)
		fprintf(logfile, "%s\n%s\n%s\n%s\n%d\n",	/* put name, date, benchmark name to logfile */
			mname, mconfig, sdate, benchmark_name,
			disk_iteration_count);
	fprintf(ss, "%s\n%s\n%s\n%s \"%s\"\n%dK\n",	/* put name, date, benchmark name to spreadsheet file */
		mname, mconfig, sdate, benchmark_name, version,
		disk_iteration_count);
	build_temp_file();
	run_each_test_with_timing();	/* run it */
	if (!no_logfile)
		fclose(logfile);	/* close logfile */
	fclose(ss);			/* close spreadsheet output */
	rm_temp_file();
	(void)printf("\n%s\n   Testing over\n", benchmark_name);	/* talk to human */
	return 0;			/* return success; compiler complains if exit() */
}

void
alarm_handler(int sig)
{
	flag = 0;
}

static void
run_each_test_with_timing()
     /*
      */
{
	time_t now, then, delta, finish;

	int
	  hr, mn, sc, trouble, count, j, test_num, (*func) ();	/* the function pointer */

	char
	  sign, cmd[256],		/* executable command to "system" */
	  params[STRLEN];

	static char *line =
		"------------------------------------------------------------------------------------------------------------\n";

	time(&now);
	delta = work * test_period;	/* total estimated time for all tests */
	hr = delta / 3600;		/* hours */
	mn = (delta % 3600) / 60;	/* minutes */
	sc = delta % 60;		/* seconds */
	then = now + delta;		/* estimated completion time */
	printf("\n\n");			/* tell user all of this */
	printf("Starting time:      %s", ctime(&now));	/* starting time */
	printf("Projected Run Time: %d:%02d:%02d\n", hr, mn, sc);
	printf("Projected finish:   %s", ctime(&then));
	printf("\n\n\n");
	printf(line);
	printf(" Test        Test        Elapsed  Iteration    Iteration          Operation\n");
	printf("Number       Name      Time (sec)   Count   Rate (loops/sec)    Rate (ops/sec)\n");
	printf(line);

	for (test_num = 1, j = 1; j < num_cmdargs; j++) {	/* do this number of tests */
		if (cmdargs[j].run == IGNORE)
			continue;
		printf("%6d %-14s ", test_num, cmdargs[j].name);
		test_num++;		/* diff from j since may IGNORE some tests */
		fflush(stdout);
		func = cmdargs[j].f;	/* point to function to run */
		sprintf(params, "%s", cmdargs[j].args);
		(void)sprintf(cmd, "%s ", cmdargs[j].name);	/* build string arguments */
		if (strcmp(cmdargs[j].args, "DISKS") == 0) {	/* handle DISKS as special case */
			sprintf(params, "%s", path);	/* add the path there */
		}
		signal(SIGALRM, alarm_handler);
		flag = 1;
		alarm(test_period);
		begin_timing();		/* start the timer */
		trouble = count = 0;
		while (flag) {
			errno = 0;	/* clear errors */
			if ((*func) (params, &results) < 0) {	/* do function */
				perror(cmdargs[j].name);	/* if error, print it */
				(void)fprintf(stderr, " *** Failed to execute %s *** \n", cmd);	/* tell what happened */
				trouble = 1;
				break;
			}
			count++;
		}
		if (trouble == 0)	/* handle error case without outputing timing */
			end_timing(cmdargs[j].name, count, cmdargs[j].factor, cmdargs[j].units);	/* release the timer */
		else
			printf(" Skipping to next test.\n");
	}				/* end of testing loop */
	time(&finish);
	printf(line);
	delta = finish - then;		/* calc diff between actual and projected run time */
	sign = ' ';
	if (delta < 0) {
		sign = '-';
		delta = -delta;
	}
	hr = delta / 3600;
	mn = (delta % 3600) / 60;
	sc = delta % 60;
	printf("Projected Completion time:  %s", ctime(&then));
	printf("Actual Completion time:     %s", ctime(&finish));
	printf("Difference:                %c%d:%02d:%02d\n", sign, hr, mn,
	       sc);

}

static void
put_prompt(char *msg)
{
	printf("%-50s: ", msg);
	fflush(stdout);
}

static void
prompt_read_string(char *buf,
		   int bufsiz,
		   char *msg)
{
	int len;

	put_prompt(msg);
	fgets(buf, bufsiz - 1, stdin);
	len = strlen(buf);
	if (len && buf[len - 1] == '\n')
		buf[len - 1] = '\0';
}

#ifdef PROMPT_FILE
static void
prompt_filesize(int *i,
		char *msg)
{
	char buffer[80], m_or_k[2];
	int flag, how_many;

	flag = 1;			/* don't iterate */
	do {				/* loop */
		put_prompt(msg);	/* display prompt to user */
		fgets(buffer, sizeof (buffer), stdin);	/* read it in */

		if (strchr(buffer, '.') != NULL)	/* found a decimal point, no decimal input allowed */
			(void)printf
				("Specify an integral number of kilobytes or megabytes.\n");
		else if (sscanf(buffer, "%d%1s", &how_many, m_or_k) < 2) {	/* need size and unit, '1s' to handle any white space */
			(void)printf("Specify both size and unit.\n");
		} else if ((*m_or_k != 'm') && (*m_or_k != 'M') &&	/* must enter k, K, M, or m */
			   (*m_or_k != 'k') && (*m_or_k != 'K'))
			(void)printf
				("Specify kilobytes or megabytes [K or M].\n");
		else if (how_many <= 0)	/* illegal size */
			(void)printf("Specify at least 1K.\n");
		else			/* input okay */
			flag = 0;
	} while (flag);
	if ((*m_or_k == 'k') || (*m_or_k == 'K'))	/* figure iteration count */
		*i = how_many;		/* our internal buffer is 1k */
	else
		*i = how_many * NBUFSIZE;	/* how many 1k buffers is it */
}
#endif

static void
prompt_read_int(int *i,
		int lower,
		int upper,
		char *msg)
{
	char
	  buffer[128];

	int
	  temp, flag = 1;

	do {				/* loop */
		/*
		 * Prompt for the info
		 */
		if (lower == -1)	/* no limits */
			(void)sprintf(buffer, "%s", msg);	/* format message */
		else
			(void)sprintf(buffer, "%s [%d to %d]", msg, lower, upper);	/* format message */
		put_prompt(buffer);
		/*
		 * Get the reply 
		 */
		fgets(buffer, sizeof (buffer), stdin);	/* read it in */
		/*
		 * Convert to numeric value
		 */
		temp = atoi(buffer);	/* convert to binary */
		if ((temp >= lower) && (temp <= upper))
			flag = 0;	/* legal value */
		if (flag && (lower != -1))
			(void)printf
				("\nThat value %d is illegal. Legal values are from %d to %d. Please try again.\n",
				 temp, lower, upper);
		else if (flag && (lower == -1))
			(void)printf
				("\nThat value %d is illegal. Legal values must be below %d. Please try again.\n",
				 temp, upper);
	} while (flag);
	*i = temp;
}


int
has_decimal_point(char *buffer)
     /*
      * report 1 if buffer has a '.' in it 
      */
{
	char *p;

	for (p = buffer; *p != '\0'; p++)
		if (*p == '.')		/* decimal point */
			return (1);
	return (0);
}

static void
get_misc_information()
{
	time_t vtime;			/* used for time manipulation below */

	prompt_read_string(mname, sizeof (mname), "Machine's name");	/* get name */
	prompt_read_string(mconfig, sizeof (mconfig), "Machine's configuration");	/* get configuration */
	prompt_read_int(&test_period,	/* get test period */
			2, 1000, "Number of seconds to run each test");
	path[0] = '\0';
	while (path[0] == '\0')
		prompt_read_string(path, sizeof (path), "Path to disk files");	/* paths */
#ifdef PROMPT_FILE
	prompt_filesize(&disk_iteration_count, "Testfile size in Kbytes or Mbytes [e.g. 2K, 1M]");	/* testfile size */
#endif
	time(&vtime);			/* get the time */
	ldate = ctime(&vtime);		/* convert to ascii */
	sscanf(ldate, "%*s %21c", sdate);	/* isolate out what we want */
	sdate[20] = '\0';		/* null terminate it */
}

void
register_test(char *name,		/* name of the test */

	      char *args,		/* pointer to the args string */

	      int (*f) (),		/* pointer to the test */

	      int factor,		/* factor */

	      char *units)
{					/* units for the factor */
	if (num_cmdargs >= MAXCMDARGS) {
		fprintf(stderr,
			"\nInternal Error: Attempted to register too many tests.\n");
		exit(1);
	}
	cmdargs[num_cmdargs].name = name;
	cmdargs[num_cmdargs].args = args;
	cmdargs[num_cmdargs].f = f;
	cmdargs[num_cmdargs].factor = factor;
	cmdargs[num_cmdargs].units = units;
	cmdargs[num_cmdargs].run = IGNORE;
	num_cmdargs++;
}

/* since we do not know the disk_iteration_count until after registering
 * tests, we place a marker value in the 'factor' field and then call
 * this routine later to update with the disk_iteration value once we
 * have it
 */
static void
update_disk_test_count()
{
	int i;

	for (i = 0; i < num_cmdargs; i++) {
		if (cmdargs[i].factor == WAITING_FOR_DISK_COUNT)
			if (strncmp(cmdargs[i].name, "sync", 4) == 0)
				cmdargs[i].factor = disk_iteration_count / 2;
			else
				cmdargs[i].factor = disk_iteration_count;
	}
}

static void
begin_timing()
{					/* before each test */
	period = rtmsec(FALSE);		/* get the starting time */
}

static void
end_timing(char *test,
	   int count,
	   int factor,			/* after each test */

	   char *units)
{
	long temp = rtmsec(FALSE);	/* get ending time */

	double
	  delta = ((double)temp - (double)period),	/* calc actual test time in milliseconds */

	  rate = 1000.0 * (double)count / delta,	/* # of times test function called per second */

	  ops = rate * (double)factor;	/* operations per second */

	char buffer[200];

	if (factor >= 0)
		sprintf(buffer, "%15.2f %s/second", ops, units);
	else
		sprintf(buffer, "<Uncalibrated> %s/second", units);

	if (!no_logfile) {
		fprintf(logfile, "%s %g %g %s\n", test, delta, rate, buffer);	/* logfile output */
		fflush(logfile);	/* force it to disk */
	}

	printf("%10.2f %10d %10.5f %s\n", delta / 1000.0, count, rate, buffer);	/* update console */

	if (ops >= 1.0)
		fprintf(ss, "%s\t%d\t%s per second\n", test, (int)ops, units);	/* spreadsheet file */
	else
		fprintf(ss, "%s\t%g\t%s per second\n", test, ops, units);	/* spreadsheet file */
	fflush(ss);			/* force it to disk */
}

static void
build_temp_file()
{
	struct stat stbuf;		/* stat buffer */
	char
	  filename[1024],		/* make it large enough */
	  block[NBUFSIZE], buf[256],	/* used to build filename for stat */
	  cmd[1024],			/* tar command */
	  cwd[256];			/* hold current working dir, for tar */

	int
	  i, status, fd;

	memset(block, 'a', sizeof (block));	/* clear it to known values */
	sprintf(filename, "%s/%s", path, TMPFILE1);
	if (verbose)
		(void)printf("Building temporary file %s\n", filename);

	unlink(filename);
	fd = creat(filename, (S_IRWXU | S_IRWXG | S_IRWXO));	/* set permissions to very permissive */
	if (fd < 0) {
		fprintf(stderr, "build_temp_file: Unable to create file %s\n",
			filename);
		perror("creat");
		exit(1);
	}
	for (i = 0; i < disk_iteration_count; i++) {
		status = write(fd, block, sizeof (block));
		if (status != sizeof (block)) {
			fprintf(stderr,
				"Write error attempting to build file %s\n",
				filename);
			perror("write");
			exit(1);
		}
	}
	close(fd);
	if (getcwd(cwd, 256) == NULL) {
		fprintf(stderr,
			"build_temp_file(): can't get current working directory\n");
		exit(1);
	}
	sprintf(buf, "%s/fakeh", path);	/* prepare to tar fakeh file into directory */
	if (stat(buf, &stbuf) < 0) {	/* fakeh already there */
		sprintf(cmd, "cd %s; tar xfo %s/fakeh.tar 2> /dev/null", path, cwd);	/* if not there, untar it */
		system(cmd);		/* do it, return value implementation-dependent */
		if (stat(buf, &stbuf) < 0) {	/* tar failed */
			sprintf(cmd, "cd %s; tar xf %s/fakeh.tar 2> /dev/null", path, cwd);	/* if not there, untar it */
			system(cmd);	/* do it, return value implementation-dependent */
			if (stat(buf, &stbuf) < 0) {	/* tar failed */
				fprintf(stderr, "build_temp_file(): cannot create %s/fakeh\n", path);	/* tell user */
				exit(1);
			}		/* end of third if-stat */
		}			/* end of second if-stat */
	}				/* end of first if-stat */
}

static void
rm_temp_file()
{
	char
	  filename[1024],		/* make it large enough */
	  cmd[256];			/* executable command to "system" */

	sprintf(filename, "%s/%s", path, TMPFILE1);
	unlink(filename);
	sprintf(cmd, "rm -fr %s/fakeh", path);	/* remove fakeh directory */
	system(cmd);
	sprintf(cmd, "rm -f %s/link* 2> /dev/null", path);	/* remove link_test files */
}

static void
read_workfile()
{
	FILE * fp;			/* file pointer */
	char
	  buf[132];			/* line buffer for reading */
	char label[32], dim;
	int n, size;

	if ((fp = fopen(S9WORKFILE, "r")) == NULL) {	/* open work file and read in tasks */
		(void)fprintf(stderr,	/* handle error */
			      "Can't find file \"%s\" in current directory.\n",
			      S9WORKFILE);
		perror("read_workfile");	/* print message */
		exit(1);		/* die here */
	}				/* end of error processing */
	while (!feof(fp) && !ferror(fp)) {	/* while we're not done */
		Cargs *found, *find_arguments();

		if (fgets(buf, sizeof (buf) - 1, fp) != NULL) {	/* read in a line */
			if (*buf == '#')
				continue;	/* comment line */
			if (strlen(buf) == 0) {	/* if not empty line and bad read */
				(void)fprintf(stderr, "Error in file '%s' (line #%d)=[%s]\n",	/* error here */
					      S9WORKFILE, work, buf);	/* dump all info */
				exit(1);	/* die */
			}		/* end of error processing */
		} /* end of read ok */
		else if (!feof(fp)) {	/* if not ok read and not eof */
			if (work) {	/* first line? */
				perror("read_workfile");	/* if not, */
				(void)fprintf(stderr, "Error reading file '%s' ", S9WORKFILE);	/* print message */
			} else		/* else its an empty file */
				(void)fprintf(stderr, "File '%s' is empty\n", S9WORKFILE);	/* print mesg */
			exit(1);	/* and die */
		} /* end of !feof() */
		else
			continue;
		buf[strlen(buf) - 1] = '\0';	/* get rid of newline */
		if ((strlen(buf) > (size_t) 0) && ((*buf == 'F') || (*buf == 'f'))) {	/* possibly specifying FILESIZE */
			n = sscanf(buf, "%s %d%c", label, &size, &dim);	/* format: FILESIZE: 10K */
			if (n == 3) {	/* if correct format */
				if ((dim == 'M') || (dim == 'm'))
					size *= NBUFSIZE;	/* how many 1k buffers */
				disk_iteration_count = size;
				continue;	/* don't update 'work' variable */
			}
		}
		found = find_arguments(buf);
		if (strcmp(found->name, "NOCMD") == 0) {	/* flag test we haven't registered */
			(void)fprintf(stderr, "Test '%s' has not been registered.\n", buf);	/* print mesg */
			exit(1);	/* and die */
		}
		found->run = RUN;
		work++;			/* add one more line */
		if (work >= WORKLD) {
			(void)fprintf(stderr, "Workfile too large, limited to %d entries.\n", WORKLD);	/* print mesg */
			exit(1);	/* and die */
		}
	}				/* and loop until done */
	(void)fclose(fp);		/* close the file (we're done w/ it) */
	if (disk_iteration_count == 0) {
		(void)fprintf(stderr,
			      "\nWorkfile must contain the testfile size in kbytes or megabytes:\n");
		(void)fprintf(stderr, "FILESIZE: <integer><KkMm>\n");
		exit(1);		/* and die */
	}
}

Cargs *
find_arguments(char *s)
{
	int i;				/* loop variable */

	for (i = 1; i < num_cmdargs; i++)	/* search all args list */
		if (strcmp(s, cmdargs[i].name) == 0)	/* match? */
			return (&cmdargs[i]);	/* if so, return it */

	(void)fprintf(stderr,
		      "find_arguments: can't find <%s> in cmdargs[], was it registered?\n",
		      s);
	return (&cmdargs[0]);		/* else return first entry, NOCMD */
}
