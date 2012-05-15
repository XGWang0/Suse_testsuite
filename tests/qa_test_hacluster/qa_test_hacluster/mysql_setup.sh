#!/bin/bash

while getopts :i:m:p: arg; do
	case $arg in
	i)	iscsi_target="$OPTARG";;
	m)	mysql_disk="$OPTARG";;
	p)	iscsi_portal="$OPTARG";;
	:)
		echo "$0:Option $OPTARG requires variable"
	exit 1;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

if [[ $iscsi_target && $iscsi_portal && $mysql_disk ]]; then

declare BE_QUIET=false

wait_for_resource ()
{
  while !crm_resource --locate --resource $1 2>&1 | grep -q 'running on';  do
    $BE_QUIET || echo -n '.' sleep 1
  done
}

  file -sL $mysql_disk | grep "ext3"
  ext=$?
  if [[ "$ext" != "0" ]]; then
    yes | mkfs.ext3 $mysql_disk
  fi

if [ ! -e /usr/bin/mysqld_safe ] ; then
  zypper in -y mysql
fi

  crm_resource --locate --resource fs_ext3
  ext=$?
    if [[ "$ext" != "0" ]]; then
crm configure << EOF
primitive fs_ext3 ocf:heartbeat:Filesystem \
        op monitor interval="20" timeout="40" start-delay="10" \
        params device="$mysql_disk" directory="/var/lib/mysql" fstype="ext3"
primitive iscsi_ext3 ocf:heartbeat:iscsi \
        params portal="$iscsi_portal:3260" target="$iscsi_target" udev="no" \
        op stop interval="0" timeout="120" \
        op start interval="0" timeout="120" \
        op monitor interval="120" timeout="30"
EOF
    fi

wait_for_resource fs_ext3

if [crm_resource --locate --resource 2>&1 | grep $(hostname)]; then
	rcmysql start
	chown -R mysql:mysql /var/lib/mysql
	rcmysql stop
fi

  crm_resource --locate --resource mysql
  mysql=$?
    if [[ "$mysql" != "0" ]]; then
crm configure << EOF
primitive mysql ocf:heartbeat:mysql \
        op monitor interval="10" timeout="120" start-delay="10" \
        params binary="/usr/bin/mysqld_safe" pid="/var/lib/mysql/mysqld.pid"
group g-mysql iscsi_ext3 fs_ext3 mysql \
        meta target-role="Started"
EOF
    fi

else
echo -i $iscsi_target -m $mysql_disk -p $iscsi_portal
echo "Wrong or missing arguments"
echo "Usage: mysql_setup.sh -c config -i iscsi_target -m mysql_disk -p iscsi_portal"
echo "       iscsi_target - iscsi target name [iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a]"
echo "       mysql_disk - disk used for mysql database [/dev/disk/by-path/ip-10.100.96.150:3260-iscsi-iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a-lun-6-part1]"
echo "       iscsi_portal - IP of iscsi target machine [10.100.96.150]"
fi
