#!/bin/bash

while getopts :f:o: arg; do
	case $arg in
	f)	fs_dir="$OPTARG";;
	o)	ocfs2_disk="$OPTARG";;
	:)
		echo "$0:Option $OPTARG requires variable".
	exit 1
	;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

if [[ $fs_dir && $ocfs2_disk ]]; then

yes | mkfs.ocfs2 -N 16 --cluster-stack=pcmk --cluster-name=pacemaker $ocfs2_disk -F

mkdir $fs_dir

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
primitive o2cb ocf:ocfs2:o2cb \       
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive ocfs2 ocf:heartbeat:Filesystem \
        params directory="$fs_dir" fstype="ocfs2" device="$ocfs2_disk" options="acl" \
        op monitor interval="20" timeout="40" \       
        op start interval="0" timeout="60s" \
        op stop interval="0" timeout="60s"
group o2stage dlm clvm o2cb cmirror
clone c-o2stage o2stage meta interleave="true"
clone c-ocfs2 ocfs2 meta interleave="true" ordered="true"
colocation colo-ocfs2-o2stage inf: c-ocfs2 c-o2stage
order order-ocfs2-o2stage 0: c-o2stage c-ocfs2
EOF

else
  echo -f $fs_dir -o $ocfs2_disk
  echo "Wrong or missing arguments"
  echo "Usage: ocfs2_configuration.sh  -f fs_dir -o ocfs2_disk"
  echo "       fs_dir - directory, where OCFS2 dick will be mounted [/ocfs2]"
  echo "       ocfs2_disk - disk used as OCFS2 storage [/dev/disk/by-path/ip-10.20.5.173:3260-iscsi-iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a-lun-2-part1]"
fi
