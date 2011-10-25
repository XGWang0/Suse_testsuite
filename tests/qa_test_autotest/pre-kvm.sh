#!/bin/sh
#this script prepare the env for autotest test 
#$1 is the iso url please use supported iso


#testcase seprate by space
testcase=" stress_boot iofuzz qemu_img timedrift vlan_tag "
config_path="/usr/lib/ctcs2/config/autotest/qa_test_autotest-config"

if [ "x$1"=="x" ];then
	iso_url=`grep iso_url $config_path |cut -d= -f2`
else
	iso_url="$1"
fi

iso_name=${iso_url##*/}

#gentrate the configure 
cd /usr/lib/autotest/tests/kvm/
echo -e "n\nn\nn"|python ./get_started.py

#find test case name / iso md5sume  from tests_base.cfg

local_iso="/tmp/kvm_autotest_root/isos/linux/"$iso_name
exp_iso_md5="`grep -A3 $iso_name /usr/lib/autotest/tests/kvm/tests_base.cfg|awk 'NR==2{print $3}'`"

if [ -z "$exp_iso_md5" ];then
	echo "can't find md5sume from config file please use a supported iso"
	exit
fi

install_casename="`grep -B16 $iso_name /usr/lib/autotest/tests/kvm/tests_base.cfg|awk '/variants:/{getline a;gsub(/.*- /,"",a);gsub(/:/,"",a);print a}'`"
install_casename=${iso_name%%-*}.$install_casename


#modify the config to run our iso

sed -i "s/qemu_kvm_f14_quick/suse_quick/;s/Fedora\.14\.64/$install_casename/;" /usr/lib/autotest/tests/kvm/tests.cfg

#fix Bug 

sed -i "s/drive_index_cd1 = 2/drive_index_cd1 = 1/;s/drive_index_unattended = 1/drive_index_unattended = 2/;" /usr/lib/autotest/tests/kvm/tests_base.cfg

# add testcases
sed -i "s/only unattended_install boot/& $testcase/;" /usr/lib/autotest/tests/kvm/tests.cfg

#check the iso
chk_md5()
{
echo "check md5sume"
iso_md5sum=`md5sum $local_iso|awk '{print $1}'`
if [ "$iso_md5sum"=="$exp_iso_md5" ];then
	echo "install iso was verified. you can run the autotest tesk"
	return 0
else
	echo "install iso md5sum verify failed"
	return 1
fi
}


if [ -e $local_iso ];then
	
	if chk_md5;then
		exit
	else
		echo "start to download install iso"
		cd /tmp/kvm_autotest_root/isos/linux/
		rm $local_iso
		wget $iso_url
		chk_md5
	fi
else 
	mkdir -p /tmp/kvm_autotest_root/isos/linux/
	echo "start to download install iso"
	cd /tmp/kvm_autotest_root/isos/linux/
	wget $iso_url
	chk_md5
fi

	

	

