#ifndef	lint
static char sccs_id[] = { " @(#) rpt9.c:1.7 1/22/96 00:00:00" };
#endif

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
#include <stdio.h>

#define NUM_HEADERS (5)			/* number of header lines */
#define LINE_SIZE (128)			/* default line size */
#define normal_format "%.0f"
#define zero_format   "%.1f"
#define bold_font  "Times-Bold"
#define normal_font  "Times-Roman"


#define OFFSET (-.50)
#define ARITH_START (7.25+OFFSET)	/* distance in inches from bottom */
#define IPC_START (7.25+OFFSET)
#define DISK_START (4.00+OFFSET)
#define LIB_START (3.25+OFFSET)
#define ALG_START (1.50+OFFSET)
#define MEM_START (2.75+OFFSET)
#define FUNC_START (1.50+OFFSET)

typedef enum { left, center, right } Where;

typedef struct _placement {
	char *tag;			/* tag in input file */
	char *format;			/* conversion format */
	double x, y;			/* where on the page to place it */
	double value;			/* the value */
} Placement;

typedef struct _highlights {
	char *text;			/* Text to display */
	Where where;
	char *font;
	int size;
	double x, y;
} Highlight;

char
 *progname,				/* name of program */
 *strdup(),				/* never quite declared when you need it */

 *headers[NUM_HEADERS];			/* top few lines of the program */
int line_count = 0;


Placement values[] = {

/*   tag        	       format		        x,		y          value (always -1) */

/* Arithmetic */
	{"add_short", normal_format, 2.25, ARITH_START + 1.00, -1.0,},
	{"div_short", normal_format, 3.25, ARITH_START + 1.00, -1.0,},
	{"mul_short", normal_format, 4.25, ARITH_START + 1.00, -1.0,},

	{"add_int", normal_format, 2.25, ARITH_START + 0.75, -1.0,},
	{"div_int", normal_format, 3.25, ARITH_START + 0.75, -1.0,},
	{"mul_int", normal_format, 4.25, ARITH_START + 0.75, -1.0,},

	{"add_long", normal_format, 2.25, ARITH_START + 0.50, -1.0,},
	{"div_long", normal_format, 3.25, ARITH_START + 0.50, -1.0,},
	{"mul_long", normal_format, 4.25, ARITH_START + 0.50, -1.0,},

	{"add_float", normal_format, 2.25, ARITH_START + 0.25, -1.0,},
	{"div_float", normal_format, 3.25, ARITH_START + 0.25, -1.0,},
	{"mul_float", normal_format, 4.25, ARITH_START + 0.25, -1.0,},

	{"add_double", normal_format, 2.25, ARITH_START + 0.00, -1.0,},
	{"div_double", normal_format, 3.25, ARITH_START + 0.00, -1.0,},
	{"mul_double", normal_format, 4.25, ARITH_START + 0.00, -1.0,},

	/*
	 * IPC 
	 */
	{"tcp_test", normal_format, 7.50, IPC_START + 1.25, -1.0,},
	{"udp_test", normal_format, 7.50, IPC_START + 1.00, -1.0,},
	{"fifo_test", normal_format, 7.50, IPC_START + 0.75, -1.0,},
	{"pipe_cpy", normal_format, 7.50, IPC_START + 0.50, -1.0,},
	{"shared_memory", normal_format, 7.50, IPC_START + 0.25, -1.0,},
	{"stream_pipe", normal_format, 7.50, IPC_START, -1.0,},
	{"dgram_pipe", normal_format, 7.50, IPC_START - 0.25, -1.0,},

	/*
	 * Disk Tests 
	 */
	{"sync_disk_rw", normal_format, 3.25, DISK_START + 2.00, -1.0,},
	{"disk_rw", normal_format, 2.25, DISK_START + 2.00, -1.0,},
	{"sync_disk_wrt", normal_format, 3.25, DISK_START + 1.75, -1.0,},
	{"disk_wrt", normal_format, 2.25, DISK_START + 1.75, -1.0,},
	{"sync_disk_cp", normal_format, 3.25, DISK_START + 1.50, -1.0,},
	{"disk_cp", normal_format, 2.25, DISK_START + 1.50, -1.0,},
	{"disk_src", normal_format, 2.75, DISK_START + 1.25, -1.0,},
	{"disk_rr", normal_format, 2.75, DISK_START + 1.00, -1.0,},
	{"disk_rd", normal_format, 2.75, DISK_START + 0.75, -1.0,},
	/*
	 * Filesystem tests 
	 */
	{"creat-clo", normal_format, 2.75, DISK_START + 0.50, -1.0,},
	{"link_test", normal_format, 2.75, DISK_START + 0.25, -1.0,},
	{"dir_rtns_1", normal_format, 2.75, DISK_START + 0.00, -1.0,},

	/*
	 * Library/System tests 
	 */
	{"jmp_test", normal_format, 7.50, LIB_START + 3.00, -1.0,},
	{"ram_copy", normal_format, 7.50, LIB_START + 2.75, -1.0,},
	{"num_rtns_1", normal_format, 7.50, LIB_START + 2.50, -1.0,},
	{"trig_rtns", normal_format, 7.50, LIB_START + 2.25, -1.0,},
	{"string_rtns", normal_format, 7.50, LIB_START + 2.00, -1.0,},
	{"mem_rtns_1", normal_format, 7.50, LIB_START + 1.75, -1.0,},
	{"mem_rtns_2", normal_format, 7.50, LIB_START + 1.50, -1.0,},
	{"sort_rtns_1", normal_format, 7.50, LIB_START + 1.25, -1.0,},
	{"signal_test", normal_format, 7.50, LIB_START + 1.00, -1.0,},
	{"misc_rtns_1", normal_format, 7.50, LIB_START + 0.75, -1.0,},
	{"shell_rtns_1", normal_format, 7.50, LIB_START + 0.50, -1.0,},
	{"shell_rtns_2", normal_format, 7.50, LIB_START + 0.25, -1.0,},
	{"shell_rtns_3", normal_format, 7.50, LIB_START + 0.00, -1.0,},

	/*
	 * Algorithmic Tests 
	 */
	{"new_raph", normal_format, 7.50, ALG_START + 1.00, -1.0,},
	{"matrix_rtns", normal_format, 7.50, ALG_START + 0.75, -1.0,},
	{"array_rtns", normal_format, 7.50, ALG_START + 0.50, -1.0,},
	{"series_1", normal_format, 7.50, ALG_START + 0.25, -1.0,},
	{"sieve", normal_format, 7.50, ALG_START + 0.00, -1.0,},

	/*
	 * Memory and Process Management 
	 */
	{"brk_test", normal_format, 2.25, MEM_START + 0.25, -1.0,},
	{"page_test", normal_format, 4.00, MEM_START + 0.25, -1.0,},
	{"exec_test", normal_format, 2.25, MEM_START + 0.00, -1.0,},
	{"fork_test", normal_format, 4.00, MEM_START + 0.00, -1.0,},

	/*
	 * Function Calls 
	 */
	{"fun_cal", normal_format, 2.25, FUNC_START + 0.25, -1.0,},
	{"fun_cal1", normal_format, 4.00, FUNC_START + 0.25, -1.0,},
	{"fun_cal2", normal_format, 2.25, FUNC_START + 0.00, -1.0,},
	{"fun_cal15", normal_format, 4.00, FUNC_START + 0.00, -1.0,},
};

#define NUM_VALUES (sizeof(values) / sizeof(values[0]))

Highlight titles[] = {
	/*
	 * Title 
	 */
	{"AIM Independent Resource Benchmark", center, bold_font, 32, 4.5,
	 10.30,},
	{"Suite IX ", center, bold_font, 24, 4.5, 10.00,},

/* arithmetic */
	{"Arithmetic", center, bold_font, 16, 2.0, ARITH_START + 1.75,},
	{"(Thousand Ops per Second)", center, bold_font, 14, 2.0,
	 ARITH_START + 1.50,},
	{"Short", left, normal_font, 16, 0.50, ARITH_START + 1.00,},
	{"Int", left, normal_font, 16, 0.50, ARITH_START + 0.75,},
	{"Long", left, normal_font, 16, 0.50, ARITH_START + 0.50,},
	{"Float", left, normal_font, 16, 0.50, ARITH_START + 0.25,},
	{"Double", left, normal_font, 16, 0.50, ARITH_START + 0.00,},
	{"Add", center, normal_font, 16, 2.0, ARITH_START + 1.25,},
	{"Div", center, normal_font, 16, 3.0, ARITH_START + 1.25,},
	{"Mult", center, normal_font, 16, 4.0, ARITH_START + 1.25,},
	/*
	 * IPC 
	 */
	{"InterProcess Communication",
	 center, bold_font, 16, 6.5, IPC_START + 1.75,},
	{"(Messages per Second)",
	 center, bold_font, 14, 6.5, IPC_START + 1.50,},
	{"TCP/IP", left, normal_font, 16, 5.0, IPC_START + 1.25,},
	{"UDP/IP", left, normal_font, 16, 5.0, IPC_START + 1.00,},
	{"FIFOs", left, normal_font, 16, 5.0, IPC_START + 0.75,},
	{"PIPEs", left, normal_font, 16, 5.0, IPC_START + 0.50,},
	{"Shared RAM", left, normal_font, 16, 5.0, IPC_START + 0.25,},
	{"Stream Pipe", left, normal_font, 16, 5.0, IPC_START + 0.00,},
	{"DataGram Pipe", left, normal_font, 16, 5.0, IPC_START - 0.25,},
	/*
	 * Disk Tests 
	 */
	{"Disk/Filesystem I/O", center, bold_font, 16, 2.0,
	 DISK_START + 2.75,},
	{"(Kbytes per Second and Ops per Second)",
	 center, bold_font, 14, 2.0, DISK_START + 2.50,},
	{"Cached", center, normal_font, 16, 2.0, DISK_START + 2.25,},
	{"Sync", center, normal_font, 16, 3.0, DISK_START + 2.25,},
	{"Rand Read", left, normal_font, 16, 0.50, DISK_START + 2.00,},
	{"Seq Write", left, normal_font, 16, 0.50, DISK_START + 1.75,},
	{"Rand Write", left, normal_font, 16, 0.50, DISK_START + 1.50,},
	{"Searches", left, normal_font, 16, 0.50, DISK_START + 1.25,},
	{"Copy", left, normal_font, 16, 0.50, DISK_START + 1.00,},
	{"Seq Read", left, normal_font, 16, 0.50, DISK_START + 0.75,},
	{"Create/Close", left, normal_font, 16, 0.50, DISK_START + 0.50,},
	{"Link/Unlink", left, normal_font, 16, 0.50, DISK_START + 0.25,},
	{"Directory", left, normal_font, 16, 0.50, DISK_START + 0.00,},

	/*
	 * Library/system tests 
	 */
	{"Library/System",
	 center, bold_font, 16, 6.5, LIB_START + 3.50,},
	{"(Various Rates)",
	 center, bold_font, 14, 6.5, LIB_START + 3.25,},
	{"Setjmp/Longjmp", left, normal_font, 16, 5.0, LIB_START + 3.00,},
	{"RAM Copy", left, normal_font, 16, 5.0, LIB_START + 2.75,},
	{"Numeric Rtns", left, normal_font, 16, 5.0, LIB_START + 2.50,},
	{"Trig Rtns", left, normal_font, 16, 5.0, LIB_START + 2.25,},
	{"String Rtns", left, normal_font, 16, 5.0, LIB_START + 2.00,},
	{"Mem Rtns 1", left, normal_font, 16, 5.0, LIB_START + 1.75,},
	{"Mem Rtns 2", left, normal_font, 16, 5.0, LIB_START + 1.50,},
	{"Sort/Search", left, normal_font, 16, 5.0, LIB_START + 1.25,},
	{"Signals", left, normal_font, 16, 5.0, LIB_START + 1.00,},
	{"Misc. Rtns", left, normal_font, 16, 5.0, LIB_START + 0.75,},
	{"Shell Rtns 1", left, normal_font, 16, 5.0, LIB_START + 0.50,},
	{"Shell Rtns 2", left, normal_font, 16, 5.0, LIB_START + 0.25,},
	{"Shell Rtns 3", left, normal_font, 16, 5.0, LIB_START + 0.00,},
	/*
	 * Algorithmic Tests 
	 */
	{"Algorithmic Tests", center, bold_font, 16, 6.5, ALG_START + 1.50,},
	{"Operations per Second", center, bold_font, 14, 6.5,
	 ALG_START + 1.25,},
	{"Newton/Raphson", left, normal_font, 16, 5.0, ALG_START + 1.00,},
	{"3D Projection", left, normal_font, 16, 5.0, ALG_START + 0.75,},
	{"Linear System", left, normal_font, 16, 5.0, ALG_START + 0.50,},
	{"Taylor Series", left, normal_font, 16, 5.0, ALG_START + 0.25,},
	{"Integer Sieve", left, normal_font, 16, 5.0, ALG_START + 0.00,},
	/*
	 * Memory and Process Management 
	 */
	{"Memory and Process Management",
	 center, bold_font, 16, 2.0, MEM_START + 0.75,},
	{"(Ops per Second)",
	 center, bold_font, 14, 2.0, MEM_START + 0.50,},
	{"Brk()", left, normal_font, 16, 0.5, MEM_START + 0.25,},
	{"Paging", left, normal_font, 16, 2.5, MEM_START + 0.25,},
	{"Exec()", left, normal_font, 16, 0.5, MEM_START + 0.00,},
	{"Fork()", left, normal_font, 16, 2.5, MEM_START + 0.00,},
	/*
	 * Function Calls 
	 */
	{"Function Calls", center, bold_font, 16, 2.0, FUNC_START + 0.75,},
	{"(Ops per Second)", center, bold_font, 14, 2.0, FUNC_START + 0.50,},
	{"0 Args", left, normal_font, 16, 0.5, FUNC_START + 0.25,},
	{"1 Arg", left, normal_font, 16, 2.5, FUNC_START + 0.25,},
	{"2 Args", left, normal_font, 16, 0.5, FUNC_START + 0.00,},
	{"15 Args", left, normal_font, 16, 2.5, FUNC_START + 0.00,},
	/*
	 * Copyright Notice 
	 */
	{"Copyright (c) 1996 - 2001 Caldera International, Inc.",
	 center, bold_font, 8, 4.0, 0.50},
	{"All Rights Reserved.",
	 center, bold_font, 8, 5.8, 0.50},
	{"These results are not certified.",
	 center, bold_font, 8, 4.5, 0.35}

};

#define NUM_TITLES (sizeof(titles) / sizeof(titles[0]))

char *ps_init[] = {
	"%! PS-Adobe-2.0",
	"/inch",
	"	{ 72 mul }",
	"	def",
	"%",
	"% beginning (initialization)",
	"%",
};

#define NUM_PS_INIT (sizeof(ps_init) / sizeof(ps_init[0]))

void
center_line(FILE * f,
	    char *line,
	    double y)
{
	fprintf(f, " (%s)\n", line);
	fprintf(f, "	/Times-Bold findfont 20 scalefont setfont\n");
	fprintf(f,
		"	dup				%% duplicate string\n");
	fprintf(f, "	stringwidth pop			%% get width\n");
	fprintf(f, "	2 div				%% divide by 2\n");
	fprintf(f,
		"	4.25 inch exch sub		%% subtract from middle\n");
	fprintf(f, "	%g inch moveto			%% go to y value\n",
		y);
	fprintf(f,
		"	show				%% print value on stack\n");
}

void
print_at(FILE * f,
	 char *line,
	 double x,
	 double y,
	 int fontsize)
{
	fprintf(f, " (%s)\n", line);
	fprintf(f, "	/Times-Bold findfont %d scalefont setfont\n",
		fontsize);
	fprintf(f, "	%g inch %g inch moveto		%% go to y value\n", x,
		y);
	fprintf(f,
		"	show				%% print value on stack\n");
}

void
print_highlight(FILE * f,
		Highlight * h)
{
	fprintf(f, "	(%s)\n", h->text);
	fprintf(f, "	/%s findfont %d scalefont setfont\n", h->font,
		h->size);
	switch (h->where) {
	case left:
		fprintf(f,
			"	%g inch %g inch moveto		%% go to y value\n",
			h->x, h->y);
		break;
	case right:
		fprintf(f,
			"	dup stringwidth pop		%% get width\n");
		fprintf(f,
			"	%g inch exch sub %g inch moveto	%% go to y value\n",
			h->x, h->y);
		break;
	case center:
		fprintf(f,
			"	dup				%% duplicate string\n");
		fprintf(f,
			"	stringwidth pop			%% get width\n");
		fprintf(f,
			"	2 div %g inch exch sub		%% calculate width\n",
			h->x);
		fprintf(f,
			"	%g inch moveto			%% go to y value\n",
			h->y);
		break;
	}
	fprintf(f,
		"	show				%% print value on stack\n");
}

void
print_right(FILE * f,
	    char *line,
	    double x,
	    double y,
	    int fontsize)
{
	fprintf(f, " (%s)\n", line);
	fprintf(f, "	/Times-Bold findfont %d scalefont setfont\n",
		fontsize);
	fprintf(f,
		"	dup				%% duplicate string\n");
	fprintf(f, "	stringwidth pop			%% get width\n");
	fprintf(f, "	%g inch exch sub %g inch moveto	%% go to y value\n", x,
		y);
	fprintf(f,
		"	show				%% print value on stack\n");
}

void
get_line(FILE * f,
	 char *line)
{
	char *p = line;

	line_count++;
	if (feof(f)) {
		fprintf(stderr, "Unexpected EOF on input file at line %d.\n",
			line_count);
		exit(1);
	}
	fgets(line, LINE_SIZE, f);
	while (*p != '\0') {		/* while not at end of string */
		if (*p == '\n') {	/* if we find an \n */
			*p = '\0';	/* make it a space */
			break;
		}
		p++;			/* and move to next one */
	}
}

int
main(int argc,
     char *argv[])
{
	int i;				/* loop variable */

	FILE * output,			/* output (print) file */
		*input;			/* input file */
	double
	  value;
	char
	  test[LINE_SIZE], buffer[LINE_SIZE];	/* holds one line */

	/*
	 * Step 1: check command line parameters
	 */
	progname = argv[0];		/* save program name */
	if (argc != 3) {
		fprintf(stderr, "Usage: %s input-file output-file\n",
			progname);
		exit(1);
	}
	/*
	 * Step 2: Open the input file, create output file
	 */
	input = fopen(argv[1], "r");	/* open input file */
	if (input == NULL) {		/* if we can't read it */
		fprintf(stderr, "%s: Unable to open input file %s\n",	/* talk to human */
			progname, argv[1]);
		exit(1);		/* and die */
	}
	output = fopen(argv[2], "w");	/* create output file */
	if (output == NULL) {		/* if we can't read it */
		fprintf(stderr, "%s: Unable to create output file %s\n",	/* talk to human */
			progname, argv[2]);
		exit(1);		/* and die */
	}
	/*
	 * Step 3: Pull out header records
	 */
	for (i = 0; i < NUM_HEADERS; i++) {
		get_line(input, buffer);	/* read in a line */
		headers[i] = strdup(buffer);	/* make it into a string */
	}
	/*
	 * Step 4: Fetch data values
	 */
	while (!feof(input)) {		/* while not at end of file */
		int flag = 0;

		get_line(input, buffer);	/* read in a line */
		sscanf(buffer, "%s\t%lf", test, &value);	/* get the values */
		for (i = 0; i < NUM_VALUES; i++) {
			if (strcmp(test, values[i].tag) == 0) {
				flag = 1;
				values[i].value = value;	/* insert value into it */
				break;
			}
		}
		if (flag == 0)
			fprintf(stderr,
				"%s: Ignoring unknown test %s from line %d.\n",
				progname, test, line_count);
	}
	fclose(input);
	/*
	 * Step 5: Prime for postscript output
	 */
	for (i = 0; i < NUM_PS_INIT; i++)
		fprintf(output, "%s\n", ps_init[i]);
	/*
	 * Step 6: Put in titles
	 */
	sprintf(buffer, "Run Date: %s", headers[2]);	/* date of run */
	center_line(output, buffer, 9.75);

	sprintf(buffer, "Machine: %s", headers[0]);	/* machine name */
	center_line(output, buffer, 9.5);

	sprintf(buffer, "Configuration: %s", headers[1]);	/* configuration */
	center_line(output, buffer, 9.25);

	sprintf(buffer, "Test File Size: %s kbytes", headers[4]);
	center_line(output, buffer, 9.00);

	for (i = 0; i < NUM_TITLES; i++)
		print_highlight(output, &titles[i]);

	for (i = 0; i < NUM_VALUES; i++) {
		if (values[i].value < 1.0)
			sprintf(buffer, zero_format, values[i].value);
		else
			sprintf(buffer, values[i].format, values[i].value);
		print_right(output, buffer, values[i].x, values[i].y, 16);
	}

	fprintf(output, "showpage\n");
	fclose(output);
	exit(0);
}
