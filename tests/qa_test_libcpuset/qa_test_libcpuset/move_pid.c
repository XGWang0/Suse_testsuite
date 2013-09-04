#include <cpuset.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

move_pid_to(pid_t pid, const char *c) {
	int rc;
	if(0 > (rc = cpuset_move(pid, c))) {
		perror("cpuset_move failed");
		printf(" pid: %d relcpuset: %s\n", pid, c);
		return rc;
	}
	return 0;
}

int usage(char *comm, int fail_) {
	printf("Usage: %s <pid> <cpuset>\n", comm);
	return fail_;
}

int main(int argc, char * argv[]) {
	if(argc < 3)
		return usage(argv[0], 1);

	pid_t pid = atoi(argv[1]);

	if(0 <= cpuset_move(pid, argv[2]))
		return 0;

	perror("cpuset_move failed");
	return 1;
}
