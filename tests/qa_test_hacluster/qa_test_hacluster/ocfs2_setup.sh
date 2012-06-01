#!/bin/bash

while getopts :f:i:o:p: arg; do
	case $arg in
	f)	fs_dir="$OPTARG";;
	i)	iscsi_target="$OPTARG";;
	o)	ocfs2_disk="$OPTARG";;
	p)	iscsi_portal="$OPTARG";;
	:)
		echo "$0:Option $OPTARG requires variable".
	exit 1
	;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

if [[ $iscsi_target && ! -e /sbin/iscsiadm ]]; then
  zypper in -y open-iscsi
fi

  if [[ $iscsi_target && $iscsi_portal ]]; then
cat << EOF > /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.1996-04.de.suse:01:ha-automation
EOF
  insserv open-iscsi
  rcopen-iscsi restart
  iscsiadm -m discovery -t st -p $iscsi_portal
  iscsiadm -m node -T $iscsi_target -p $iscsi_portal:3260 --login
  iscsiadm -m node -T $iscsi_target -o update -n node.startup -v automatic
  sleep 10
fi

  mkdir $fs_dir

if [[ $fs_dir && $ocfs2_disk ]]; then
# select first machine in the group to format ocfs2 disk
  machine=$(echo $ROLE_0_NAME | sed -e 's/,.*//')
  if [[ $machine = $(hostname) ]]; then
    yes | mkfs.ocfs2 -N 4 --cluster-stack=pcmk --cluster-name=pacemaker $ocfs2_disk -F
    if [[ $iscsi_target && $iscsi_portal ]]; then
      crm_resource --locate --resource iscsi_ocfs2 2>&1 | grep -q 'running on'
      iscsi="$?"
      if [[ "$iscsi" != "0" ]]; then
crm configure << EOF
primitive iscsi_ocfs2 ocf:heartbeat:iscsi \
        params portal="$iscsi_portal:3260" target="$iscsi_target" udev="no" \
        op stop interval="0" timeout="120" \
        op start interval="0" timeout="120" \
        op monitor interval="120" timeout="30" \
        meta target-role="Started"
EOF
      fi
    fi

    crm_resource --locate --resource base-group 2>&1 | grep -q 'running on' 2>&1 > /dev/null
    base="$?"
    if [[ "$base" != "0" ]]; then
crm configure << EOF
primitive dlm ocf:pacemaker:controld \
        op start interval="0" timeout="90" \
        op stop interval="0" timeout="100" \
        op monitor interval="60" timeout="60"
primitive o2cb ocf:ocfs2:o2cb \
        op start interval="0" timeout="90" \
        op stop interval="0" timeout="100" \
        op monitor interval="60" timeout="60"
EOF
      if [[ $iscsi_target && $iscsi_portal ]]; then
crm configure << EOF
group base-group dlm o2cb iscsi_ocfs2
EOF
      else
crm configure << EOF
group base-group dlm o2cb
EOF
      fi
    fi

    crm_resource --locate --resource clusterfs 2>&1 | grep -q 'running on' 2>&1 > /dev/null
    clusterfs="$?"
    if [[ "$clusterfs" != "0" ]]; then
crm configure << EOF
primitive clusterfs ocf:heartbeat:Filesystem \
        params device="$ocfs2_disk" directory="$fs_dir" fstype="ocfs2" \
        op start interval="0" timeout="60" \
        op stop interval="0" timeout="60" \
        op monitor interval="20" timeout="40"
clone base-clone base-group \
        meta interleave="true" target-role="Started"
clone c-clusterfs clusterfs \
        meta interleave="true" target-role="Started"
colocation clusterfs-with-base inf: c-clusterfs base-clone
order base-then-clusterfs inf: base-clone c-clusterfs
EOF

      crm resource cleanup o2cb
    fi
    sleep 20
    crm resource cleanup base-clone
    crm resource cleanup c-clusterfs
  fi

else
  echo -f $fs_dir -i $iscsi_target -o $ocfs2_disk -p $iscsi_portal
  echo "Wrong or missing arguments"
  echo "Usage: ocfs2_setup.sh -f fs_dir -i iscsi_target -o ocfs2_disk -p iscsi_portal"
  echo "       fs_dir - directory, where OCFS2 dick will be mounted [/ocfs2]"
  echo "       iscsi_target - iscsi target name [iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a]"
  echo "       ocfs2_disk - disk used as OCFS2 storage [/dev/disk/by-path/ip-10.100.96.150:3260-iscsi-iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a-lun-2-part1]"
  echo "       iscsi_portal - IP of iscsi target machine [10.100.96.150]"
fi
