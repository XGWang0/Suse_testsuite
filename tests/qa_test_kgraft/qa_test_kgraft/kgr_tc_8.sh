#!/bin/bash

# Test Case 8: Patch with replace-all

set -e
. $(dirname $0)/kgr_tc_functions.sh

kgr_tc_init "Test Case 8: Patch with replace-all"

N_PATCHES=4
kgr_tc_milestone "Compiling kGraft patch"
SOURCE_DIR="$(dirname $0)"
PATCH_DIR="/tmp/kgraft-patch/replace-all"
KERN_FLAVOR=$(uname -r | sed 's/^.*-//')
KERN_ARCH=$(uname -m)
for N in $(seq $N_PATCHES) final; do
    PATCH_SUBDIR="$PATCH_DIR/patch_replace-all_$N"
    mkdir -p "$PATCH_SUBDIR"
    sed "s/@@SEQ_N@@/-replace-all_$N/g" "$SOURCE_DIR"/kgr_tc_Makefile.tpl > "$PATCH_SUBDIR"/Makefile
    sed "s/@@SEQ_N@@/_replace_all_$N/g" "$SOURCE_DIR"/kgr_tc-kgraft_patch_getpid-replace-all.c.tpl \
        > "$PATCH_SUBDIR"/kgraft_patch_getpid-replace-all_$N.c
    make -C /usr/src/linux-obj/$KERN_ARCH/$KERN_FLAVOR M="$PATCH_SUBDIR" O="$PATCH_SUBDIR"
done

for N in $(seq 1 $N_PATCHES) final; do
    PATCH_SUBDIR="$PATCH_DIR/patch_replace-all_$N"
    kgr_tc_milestone "Inserting getpid patch $N"
    insmod "$PATCH_SUBDIR"/kgraft_patch_getpid-replace-all_$N.ko

    kgr_tc_milestone "STOP/CONT processes (patch $N)"
    kgr_kick_processes

    kgr_tc_milestone "Wait for completion (patch $N)"
    if ! kgr_wait_complete 61; then
        kgr_dump_blocking_processes
        kgr_tc_abort "patching didn't finish in time (patch $N)"
    fi
done

for N in $(seq 1 $N_PATCHES); do
    PATCH_SUBDIR="$PATCH_DIR/patch_8_$N"
    kgr_tc_milestone "Removing getpid patch $N"
    rmmod kgraft_patch_getpid-replace-all_$N
    if test $? -ne 0;then
        kgr_tc_abort "FAILED to remove the kernel module kgraft_patch_getpid_8_$N"
    fi
done

kgr_tc_milestone "Try to remove getpid patch final"
rmmod kgraft_patch_getpid-replace-all_final
if test $? -eq 0;then
    kgr_tc_abort "It should not be possible to remove the kernel module kgraft_patch_getpid_8_final"
fi


# test passed if execution reached this line
# failures beyond this point are not test case failures
trap - EXIT
kgr_tc_milestone "Call hooks before exit"
call_recovery_hooks
kgr_tc_milestone "TEST PASSED, reboot to remove the kGraft patch"
