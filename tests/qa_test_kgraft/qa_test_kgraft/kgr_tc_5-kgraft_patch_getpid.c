/*
 * kgraft_patch_getpid - patch getpid with the same code
 *
 * We patch two (arbitrarily chosen) functions at once...
 *
 *  Copyright (c) 2013-2014 SUSE
 *   Authors: Jiri Kosina
 *	      Vojtech Pavlik
 *	      Jiri Slaby
 */

/*
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
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

#include <asm/processor.h>

/*
 * This all should be autogenerated from the patched sources
 */

asmlinkage long kgr_sys_getpid@@SEQ_N@@(void)
{
	return task_tgid_vnr(current);
}

static struct kgr_patch patch = {
	.name = "qa_getpid_patcher@@SEQ_N@@",
	.owner = THIS_MODULE,
	.patches = {
		KGR_PATCH(sys_getpid, kgr_sys_getpid@@SEQ_N@@, true),
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
