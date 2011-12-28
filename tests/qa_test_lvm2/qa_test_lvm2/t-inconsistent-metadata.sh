#!/bin/bash
# Copyright (C) 2008 Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

. /usr/share/qa/qa_test_lvm2/lib/test

aux prepare_vg 3 12

lvcreate -m 1 -l 1 -n mirror $vg
lvcreate -l 1 -n resized $vg
lvchange -a n $vg/mirror

aux backup_dev $(cat $TESTDIR/DEVICES)

init() {
	aux restore_dev $(cat $TESTDIR/DEVICES)
	lvs -o lv_name,lv_size --units k $vg | tee $TESTDIR/lvs.out
	grep resized $TESTDIR/lvs.out | not grep 8192
	lvresize -L 8192K $vg/resized
	aux restore_dev $dev1
}

check() {
	lvs -o lv_name,lv_size --units k $vg | tee $TESTDIR/lvs.out
	grep resized $TESTDIR/lvs.out | grep 8192
}

# vgscan fixes up metadata
init
vgscan 2>&1 | tee $TESTDIR/cmd.out
grep "Inconsistent metadata found for VG $vg" $TESTDIR/cmd.out
vgscan 2>&1 | tee $TESTDIR/cmd.out
not grep "Inconsistent metadata found for VG $vg" $TESTDIR/cmd.out
check

#FIXME: Not implemented
# vgdisplay fixes
#init
#vgdisplay 2>&1 | tee $TESTDIR/cmd.out
#grep "Volume group \"$vg\" inconsistent" $TESTDIR/cmd.out
#vgdisplay 2>&1 | tee $TESTDIR/cmd.out
#not grep "Volume group \"$vg\" inconsistent" $TESTDIR/cmd.out
#check

# lvs fixes up
init
lvs 2>&1 | tee $TESTDIR/cmd.out
grep "Inconsistent metadata found for VG $vg" $TESTDIR/cmd.out
vgdisplay 2>&1 | tee $TESTDIR/cmd.out
not grep "Inconsistent metadata found for VG $vg" $TESTDIR/cmd.out
check

#FIXME: Not implemented
# vgs fixes up as well
#init
#vgs 2>&1 | tee $TESTDIR/cmd.out
#grep "Inconsistent metadata found for VG $vg" $TESTDIR/cmd.out
#vgs 2>&1 | tee $TESTDIR/cmd.out
#not grep "Inconsistent metadata found for VG $vg" $TESTDIR/cmd.out
#check

echo Check auto-repair of failed vgextend - metadata written to original pv but not new pv
vgremove -f $vg
pvremove -ff $(cat $TESTDIR/DEVICES)
pvcreate $(cat $TESTDIR/DEVICES)
aux backup_dev $dev2
vgcreate $vg $dev1
vgextend $vg $dev2
aux restore_dev $dev2
should check compare_fields vgs $vg vg_mda_count pvs $dev2 vg_mda_count