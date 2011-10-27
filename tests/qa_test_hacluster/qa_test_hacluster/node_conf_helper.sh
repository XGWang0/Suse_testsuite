#!/bin/bash

devel_hae_11_sp1=`grep devel_hae_11_sp1 qa_test_hacluter-config |cut -d= -f2`

while getopts :b:di:l:m:p:r:s:t: arg; do
	case $arg in
	b)	bindnetaddr="$OPTARG";;
	d)	devel=TRUE;;
	i)	iscsi_sbd_host="$OPTARG";;
	l)	login="$OPTARG";;
	m)	mcastaddr="$OPTARG";;
	p)	password="$OPTARG";;
	s)	sbd_disk="$OPTARG";;
	t)	target="$OPTARG";;
	:)
		echo "$0:Option $OPTARG requires variable".
	exit 1
	;;
	\?)
		echo "Wrong option $OPTARG was ignored".
	;;
	esac
done

if [[ $bindnetaddr && $mcastaddr && $iscsi_sbd_host && $sbd_disk && $target ]]; then

sntp -P no -r pool.ntp.org

zypper up

if [ ! -e /sbin/iscsiadm ]; then
  zypper in -y open-iscsi
fi

if [ "$devel" = "TRUE" ]; then
  zypper lr | grep ha-devel 2>&1 > /dev/null
  ha_devel=$?
  if [ "$ha_devel" != "0" ]; then
    zypper ar $devel_hae_11_sp1 ha-devel
  fi

  zypper ref

  zypper se pacemaker | grep "i |" 2>&1 > /dev/null
  pacemaker=$?
  if [ "$pacemaker" != "0" ]; then
    zypper in -y pacemaker ocfs2-tools cmirrord lvm2-clvm
  fi

else
  zypper se -t pattern | grep ha_sles | grep "i |" 2>&1 > /dev/null
  ha_sles=$?
  if [ "$ha_sles" != "0" ]; then
    zypper in -y -t pattern ha_sles
  fi
fi

#cat<<EOF > /etc/iscsi/initiatorname.iscsi
#InitiatorName=iqn.1996-04.de.suse:01:ha-automation
#EOF

grep ICSCI-AUTO-SETUP-WAS-HERE /etc/iscsi/iscsid.conf 2>&1 > /dev/null
rc=$?
if [ "$rc" != "0" ]; then
echo "# ISCSI-AUTO-SETUP-WAS-HERE
node.session.auth.username = $login
node.session.auth.password = $password" >> /etc/iscsi/iscsid.conf
fi

cat<<EOF  > /etc/corosync/corosync.conf
echo aisexec {
        #Group to run aisexec as. Needs to be root for Pacemaker

        group:  root

        #User to run aisexec as. Needs to be root for Pacemaker

        user:   root

}
service {
        #Default to start mgmtd with pacemaker

        use_mgmtd:      yes

        ver:    0

        name:   pacemaker

}
totem {
        #The mode for redundant ring. None is used when only 1 interface specified, otherwise, only active or passive may be choosen

        rrp_mode:       none

        #How long to wait for join messages in membership protocol. in ms

        join:   60

        #The maximum number of messages that may be sent by one processor on receipt of the token.

        max_messages:   20

        #The virtual synchrony filter type used to indentify a primary component. Change with care.

        vsftype:        none

        #Timeout for a token lost. in ms

        token:  3000

        #How long to wait for consensus to be achieved before starting a new round of membership configuration.

        consensus:      4000

        #HMAC/SHA1 should be used to authenticate all message

        secauth:        off

        #How many token retransmits should be attempted before forming a new configuration.

        token_retransmits_before_loss_const:    10

        #How many threads should be used to encypt and sending message. Only have meanings when secauth is turned on

        threads:        0

        #The only valid version is 2

        version:        2

        interface {
                #Network Address to be bind for this interface setting

                bindnetaddr:    $bindnetaddr

                #The multicast address to be used

                mcastaddr:      $mcastaddr

                #The multicast port to be used

                mcastport:      5405

                #The ringnumber assigned to this interface setting

                ringnumber:     0

        }
        #To make sure the auto-generated nodeid is positive

        clear_node_high_bit:    yes

}
logging {
        #Log to a specified file

        to_logfile:     no

        #Log to syslog

        to_syslog:      yes

        #Whether or not turning on the debug information in the log

        debug:  off

        #Log timestamp as well

        timestamp:      on

        #Log to the standard error output

        to_stderr:      yes

        #Logging file line in the source code as well

        fileline:       off

        #Facility in syslog

        syslog_facility:        daemon

}
amf {
        #Enable or disable AMF 

        mode:   disable
}
EOF


cat<<EOF > /etc/init.d/ais
#! /bin/sh

# init file for configuring iscsi and starting openais
# For SuSE and cousins
### BEGIN INIT INFO
# Provides:                   ais
# Required-Start:             \$local_fs \$network
# Required-Stop:              \$local_fs \$network
# Default-Start:              2 3 5
# Default-Stop:               2 3 5
# Short-Description:          Configures network cards for IPv6 testing
# Description:                IPv6 testing configuration
# X-UnitedLinux-Default-Enabled: yes
### END INIT INFO

# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2, or (at your option) any later
# version. 
# You should have received a copy of the GNU General Public License (for
# example COPYING); if not, write to the Free Software Foundation, Inc., 675
# Mass Ave, Cambridge, MA 02139, USA.

    case \$1 in
        start)
            rcopen-iscsi start
	    iscsiadm -m discovery -t st -p $iscsi_sbd_host
            iscsiadm -m node -T $target -p $iscsi_sbd_host:3260 --login
            sleep 5
            rcopenais start
            echo
            ;;
        stop)
            rcopenais stop
            iscsiadm -m node -T $target -p $iscsi_sbd_host:3260 --logout
            echo
            ;;
        reload)
            \$0 stop
            \$0 start
            echo
            ;;
        report)
            rcopen-iscsi report
            rcopenais report
            echo
            ;;
        restart)
            \$0 stop
            \$0 start
            echo
            ;;
        status)
            rcopen-iscsi status
            rcopenais status
            ;;
        *)
            echo "Usage: \$0 {start|stop|reload|report|restart|status}"
            RETVAL=1
    esac

    exit \$RETVAL

rc_exit
EOF

declare BE_QUIET=false

status_long()
{
	$BE_QUIET && return
	echo -n "  $1..."
}

status_done()
{
	$BE_QUIET && return
	echo "done"
}

wait_for_cluster()
{
	status_long "Waiting for cluster"
	while ! crm_mon -1 | grep -qi online; do
		$BE_QUIET || echo -n "."
		sleep 5
	done
	status_done
}

rcopen-iscsi start

iscsiadm -m discovery -t st -p $iscsi_sbd_host

chmod +x /etc/init.d/ais

insserv ais

ln -s /etc/init.d/ais /usr/sbin/rcais

iscsiadm -m node -T $target -p $iscsi_sbd_host:3260 --login

cat<<EOF > /etc/sysconfig/sbd
SBD_DEVICE="$sbd_disk"
SBD_OPTS="-W"
EOF

sbd -d /dev/sda1 allocate $(hostname)

rcais restart

wait_for_cluster

crm configure primitive sbd_stonith stonith:external/sbd meta target-role="Started" op monitor interval="15" timeout="15" params sbd_device="$sbd_disk"

else
  echo -b $bindnetaddr -d -m $mcastaddr -i $iscsi_sbd_host -l $login -p $password -s $sbd_disk -t $target
  echo "Wrong or missing arguments"
  echo "Usage: main_script -b bindnetaddr -d -m mcastaddr -i iscsi_sbd_host -l login -p password -s sbd_disk -t target"
  echo "       bindnetaddr - address used for corosync [10.20.3.0]"
  echo "       -d signalls ha devel repo is used"
  echo "       mcastaddr - multicast addresss for cluster [239.50.1.1]"
  echo "       iscsi_sbd_host - IP address of your iscsi shared disk provider [10.20.5.173]"
  echo "       login - login for iscsi target"
  echo "       password - password for iscsi target"
  echo "       sbd_disk - disk used for sbd/STONITH [/dev/disk/by-path/ip-10.20.5.173:3260-iscsi-iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a-lun-5-part1]"
  echo "       target - [iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a]"
fi
