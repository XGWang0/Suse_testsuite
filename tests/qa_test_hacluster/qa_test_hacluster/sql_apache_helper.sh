#!/bin/bash

if [ ! -e /usr/bin/mysqld_safe ]; then
  zypper in -y mysql
fi

if [ ! -e /etc/init.d/apache2 ]; then
  zypper in -y apache2
fi

declare BE_QUIET=false

wait_for_resource()
{
	while ! crm_resource --locate --resource $1 2>&1 | grep -q 'running on'; do
		$BE_QUIET || echo -n '.'
		chown -R mysql:mysql /var/lib/mysql
		sleep 1
	done
}

wait_for_resource fs-mysql

rcmysql start
rcmysql stop

wait_for_resource fs-mysql

rcmysql start
rcmysql stop

wait_for_resource sql1
