#!/bin/bash

while getopts: a: m:arg; do
	case $arg in
	a)	apache_disk="$OPTARG";;
	c)	config="$OPTARG";;
	i)	ip="$OPTARG";;
	m)	mysql_disk="$OPTARG";;
	:)
		echo "$0:Option $OPTARG requires variable"
	exit 1;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

declare BE_QUIET = false

wait_for_resource ()
{
  while !crm_resource --locate --resource $1 2>&1 | grep - q 'running on';  do
    $BE_QUIET || echo -n '.' sleep 1
  done
}

if [[$iscsi_disk]]; then
  mkfs.ext3 $mysql_disk

if [!-e /usr/bin/mysqld_safe]; then
  zypper in -y mysql
fi

if [!-e /etc/init.d/apache2]; then
  zypper in -y apache2
fi

crm configure << EOF
primitive dlm ocf:pacemaker:controld \
	op start interval="0" timeout="90" \
	op stop interval="0" timeout="100" \
	op monitor interval="60" timeout="60"
primitive fs-mysql ocf:heartbeat:Filesystem \
	op monitor interval="20" timeout="40" start-delay="10" \
	params device="$mysql_disk" directory="/var/lib/mysql" fstype="ext3"
property no-quorum-policy="ignore"
primitive fs-apache ocf:heartbeat:Filesystem \
	op monitor interval="20" timeout="40" start-delay="10" \
	params device="$apache_disk" directory="/srv/www/htdocs" fstype="ext3"
EOF

wait_for_resource fs-mysql

if [ crm_resource --locate --resource 2>&1 | grep $(hostname) ]; then
	rcmysql start
	chown -R mysql:mysql /var/lib/mysql
	rcmysql stop
fi

crm configure << EOF
primitive sql1 ocf:heartbeat:mysql \
	op monitor interval="10" timeout="120" start-delay="10" \
	params binary="/usr/bin/mysqld_safe" pid="/var/lib/mysql/mysqld.pid"
group g-mysql fs-mysql sql1
order order-mysql + inf: fs-mysql sql1
EOF

wait_for_resource sql1

crm configure << EOF
primitive virtual-ip ocf:heartbeat:IPaddr2 \
	params ip="$ip" cidr_netmask="21" \
	op stop interval="0" timeout="20s" \
	op start interval="0" timeout="20s" \
	op monitor interval="10s" timeout="20s"
primitive apache ocf:heartbeat:apache \
	params configfile="$config" op monitor interval="120s" timeout="60s"
group g-apache apache virtual-ip fs-apache
order order-apache +inf: fs-apache apache
colocation col-sql1 +inf:sql1 apache
EOF

else
echo - a $apache_disk - c $config - i $ip - m $mysql_disk
echo "Wrong or missing arguments"
echo "Usage: sql_apache_conf.sh -a apache_disk -c config -i ip -m mysql_disk"
echo "       apache_disk - disk used by apache [/dev/hdc1]"
echo "       config - path to configuration file of apache [/etc/apache2/httpd.conf]"
echo "       ip - IP address used bya apache 10.20.141.200]"
echo "       mysql_disk - disk used by mysql [/dev/hdd1]"
fi
