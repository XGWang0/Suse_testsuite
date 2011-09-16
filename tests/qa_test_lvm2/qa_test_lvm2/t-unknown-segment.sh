#!/bin/sh
# Copyright (C) 2009 Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

. /usr/share/qa/qa_test_lvm2/lib/test

aux prepare_vg 4

lvcreate -l 1 -n $lv1 $vg
lvcreate -l 2 -m 1 -n $lv2 $vg

vgcfgbackup -f $TESTDIR/bak0 $vg
sed -e 's,striped,unstriped,;s,mirror,unmirror,' -i.orig $TESTDIR/bak0
vgcfgrestore -f $TESTDIR/bak0 $vg

# we have on-disk metadata with unknown segments now
not lvchange -a y $vg/$lv1 # check that activation is refused

vgcfgbackup -f $TESTDIR/bak1 $vg
cat $TESTDIR/bak1
sed -e 's,unstriped,striped,;s,unmirror,mirror,' -i.orig $TESTDIR/bak1
vgcfgrestore -f $TESTDIR/bak1 $vg
vgcfgbackup -f $TESTDIR/bak2 $vg

egrep -v 'description|seqno|creation_time|Generated' < $TESTDIR/bak0.orig > $TESTDIR/a
egrep -v 'description|seqno|creation_time|Generated' < $TESTDIR/bak2 > $TESTDIR/b
diff -u $TESTDIR/a $TESTDIR/b
