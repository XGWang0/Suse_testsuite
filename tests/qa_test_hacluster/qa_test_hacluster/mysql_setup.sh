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

if [[ $iscsi_target && ! -e /sbin/iscsiadm ]]; then
  zypper in -y open-iscsi
fi

if [[ $iscsi_target && $iscsi_portal ]]; then
cat<<EOF > /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.1996-04.de.suse:01:ha-automation
EOF

  fi

  if [ ! -e /usr/bin/mysqld_safe ] ; then
    zypper in -y mysql
  fi

#in case iscsi is used, iscsi target is checked and logged into, then it is set to autoconnect on iscsi daemon restart
  if [[ $iscsi_target && $iscsi_portal && ! -e $mysql_disk ]]; then
    insserv open-iscsi
    rcopen-iscsi restart
    iscsiadm -m discovery -t st -p $iscsi_portal
    iscsiadm -m node -T $iscsi_target -p $iscsi_portal:3260 --login
    iscsiadm -m node -T $iscsi_target -o update -n node.startup -v automatic
    sleep 5
  fi

# select first machine in the group to format ext3 disk
  machine=$(echo $ROLE_0_NAME | sed -e 's/,.*//')
  if [[ $machine = $(hostname) ]]; then
    yes | mkfs.ext3 $mysql_disk
    mount $mysql_disk /var/lib/mysql
    chown -R mysql:mysql /var/lib/mysql
    rcmysql start
    rcmysql stop
    umount /var/lib/mysql
    sleep 5
    
# deployment of iscsi primitive if there is none and iscsi is to be used
    if [[ $iscsi_target && $iscsi_portal ]]; then
      crm_resource --locate --resource iscsi_ext3 2>&1 | grep -q 'running on' 2>&1 > /dev/null
      iscsi="$?"
      if [[ "$iscsi" != "0" ]]; then
        crm configure << EOF
primitive iscsi_ext3 ocf:heartbeat:iscsi \
        params portal="$iscsi_portal:3260" target="$iscsi_target" udev="no" \
        op stop interval="0" timeout="120" \
        op start interval="0" timeout="120" \
        op monitor interval="120" timeout="30"
EOF
        fi
    fi
    
# deployment of primitive which handles mounting of disks to propper place
    crm_resource --locate --resource fs_ext3 2>&1 | grep -q 'running on' 2>&1 > /dev/null
    fs="$?"
    if [[ "$fs" != "0" ]]; then
       crm configure << EOF
primitive fs_ext3 ocf:heartbeat:Filesystem \
        op monitor interval="20" timeout="40" start-delay="10" \
        op stop interval="0" timeout="60" \
        op start interval="0" timeout="60" \
        params device="$mysql_disk" directory="/var/lib/mysql" fstype="ext3"
EOF
    fi

    crm_resource --locate --resource g-mysql 2>&1 | grep -q 'running on' 2>&1 > /dev/null
    mysql="$?"
    if [[ "$mysql" != "0" ]]; then
crm configure << EOF
primitive mysql ocf:heartbeat:mysql \
        op monitor interval="10" timeout="120" start-delay="10" \
        op stop interval="0" timeout="120" \
        op start interval="0" timeout="120" \
        params binary="/usr/bin/mysqld_safe" pid="/var/lib/mysql/mysqld.pid"
EOF
    fi
    if [[ $iscsi_target && $iscsi_portal ]]; then
crm configure << EOF
group g-mysql iscsi_ext3 fs_ext3 mysql \
        meta target-role="Started"
EOF
    else
      crm_resource --locate --resource g-mysql 2>&1 | grep -q 'running on' 2>&1 > /dev/null
      g_mysql="$?"
      if [[ "$g_mysql" != "0" ]]; then
crm configure << EOF
group g-mysql fs_ext3 mysql \
        meta target-role="Started"
EOF
      fi
    fi
    wait_for_resource g-mysql
    crm resource cleanup g-mysql
  fi

else
echo -i $iscsi_target -m $mysql_disk -p $iscsi_portal
echo "Wrong or missing arguments"
echo "Usage: mysql_setup.sh -i iscsi_target -m mysql_disk -p iscsi_portal"
echo "       iscsi_target - iscsi target name [iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a]"
echo "       mysql_disk - disk used for mysql database [/dev/disk/by-path/ip-10.100.96.150:3260-iscsi-iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a-lun-6-part1]"
echo "       iscsi_portal - IP of iscsi target machine [10.100.96.150]"
fi
