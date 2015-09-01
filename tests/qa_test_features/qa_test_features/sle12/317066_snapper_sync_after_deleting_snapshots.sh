#!/bin/bash
# ****************************************************************************
# Copyright © 2015 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************

cat << EOF
This is a test for FATE#317066, written in bash.

The test results are determined by the return value of this script:

  0	PASSED
  1	FAILED
 11	INTERNAL ERROR
 22	SKIPPED

Happy testing!

EOF

sleep 3


MOUNT_POINT="/abuild"
TEST_DEVICE="/dev/sdb1"

TESTDIR_NAME='test'
TESTFILE_NAME='zerodata'

TESTDIR=${MOUNT_POINT}/${TESTDIR_NAME}
TESTFILE=${MOUNT_POINT}/${TESTDIR_NAME}/${TESTFILE_NAME}

test_init()
{
    if ! [ -b ${TEST_DEVICE} ]; then
        exit 22
    fi
    while mount | grep ${TEST_DEVICE};
    do
        umount ${TEST_DEVICE}
    done
    mkfs.btrfs -f -q ${TEST_DEVICE}
    if [ $? -ne 0 ]; then
        echo "Formatting ${TEST_DEVICE} to BtrFS is failed." >&2
        exit 11
    fi
    mkdir -pv ${MOUNT_POINT}
    mount ${TEST_DEVICE} ${MOUNT_POINT}
    if [ $? -ne 0 ]; then
        echo "Mountting ${TEST_DEVICE} to ${MOUNT_POINT} is failed." >&2
        exit 11
    fi
    btrfs subvol create ${TESTDIR}
    if ! [ -d ${TESTDIR} ]; then
        echo "TESTDIR is not a directory" >&2
        exit 11
    fi

    mount -t btrfs -o subvol=${TESTDIR_NAME} ${TEST_DEVICE} ${TESTDIR}

    snapper -c 'test' -t 'default' create-config ${TESTDIR}

    dd bs=330M count=1 if=/dev/urandom of=${TESTFILE}

    btrfs fi sync ${TESTDIR}

echo "testing -- start point"
echo "testing -- Before All of testing"
echo "========================================"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}
echo "========================================"
echo 
}

test_cleanup()
{
    snapper -c 'test' delete-config
    while mount | grep ${TEST_DEVICE};
    do
        umount ${TEST_DEVICE}
    done
}


test_btrfs_cli ()
{

#
# Create snapshots
#


echo "CLI testing -- start point"
echo "CLI testing -- Before Create Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}


    for i in `seq 1`
    do
        btrfs subvolume snapshot ${TESTDIR} ${TESTDIR}/../${TESTDIR_NAME}-pre-${i}
        dd bs=330M count=1 if=/dev/urandom of=${TESTFILE}
        btrfs subvolume snapshot ${TESTDIR} ${TESTDIR}/../${TESTDIR_NAME}-post-${i}
    done
    sync

echo "CLI testing -- After Create Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}

sleep 5
#
# Delete snapshots
#

echo "CLI testing -- Delete snapshots start"
echo "CLI testing -- Before Remove Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}
    
    for i in `seq 10` ; do
        btrfs subvolume delete --commit-after ${TESTDIR}/../${TESTDIR_NAME}-pre-${i}
        btrfs subvolume delete --commit-after ${TESTDIR}/../${TESTDIR_NAME}-post-${i}
    done

echo "CLI testing -- After Remove Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}


sleep 5
}
test_btrfs_snapper()
{

#
# Create snapshots
#
echo "Snapper testing -- Create snapshots start"
echo "Snapper testing -- Before Create Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}
	

    for i in `seq 10` ; do
        snapper -c 'test' create --command "dd bs=1M count=250 if=/dev/urandom of=${TESTFILE}" --desc "generate trash"
    done

    btrfs filesystem sync ${MOUNT_POINT}

echo "Snapper testing -- After Create Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}

#
# Delete snapshots
#

echo "Snapper testing -- Delete snapshots start"
echo "Snapper testing -- Before Delete Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}

    startid=$(snapper -c 'test' ls | grep "generate trash" | head -n 1 | awk -F "|" '{print $2}' |xargs echo)

sleep 10;
set -x
    snapper -c "test" delete --sync ${startid}-1000
    if [ $? -ne 0 ]; then
        echo "snapper delete --sync option testing failed" 2>&1
        exit 1
    fi
set +x

echo "Snapper testing -- After remove Snapshots"
    btrfs filesystem df ${MOUNT_POINT}
    btrfs filesystem show ${MOUNT_POINT}

}

test_btrfs_snapper_root()
{

#
# Create snapshots
#
echo "Snapper testing -- Create snapshots start"
echo "Snapper testing -- Before Create Snapshots"
    btrfs filesystem df /
    btrfs filesystem show /
	

    for i in `seq 10` ; do
        snapper create --command "dd bs=1M count=250 if=/dev/urandom of=/test" --desc "generate trash"
    done

    btrfs filesystem sync /

echo "Snapper testing -- After Create Snapshots"
    btrfs filesystem df /
    btrfs filesystem show /

#
# Delete snapshots
#

echo "Snapper testing -- Delete snapshots start"
echo "Snapper testing -- Before Delete Snapshots"
    btrfs filesystem df /
    btrfs filesystem show /

    startid=$(snapper ls | grep "generate trash" | head -n 1 | awk -F "|" '{print $2}' |xargs echo)

sleep 10;
set -x
    snapper delete --sync ${startid}-1000
    if [ $? -ne 0 ]; then
        echo "snapper delete --sync option testing failed" 2>&1
        exit 1
    fi
set +x

echo "Snapper testing -- After remove Snapshots"
    btrfs filesystem df /
    btrfs filesystem show /

}

echo "-------------------------------------------"
echo "=============Testing initial==============="
test_init
echo "=============Testing initial Finish========"
echo "-------------------------------------------"
echo "============BtrFS CLI testing=============="
test_btrfs_cli
echo "============BtrFS CLI testing Finish======="
echo "-------------------------------------------"
echo "==============Snapper testing=============="
test_btrfs_snapper
echo "==============Snapper testing Finish======="
echo "-------------------------------------------"
echo "=============Testing cleanup==============="
test_cleanup
echo "=============Testing cleanup Finish========"
echo "-------------------------------------------"


echo "-------------------------------------------"
echo "==============Snapper testing=============="
test_btrfs_snapper_root
echo "==============Snapper testing Finish======="
echo "-------------------------------------------"
exit 0

