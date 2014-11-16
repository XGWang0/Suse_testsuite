#!/bin/sh

FSTYPE="$1"
# TODO: shared config
TEST_DIR="/mnt/enospc-test-dir"

cd $TEST_DIR || exit 1
testfile=quick-test-"$FSTYPE"
touch "$testfile" || exit 1
rm -- "$testfile" || exit 1

echo "Quick test ok"
