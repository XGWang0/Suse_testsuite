#!/bin/bash

# Script to run xfstests
# Take following environment variables as input:
# FSTYPE - type of filesystem to test
# MKFS_OPTS - options for mkfs when creating filesystem
# MOUNT_OPTS - options for mount when mounting filesystem
# TEST_NAME - name of the test used for output file name

XFSTESTS_PATH=/usr/share/qa/qa_test_xfstests/xfstests/
TEST_DEV_SPACE=20GB
SCRATCH_DEV_SPACE=20GB

#
# Configuration section ends here
#

if [ -z "$FSTYPE" ]; then
	echo "Filesystem type must be specified!" >&2
	exit 1
fi

if [ -z "$TESTS_LOGDIR" ]; then
	TESTS_LOGDIR="/var/log/qa/"
fi
RESULT_BASE="$TESTS_LOGDIR"/xfstests/xfstests-"$TEST_NAME"-`date +"%Y-%m-%d-%H-%M-%S"`
SETUP_LOG="$RESULT_BASE/setup.log"

if [ ! -d "$RESULT_BASE" ]; then
	mkdir -p "$RESULT_BASE" || exit 1
fi

echo "Starting setup for xfstests run." >$SETUP_LOG

function delete_partition
{
	DEV=$1

	BASE_DEV=${DEV%%[0-9]*}
	NUM=${DEV:${#BASE_DEV}}
	echo "Cleaning up partition $NUM on device $BASE_DEV"
	parted -s $BASE_DEV "rm $NUM"
}

function cleanup
{
	if [ -n "$SCRATCH_DEV" ]; then
		delete_partition "$SCRATCH_DEV" >>$SETUP_LOG 2>&1
	fi
	if [ -n "$TEST_DEV" ]; then
		delete_partition "$TEST_DEV" >>$SETUP_LOG 2>&1
	fi
}

trap "cleanup" 0 1 2 3 15

function create_partition
{
	parted -l -m | awk -v "space=$1" -F ':' '
	function space_to_kb(space,    base, unit)
	{
		base = strtonum(space);
		unit = substr(space, length(space) - 1, 1)
		if (unit == "T") {
			base *= 1024*1024*1024
		} else if (unit == "G") {
			base *= 1024*1024
		} else if (unit == "M") {
			base *= 1024
		}
		return base
	}

	BEGIN	{ space = space_to_kb(space) }
	/^$/	{
			if (size - end > space) {
				print dev,end "kB",end+space "kB",num+1
				exit
			}
			next
		}
	/^BYT;$/{
			skip = 0
			getline
			if ($3 == "loop") {
				skip = 1
				next
			}
			dev = $1
			size = space_to_kb($2)
			next
		}
		{
			if (skip == 0) {
				end = space_to_kb($3)
				num = $1
			}
		}
	' | {
		read DEV START END NUM
		if [ -z "$DEV" ]; then
			exit 1
		fi
		parted -s -a minimal "$DEV" "mkpart logical $START $END" >/dev/null || exit 1
		echo "$DEV$NUM"
	} 2>>$SETUP_LOG
	if [ $? -ne 0 ]; then
		echo "Cannot find device with enough space ($1 required)" >>$SETUP_LOG
		exit 1
	fi
}

if [ -n "$MOUNT_OPTS" ]; then
	export MOUNT_OPTIONS="-o $MOUNT_OPTS"
fi
export MKFS_OPTIONS="$MKFS_OPTS"
export FSTYP="$FSTYPE"
export RESULT_BASE
export TEST_DIR="/mnt/test-dir"
export SCRATCH_MNT="/mnt/scratch-dir"
export TEST_DEV=`create_partition $TEST_DEV_SPACE`
export SCRATCH_DEV=`create_partition $SCRATCH_DEV_SPACE`

if [ ! -d "$TEST_DIR" ]; then
	mkdir -p "$TEST_DIR" >>$SETUP_LOG 2>&1 || exit 1
fi
if [ ! -d "$SCRATCH_MNT" ]; then
	mkdir -p "$SCRATCH_MNT" >>$SETUP_LOG 2>&1 || exit 1
fi

# XFS needs force to overwrite existing filesystems... 
if [ "$FSTYP" == "xfs" ]; then
	MKFS_OPTS_SPECIAL="-f"
fi

function wait_for_dev
{
	DEV="$1"
	WAITED=0
	echo "Waiting to $DEV to appear..." >>$SETUP_LOG
	while [ ! -e "$DEV" ]; do
		sleep 1
		WAITED=$((WAITED+1))
		if [ $WAITED -ge 10 ]; then
			echo "Device $DEV did not appear!" >>$SETUP_LOG
			exit 1
		fi
	done
	echo "Done." >>$SETUP_LOG
}

wait_for_dev $TEST_DEV
wait_for_dev $SCRATCH_DEV

mkfs.$FSTYP $MKFS_OPTS_SPECIAL $MKFS_OPTS $TEST_DEV >>$SETUP_LOG 2>&1 || exit 1
mount -t $FSTYP $MOUNT_OPTS $TEST_DEV $TEST_DIR >>$SETUP_LOG 2>&1 || exit 1
echo "Running xfstests..." >>$SETUP_LOG
pushd $XFSTESTS_PATH >>$SETUP_LOG 2>&1
./check -g auto &>$RESULT_BASE/xfstests_output
popd >>$SETUP_LOG 2>&1
echo "xfstests done" >>$SETUP_LOG
umount $TEST_DIR >>$SETUP_LOG 2>&1

# Copy log files for each testcase to a separate directory
pushd "$RESULT_BASE" >>$SETUP_LOG 2>&1
for DIR in *; do
	if [ -d "$DIR" ]; then
		pushd "$DIR"
		for FILE in *; do
			TESTNUM=${FILE%%.*}
			if [ ! -d "$TESTNUM" ]; then
				mkdir "$TESTNUM"
				cp "$XFSTESTS_PATH/tests/$DIR/$TESTNUM.out" "$TESTNUM/"
			fi
			mv "$FILE" "$TESTNUM/"
		done
		popd
	fi
done >>$SETUP_LOG 2>&1
popd >>$SETUP_LOG 2>&1
