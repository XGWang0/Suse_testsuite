#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/mman.h>
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define M(k) K(1024*(k))
#define K(k) (1024*k)
#define PAGE_SIZE 4096UL
#define MEMS_SIZE 4

struct area {
	void *addr;
	size_t size;
};

static size_t total_mem = M(1700);
static int should_rewalk = 0;

static void dirty_pages(void *addr, size_t size)
{
	unsigned char *p = (unsigned char *)addr;

	if (!addr)
		return;
	printf("Pageing in %p with size %luB\n", addr, size);
	for (; p < (unsigned char *)addr + size; p += PAGE_SIZE)
		*p = 1;
}

static struct area * prepare_anon(size_t size, int private)
{
	int flags = MAP_ANONYMOUS;
	void *addr;
	struct area *area = NULL;

	if (!size)
		return NULL;

	flags |= (private)?MAP_PRIVATE:MAP_SHARED;
	printf("mmap annonymous %luB in %s mode\n", size, 
			(private)?"private":"shared");
	if ((addr = mmap(NULL, size, PROT_READ|PROT_WRITE, 
					flags, -1, 0)) == MAP_FAILED) {
		perror("mmap:");
		return NULL;
	}
	dirty_pages(addr, size);

	area = (struct area *)malloc(sizeof(*area));
	area->addr = addr;
	area->size = size;
	return area;
}

static void find_size_for_prefix(char **argv, 
		const char *prefix, size_t *size)
{
	for (argv++; *argv; argv++) {
		if (!strncmp(prefix, *argv, strlen(prefix))) {
			const char *str_val = *argv+strlen(prefix);
			char * end;
			size_t val = strtoul(str_val, &end, 10);
			switch(*end) {
				case 'G':
					val *= 1024;
				case 'M':
					val *= 1024;
				case 'K':
					val *= 1024;
					end++;
					break;

			}
			if ((*end))
				printf("Invalid value (%s) for %s\n", str_val, prefix);
			else
				*size = val;

			return;
		}
	}
}

static struct area *prepare_private_anon(char **argv)
{
	size_t anon_size = total_mem/3;
	
	find_size_for_prefix(argv, "private_anon=", &anon_size);
	return prepare_anon(anon_size, 1);
}

static struct area *prepare_shared_anon(char **argv)
{
	size_t anon_size = total_mem/3;
	
	find_size_for_prefix(argv, "shared_anon=", &anon_size);
	return prepare_anon(anon_size, 0);
}

static struct area *prepare_shm(char **argv)
{
	void* addr;
	int shmid;
	size_t shm_size = total_mem/3;
	key_t key = IPC_PRIVATE;
	struct area *area = NULL;

	find_size_for_prefix(argv, "shm=", &shm_size);
	if (!shm_size)
		return NULL;

	find_size_for_prefix(argv, "shm_key=", &key);
	shmid = shmget(key, shm_size, IPC_CREAT | 0774);
	if (shmid == -1) {
		perror("Fail to get shm segment");
		return NULL;
	}
	printf("SHM with %luB created\n", shm_size);
	if ((addr = shmat(shmid, NULL, 0)) == (void*)(-1UL)) {
		perror("Fail to attach");
		return NULL;
	}

	dirty_pages(addr, shm_size);
	/* Mark for deletion, so it goes away on shmdt */
	shmctl(shmid, IPC_RMID, NULL);

	area = (struct area *)malloc(sizeof(*area));
	area->addr = addr;
	area->size = shm_size;
	return area;
}

static void walk_mems(struct area **mems, size_t mems_count)
{
	int i;
	printf("%d: walking memory\n", getpid());
	for (i = 0; i < mems_count; i++)
		if (mems[i])
			dirty_pages(mems[i]->addr, mems[i]->size);
}

static void work(int work_mode, struct area **mems, size_t mems_count)
{
	if (work_mode == 0)
		return;
	if (work_mode == 1)
		while(1) {
			sleep(1);
			if (should_rewalk) {
				should_rewalk = 0;
				walk_mems(mems, mems_count);
			}
		}

	if (work_mode == 2) {
		while(1) {
			walk_mems(mems, mems_count);
			sleep(1);
		}
	}
}

void rewalk_handler(int sig)
{
	if (sig != SIGUSR1)
		return;
	should_rewalk = 1;
}

int main(int argc, char **argv)
{
	int slot, i;
	size_t work_mode = 0;
	struct area *mems[MEMS_SIZE];
	struct sigaction sig = {.sa_handler=rewalk_handler, };

	sigaction(SIGUSR1, &sig,NULL);
	memset(mems, 0, sizeof(mems));
	find_size_for_prefix(argv, "total_mem=", &total_mem);
	printf("Total memory %luB\n", total_mem);
	mems[0] = prepare_private_anon(argv);
	mems[1] = prepare_shared_anon(argv);
	mems[2] = prepare_shm(argv);

	find_size_for_prefix(argv, "work_mode=", &work_mode);
	work(work_mode, mems, sizeof(mems)/sizeof(*mems));

	return 0;
}
