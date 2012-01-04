#!/bin/bash

while getopts :o: arg; do
	case $arg in
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

if [[ $ocfs2_disk ]]; then

zypper se | grep ctdb | grep "i |" 2>&1 > /dev/null
ctdb=$?
if [ "$ctdb" != "0" ]; then
  zypper in -y ctdb
fi

zypper se | grep "| samba" | grep "i |" 2>&1 > /dev/null
samba=$?
if [ "$samba" != "0" ]; then
  zypper in -y samba samba-winbind
fi

mkdir /mnt/samba

yes | mkfs.ocfs2 -N 16 --cluster-stack=pcmk --cluster-name=pacemaker $ocfs2_disk -F

crm configure <<EOF
primitive clvm ocf:lvm2:clvmd \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive cmirror ocf:lvm2:cmirrord \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive ctdb ocf:heartbeat:CTDB \
        op monitor interval="10" timeout="20" \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s" \
        params ctdb_recovery_lock="/mnt/samba/ctdb.lock"
primitive dlm ocf:pacemaker:controld \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive o2cb ocf:ocfs2:o2cb \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive ocfs2 ocf:heartbeat:Filesystem \
        params directory="/mnt/samba" fstype="ocfs2" device="$ocfs2_disk" options="acl" \
        op monitor interval="20" timeout="40" \
        op start interval="0" timeout="60s" \
        op stop interval="0" timeout="60s"
group o2stage dlm clvm o2cb cmirror
clone c-ctdb ctdb \
        meta interleave="true" target-role="Started"
clone c-o2stage o2stage \
        meta interleave="true"
clone c-ocfs2 ocfs2 \
        meta interleave="true" ordered="true"
colocation colo-ocfs2-o2stage inf: c-ocfs2 c-o2stage
colocation ctdb-with-fs inf: c-ctdb c-ocfs2
order order-ocfs2-o2stage 0: c-o2stage c-ocfs2
order start-ctdb-after-ocfs2 inf: c-ocfs2 c-ctdb
EOF

else
  echo -o $ocfs2_disk
  echo "Wrong or missing arguments"
  echo "Usage: ctdb_tesplan2837.sh -o ocfs2_disk"
  echo "       ocfs2_disk - disk to be used as ocfs2 [/dev/disk/by-path/ip-10.20.5.173:3260-iscsi-iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a-lun-2-part1]"
fi
