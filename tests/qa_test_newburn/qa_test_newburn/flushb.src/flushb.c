/*
 * This program was ripped from the e2fsprogs package v1.15, unmodified
 * for use in Cerberus except for this notice.  Please do not bother
 * the e2fs maintainer for problems with this program, as it may be out
 * of sync.
 * - Jason T. Collins <jcollins@valinux.com>
 */

/*
 * flushb.c --- This routine flushes the disk buffers for a disk
 */

#include <stdio.h>
/* #include <string.h> */
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>

#include <linux/fs.h>

#ifdef __STDC__
#define NOARGS void
#else
#define NOARGS
#define const
#endif

const char *progname;

static void usage(NOARGS)
{
	fprintf(stderr, "Usage: %s disk\n", progname);
	exit(1);
}	
	
int main(int argc, char **argv)
{
	int	fd;
	
	progname = argv[0];
	if (argc != 2)
		usage();

	fd = open(argv[1], O_RDONLY, 0);
	if (fd < 0) {
		perror("open");
		exit(1);
	}
	/*
	 * Note: to reread the partition table, use the ioctl
	 * BLKRRPART instead of BLKFSLBUF.
	 */
#ifdef BLKFLSBUF
	if (ioctl(fd, BLKFLSBUF, 0) < 0) {
		perror("ioctl BLKFLSBUF");
		exit(1);
	}
	return 0;
#else
	fprintf(stderr,
		"BLKFLSBUF ioctl not supported!  Can't flush buffers.\n");
	return 1;
#endif
}
