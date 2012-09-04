#!/bin/bash

while getopts :p: arg; do
	case $arg in
	p)	port="$OPTARG"
	;;
	:)
		echo "$0:Option $OPTARG requires variable".
	exit 1
	;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

if [[ $port ]]; then

grep CTS-AUTO-SETUP-WAS-HERE /etc/syslog-ng/syslog-ng.conf 2>&1 > /dev/null
rc="$?"

if [ $rc != 0 ]; then
echo "# CTS-AUTO-SETUP-WAS-HERE
destination ha_tcp { tcp($ROLE_0_NAME port($port));};
filter f_ha_tcp  { facility(daemon); };
log { source(src); filter(f_ha_tcp); destination(ha_tcp); };" >> /etc/syslog-ng/syslog-ng.conf
else
   printf "\n - Syslog-ng is already configured"
fi

rcsyslog restart

else
  echo -p $port
  echo "Wrong or missing arguments"
  echo "Usage: cts_helper -p port"
  echo "       port - port to be used for communication"
fi
