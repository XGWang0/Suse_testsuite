#!/bin/sh
# Copyright (C) 2007-2008 Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Test vgsplit command options for validity

. /usr/share/qa/qa_test_lvm2/lib/test

aux prepare_devs 5

for mdatype in 1 2
do

pvcreate -M$mdatype $(cat $TESTDIR/DEVICES)

# ensure name order does not matter
# NOTE: if we're using lvm1, we must use -M on vgsplit
vgcreate -M$mdatype $vg1 $(cat $TESTDIR/DEVICES)
vgsplit -M$mdatype $vg1 $vg2 $dev1
vgremove $vg1 $vg2

vgcreate -M$mdatype $vg2 $(cat $TESTDIR/DEVICES)
vgsplit -M$mdatype $vg2 $vg1 $dev1
vgremove $vg1 $vg2

# vgsplit accepts new vg as destination of split
# lvm1 -- bz244792
vgcreate -M$mdatype $vg1 $(cat $TESTDIR/DEVICES)
vgsplit $vg1 $vg2 $dev1 1>$TESTDIR/err
grep "New volume group \"$vg2\" successfully split from \"$vg1\"" $TESTDIR/err 
vgremove $vg1 $vg2

# vgsplit accepts existing vg as destination of split
vgcreate -M$mdatype $vg1 $dev1 $dev2 
vgcreate -M$mdatype $vg2 $dev3 $dev4 
vgsplit $vg1 $vg2 $dev1 1>$TESTDIR/err
grep "Existing volume group \"$vg2\" successfully split from \"$vg1\"" $TESTDIR/err 
vgremove $vg1 $vg2

# vgsplit accepts --maxphysicalvolumes 128 on new VG
vgcreate -M$mdatype $vg1 $dev1 $dev2 
vgsplit --maxphysicalvolumes 128 $vg1 $vg2 $dev1 
check vg_field $vg2 max_pv 128 
vgremove $vg1 $vg2

# vgsplit accepts --maxlogicalvolumes 128 on new VG
vgcreate -M$mdatype $vg1 $dev1 $dev2 
vgsplit --maxlogicalvolumes 128 $vg1 $vg2 $dev1 
check vg_field $vg2 max_lv 128 
vgremove $vg1 $vg2

# vgsplit rejects split because max_pv of destination would be exceeded
vgcreate -M$mdatype --maxphysicalvolumes 2 $vg1 $dev1 $dev2
vgcreate -M$mdatype --maxphysicalvolumes 2 $vg2 $dev3 $dev4
not vgsplit $vg1 $vg2 $dev1 2>$TESTDIR/err;
grep "^  Maximum number of physical volumes (2) exceeded" $TESTDIR/err
vgremove $vg1 $vg2

# vgsplit rejects split because maxphysicalvolumes given with existing vg
vgcreate -M$mdatype --maxphysicalvolumes 2 $vg1 $dev1 $dev2 
vgcreate -M$mdatype --maxphysicalvolumes 2 $vg2 $dev3 $dev4 
not vgsplit --maxphysicalvolumes 2 $vg1 $vg2 $dev1 2>$TESTDIR/err;
grep "^  Volume group \"$vg2\" exists, but new VG option specified" $TESTDIR/err 
vgremove $vg1 $vg2

# vgsplit rejects split because maxlogicalvolumes given with existing vg
vgcreate -M$mdatype --maxlogicalvolumes 2 $vg1 $dev1 $dev2 
vgcreate -M$mdatype --maxlogicalvolumes 2 $vg2 $dev3 $dev4 
not vgsplit --maxlogicalvolumes 2 $vg1 $vg2 $dev1 2>$TESTDIR/err
grep "^  Volume group \"$vg2\" exists, but new VG option specified" $TESTDIR/err 
vgremove $vg1 $vg2

# vgsplit rejects split because alloc given with existing vg
vgcreate -M$mdatype --alloc cling $vg1 $dev1 $dev2 
vgcreate -M$mdatype --alloc cling $vg2 $dev3 $dev4 
not vgsplit --alloc cling $vg1 $vg2 $dev1 2>$TESTDIR/err;
grep "^  Volume group \"$vg2\" exists, but new VG option specified" $TESTDIR/err 
vgremove $vg1 $vg2

# vgsplit rejects split because clustered given with existing vg
vgcreate -M$mdatype --clustered n $vg1 $dev1 $dev2 
vgcreate -M$mdatype --clustered n $vg2 $dev3 $dev4 
not vgsplit --clustered n $vg1 $vg2 $dev1 2>$TESTDIR/err
grep "^  Volume group \"$vg2\" exists, but new VG option specified" $TESTDIR/err 
vgremove $vg1 $vg2

# vgsplit rejects vg with active lv
pvcreate -M$mdatype -ff $dev3 $dev4 
vgcreate -M$mdatype $vg1 $dev1 $dev2 
vgcreate -M$mdatype $vg2 $dev3 $dev4 
lvcreate -l 4 -n $lv1 $vg1 
not vgsplit $vg1 $vg2 $dev1 2>$TESTDIR/err;
grep "^  Logical volumes in \"$vg1\" must be inactive\$" $TESTDIR/err 
vgremove -f $vg1 $vg2

# vgsplit rejects split because max_lv is exceeded
vgcreate -M$mdatype --maxlogicalvolumes 2 $vg1 $dev1 $dev2 
vgcreate -M$mdatype --maxlogicalvolumes 2 $vg2 $dev3 $dev4 
lvcreate -l 4 -n $lv1 $vg1 
lvcreate -l 4 -n $lv2 $vg1 
lvcreate -l 4 -n $lv3 $vg2 
vgchange -an $vg1 $vg2
not vgsplit $vg1 $vg2 $dev1 2>$TESTDIR/err;
grep "^  Maximum number of logical volumes (2) exceeded" $TESTDIR/err 
vgremove -f $vg1 $vg2

# vgsplit verify default - max_lv attribute from new VG is same as source VG" \
vgcreate -M$mdatype $vg1 $dev1 $dev2 
lvcreate -l 4 -n $lv1 $vg1 
vgchange -an $vg1 
vgsplit $vg1 $vg2 $dev1 
check compare_vg_field $vg1 $vg2 max_lv 
vgremove -f $vg1 $vg2

# vgsplit verify default - max_pv attribute from new VG is same as source VG" \
vgcreate -M$mdatype $vg1 $dev1 $dev2 
lvcreate -l 4 -n $lv1 $vg1 
vgchange -an $vg1 
vgsplit $vg1 $vg2 $dev1 
check compare_vg_field $vg1 $vg2 max_pv 
vgremove -f $vg1 $vg2

# vgsplit verify default - vg_fmt attribute from new VG is same as source VG" \
vgcreate -M$mdatype $vg1 $dev1 $dev2 
lvcreate -l 4 -n $lv1 $vg1 
vgchange -an $vg1 
vgsplit $vg1 $vg2 $dev1 
check compare_vg_field $vg1 $vg2 vg_fmt 
vgremove -f $vg2 $vg1

# vgsplit rejects split because PV not in VG
vgcreate -M$mdatype $vg1 $dev1 $dev2 
vgcreate -M$mdatype $vg2 $dev3 $dev4 
lvcreate -l 4 -n $lv1 $vg1 
lvcreate -l 4 -n $lv2 $vg1 
vgchange -an $vg1 
not vgsplit $vg1 $vg2 $dev3 2>$TESTDIR/err;
vgremove -f $vg2 $vg1
done

# ONLY LVM2 metadata
# setup PVs" '
pvcreate --metadatacopies 0 $dev5

# vgsplit rejects to give away pv with the last mda copy
vgcreate $vg1 $dev5 $dev2  
lvcreate -l 10 -n $lv1  $vg1 
lvchange -an $vg1/$lv1 
check pvlv_counts $vg1 2 1 0 
not vgsplit  $vg1 $vg2 $dev5;
check pvlv_counts $vg1 2 1 0 
vgremove -ff $vg1

# vgsplit rejects split because metadata types differ
pvcreate -ff -M1 $dev3 $dev4 
pvcreate -ff $dev1 $dev2 
vgcreate -M1 $vg1 $dev3 $dev4 
vgcreate $vg2 $dev1 $dev2 
not vgsplit $vg1 $vg2 $dev3 2>$TESTDIR/err;
grep "^  Metadata types differ" $TESTDIR/err 
vgremove $vg1 $vg2