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

#shutdown openais
if [ -e /etc/init.d/openais ];then
	/etc/init.d/openais stop
	echo >/etc/sysconfig/sbd
fi

source /usr/share/qa/qa_test_cts/lib.sh

# initrial the syslog daemon
server_log_init

# init the ha software REPO
ha_repo_init

# init the hostname/ssh
build_ip_name_hash

dns_hosts

#ssh auto
for i in `seq 1 $client_No`
do
	non_ssh ${client_name[$i]} 
done

#sync the syslog status

if ! check_syslog_keywords syslogd_initial 20;then
	echo "can not initial syslog"
	exit 2
fi

#check nodes status

if ! check_syslog_keywords corosync_initial;then
	echo "can not initial corosync"
	exit 2
fi


sleep 30


#the test name should be one of  mysql/ocfs2/ctdb

cts_test_name=$1



if [ "$cts_test_name" == "" ];then

	#just run the cts test suite without cluster config

	ctl_send "run_cts_base_test"
        cts_stonith_opt="--stonith 0"
        echo ${client_name[$i]} "crm configure property stonith-enabled=false"
        ssh ${client_name[$i]}  "crm configure property stonith-enabled=false"

elif [ "$cts_test_name" == "mysql" ];then 

	#run the cts test suite with mysql_cluster config(require 2 share storage:1 for stonith;1 for mysql data)
	ctl_send "run_cts_mysql_test"
	echo "running mysql testsuite..."
	#check stonith sbd
	if check_syslog_keywords cts_stonith_iscsi_initial;then
		echo "stonith iscsi init succeed"
		if check_syslog_keywords cts_mysql_crm_initial;then
			echo "mysql test suite init succeed. start to run the testsuite..."
			cts_stonith_opt="--stonith-type sbd"
		else
			echo "can not init the mysql crm"
			exit 2
		fi
	else
		echo "can not init the stonith sbd storage"
		exit 2
	fi

elif [ "$cts_test_name" == "ocfs2" ];then 
	
	#run the cts test suite with ocfs2_cluster config
	
	ctl_send "run_cts_ocfs2_test"
	echo "running ocfs testsuite..."
	#check ocfs storage
	if check_syslog_keywords cts_ocfs2_iscsi_initial;then
		echo "ocfs storage init ok"
		if check_syslog_keywords cts_ocfs2_crm_initial;then
			echo "ocfs2 test suite init succeed. start to run the testsuite..."
        		#ssh ${client_name[$i]}  "crm configure property stonith-enabled=false"
			cts_stonith_opt="--stonith-type sbd"
		else
			echo "can not init the ocfs crm"
			exit 2
		fi
	else
		echo "can not init the ocfs2 storage"
		exit 2
	fi

elif [ "$cts_test_name" == "ctdb" ];then

	#run the cts test suite with ctdb_cluster config

	ctl_send "run_cts_ctdb_test"
	echo "running ctdb testsuite..."
	#check ocfs storage
	if check_syslog_keywords cts_ocfs2_iscsi_initial;then
		echo "ocfs storage init ok"
		if check_syslog_keywords cts_ctdb_crm_initial;then
			echo "ctdb with ocfs2 test suite init succeed. start to run the testsuite..."
			ssh ${client_name[$i]}  "crm configure property stonith-enabled=false"
			cts_stonith_opt="--stonith 0"
		else
			echo "can not init the ocfs crm"
			exit 2
		fi
	else
		echo "can not init the ocfs2 storage"
		exit 2
	fi

fi

#start to run
cts_logdir=/var/log/qa/ctcs2/`date +"qa_cts-%Y-%m-%d-%H-%M-%S"`
mkdir -p $cts_logdir
cts_logfile=$cts_logdir/qa_cts

python /usr/share/pacemaker/tests/cts/CTSlab.py -L /var/log/ha-log-daemon --syslog-facility daemon --no-unsafe-tests --stack corosync --at-boot 1  $cts_stonith_opt  5 --nodes "`echo $ROLE_1_NAME|sed 's/,/ /g'`" 2>&1 |tee $cts_logfile


if [ -n "`grep \<\ TESTS\ COMPLETED $cts_logfile`" ];then
        touch $cts_logdir/done
        cts_begin_time_s="`sed -n '/BEGINNING/{s/>.*//;p}' $cts_logfile`"
        cts_begin_time=`date -d "$cts_begin_time_s" +%s`
        cts_end_time_s="`sed -n '/TESTS COMPLETED/{s/<.*//;p}' $cts_logfile`"
        cts_end_time=`date -d "$cts_end_time_s" +%s`
        cts_runtime=`expr $cts_end_time - $cts_begin_time`
else
	exit 2
fi

#failed succeeded times_run test_time  int_errors skipped

echo cts_random_run >$cts_logdir/test_results

grep Overall\ Results $cts_logfile |awk 'BEGIN{fail=0;succ=0;count=0;erro=0;skip=0}{fail=substr($6,0,length($6)-1);skip=substr($8,0,length($8)-1);succ=substr($10,0,length($10)-1);erro=substr($12,0,length($12)-1)}END{count=fail+succ+skip;print fail,succ,count,"timesrun",erro,skip}'|sed "s/timesrun/$cts_runtime/" >>$cts_logdir/test_results

#clean syslog-ng config auto

for i in `seq 1 $client_No`
do
	ssh ${client_name[$i]} "sed -i '/qa_cts_auto-server_tag/d;/qa_cts_auto-nodes_tag/d' /etc/syslog-ng/syslog-ng.conf"
	ssh ${client_name[$i]} "rcsyslog restart"
	ssh ${client_name[$i]} "echo >/etc/sysconfig/sbd"
done

echo >/etc/sysconfig/sbd
sed -i '/qa_cts_auto-server_tag/d;/qa_cts_auto-nodes_tag/d' /etc/syslog-ng/syslog-ng.conf
rcsyslog restart
/usr/share/qa/tools/remote_qa_db_report.pl -c "CTS $cts_test_name TEST FOR HA"


