#! /bin/bash

ARCH=$HOSTTYPE
if [ -n "$ARCH" ]; then
        echo "Architecture is $ARCH"
else
        echo "Error: Cannot determine architecture";
        exit 1
fi

release=`egrep -o '[aA]lpha[0-9]+|[bB]eta[0-9]+|RC[0-9]+|GMC|GMC[0-9]+|GM' /etc/issue`
if [ -z "$release" ]; then
        release="GMC"
else
        echo "The release is $release"
fi

snapper set-config TIMELINE_CREATE=no
zypper --no-gpg-checks -n ar http://dist.nue.suse.com/ibs/QA:/Head/SLE-11-SP4/ hamsta
zypper --no-gpg-checks -n ar http://dist.suse.de/install/SLP/SLE-11-SP4-SDK-$release/$ARCH/DVD1/ sle11sp4-sdk
#zypper --no-gpg-checks -n ar http://dist.ext.suse.de/ibs/QA:/Head/SUSE_SLE-12_GA/ hamsta
##zypper --no-gpg-checks -n ar http://dist.suse.de/ibs/SUSE:/SLE-12:/GA/standard/ sle12-sdk
#zypper --no-gpg-checks -n ar http://dist.suse.de/install/SLP/SLE-12-SDK-$release/$ARCH/DVD1/ sle12-sdk
#zypper --no-gpg-checks -n ar http://download.suse.de/install/SLP/SLE-12-Module-Web-Scripting-$release/$ARCH/CD1/ Web_Scripting
zypper --gpg-auto-import-keys ref

QA_LIB_PACKAGES="qa_lib_ctcs2 qa_lib_keys qa_lib_config qa_lib_perl qa_tools qa_db_report"
VALIDATION_PACKAGES="qa_test_process_stress qa_test_sched_stress qa_test_fs_stress"
KERNEL_PACKAGES=`awk '{print $1}' /usr/share/qa/qa_testset_kernel/kernel_test_packages`
REGRESSION_PACKAGES=`awk '{print $1}' /usr/share/qa/qa_testset_kernel/regression_test_packages`

INSTALL_PACKAGES=""
while getopts "akrv" arg
do
        case $arg in
             a)
                INSTALL_PACKAGES="$INSTALL_PACKAGES $VALIDATION_PACKAGES $REGRESSION_PACKAGES $KERNEL_PACKAGES"
                ;;
             k)
                INSTALL_PACKAGES="$INSTALL_PACKAGES $KERNEL_PACKAGES"
                ;;
             r)
                INSTALL_PACKAGES="$INSTALL_PACKAGES $REGRESSION_PACKAGES"
                ;;
             v)
                INSTALL_PACKAGES="$INSTALL_PACKAGES $VALIDATION_PACKAGES"
                ;;
             ?)
                echo "Error: unkonw argument"
                exit 1
                ;;
        esac
done

#test -z "$INSTALL_PACKAGES" && INSTALL_PACKAGES="$INSTALL_PACKAGES $VALIDATION_PACKAGES $REGRESSION_PACKAGES $KERNEL_PACKAGES"
if [ -z "$INSTALL_PACKAGES" ] ; then 
        INSTALL_PACKAGES="$VALIDATION_PACKAGES $REGRESSION_PACKAGES $KERNEL_PACKAGES"
fi

install_package () {
for pkg in "$@" ; do
        if rpm -q $pkg > /dev/null 2>&1 ; then
                echo -e "$pkg has already been installed.\n"
		logger "$pkg has already been installed."
        else
                zypper -n in -l $pkg > /dev/null 2>&1
                if rpm -q $pkg > /dev/null 2>&1 ;then
                        echo -e "$pkg is installed.\n"
			logger "$pkg is installed."
                else                                                                                    
                        echo -e "$pkg is not installed. Please install needed packages manually."
			logger "$pkg is not installed. Please install needed packages manually."
                fi                                                                                      
                                                                                                        
        fi                                                                                              
done 
}

INSTALL_PACKAGES="$QA_LIB_PACKAGES $INSTALL_PACKAGES"
install_package $INSTALL_PACKAGES

