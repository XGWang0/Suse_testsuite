#!/bin/sh
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

