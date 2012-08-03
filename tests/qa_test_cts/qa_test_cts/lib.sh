#!/bin/sh
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************

source /usr/share/qa/lib/config ''

iscsi_username="`get_qa_config ISCSI_USERNAME`"
iscsi_password="`get_qa_config ISCSI_PASSWORD`"
iscsi_T="`get_qa_config ISCSI_MYSQL_STORAGE`"
iscsi_S="`get_qa_config ISCSI_STONITH_STORAGE`"
iscsi_O="`get_qa_config ISCSI_OCFS2_STORAGE`"

echo "$iscsi_T $iscsi_S $iscsi_O"
iscsi_disk=
stonith_iscsi_disk=
ocfs2_iscsi_disk=

repo_sles_11_sp1=`grep repo_sles_11_sp1 /usr/share/qa/qa_test_cts/qa_test_cts-config |cut -d= -f2`
repo_sles_11_sp2=`grep repo_sles_11_sp2 /usr/share/qa/qa_test_cts/qa_test_cts-config |cut -d= -f2`

update_sles_11_sp1=`grep update_sles_11_sp1 /usr/share/qa/qa_test_cts/qa_test_cts-config |cut -d= -f2`
ga_sles_11_sp1=`grep ga_sles_11_sp1 /usr/share/qa/qa_test_cts/qa_test_cts-config |cut -d= -f2`
ga_sles_11_sp2=`grep ga_sles_11_sp2 /usr/share/qa/qa_test_cts/qa_test_cts-config |cut -d= -f2`

ha_mcast=226.94.1.2
ha_network=`ip addr|awk '/inet /{gsub(/.* inet /,"");gsub(/[0-9]+\/.*/,"");a=\$0"0"}END{print a}'`
ha_mcast_port=4444

client_No=0



function wait_for_resource {

local keywords
local times_start
local times_limit
keywords=$1
times_start=0
times_limit=10

while :
do
        times_start=`expr $times_start + 1`
        if [ $times_start == $times_limit ];then
        echo "can not verify the resource $keywords for client"
        return 2
        fi
	crm_resource --locate --resource $1 2>&1 | grep 'running on'
	r_c=$?
	if [ $r_c == 0 ];then
	echo "resource start to running"
	chown -R mysql:mysql /var/lib/mysql
	break
	fi
        sleep 15
done
}





function build_ip_name_hash {

	for c_ip in `echo $ROLE_1_IP|sed 's/,/ /g'`
	do
		client_No=`expr $client_No + 1`
		client_ip[$client_No]=$c_ip
	done	
	client_No=0
	for c_name in `echo $ROLE_1_NAME|sed 's/,/ /g'`
	do
		client_No=`expr $client_No + 1`
		client_name[$client_No]=$c_name
	done	

}

function non_ssh {

	target_ip=$1
	
        expect -f /usr/share/qa/qa_test_cts/first-check.exp $target_ip
        if [ $? -gt 0 ];then
                echo "Opps error with ssh key!"
                exit 2
        fi

}

function dns_hosts {
	
	sed -i '/qa_cts_dns_tag/d' /etc/hosts
	for i in `seq 1 $client_No`
	do
		echo ${client_ip[$i]} ${client_name[$i]} '#qa_cts_dns_tag' >> /etc/hosts
	done
	echo $ROLE_0_IP $ROLE_0_NAME '#qa_cts_dns_tag' >> /etc/hosts
}

function del_tail {
	#/etc/syslog-ng/syslog-ng.conf
	filename=$1
	filename_no=$(($2 - 1))
	echo $filename_no $filename
	sed -i ":a;1,$filename_no{N;ba};:b;;N;P;\$d;D;\$ ! bb;" $filename
}

function server_log_init {
	echo > /var/log/ha-log-daemon
	sed -i "/qa_cts_auto-server_tag/d" /etc/syslog-ng/syslog-ng.conf
	sed -i "/qa_cts_auto-nodes_tag/d" /etc/syslog-ng/syslog-ng.conf
	#add 4 lines
	cat <<eof >>/etc/syslog-ng/syslog-ng.conf
source s_tcp { tcp(port(15789) max-connections(512)); }; #qa_cts_auto-server_tag
destination     d_ha  { file("/var/log/ha-log-daemon"); }; #qa_cts_auto-server_tag
log { source(s_tcp); destination(d_ha); }; #qa_cts_auto-server_tag
eof
/etc/init.d/syslog restart
}

function nodes_log_init {
	sleep 5
	server_ip=$1
	sed -i "/qa_cts_auto-nodes_tag/d" /etc/syslog-ng/syslog-ng.conf
	sed -i "/qa_cts_auto-server_tag/d" /etc/syslog-ng/syslog-ng.conf
	#add 7 lines 
	cat<<eof >>/etc/syslog-ng/syslog-ng.conf
source s_tcp { tcp(port(15789) max-connections(512)); }; #qa_cts_auto-nodes_tag
filter f_ha  { facility(daemon); }; #qa_cts_auto-nodes_tag
filter f_ha_tcp  { facility(daemon); }; #qa_cts_auto-nodes_tag
destination ha_local { file("/var/log/ha_cluster" perm(0644)); }; #qa_cts_auto-nodes_tag
destination ha_tcp { tcp($server_ip port(15789));}; #qa_cts_auto-nodes_tag
log { source(src); filter(f_ha_tcp); destination(ha_tcp); }; #qa_cts_auto-nodes_tag
log { source(src); source(s_tcp); filter(f_ha); destination(ha_local); }; #qa_cts_auto-nodes_tag
eof
/etc/init.d/syslog restart
logger -p daemon.info "syslogd_initial succeed"
}


function ha_repo_init {
	if [ -z "`zypper ls |awk '{if($3=="ha")print "yes"}'|tail -1`" ];then
		if [ -n "`grep \"Server 11 SP1\" /etc/issue`" ];then
			zypper sa -t rpm-md $repo_sles_11_sp1 ha
			zypper sa -t rpm-md $update_sles_11_sp1 sp1-kernel-extra
			zypper sa -t rpm-md $ga_sles_11_sp1 sp1-ctdb
			zypper --gpg-auto-import-keys ref
		elif [ -n "`grep \"Server 11 SP2\" /etc/issue`" ];then
			zypper sa -t rpm-md $repo_sles_11_sp2 ha
			zypper sa -t rpm-md $ga_sles_11_sp2 sp2-kernel-extra
			zypper --gpg-auto-import-keys ref
		else
			echo "HA repo is only for SLES 11"
			exit 2
		fi
	fi
	zypper ref
	zypper -n in corosync pacemaker pacemaker-mgmt pacemaker-mgmt-devel libpacemaker-devel lvm2-clvm ocfs2-tools ocfs2-tools-o2cb ocfs2-kmp-default kernel-default-extra ctdb
	if [ -n "`rpm -qa|grep pacemaker-mgmt-devel`" ] && [ -n "`rpm -qa|grep corosync-`" ];then
		echo cts installation succeed
	else
		echo cts installation failed
		exit 2
	fi
}


function check_syslog_keywords {
local keywords
local times_start
local times_limit
keywords=$1
times_limit=$2
times_start=0
if [ -z "$times_limit" ];then 
	times_limit=15
fi

while :
do
        times_start=`expr $times_start + 1`
        if [ $times_start == $times_limit ];then
        echo "can not verify the keyword $keywords for client"
	return 2
        fi

        if [ ! -e "/var/log/ha-log-daemon" ];then
        continue
        fi

        #if [ "`grep -c syslogd_initial /var/log/ha-log-daemon`" == "$client_No" ];then
        if [ "`grep -c $keywords /var/log/ha-log-daemon`" == "$client_No" ];then
        break
        fi

        sleep 10
done

return 0

}

function crm_sync_send {
local htimes
htimes=`echo $ROLE_1_IP|sed 's/,/\n/g'|wc -l`
for i in `seq 1 $htimes`
do
	logger -p daemon.info "$1"
done
}

function ctl_send {
local htimes
htimes=`echo $ROLE_1_IP|sed 's/,/\n/g'|wc -l`
for i in `seq 1 $htimes`
do
	ssh ${client_name[$i]} "logger -p daemon.info $1"
done
}


function check_ctl_keywords {

local keywords
local htimes
local times_start
local times_limit
local tmptimes
times_start=0
times_limit=$2
keywords=$1
if [ -z "$times_limit" ];then
	times_limit=15
fi
htimes=`echo $ROLE_1_IP|sed 's/,/\n/g'|wc -l`;
#htimes = `expr $htimes + 1`

while :
do
        times_start=`expr $times_start + 1`
        if [ $times_start == $times_limit ];then
        echo "can not verify the keyword $keywords for client"
        return 2
        fi
	tmptimes=`ssh $ROLE_0_IP "grep -c \"$keywords\" /var/log/ha-log-daemon"`
        if [ $tmptimes -eq $htimes ];then
        break
        fi
	sleep 10
done
return 0

}

function quick_ctl_check {

local keywords
local htimes
local tmptimes
keywords=$1
htimes=`echo $ROLE_1_IP|sed 's/,/\n/g'|wc -l`;
tmptimes=`ssh $ROLE_0_IP "grep -c \"$keywords\" /var/log/ha-log-daemon"`
if [ $tmptimes -eq $htimes ];then
        return 0
fi
return 1

}


function corosync_init {
	/etc/init.d/openais stop
	rm -rf /var/lib/heartbeat/hostcache
	rm -rf /var/lib/heartbeat/crm/cib*
	logger -p daemon.info "corosync_shutdown_cleanup succeed"
	echo "corosync_shutdown_cleanup succeed"
	cp /etc/corosync/corosync.conf.example /etc/corosync/corosync.conf
	sed -i "s/bindnetaddr:.*/bindnetaddr: $ha_network/;s/mcastaddr:.*/mcastaddr: $ha_mcast/;s/mcastport:.*/mcastport: $ha_mcast_port/" /etc/corosync/corosync.conf

	if check_ctl_keywords "corosync_shutdown_cleanup";then
		echo >/etc/sysconfig/sbd
		/etc/init.d/openais start
		chkconfig --level 35 openais on
		if [ $? != 0 ];then
		echo "can not start openais (corosync)"
		exit 2
		fi
	else
		sleep 1
		logger -p daemon.info "can_not_sync_corosync"
		echo "can not sync the corosync"
		exit 2
	fi
	
	logger -p daemon.info "corosync_initial succeed"
	
}


function mysql_setup {


if [ ! -e /usr/bin/mysqld_safe ]; then
	zypper in -y mysql
fi
rcmysql start
rcmysql stop

}

function check_stonith_iscsi {
local iscsi_rc=
local iscsi_ip=
local iscsi_port=
local iscsi_target=
echo "start to check stonith iscsi"
if [ -n "$iscsi_S" ];then
	zypper in -y open-iscsi
	sed -i '/^node\.startup =/s/.*/node.startup = automatic/;/^node\.session\.iscsi\.InitialR2T =/s/.*/node.session.iscsi.InitialR2T = Yes/' /etc/iscsi/iscsid.conf
	#set auth
	if [ -n "$iscsi_username" ];then
		sed -i '/node\.session\.auth\.username =/d;/node\.session\.auth\.password =/d;' /etc/iscsi/iscsid.conf
		echo "# ISCSI-AUTO-SETUP-WAS-HERE
		node.session.auth.username = $iscsi_username
		node.session.auth.password = $iscsi_password" >> /etc/iscsi/iscsid.conf
	fi
	if [ -z "`ps -ef|grep [i]scsid|tail -1`" ];then
	rcopen-iscsi start
	fi
	chkconfig --level 35 open-iscsi on
	iscsi_ip=${iscsi_S%%:*}
	iscsi_port=${iscsi_S%%,*}
	iscsi_port=${iscsi_port##*:}
	iscsi_target=${iscsi_S##* }
	iscsiadm -m discovery -p $iscsi_ip:$iscsi_port -t sendtargets|grep $iscsi_target
	if [ $? == 0 ] ;then
		echo "stonith iscsi target found"
		iscsiadm -m node -T $iscsi_target --login
		iscsi_rc=$?
		if [ $iscsi_rc == 0 ] || [ $iscsi_rc == 255 ] || [ $iscsi_rc == 15 ]; then
			echo "iscsi target login"
			iscsiadm -m node -T $iscsi_target --op update -n node.startup -v automatic
			echo "$iscsi_target"
			sleep 5
			stonith_iscsi_disk="/dev/disk/by-path/`ls /dev/disk/by-path/|grep \"$iscsi_target\" |head -1`"
			if [ -d $stonith_iscsi_disk ];then
			echo "can not find stonith iscsi disk"
			return 1
			fi
			echo $stonith_iscsi_disk
			logger -p daemon.info "cts_stonith_iscsi_initial succeed"
			return 0
		fi
		return 1
	fi
else
	return 1
fi
}

function stonith_iscsi_init {
local myip=`ifconfig |sed -n '/eth/{n;s/.*addr://;s/[[:space:]]\+Bcast.*//;p}'`
firstip=`echo $ROLE_1_IP|sed 's/,.*//'`
modprobe softdog
sed -i '/softdog/d' /etc/init.d/boot.local
echo "modprobe softdog" >>/etc/init.d/boot.local
if [ "$myip" == "$firstip" ];then
	sbd -d $stonith_iscsi_disk create
	echo $stonith_iscsi_disk "sbd_iscsi_init succeed"
	crm_sync_send "sbd_iscsi_init succeed"
fi
#sync sbd disk init
if check_ctl_keywords "sbd_iscsi_init";then
	sbd -d $stonith_iscsi_disk allocate $(hostname)
	cat<<eof >/etc/sysconfig/sbd
SBD_DEVICE="$stonith_iscsi_disk"
SBD_OPTS="-W"
eof
fi

}
function check_mysql_iscsi {
local iscsi_rc=
local iscsi_ip=
local iscsi_port=
local iscsi_target=
if [ -n "$iscsi_T" ];then
	zypper in -y open-iscsi
	if [ -z "`ps -ef|grep [i]scsid|tail -1`" ];then
	rcopen-iscsi start
	fi
	iscsi_ip=${iscsi_T%%:*}
	iscsi_port=${iscsi_T%%,*}
	iscsi_port=${iscsi_port##*:}
	iscsi_target=${iscsi_T##* }
	iscsiadm -m discovery -p $iscsi_ip:$iscsi_port -t sendtargets|grep $iscsi_target
	if [ $? == 0 ] ;then
		echo "iscsi target found"
		iscsiadm -m node -T $iscsi_target --login
		iscsi_rc=$?
		if [ $iscsi_rc == 0 ] || [ $iscsi_rc == 255 ] || [ $iscsi_rc == 15 ]; then
			iscsiadm -m node -T $iscsi_target --op update -n node.startup -v automatic
			echo "iscsi target login"
			echo "$iscsi_target"
			sleep 5
			iscsi_disk="/dev/disk/by-path/`ls /dev/disk/by-path/|grep \"$iscsi_target\" |head -1`"
			echo $iscsi_disk
			if [ -d $iscsi_disk ];then
			echo "can not find iscsi disk"
			return 1
			fi
			logger -p daemon.info "cts_mysql_iscsi_initial succeed"
			return 0
		fi
		return 1
	fi
else
	return 1
fi

}


function crm_set_mysql {

local myip=`ifconfig |sed -n '/eth/{n;s/.*addr://;s/[[:space:]]\+Bcast.*//;p}'`
firstip=`echo $ROLE_1_IP|sed 's/,.*//'`



if [ "$myip" == "$firstip" ];then
	crm_mon -1
	sleep 30
	crm configure property default-action-timeout="140"
	sleep 3
	#start to config crm
	crm configure primitive sbd_stonith stonith:external/sbd meta target-role="Started" op monitor interval="15" timeout="15" params sbd_device="$stonith_iscsi_disk"
	sleep 2
	yes|mkfs.ext3 -q $iscsi_disk
	echo 
	crm configure <<EOF
primitive fs1 ocf:heartbeat:Filesystem \
	op monitor interval="20" timeout="40" start-delay="10" \
	params device="$iscsi_disk" directory="/var/lib/mysql" fstype="ext3"
	property no-quorum-policy="ignore"
EOF
sleep 3
crm configure <<EOF
primitive sql1 ocf:heartbeat:mysql \
        op monitor interval="10" timeout="120" start-delay="10" \
        params binary="/usr/bin/mysqld_safe" pid="/var/lib/mysql/mysqld.pid"
colocation col-sql1 +inf: sql1 fs1
order order-sql1 +inf: fs1 sql1
EOF
sleep 10
wait_for_resource fs1
wait_for_resource sql1
crm_sync_send "cts_mysql_crm_initial succeed"



fi

}

function crm_set_ocfs2 {

ocfs2_mount_dir="/ocfs2"
mkdir -p $ocfs2_mount_dir

local myip=`ifconfig |sed -n '/eth/{n;s/.*addr://;s/[[:space:]]\+Bcast.*//;p}'`
firstip=`echo $ROLE_1_IP|sed 's/,.*//'`

if [ "$myip" == "$firstip" ];then

	echo "start to format $ocfs2_iscsi_disk"
	yes|mkfs.ocfs2 -N16 -F --cluster-stack=pcmk --cluster-name=pacemaker $ocfs2_iscsi_disk
	crm_mon -1
	sleep 30
	crm configure property default-action-timeout="140"
	crm configure primitive sbd_stonith stonith:external/sbd meta target-role="Started" op monitor interval="15" timeout="15" params sbd_device="$stonith_iscsi_disk"
	sleep 5
	#start to config crm
	
	crm configure <<EOF
primitive clvm ocf:lvm2:clvmd \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive cmirror ocf:lvm2:cmirrord \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive dlm ocf:pacemaker:controld \       
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive o2cb ocf:ocfs2:o2cb \       
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive ocfs2 ocf:heartbeat:Filesystem \
        params directory="$ocfs2_mount_dir" fstype="ocfs2" device="$ocfs2_iscsi_disk" options="acl" \
        op monitor interval="20" timeout="40" \       
        op start interval="0" timeout="60s" \
        op stop interval="0" timeout="60s"
group o2stage dlm clvm o2cb cmirror
clone c-o2stage o2stage meta interleave="true"
clone c-ocfs2 ocfs2 meta interleave="true" ordered="true"
colocation colo-ocfs2-o2stage inf: c-ocfs2 c-o2stage
order order-ocfs2-o2stage 0: c-o2stage c-ocfs2
property no-quorum-policy="ignore"
EOF

crm_sync_send "cts_ocfs2_crm_initial succeed"

fi

}


function crm_set_ctdb {

zypper in -y samba samba-winbind ctdb
ocfs2_mount_dir="/mnt/samba"
mkdir -p $ocfs2_mount_dir

local myip=`ifconfig |sed -n '/eth/{n;s/.*addr://;s/[[:space:]]\+Bcast.*//;p}'`
firstip=`echo $ROLE_1_IP|sed 's/,.*//'`
node_names="`echo $ROLE_1_NAME|sed 's/,/ /g'`"
if [ "$myip" == "$firstip" ];then

	echo "start to format $ocfs2_iscsi_disk"
	yes|mkfs.ocfs2 -N16 -F --cluster-stack=pcmk --cluster-name=pacemaker $ocfs2_iscsi_disk
	crm_mon -1
	sleep 30
	crm configure property default-action-timeout="140"
	sleep 5
	#start to config crm
	
	crm configure <<EOF
primitive clvm ocf:lvm2:clvmd \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive cmirror ocf:lvm2:cmirrord \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive ctdb ocf:heartbeat:CTDB \
        op monitor interval="10" timeout="20" \
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s" \
        params ctdb_recovery_lock="/mnt/samba/ctdb.lock" \
	       ctdb_manages_samba="yes" \
	       ctdb_manages_winbind="yes" 
primitive dlm ocf:pacemaker:controld \       
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive o2cb ocf:ocfs2:o2cb \       
        op start interval="0" timeout="90s" \
        op stop interval="0" timeout="100s"
primitive ocfs2 ocf:heartbeat:Filesystem \
        params directory="$ocfs2_mount_dir" fstype="ocfs2" device="$ocfs2_iscsi_disk" options="acl" \
        op monitor interval="20" timeout="40" \       
        op start interval="0" timeout="60s" \
        op stop interval="0" timeout="60s"
primitive st-ssh stonith:external/ssh \
	 params hostlist="$node_names"
group o2stage dlm clvm o2cb cmirror
clone c-ctdb ctdb meta interleave="true" target-role="Started"
clone c-o2stage o2stage meta interleave="true"
clone c-ocfs2 ocfs2 meta interleave="true" ordered="true"
clone fencing st-ssh
colocation colo-ocfs2-o2stage inf: c-ocfs2 c-o2stage
colocation ctdb-with-fs inf: c-ctdb c-ocfs2
order order-ocfs2-o2stage 0: c-o2stage c-ocfs2
order start-ctdb-after-ocfs2 inf: c-ocfs2 c-ctdb
property no-quorum-policy="ignore"
EOF

crm_sync_send "cts_ctdb_crm_initial succeed"

fi

}


function check_ocfs2_iscsi {
local iscsi_rc=
local iscsi_ip=
local iscsi_port=
local iscsi_target=
if [ -n "$iscsi_O" ];then
	zypper in -y open-iscsi
	if [ -z "`ps -ef|grep [i]scsid|tail -1`" ];then
	rcopen-iscsi start
	fi
	iscsi_ip=${iscsi_O%%:*}
	iscsi_port=${iscsi_O%%,*}
	iscsi_port=${iscsi_port##*:}
	iscsi_target=${iscsi_O##* }
	iscsiadm -m discovery -p $iscsi_ip:$iscsi_port -t sendtargets|grep $iscsi_target
	if [ $? == 0 ] ;then
		echo "iscsi target found"
		iscsiadm -m node -T $iscsi_target --login
		iscsi_rc=$?
		if [ $iscsi_rc == 0 ] || [ $iscsi_rc == 255 ] || [ $iscsi_rc == 15 ] ; then
			iscsiadm -m node -T $iscsi_target --op update -n node.startup -v automatic
			echo "iscsi target login"
			echo "$iscsi_target"
			sleep 5
			ocfs2_iscsi_disk="/dev/disk/by-path/`ls /dev/disk/by-path/|grep \"$iscsi_target\" |head -1`"
			if [ -d $ocfs2_iscsi_disk ];then
			echo "can not find iscsi disk"
			return 1
			fi
			echo $ocfs2_iscsi_disk
			echo "cts_ocfs2_iscsi_initial succeed"
			logger -p daemon.info "cts_ocfs2_iscsi_initial succeed"
			return 0
		fi
		echo "can not verify the iscsiadm return code"
		return 1
	fi
else
	return 1
fi

}


