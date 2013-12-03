#!/bin/bash

# Script to run xfstests
# Take following environment variables as input:
# FSTYPE - type of filesystem to test
# MKFS_OPTS - options for mkfs when creating filesystem
# MOUNT_OPTS - options for mount when mounting filesystem
# TEST_NAME - name of the test used for output file name
# BLACKLIST - name of the file that contain blacklisted testcases 
#             (use as -X <file>)

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

if [ ! -z "$BLACKLIST" ] ; then
	exists=0
	for d in $FSTYPE generic shared ; do
		[ -r "$XFSTESTS_PATH/tests/$d/$BLACKLIST" ] && exists=1
	done
	if [ $exists = "0" ] ; then
		echo "Blacklist file '$BLACKLIST' does not exist in searched locations!" >&2
		exit 1
	fi
	BLACKLIST="-X $BLACKLIST"
fi

echo "Starting setup for xfstests run." >$SETUP_LOG

function delete_partition
{
	DEV=$1

	case $DEV in
		/dev/cciss/*)
			BASE_DEV=${DEV%%p[0-9]*}
			NUM=${DEV:$((${#BASE_DEV}+1))} ;;
		*)
			BASE_DEV=${DEV%%[0-9]*}
			NUM=${DEV:${#BASE_DEV}} ;;
	esac
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
			base *= 1000000000
		} else if (unit == "G") {
			base *= 1000000
		} else if (unit == "M") {
			base *= 1000
		}
		return base
	}

	BEGIN	{ space = space_to_kb(space) }
	/^$/	{
			end++
			if (size - end > space) {
				if (partlabel == "msdos") {
					if (seenextended) {
						type = "logical"
					} else {
						type = "extended"
						num = 4
					}
				} else {
					type = "primary"
				}
				# We use GB in the end to avoid problems with
				# precision in which parted displays partition
				# information
				print dev,end/1000000 "GB",(end+space)/1000000 "GB",num+1,type,size/1000000 "GB"
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
			partlabel = $6
			seenextended = 0
			next
		}
		{
			if (skip == 0) {
				num = $1
				if ($6 == "extended" || index($7, "type=0f") > 0) {
					seenextended = 1
					end = space_to_kb($2)
				} else {
					end = space_to_kb($3)
				}
			}
		}
	' | {
		read DEV START END NUM TYPE DEVSIZE
		echo "$DEV $START $END $NUM $TYPE $DEVSIZE" >&2
		if [ -z "$DEV" ]; then
			exit 1
		fi
		# Need to create extended partition?
		if [ "$TYPE" == "extended" ]; then
			parted -s -a minimal "$DEV" \
				"mkpart extended $START $DEVSIZE" >/dev/null \
				|| exit 1
			TYPE="logical"
		fi
		parted -s -a minimal "$DEV" \
			"mkpart $TYPE $START $END" >/dev/null || exit 1
		case $DEV in
			/dev/cciss/*) echo "${DEV}p$NUM" ;;
			*) echo "$DEV$NUM" ;;
		esac
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

# Failed to create partition? Exit.
if [ -z "$SCRATCH_DEV" -o -z "$TEST_DEV" ]; then
	exit 1
fi

if [ ! -d "$TEST_DIR" ]; then
	mkdir -p "$TEST_DIR" >>$SETUP_LOG 2>&1 || exit 1
fi
if [ ! -d "$SCRATCH_MNT" ]; then
	mkdir -p "$SCRATCH_MNT" >>$SETUP_LOG 2>&1 || exit 1
fi

# XFS and btrfs need force to overwrite existing filesystems...
if [ "$FSTYP" == "xfs" -o "$FSTYP" == "btrfs" ]; then
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
./check $BLACKLIST -g auto &>$RESULT_BASE/xfstests_output
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
