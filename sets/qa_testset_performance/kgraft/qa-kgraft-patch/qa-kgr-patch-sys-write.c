/*
 * sys_write
 *
 *  Copyright (c) 2013-2014 SUSE
 *   Authors: Lance Wang
 */
/*
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

/*
 * NOTE  For sle12 3.12.28-4
 */
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/kgraft.h>
#include <linux/kallsyms.h>
#include <linux/sched.h>
#include <linux/types.h>
#include <linux/capability.h>
#include <linux/ptrace.h>
#include <linux/syscalls.h>
#include <linux/file.h>
#include <linux/fs.h>
#include <asm/processor.h>

#include "qa-kgr-patch-syscall.h"

/* inline functions copied from read_write.c */

static inline loff_t file_pos_read(struct file *file)
{
        return file->f_pos;
}

static inline void file_pos_write(struct file *file, loff_t pos)
{
        file->f_pos = pos;
}

KGR_SYSCALL_DEFINE3(v1, write, unsigned int, fd, const char __user *, buf,
		size_t, count)
{
	struct fd f = fdget(fd);
	ssize_t ret = -EBADF;

	if (f.file) {
		loff_t pos = file_pos_read(f.file);
		ret = vfs_write(f.file, buf, count, &pos);
		if (ret >= 0)
			file_pos_write(f.file, pos);
		fdput(f);
	}

#ifndef QA_TEST_TO_BE_DELETED
    do {
        static unsigned int whistle_count;
        if (++whistle_count % 1024 == 0) {
            printk("%s: 1024 times called again\n", __func__);
        }
    } while(0);
#endif

	return ret;
}

static struct kgr_patch patch = {
	.name = "qa_sys_write_patcher",
	.owner = THIS_MODULE,
	.patches = {
		KGR_PATCH(SyS_write, KGR_PATHED_SYSCALL_NAME(v1, write), true),
		KGR_PATCH_END
	}
};

static int __init kgr_patcher_init(void)
{
	return kgr_patch_kernel(&patch);
}

static void __exit kgr_patcher_cleanup(void)
{
	kgr_patch_remove(&patch);
}

module_init(kgr_patcher_init);
module_exit(kgr_patcher_cleanup);

MODULE_LICENSE("GPL");
