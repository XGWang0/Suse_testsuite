#!/bin/bash

while getopts :l:p:s:t: arg; do
	case $arg in
	l)	log_file="$OPTARG"
	;;
	p)	port="$OPTARG"
	;;
	s)	stonith="$OPTARG"
	;;
	t)	tests="$OPTARG"
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

if [[ $log_file && $port && $stonith && $tests ]]; then

touch $log_file

key=`cat /usr/share/qa/keys/ssh/ssh_host_rsa_key.pub | sed s/root@vulture//g`

node=$ROLE_1_NAME
for i in `echo ${node} | tr ',' '\n'` ; do
   str=${str},${i}
   grep ${i} /root/.ssh/known_hosts 2>&1 > /dev/null
   machine=$?
   if [ $machine != 0 ]; then
     echo ${i} $key>> /root/.ssh/known_hosts
   fi
done

if [ ! -e /usr/share/pacemaker/tests/cts/cluster_test ]; then
  zypper in -y libpacemaker-devel
fi

nodes=$(echo $ROLE_1_NAME | sed "s/,/ /g")

echo "Nodes to be tested: $nodes"

grep CTS-AUTO-SETUP-WAS-HERE /etc/syslog-ng/syslog-ng.conf 2>&1 > /dev/null
rc=$?
if [ $rc != 0 ]; then
echo "# CTS-AUTO-SETUP-WAS-HERE
source s_tcp { tcp(port($port) max-connections(99999)); };
filter f_ha  { facility(daemon); };
destination ha_local { file($log_file perm(0644)); };
log { source(src); source(s_tcp); filter(f_ha); destination(ha_local); };" >> /etc/syslog-ng/syslog-ng.conf
fi

rcsyslog restart

cat<<EOF > ~/.cts
# CTS Test data
CTS_master="$ROLE_0_NAME"
CTS_stack="corosync"
CTS_node_list="$nodes"
CTS_logfile="$log_file"
CTS_logport="$port"
CTS_logfacility=daemon
CTS_asked_once=1
CTS_adv=""
CTS_stonith=$stonith
CTS_stonith_args=""
CTS_boot="1"
EOF

python /usr/share/pacemaker/tests/cts/CTSlab.py -L $log_file --syslog-facility daemon --no-unsafe-tests --stack corosync --at-boot 1 --stonith-type $stonith $tests --nodes "$nodes"

else
  echo -l $log_file -p $port -s $stonith -t $tests
  echo "Wrong or missing arguments"
  echo "Usage: cts_runner -l log_file -p port -t tests"
  echo "       log_file - log file where logs will be stored [/var/log/cluster_test.log]"
  echo "       port - port to be used for communication"
  echo "       stonith - stonith RA [sbd]"
  echo "       tests - number of tests to be done [500]"
fi
