#!/bin/sh

FSTYPE="$1"
shift
testdirname="$1"
shift

if [ -z "$FSTYPE" ]; then
	echo "usage: $0 fsname testdir [fs_mark args...]"
	exit 1
fi

if [ -z "$testdirname" ]; then
	echo "usage: $0 fsname testdir [fs_mark args...]"
	exit 1
fi

# TODO: shared config
TEST_DIR="/mnt/enospc-test-dir"

cd $TEST_DIR || exit 1

mkdir "$testdirname"

fs_mark -d . "$@"

cd ..
rm -rf -- "$testdirname"
# directory must be gone
cd "$testdirname" && exit 1
