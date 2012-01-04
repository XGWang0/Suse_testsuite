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

aux prepare_vg 4

#lvcreate -m 1 --mirrorlog disk --ig -L 1 -n mirror $vg
lvcreate -m 1 --mirrorlog disk -L 1 -n mirror $vg
not lvconvert -m 2 --mirrorlog core $vg/mirror $dev3 2>&1 | tee $TESTDIR/errs
grep "two steps" $TESTDIR/errs

lvconvert -m 2 $vg/mirror $dev3
lvconvert --mirrorlog core $vg/mirror
not lvconvert -m 1 --mirrorlog disk $vg/mirror $dev3 2>&1 | tee $TESTDIR/errs
grep "two steps" $TESTDIR/errs

#FIXME: Not implemented
#not lvconvert -m 1 --mirrorlog mirrored $vg/mirror $dev3 $dev4 2>&1 | tee $TESTDIR/errs
#grep "two steps" $TESTDIR/errs
