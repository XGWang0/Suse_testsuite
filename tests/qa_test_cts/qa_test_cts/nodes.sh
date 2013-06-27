#!/bin/sh
# ****************************************************************************
# Copyright © 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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

source /usr/share/qa/qa_test_cts/lib.sh

#init the ha software REPO
ha_repo_init

#init hostname/ssh
build_ip_name_hash

dns_hosts

#ssh auto
for i in `seq 1 $client_No`
do
	non_ssh ${client_name[$i]} 
done

non_ssh $ROLE_0_NAME

#syslog daemon init
nodes_log_init $ROLE_0_IP

#corosync init
corosync_init 


#wait for test info in 300 secs from controllor 

iii=0
while [ $iii -le 30 ]
do
	iii=`expr $iii + 1`
	sleep 10

	#check base test
	if quick_ctl_check run_cts_base_test;then
		echo run_cts_base_test
		break
	fi

	#check mysql test
	if quick_ctl_check run_cts_mysql_test;then
		echo run_cts_mysql_test
		if check_stonith_iscsi;then
			if stonith_iscsi_init;then
				mysql_setup
				if check_mysql_iscsi;then
					crm_set_mysql
				fi
			fi
		fi
		break
	fi

	#check ocfs2 test
	if quick_ctl_check run_cts_ocfs2_test;then
		echo run_cts_ocfs2_test
		if check_ocfs2_iscsi && check_stonith_iscsi;then
			stonith_iscsi_init
			crm_set_ocfs2
		fi
		break
	fi

	#check ctdb test
	if quick_ctl_check run_cts_ctdb_test;then
		echo run_cts_ctdb_test
		if check_ocfs2_iscsi;then
			crm_set_ctdb
		fi
		break
	fi
done

exit 0


