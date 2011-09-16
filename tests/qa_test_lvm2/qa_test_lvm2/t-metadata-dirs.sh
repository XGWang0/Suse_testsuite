#!/bin/sh
# Copyright (C) 2011 Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

. /usr/share/qa/qa_test_lvm2/lib/test


aux prepare_devs 3
pvcreate --metadatacopies 0 $(cat $TESTDIR/DEVICES)

not vgcreate $vg $(cat $TESTDIR/DEVICES)

aux lvmconf "metadata/dirs = [ \"/etc/lvm/mda\" ]"

vgcreate $vg $dev1
vgs
check vg_field $vg vg_mda_count 1
vgremove -ff $vg

vgcreate $vg $(cat $TESTDIR/DEVICES)
check vg_field $vg vg_mda_count 1

vgremove -ff $vg
pvcreate --metadatacopies 1 --metadataignore y $dev1
vgcreate $vg $(cat $TESTDIR/DEVICES)
check vg_field $vg vg_mda_count 2

vgremove -ff $vg
pvcreate --metadatacopies 1 --metadataignore n $dev1
vgcreate $vg $(cat $TESTDIR/DEVICES)
check vg_field $vg vg_mda_count 2

vgremove -ff $vg
pvcreate --metadatacopies 0 $dev1

aux lvmconf "metadata/dirs = [ \"$TESTDIR/mda\", \"$TESTDIR/mda2\" ]"
vgcreate $vg $(cat $TESTDIR/DEVICES)
check vg_field $vg vg_mda_count 2
