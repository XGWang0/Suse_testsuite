#! /bin/bash

ARCH=$HOSTTYPE
if [ "$ARCH" != "" ]; then
        echo "architecture is $ARCH"
else
        echo "cannot determine architecture";
        exit 1
fi

release=`egrep -o '[aA]lpha[1-9]|[bB]eta[1-9]|RC[1-9]' /etc/issue`
if [ -z "$release" ]; then
        release="GMC"
else
        echo "This is release is $release"
fi

zypper --no-gpg-checks -n ar http://dist.ext.suse.de/ibs/QA:/Head/SUSE_SLE-12_GA/ hamsta
zypper --no-gpg-checks -n ar http://dist.suse.de/ibs/SUSE:/SLE-12:/GA/standard/ sle12-sdk
zypper --gpg-auto-import-keys ref

QA_LIB_PACKAGES="qa_lib_ctcs2 qa_lib_keys qa_lib_perl qa_lib_config qa_tools qa_db_report"

Validation="qa_test_process_stress qa_test_sched_stress qa_test_fs_stress"
KERNEL_PACKAGES=`awk '{print $1}' /usr/share/qa/qa_testset_kernel/kernel_test_packages`
REGRESSION_PACKAGES=`awk '{print $1}' /usr/share/qa/qa_testset_kernel/regression_test_packages`


for pkg in $QA_LIB_PACKAGES $Validation $REGRESSION_PACKAGES $KERNEL_PACKAGES ; do
        if rpm -q $pkg > /dev/null 2>&1 ; then
                echo -e "$pkg has already been installed\n"
                echo $pkg | grep qa_test
                if [ $? == 0 ] ;then
                        echo -e "$pkg" >> /tmp/test_packages
                fi
        else
                zypper -n in -l $pkg > /dev/null 2>&1
                if rpm -q $pkg > /dev/null 2>&1 ;then
                        echo -e "$pkg is installed\n"
                        echo $pkg | grep qa_test
                        if [ $? == 0 ] ;then
                                echo -e "$pkg" >> /tmp/test_packages
                        fi
                else                                                                                    
                        echo -e "$pkg is not installed. Please install needed packages manually."       
                fi                                                                                      
                                                                                                        
        fi                                                                                              
done 
