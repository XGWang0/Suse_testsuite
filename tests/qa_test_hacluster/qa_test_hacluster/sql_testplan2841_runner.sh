#!/bin/bash

while getopts :i: arg; do
	case $arg in
	i)	iscsi_disk="$OPTARG";;
	:)
		echo "$0:Option $OPTARG requires variable".
	exit 1
	;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

declare BE_QUIET=false

wait_for_resource()
{
	while ! crm_resource --locate --resource $1 2>&1 | grep -q 'running on'; do
		$BE_QUIET || echo -n '.'
		chown -R mysql:mysql /var/lib/mysql
		sleep 1
	done
}

if [[ $iscsi_disk ]]; then

mkfs.ext3 $iscsi_disk

if [ ! -e /usr/bin/mysqld_safe ]; then
  zypper in -y mysql
fi

crm configure <<EOF
primitive fs1 ocf:heartbeat:Filesystem \
	op monitor interval="20" timeout="40" start-delay="10" \
	params device="$iscsi_disk" directory="/var/lib/mysql" fstype="ext3"
property no-quorum-policy="ignore"
EOF

wait_for_resource

rcmysql start
rcmysql stop

crm resource migrate fs1 2> /dev/null

wait_for_resource

rcmysql start
rcmysql stop

crm configure <<EOF
primitive sql1 ocf:heartbeat:mysql \
	op monitor interval="10" timeout="120" start-delay="10" \
	params binary="/usr/bin/mysqld_safe" pid="/var/lib/mysql/mysqld.pid"
colocation col-sql1 +inf: sql1 fs1
order order-sql1 +inf: fs1 sql1
EOF

wait_for_resource sql1
crm_mon -1

crm resource migrate fs1 2> /dev/null
wait_for_resource sql1
crm_mon -1

else
  echo -i $iscsi_disk
  echo "Wrong or missing arguments"
  echo "Usage: sql_testplan2841_conf.sh -i iscsi_disk"
  echo "       iscsi_disk - disk used for storage of MySQL data [/dev/disk/by-path/ip-10.20.138.1:3260-iscsi-iqn.2010-11.suse.qa:1d1fc26d-1bf8-47be-b67c-c7bcdb676508-lun-2-part1]"
fi
