#!/bin/bash



#devel_hae_11_sp1=`grep devel_hae_11_sp1 qa_test_hacluter-config | cut -d= -f2`
#devel_hae_11_sp2=`grep devel_hae_11_sp2 qa_test_hacluter-config | cut -d= -f2`

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

while getopts :b:i:s:t: arg; do
	case $arg in
	a)	addon="$OPTARG";;
	b)	bindnetaddr="$OPTARG";;
	i)	iscsi_host="$OPTARG";;
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

sntp -P no -r ntp.suse.cz

if [[ $iscsi_host && ! -e /sbin/iscsiadm ]]; then
  zypper in -y open-iscsi
fi

if [[ $bindnetaddr && $sbd_disk ]]; then
  zypper se -t pattern | grep ha_sles | grep "i |" 2>&1 > /dev/null
  ha_sles=$?
  if [ "$ha_sles" != "0" ]; then
    zypper ar $addon sle-hae
    zypper in -l -y -t product sle-hae
    zypper in -y -t pattern ha_sles
  fi
  if [ $iscsi_host ]; then

cat<<EOF > /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.1996-04.de.suse:01:ha-automation
EOF

    if [[ $login && $password ]]; then
      grep ICSCI-AUTO-SETUP-WAS-HERE /etc/iscsi/iscsid.conf 2>&1 > /dev/null
      rc=$?
      if [[ "$rc" != "0" ]]; then
      echo "# ISCSI-AUTO-SETUP-WAS-HERE
      node.session.auth.username = $login
      node.session.auth.password = $password" >> /etc/iscsi/iscsid.conf
      fi
    fi
  fi

  if [[ $iscsi_host && $target ]]; then
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
	    iscsiadm -m discovery -t st -p $iscsi_host
            iscsiadm -m node -T $target -p $iscsi_host:3260 --login
            sleep 5
            rcopenais start
            echo
            ;;
        stop)
            rcopenais stop
            iscsiadm -m node -T $target -p $iscsi_host:3260 --logout
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

rcopen-iscsi start

iscsiadm -m discovery -t st -p $iscsi_host

chmod +x /etc/init.d/ais

ln -s /etc/init.d/ais /usr/sbin/rcais

  iscsiadm -m discovery -t st -p $iscsi_host
  iscsiadm -m node -T $target -p $iscsi_host:3260 --login

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

        token:  5000

        #How long to wait for consensus to be achieved before starting a new round of membership configuration.

        consensus:      6000

        #HMAC/SHA1 should be used to authenticate all message

        secauth:        off

        #How many token retransmits should be attempted before forming a new configuration.

        token_retransmits_before_loss_const:    10

        #How many threads should be used to encypt and sending message. Only have meanings when secauth is turned on

        threads:        0

        #

        transport:      udpu

        #The only valid version is 2

        version:        2

        interface {
EOF

ipaddr=$(echo $ROLE_0_IP | tr "," "\n")

for member in $ipaddr
do
    echo "                member {
                        memberaddr:     $member" >> /etc/corosync/corosync.conf
    echo "                }" >> /etc/corosync/corosync.conf
done

ipaddr=$(echo $ROLE_1_IP | tr "," "\n")

for member in $ipaddr
do
    echo "                member {
                        memberaddr:     $member" >> /etc/corosync/corosync.conf
    echo "                }" >> /etc/corosync/corosync.conf
done

cat<<EOF >> /etc/corosync/corosync.conf
                #The multicast port to be used

                mcastport:      5405

                #Network Address to be bind for this interface setting

                bindnetaddr:    $bindnetaddr

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

        timestamp:      off

        #Log to the standard error output

        to_stderr:      yes

        #Logging file line in the source code as well

        fileline:       no

        #Facility in syslog

        syslog_facility:        daemon

}
amf {
        #Enable or disable AMF

        mode:   disable
}
EOF

cat<<EOF > /etc/sysconfig/sbd
SBD_DEVICE="$sbd_disk"
SBD_OPTS="-W"
EOF

  if [[ $server ]]; then
    sbd -d $sbd_disk create
  fi

  sbd -d $sbd_disk dump | grep "Header version"
  sbd=$?
  if [[ "$sbd" != "0" ]]; then
    sbd -d $sbd_disk create
  fi

  sbd -d $sbd_disk list | grep $(hostname) 2>&1 > /dev/null
  sbd_host=$?
  if [[ "$sbd_host" != "0" ]]; then
    sbd -d $sbd_disk allocate $(hostname)
  fi

  if [[ $iscsi_host ]]; then
    rcais start
  else
    rcopenais start
  fi

  wait_for_cluster

  crm configure primitive sbd_stonith stonith:external/sbd

else
  echo -b $bindnetaddr -i $iscsi_host -s $sbd_disk -t $target
  echo "Wrong or missing arguments"
  echo "Usage: node_conf_runner -b bindnetaddr -d -i iscsi_host -s sbd_disk -t target"
  echo "       addon - url to add-on directory"
  echo "       bindnetaddr - address used for corosync [10.100.101.1]"
  echo "       mcastaddr - multicast addresss for cluster [239.50.1.1]"
  echo "       iscsi_host - IP address of your iscsi shared disk provider [10.100.96.150]"
  echo "       login - login for iscsi target"
  echo "       password - password for iscsi target"
  echo "       sbd_disk - disk used for sbd/STONITH [/dev/disk/by-path/pci-0000:00:01.1-scsi-0:0:1:0-part1]"
  echo "       target - [iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a]"
fi
