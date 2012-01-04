#!/bin/bash
# Copyright (C) 2010 Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

. /usr/share/qa/qa_test_lvm2/lib/test

extend() {
	lvextend --use-policies --config "activation { snapshot_extend_threshold = $1 }" $vg/snap
}

write() {
	mkdir $TESTDIR/mnt
	mount /dev/$vg/snap $TESTDIR/mnt
	dd if=/dev/zero of=$TESTDIR/mnt/file$1 bs=1k count=$2
	umount $TESTDIR/mnt
	rm -rf $TESTDIR/mnt
}

percent() {
	lvs $vg/snap -o snap_percent --noheadings | cut -c4- | cut -d. -f1
}

which mkfs.ext2 || exit 200

aux prepare_vg 2
aux prepare_dmeventd

lvcreate -l 8 -n base $vg
mkfs.ext2 /dev/$vg/base

lvcreate -s -l 4 -n snap $vg/base
lvchange --monitor y $vg/snap

write 1 4096
pre=`percent`
sleep 10 # dmeventd only checks every 10 seconds :(
post=`percent`

test $pre = $post
write 2 5000
pre=`percent`
sleep 10 # dmeventd only checks every 10 seconds :(
post=`percent`
test $pre -gt $post
