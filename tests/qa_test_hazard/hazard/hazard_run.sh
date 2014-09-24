#!/bin/bash 
#check the uid

if [ `id -u` -gt 0 ];then
	echo "you should be root to run this script"
	exit 2
fi
function Usage () {
cat <<'EOF'
Usage: hazard_run.sh [options] <clients_1> <clients_2>
	-A <hours>       = DYING client must be ALIVE within <hours> (int)
	-D <1/2-hours>   = DYING client must be DEAD within <1/2-hours> (int)
	-F               = dump configuration only (run no tests)
	-I               = exit after creating io.* (run no tests)
	-S               = exit after creating scan.* (run no tests)
	-c <conf>        = use built-in configuration <conf>
	-o <option> ...  = add <option> as 'option:' line
	-t <hours>       = terminate tests after <hours> (float)
Where: <conf> is the number or a unique substring from one of:
       0 = empty
       1 = diskevery stress
       2 = raw stress only
       3 = filesystem stress only
       4 = stress without probes
       5 = diskall stress
       6 = diskall with reboots
       7 = dt stress
       8 = stress (default)
       9 = stress with aborts
       10 = stress with device Resets (bdr/BDRs)
       11 = stress with bus resets
       12 = trouble
       13 = stress with reboots
       14 = stress with panics
       15 = recovery time
       16 = disaster
       17 = mi_wr async stress
       18 = svtfse stress
       19 = svtseek stress

EOF
}
function Clean () {

	echo "start to clean up"
	#Clean up the client 


	#Clean up the hazard server
	sed -i "s/127\.0\.0\.1.*/127.0.0.1 localhost/" /etc/hosts
	echo "clean up (done)"
	if [ -z "$*" ];then
		exit 2
	fi
	for ip in $client_ips
	do
		abuild="`echo $mark_abuild|sed 's/ /\n/g'|grep $ip`"
		if [ -n "$abuild" ];then
			restore_disk="`echo $abuild|sed 's/.*%//'`"
			ssh -l root $ip "lvremove /dev/hazard/hazard_stress <<eof
y
eof
"
			ssh -l root $ip "vgremove hazard"
			#restore for ia64
			fdiskpath=`ssh -l root $ip "which fdisk"`
			if [ -z "$fdiskpath" ];then
				ssh -l root $ip "parted -s $restore_disk mklabel msdos"
				psize=`ssh -l root $ip "parted -s $restore_disk print|sed 's/.*- //;1q'"`
				ssh -l root $ip "parted -s $restore_disk mkpart primary ext3 0 $psize"
				
				
			else
			#restore for x86
			ssh -l root $ip "fdisk $restore_disk <<eof
n
p
1


w
"
			fi
			ssh -l root $ip "mkfs.ext3 ${restore_disk}1"
			ssh -l root $ip "mount ${restore_disk}1 /abuild"

			
		fi
		ssh -l root $ip "sed  -i 's/disable[ \t]\+= .*/disable \t = yes/' /etc/xinetd.d/rsh"
		ssh -l root $ip "echo >/etc/hosts.equiv"
		ssh -l root $ip "echo >/root/.rhosts"
		ssh -l root $ip "/etc/init.d/xinetd stop"
		ssh -l root $ip "chkconfig -s xinetd off"
		ssh -l root $ip "sed -i '/$old_hostname/d' /root/.ssh/authorized_keys"
		echo "clean up (done)"
	done

}
#change domain name 
old_hostname=`hostname`
sed -i "s/127\.0\.0\.1.*/127.0.0.1 ${old_hostname}.suse.de ${old_hostname}/" /etc/hosts
ping -c1 ${old_hostname}.suse.de >/dev/null 2>&1
sleep 4
client_passwd=''

#Get local ip address

local_ips="`ifconfig |sed -n '/inet addr:/{s/[A-Z].*//;s/[^:]\+://;p}'|grep -v ^127|tail -1`"

#prepare the log dir
rm -rf /var/log/qa/hazard
mkdir -p /var/log/qa/hazard
	
tmp_hazard_dbdir="/tmp/hazard__$$"
mkdir -p $tmp_hazard_dbdir
#defind the csums file
csums="/usr/lib/hazard/i386-linux24-client.csums
/usr/lib/hazard/i386-linux26-client.csums
/usr/lib/hazard/ia64-linux24-client.csums
/usr/lib/hazard/ia64-linux26-client.csums
/usr/lib/hazard/x86_64-linux24-client.csums
/usr/lib/hazard/x86_64-linux26-client.csums"

#update the shabang of csums file
shellpath=`which sh`

for csumsfile in $csums
do
	shabang="#!$shellpath"
	sed -i "1s@.*@$shabang@" $csumsfile || Clean
done


#Get the host ip  option of hazard
while getopts :o:A:D:t:c:ISF opts
do
	case $opts in
		o)	hazard_o=$OPTARG
		;;
		c)	hazard_c=$OPTARG
		;;
		A)	hazard_A=$OPTARG
		;;
		D)	hazard_D=$OPTARG
		;;
		t)	hazard_t=$OPTARG
		;;
		I)	hazard_I="x"
		;;
		S)	hazard_S="x"
		;;
		F)	hazard_F="x"
		;;
		?)	echo "Oops never heard of this option :)"
			Usage
			Clean
		;;
	esac
done



#find out the client ip

shift $((OPTIND-1))
client_ips="$@"
echo "$client_ips"

if [ -z "$client_ips" ];then
	echo "can't find out the client ip address abort"
	Clean
fi

#check the ssh-keygen  currently use qa_keys
#if [ ! -e "/root/.ssh/id_rsa" ];then
#	expect -f /usr/lib/hazard/ssh-keygen.exp
#	if [ $? -gt 0 ];then
#		echo "Opps error with generator ssh key!"
#		Clean
#	fi
#fi
#Update the ssh authorized 
for ip in $client_ips

do
	sed -i "/$ip/d" /root/.ssh/known_hosts
	expect -f /usr/lib/hazard/first-check.exp $ip
	if [ $? -gt 0 ];then
                echo "Opps error with ssh key!"
                Clean
        fi

	#configure the rsh in client
	zypper_version=`ssh -l root $ip zypper -V 2>&1`
	zypper_version=${zypper_version:7:1}
	zypper_opt='-qn in'
	if [ -n "$zypper_version" -a $zypper_version -lt 1 ];then
		zypper_opt=' --no-gpg-checks in -y'
	fi	
	ssh -l root $ip "zypper $zypper_opt rsh-server"
	if [ -z "`ssh -l root $ip 'rpm -qa|grep rsh-server'`" ];then
		echo "can not install rsh-server abort"
		Clean
	fi
	
	ssh -l root $ip "chkconfig xinetd 2345" 	
	ssh -l root $ip "sed  -i 's/disable[ \t]\+= .*/disable \t = no/' /etc/xinetd.d/rsh"
	ssh -l root $ip "echo -e \"$local_ips\" >/etc/hosts.equiv"
	ssh -l root $ip "echo $local_ips	root >/root/.rhosts"
	ssh -l root $ip "/etc/init.d/xinetd restart"

	#get the hardware info and rpm list

	ssh -l root $ip "rpm -qa --qf \"%{NAME} %{VERSION}-%{RELEASE}\n\" | sort " >/var/log/qa/hazard/$ip-rpmlist
	ssh -l root $ip "/usr/sbin/hwinfo --all" >/var/log/qa/hazard/$ip-hwinfo
	
	#update the qa_db_report argument
	qadb_arg_p=`ssh -l root $ip "perl -I /usr/share/qa/lib -Mdetect -e '@p=&detect_product;print \\\$p[5].chr(45).\\\$p[3]'"`
	qadb_arg_m=`ssh -l root $ip "hostname"`
	qadb_arg_k=`ssh -l root $ip "perl -I /usr/share/qa/lib -Mdetect -e 'print &get_kernel_version'"`
	qadb_arg_a=`ssh -l root $ip "perl -I /usr/share/qa/lib -Mdetect -e 'print &get_architecture'"`
	
	echo " -p $qadb_arg_p -c \"hazart-test on $qadb_arg_m\" -a $qadb_arg_a -f $tmp_hazard_dbdir/ -k $qadb_arg_k -m $qadb_arg_m " >/var/log/qa/hazard/$ip-dbarg
	
	
	#create LVM
	lv_disk=`ssh -l root $ip "lvscan"`
	echo $lv_disk
	if [ -n "$lv_disk" ];then
		continue
	fi
	abuilds=`ssh -l root $ip "mount|grep -i abuild"`
	if [ -z "$abuilds" ];then
		continue
	fi
	ssh -l root $ip "umount /abuild"
	echo "umount the abuild"
	disk_no=`ssh -l root $ip "hwinfo --disk|sed -n '/Device File:/p'|wc -l"`
	echo $disk_no
	if [ $disk_no -ne 2 ];then
		continue
	fi
	disk_name=`ssh -l root $ip "hwinfo --disk|sed -n '/Device File:/p'|awk '{print \\\$3}'|tail -1"`
	echo $disk_name

	ssh -l root $ip "dd if=$disk_name of=/tmp/diskmbr bs=512 count=1"
	ssh -l root $ip "dd if=/dev/zero of=$disk_name bs=512 count=1"
	ssh -l root $ip "pvcreate $disk_name;vgcreate hazard $disk_name"

	vg_size=`ssh -l root $ip "vgdisplay|sed -n '/Free  PE/{s/.*\/ //;s/ //;p}'"`
	size_1=`echo $vg_size|sed 's/\..*//'`
	size_2=`echo $vg_size|sed 's/[0-9\.]//g'`

	ssh -l root $ip "lvcreate -n hazard_stress -L ${size_1}$size_2 hazard"
	mark_abuild="$mark_abuild $ip%$disk_name"
	echo "mark the abuild ip and disk"

done
#Update Arg
arg=
if [ -n "$hazard_D" ];then
	arg="$arg -D $hazard_D"
fi
if [ -n "$hazard_A" ];then
	arg="$arg -A $hazard_A"
fi
if [ -n "$hazard_t" ];then
	arg="$arg -t $hazard_t"
fi
if [ -n "$hazard_o" ];then
	arg="$arg -o $hazard_o"
fi
if [ -n "$hazard_c" ];then
	arg="$arg -c $hazard_c"
fi
if [ -n "$hazard_I" ];then
	arg="$arg -I"
fi
if [ -n "$hazard_F" ];then
	arg="$arg -F"
fi
if [ -n "$hazard_S" ];then
	arg="$arg -S"
fi


#Start to do the hazard stress work:

echo ----------------------------Start to workg------------------------

cd /usr/lib/hazard
echo "/usr/lib/hazard/hazard -d /var/log/qa/hazard $arg $client_ips"
date +%s >/var/log/qa/hazard/time_se
/usr/lib/hazard/hazard -N -L -u -d /var/log/qa/hazard $arg $client_ips
sleep 1
cd $OLDPWD
date +%s >>/var/log/qa/hazard/time_se
echo -----------------------------end------------------------------

RESULT=`/usr/lib/hazard/log -T15 -d /var/log/qa/hazard/ |grep 'FAILED!!!'`
TIMESRUN=`awk 'NR==2{print $0-a;exit}{a=$0}' /var/log/qa/hazard/time_se`
RESULT_E="pass"
returnvalue=0
if [ -n "$RESULT" -o $TIMESRUN -le 20 ];then
	RESULT_E="fail"
	returnvalue=1
fi
echo $TIMESRUN"#"$RESULT_E >/var/log/qa/hazard/results
mkdir /var/log/qa/hazard/hazard_stress
/usr/lib/hazard/log -d /var/log/qa/hazard/ >/var/log/qa/hazard/hazard_stress/results
store_hazardlog="/tmp/hazard/hazard_$$_`date +%s`"
echo $store_hazardlog
mkdir -p $store_hazardlog
cp -ar /var/log/qa/hazard $store_hazardlog/
Clean all
#submit qadb
for h_ip in $client_ips
do
	rm -rf $tmp_hazard_dbdir/*
	cp -ar /var/log/qa/hazard  $tmp_hazard_dbdir/	
	cp $tmp_hazard_dbdir/hazard/${h_ip}-rpmlist $tmp_hazard_dbdir/hazard/rpmlist
	cp $tmp_hazard_dbdir/hazard/${h_ip}-hwinfo $tmp_hazard_dbdir/hazard/hwinfo
	/usr/share/qa/tools/remote_qa_db_report.pl `cat ${tmp_hazard_dbdir}/hazard/${h_ip}-dbarg`
	rm -rf $tmp_hazard_dbdir/*
done

#/usr/share/qa/tools/remote_qa_db_report.pl -c "hazard test"
rm -rf /var/log/qa/hazard
exit $returnvalue
