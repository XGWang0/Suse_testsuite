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

MOUNT_POINT_UNCOM="/root/btrfs_uncompress"
MOUNT_POINT_COM="/root/btrfs_compress"

TESTDIR_COM="/root/com"
TESTDIR_UNCOM="/root/uncom"

DATA="/root/data"

if ! mkdir -p ${MOUNT_POINT_COM};then
    echo "can't mkdir directory"
    exit 1
fi

if ! mkdir -p ${MOUNT_POINT_UNCOM};then
    echo "can't mkdir directory"
    exit 1
fi

dd if=/dev/urandom of=${TESTDIR_COM} bs=10M count=30
if test $? -ne 0;then
    echo "can't dd "
    exit 1
fi

dd if=/dev/urandom of=${TESTDIR_UNCOM} bs=10M count=30
if test $? -ne 0;then
    echo "can't dd "
    exit 1
fi

mkfs.btrfs -f ${TESTDIR_UNCOM}
if test $? -ne 0;then
    echo "can't format uncompress block"
    exit 1
fi

mkfs.btrfs -f ${TESTDIR_COM}
if test $? -ne 0;then
    echo "can't format compress block"
    exit 1
fi

mount ${TESTDIR_COM} ${MOUNT_POINT_COM} -o compress-force
if test $? -ne 0;then
    echo "can't mount via compress option "
    exit 1
fi

mount ${TESTDIR_UNCOM} ${MOUNT_POINT_UNCOM}
if test $? -ne 0;then
    echo "can't mount via without option"
    exit 1
fi

btrfs filesystem sync ${MOUNT_POINT_COM}
if test $? -ne 0;then
    echo "can't sync compress file "
    exit 1
fi

btrfs filesystem sync ${MOUNT_POINT_UNCOM}
if test $? -ne 0;then
    echo "can't sync uncompress file "
    exit 1
fi

value_com=`btrfs filesystem show ${MOUNT_POINT_COM}|sed -n '/size.*dev.loop/{s/.*used //;s/\..*//;p;q}'`

value_uncom=`btrfs filesystem show ${MOUNT_POINT_UNCOM}|sed -n '/size.*dev.loop/{s/.*used //;s/\..*//;p;q}'`

if [ $value_com -eq $value_uncom ];then
    echo "the file of size is eq"
else
    echo "test failed!"
OB
fi

dd if=/dev/urandom of=${DATA} bs=10M count=10
if test $? -ne 0;then
    echo "can't dd "
    exit 1
fi

cp ${DATA} ${MOUNT_POINT_UNCOM}
cp ${DATA} ${MOUNT_POINT_COM}
btrfs filesystem sync ${MOUNT_POINT_UNCOM}
btrfs filesystem sync ${MOUNT_POINT_COM}

value_com=`btrfs filesystem show ${MOUNT_POINT_COM}|sed -n '/size.*dev.loop/{s/.*used //;s/\..*//;p;q}'`
value_uncom=`btrfs filesystem show ${MOUNT_POINT_UNCOM}|sed -n '/size.*dev.loop/{s/.*used //;s/\..*//;p;q}'`
if [ $value_com -lt $value_uncom ];then
    echo "test succeed!"
else
    echo "test faild!"
fi
umount  ${MOUNT_POINT_UNCOM}
umount  ${MOUNT_POINT_COM}
rm -rf ${MOUNT_POINT_UNCOM} ${MOUNT_POINT_COM} ${DATA} ${TESTDIR_UNCOM} ${TESTDIR_COM}
