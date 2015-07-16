#!/bin/bash
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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
#


#
# This script generates vh-update tcfs
#
function usage() {
    echo ""
    echo "Usage: $0 [-m std/dev] [-v xen/kvm] [-b base] [-u upgrade]"
    echo "-m, std means update virt rpms from standard update repo;"
    echo "    dev means update virt rpms from developer's virt-devel/virt-test repo."
    echo "    default to std."
    echo "-v, hypervisor type, xen/kvm supported, default to kvm."
    echo "-b, base product name, need to follow convention os-release-spack, example sles-11-sp3"
    echo "    default to sles-11-sp3"
    echo "-u, upgrade product name, follow same convention with -b, default to sles-11-sp4"
	exit 1
}

while getopts "m:v:b:u:" OPTIONS
do
    case $OPTIONS in
        m)mode="$OPTARG";;
        v)hypervisor="$OPTARG";;
        b)base="$OPTARG";;
        u)upgrade="$OPTARG";;
        \?)usage;;
        *)usage;;
    esac
done

[ -z "$mode" ] && mode="std"
[ -z "$hypervisor" ] && hypervisor="kvm"
[ -z "$base" ] && base="sles-11-sp3"
[ -z "$upgrade" ] && upgrade="sles-11-sp4"

shortBase=${base//-/}
shortUpgrade=${upgrade//-/}

case $mode in
	std)vFlag="off"; rareUpdateFlag="on";;
	dev)vFlag="on"; rareUpdateFlag="off";;
esac

tcfDir=/usr/share/qa/qa_test_virtualization/tcf
linkDir=/usr/share/qa/tcf
toolDir=/usr/share/qa/tools
testNamePrefix="test-VH-Upgrade-$mode-$hypervisor-$shortBase-$shortUpgrade"

#generate tcfs
for phase in vhUpdateVirt vhPrepAndUpdate vhUpdatePostVerification;do
	if [ "$phase" = "vhUpdateVirt" ];then
		step="01"
		timer=3600
	elif [ "$phase" = "vhPrepAndUpdate" ];then
		step="02"
		timer=28800
	elif [ "$phase" = "vhUpdatePostVerification" ];then
		step="03"
		timer=9000
	fi
	tcfName="$testNamePrefix-$step.tcf"
	cat > $tcfDir/$tcfName << EOF
timer $timer
fg 1 $phase /usr/share/qa/virtautolib/lib/vh-update.sh -p $phase -t $hypervisor -m ${base}-64 -n ${upgrade}-64 -r off -f $rareUpdateFlag -v $vFlag
wait

EOF
	ln -s $tcfDir/$tcfName $linkDir
	echo "Generated test file: $tcfDir/$tcfName,  link to $linkDir/$tcfName"
done

#generate run file
runName="${testNamePrefix}-run"
cp $toolDir/_generate_vh-update_run_template $toolDir/$runName
chmod +x $toolDir/$runName
echo "Generated test run file: $toolDir/$runName"

