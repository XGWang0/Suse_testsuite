#!/bin/bash

# Test Case 3: Patch under pressure
# Patch a heavily hammered function in kernel

set -e
. $(dirname $0)/kgr_tc_functions.sh
kgr_tc_init "Test Case 3: Patch under pressure"

kgr_tc_milestone "Compiling kGraft patch"
SOURCE_DIR="$(dirname $0)"
PATCH_DIR="/tmp/kgraft-patch/"
mkdir -p "$PATCH_DIR"
cp -v "$SOURCE_DIR"/kgr_tc_3-Makefile "$PATCH_DIR"/Makefile
cp -v "$SOURCE_DIR"/kgr_tc_3-kgraft_patch_getpid.c "$PATCH_DIR"/kgraft_patch_getpid.c
KERN_VERSION=$(uname -r | sed 's/-[^-]*$//')
KERN_FLAVOR=$(uname -r | sed 's/^.*-//')
KERN_ARCH=$(uname -m)
make -C /usr/src/linux-$KERN_VERSION-obj/$KERN_ARCH/$KERN_FLAVOR M="$PATCH_DIR" O="$PATCH_DIR"

kgr_tc_milestone "Compiling call_getpid"
gcc -o "$PATCH_DIR"/call_getpid "$SOURCE_DIR"/kgr_tc_3-call_getpid.c

kgr_tc_milestone "Running call_getpid"
"$PATCH_DIR"/call_getpid &
push_recovery_fn "kill $!"

kgr_tc_milestone "Inserting getpid patch"
insmod "$PATCH_DIR"/kgraft_patch_getpid.ko
if [ ! -e /sys/kernel/kgraft/qa_getpid_patcher ]; then
   kgr_tc_abort "don't see qa_getpid_patcher in kGraft sys directory"
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
kgr_tc_milestone "Terminating call_getpid"
kill %?call_getpid || true

trap - EXIT
kgr_tc_milestone "TEST PASSED, reboot to remove the kGraft patch"
