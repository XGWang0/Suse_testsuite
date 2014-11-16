#!/bin/bash

# TODO: copied from run_xfstests.sh

# FSTYPE - type of filesystem to test
# MKFS_OPTS - options for mkfs when creating filesystem
# MOUNT_OPTS - options for mount when mounting filesystem
# DEV_SPACE - size of filesystem to create

# sane default
DEV_SPACE=${DEV_SPACE:-20GB}

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

echo "Starting setup for fs_enospc run."

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

# todo?
function cleanup
{
	if [ -n "$TEST_DEV" ]; then
		delete_partition "$TEST_DEV" 2>&1
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
			end = 0
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
	}
	if [ $? -ne 0 ]; then
		echo "Cannot find device with enough space ($1 required)"
		exit 1
	fi
}

if [ -n "$MOUNT_OPTS" ]; then
	export MOUNT_OPTIONS="-o $MOUNT_OPTS"
fi
export MKFS_OPTIONS="$MKFS_OPTS"
export TEST_DIR="/mnt/enospc-test-dir"
export TEST_DEV=`create_partition $TEST_DEV_SPACE`

# Failed to create partition? Exit.
if [ -z "$TEST_DEV" ]; then
	exit 1
fi

if [ ! -d "$TEST_MNT" ]; then
	mkdir -p "$TEST_DIR" 2>&1 || exit 1
fi

# XFS and btrfs need force to overwrite existing filesystems...
if [ "$FSTYPE" == "xfs" -o "$FSTYPE" == "btrfs" ]; then
	MKFS_OPTS_SPECIAL="-f"
fi

function wait_for_dev
{
	DEV="$1"
	WAITED=0
	echo "Waiting to $DEV to appear..."
	while [ ! -e "$DEV" ]; do
		sleep 1
		WAITED=$((WAITED+1))
		if [ $WAITED -ge 10 ]; then
			echo "Device $DEV did not appear!"
			exit 1
		fi
	done
	echo "Done."
}

wait_for_dev $TEST_DEV

mkfs.$FSTYP $MKFS_OPTS_SPECIAL $MKFS_OPTS $TEST_DEV 2>&1 || exit 1
mount -t $FSTYP $MOUNT_OPTS $TEST_DEV $TEST_DIR 2>&1 || exit 1
