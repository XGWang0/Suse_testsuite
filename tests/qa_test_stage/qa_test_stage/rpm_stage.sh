#!/bin/sh
#
#the qa_lib_keys should be installed for scp the rpm to SUT(stage machine)
#expect shoud install to avoid fresh install prompt

#setup the PATH
PATH="/sbin:/usr/sbin:/usr/local/sbin:/root/bin:/usr/local/bin:/usr/bin:/bin"

###########################Config Start#############################
#monitor info
monitor_remote_dir="$1"
monitor_hostip="$2"


#email for job result/finish info
email=jtang@suse.com

# the build url for reinstall 
#reinstall_url="http://147.2.207.242/iso_mnt/SLES-11-SP2-DVD-i586-Beta4-DVD1/"
reinstall_url="$3"

# the ip of hamsta master

hamst_ipadd=`cat /var/log/hamsta.log |grep "Start of XM[L]"|tail -1|sed "s/.*\[//;s/].*//"`

# the stage machine from hamsta

host_ip=$ROLE_1_IP

# rpm dir in stage machine

rpm_dir=/home

# required file
first_check_exp=/usr/share/qa/qa_test_stage/first-check.exp
feed_hamsta=/usr/share/qa/qa_test_stage/feed_hamsta.pl


###########################Config End################################

#lock file to avoid muti-run
lock_f=/var/run/rpm_stage.pid

if [ -e /var/run/rpm_stage.pid ];then
	echo "A thread is already running, skip this cycle"
fi

echo $$ > $lock_f



e_clean(){
	ssh -l root $monitor_hostip "rm -rf $monitor_remote_dir/nowrunning"
	rm /var/run/rpm_stage.pid
}
#avoid prompt
expect -f $first_check_exp root@$monitor_hostip
if [ $? != 0 ];then
	echo "ssh key config failed"
	exit 2
fi
expect -f $first_check_exp root@$host_ip
if [ $? != 0 ];then
	echo "ssh key config failed"
	exit 2
fi


a=0
while [ $a -le 4 ]
do
 a=`expr $a + 1`

 #get the current dir name and now dir name
 current=`ssh -l root $monitor_hostip "ls -l $monitor_remote_dir|sed -n \"/current/{s/.*> //;p;q}\""`
 now=`ssh -l root $monitor_hostip "ls -l $monitor_remote_dir|sed -n \"/now/{s/.*> //;p;q}\""`

 #check the link 

 if [ -z "$current" -o -z "$now" ];then
 	echo "missing link ,please check the link"
	exit 2
 fi


 #check different start
 if [ "$current" != "$now" ] ;then
 
 	#new build found start stage process
 
 	#update the link
 	ssh -lroot $monitor_hostip "rm $monitor_remote_dir/current"
 	ssh -lroot $monitor_hostip "ln -s $now $monitor_remote_dir/current"
 
 	#backup the now to nowrunning
 	ssh -lroot $monitor_hostip "rm -rf $monitor_remote_dir/nowrunning"
 	ssh -lroot $monitor_hostip "cp -ar $monitor_remote_dir/$now $monitor_remote_dir/nowrunning"
 	if [ $? != 0 ];then
 		echo "copy file faied , please check the disk space"
 		e_clean
 		exit 2
 	fi
 
 	# send reinstall job to stage machine
 
 	$feed_hamsta -w -c"send reinstall ip $host_ip $reinstall_url $email $now" $hamst_ipadd
 
 	if [ $? != 0 ];then
 		echo "reinstall failed,please check the reinstall job from hamsta"
 		e_clean
 		exit 2
 	fi
 
 
 
 	# scp the "now" rpm to the SUT (stage machine)
 	monitor_hostip="$2"
 	scp -r root@$monitor_hostip$monitor_remote_dir/nowrunning root@$host_ip:$rpm_dir/
 	if [ $? != 0 ];then
 		echo "scp file failed"
 		e_clean
 		exit 2
 	fi
 
 
 	# Install the rpm package 
 
 	$feed_hamsta -w -c "send one line cmd ip $host_ip echo#rpm#-ivh#$rpm_dir/nowrunning/*;ls#$rpm_dir/nowrunning/* $email $now" $hamst_ipadd
 	if [ $? != 0 ];then
 		echo "rpm install failed please check the install log from hamsta ";
 		e_clean
 		exit 
 	fi
 
 	# run some test
 
 	echo "stuff"
 	if [ $? != 0 ];then
 		echo "test failed"
 		e_clean
 	fi
 	
 	#Got here every test passed
 
 	echo "passed"
 	#update link to stable
 	ssh -lroot $monitor_hostip "rm $monitor_remote_dir/stable"
 	ssh -lroot $monitor_hostip "ln -s $now $monitor_remote_dir/stable"
 	e_clean
 fi
 echo now build detected . go to next cycle.
 sleep 3
done
 
 
 
 
 
 
 	
 
 
