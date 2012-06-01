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

# time sync
sntp -P no -r ntp.suse.cz

if [[ $iscsi_host && ! -e /sbin/iscsiadm ]]; then
  zypper in -y open-iscsi
fi

if [[ $bindnetaddr && $sbd_disk ]]; then
  zypper se -t pattern | grep ha_sles | grep "i |" 2>&1 > /dev/null
  ha_sles="$?"
  if [ "$ha_sles" != "0" ]; then
    zypper in -l -y -t product sle-hae
    zypper in -y -t pattern ha_sles
  fi

  if [ $iscsi_host ]; then
cat<<EOF > /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.1996-04.de.suse:01:ha-automation
EOF
  fi

#in case iscsi is used, iscsi target is checked and logged into, then it is set to autoconnect on iscsi daemon restart
  if [[ $iscsi_host && $target ]]; then
    rcopen-iscsi start
    iscsiadm -m discovery -t st -p $iscsi_host
    iscsiadm -m node -T $target -p $iscsi_host:3260 --login
    sleep 10
    sed -i "s/node.startup = manual/node.startup = automatic/" "/etc/iscsi/nodes/$iscsi_target/$iscsi_portal,3260,1/default"
    grep node.startup "/etc/iscsi/nodes/$iscsi_target/$iscsi_portal,3260,1/default"
    rcopen-iscsi restart
  fi

# deployment of corosync configuration with unicast communication
cat<<EOF  > /etc/corosync/corosync.conf
aisexec {
        #Group to run aisexec as. Needs to be root for Pacemaker

        group:  root

        #User to run aisexec as. Needs to be root for Pacemaker

        user:   root

}
service {
        #Default to start mgmtd with pacemaker

        use_mgmtd:      yes

        #Use logd for pacemaker

        use_logd:       yes

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

        interface {
                #Network Address to be bind for this interface setting

                bindnetaddr:    $bindnetaddr
EOF

ipaddr=$(echo $ROLE_0_IP | tr "," "\n")

for member in $ipaddr
do
    echo "                member {
                        memberaddr:     $member" >> /etc/corosync/corosync.conf
    echo "                }" >> /etc/corosync/corosync.conf
done

cat<<EOF >> /etc/corosync/corosync.conf
                #The multicast port to be used

                mcastport:      5405

                #The ringnumber assigned to this interface setting

                ringnumber:     0

        }
        #HMAC/SHA1 should be used to authenticate all message

        secauth:        off

        #The only valid version is 2

        version:        2

        #

        transport:      udpu

        #How many token retransmits should be attempted before forming a new configuration.

        token_retransmits_before_loss_const:    10

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

        to_stderr:      no

        #Logging file line in the source code as well

        fileline:       off

        #Facility in syslogrm -f /var/lib/heartbeat/hostcache
rm /var/lib/heartbeat/crm/cib*


        syslog_facility:        daemon

}
amf {
        #Enable or disable AMF

        mode:   disabled

}
EOF

# preparatin of SBD STONITH device
cat<<EOF > /etc/sysconfig/sbd
SBD_DEVICE="$sbd_disk"
SBD_OPTS="-W"
EOF

# select first machine in the group to prepare SBD disk
machine=$(echo $ROLE_0_NAME | sed -e 's/,.*//')

  if [[ $machine = $(hostname) ]]; then
    sbd -d $sbd_disk create
  fi

# allocation of SBD slots to nodes
  sbd -d $sbd_disk list | grep $(hostname) 2>&1 > /dev/null
  sbd_host="$?"
  if [[ "$sbd_host" != "0" ]]; then
    sbd -d $sbd_disk allocate $(hostname)
  fi

  if [[ $iscsi_host ]]; then
    rcais restart
  else
    rcopenais start
  fi

  wait_for_cluster

# addinf stonith primitive, if there is none
  crm_resource --locate --resource sbd_stonith  2>&1 | grep -q 'running on' > /dev/null
  stonith="$?"
    if [[ "$stonith" != "0" ]]; then
      crm configure primitive sbd_stonith stonith:external/sbd
    fi

else
  echo -b $bindnetaddr -i $iscsi_host -s $sbd_disk -t $target
  echo "Wrong or missing arguments"
  echo "Usage: node_setup.sh -b bindnetaddr -d -i iscsi_host -s sbd_disk -t target"
  echo "       bindnetaddr - address used for corosync [10.100.101.1]"
  echo "       iscsi_host - IP address of your iscsi shared disk provider [10.100.96.150]"
  echo "       sbd_disk - disk used for sbd/STONITH [/dev/disk/by-path/pci-0000:00:01.1-scsi-0:0:1:0-part1]"
  echo "       target - [iqn.1986-03.com.hp:storage.msa2012i.0839d71eda.a]"
fi
