#!/bin/bash

while getopts :d:m:s: arg; do
	case $arg in
	d)	disks="$OPTARG";;
	m)	mnt="$OPTARG";;
	s)	size="$OPTARG";;
	:)
		echo "$0:Option $OPTARG requires variable".
	exit 1
	;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

if [[ $disks && $size ]]; then

for i in $disks
do
  mkfs.xfs -f $i
done

pvcreate $disks
vgcreate -cn clvm1 $disks
lvcreate --name testmirror -m 1 -L $size clvm1 --alloc anywhere
vgchange -cy clvm1

yes | mkfs.ext3 /dev/clvm1/testmirror

mkdir $mnt

crm configure <<EOF
primitive clvm ocf:lvm2:clvmd \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive cmirror ocf:lvm2:cmirrord \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive dlm ocf:pacemaker:controld \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive vg1 ocf:heartbeat:LVM \
        params volgrpname="clvm1" \
        op start interval="0" timeout="30s" \
        op stop interval="0" timeout="30s"
primitive fs1 ocf:heartbeat:Filesystem \
        op monitor interval="20" timeout="40" start-delay="10" \
        op start interval="0" timeout="60s" \
        op stop interval="0" timeout="60s" \
        params device="/dev/clvm1/testmirror" directory="$mnt" fstype="ext3"
group clvmstage dlm clvm cmirror vg1
clone c-clvmstage clvmstage meta interleave="true"
EOF

else
  echo -d $disks -m $mnt -s $size
  echo "Wrong or missing arguments"
  echo "Usage: clvm_runner.sh -d disks_used -m mount_point -s size_of_lvm"
  echo "       disks_used - disks used for lvm [/dev/sdd1 /dev/sde1]"
  echo "       mount_point - lvm mount point [/mnt/ext3]"
  echo "       size_of_lvm - size of lvm [49G]"
fi
