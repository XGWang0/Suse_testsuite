#!/bin/bash

# Test Case 3: Patch under cpu pressure
# Patch a heavily hammered function in kernel

set -e
. $(dirname $0)/kgr_tc_functions.sh
. $(dirname $0)/kgr_tc_workload.sh

kgr_tc_init "Test Case 6: Patch under cpu pressure"

kgr_tc_milestone "Compiling kGraft patch"
SOURCE_DIR="$(dirname $0)"
PATCH_DIR="/tmp/kgraft-patch/6"
mkdir -p "$PATCH_DIR"
sed "s/@@SEQ_N@@/_6/g" "$SOURCE_DIR"/kgr_tc_Makefile.tpl > "$PATCH_DIR"/Makefile
sed "s/@@SEQ_N@@/_6/g" "$SOURCE_DIR"/kgr_tc-kgraft_patch_getpid.c.tpl \
	> "$PATCH_DIR"/kgraft_patch_getpid_6.c
KERN_VERSION=$(uname -r | sed 's/-[^-]*$//')
KERN_FLAVOR=$(uname -r | sed 's/^.*-//')
KERN_ARCH=$(uname -m)
make -C /usr/src/linux-$KERN_VERSION-obj/$KERN_ARCH/$KERN_FLAVOR M="$PATCH_DIR" O="$PATCH_DIR"

add_workload cpu
kgr_tc_milestone "Staring workload"
start_workload

kgr_tc_milestone "Inserting getpid patch"
insmod "$PATCH_DIR"/kgraft_patch_getpid_6.ko
if [ ! -e /sys/kernel/kgraft/qa_getpid_patcher_6 ]; then
   kgr_tc_abort "don't see qa_getpid_patcher_6 in kGraft sys directory"
fi

kgr_tc_milestone "STOP/CONT processes"
kgr_kick_processes

kgr_tc_milestone "Wait for completion"
if ! kgr_wait_complete 61; then
    kgr_dump_blocking_processes
    kgr_tc_abort "patching didn't finish in time"
fi

# test passed if execution reached this line
# failures beyond this point are not test case failures
trap - EXIT
kgr_tc_milestone "Call hooks before exit"
call_recovery_hooks
kgr_tc_milestone "TEST PASSED, reboot to remove the kGraft patch"
