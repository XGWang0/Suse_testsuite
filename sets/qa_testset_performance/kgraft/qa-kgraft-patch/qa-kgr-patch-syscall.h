/*
 *  Copyright (c) 2013-2014 SUSE
 *   Authors: Lance Wang
 */
/*
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 */

#define KGR_PATHED_SYSCALL_NAME(ver, name) SyS_##name##__kgr_patched_##ver

#define KGR_SYSCALL_DEFINE0(sname, ver)  TODO

#define __KGR_SYSCALL_DEFINEx(x, name, ver, ...) __SYSCALL_DEFINEx(x, _##name##__kgr_patched_##ver, __VA_ARGS__)
#define KGR_SYSCALL_DEFINE1(ver, name, ...) __KGR_SYSCALL_DEFINEx(1, name, ver, __VA_ARGS__)
#define KGR_SYSCALL_DEFINE2(ver, name, ...) __KGR_SYSCALL_DEFINEx(2, name, ver, __VA_ARGS__)
#define KGR_SYSCALL_DEFINE3(ver, name, ...) __KGR_SYSCALL_DEFINEx(3, name, ver, __VA_ARGS__)
#define KGR_SYSCALL_DEFINE4(ver, name, ...) __KGR_SYSCALL_DEFINEx(4, name, ver, __VA_ARGS__)
#define KGR_SYSCALL_DEFINE5(ver, name, ...) __KGR_SYSCALL_DEFINEx(5, name, ver, __VA_ARGS__)
#define KGR_SYSCALL_DEFINE6(ver, name, ...) __KGR_SYSCALL_DEFINEx(6, name, ver, __VA_ARGS__)

