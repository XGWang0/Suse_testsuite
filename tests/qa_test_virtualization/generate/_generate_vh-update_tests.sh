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
    echo "Usage: $0 [-m std/dev] [-v xen/kvm] [-b base] [-u upgrade] [-l milestoneTestRepo] [-r upgradeRepo]"
    echo "-m, std means update virt rpms from standard update repo;"
    echo "    dev means update virt rpms from developer's virt-devel/virt-test repo."
    echo "    default to std."
    echo "-v, hypervisor type, xen/kvm supported, default to kvm."
    echo "-b, base product name, need to follow convention os-release-spack, example sles-11-sp3"
    echo "    default to sles-11-sp3"
    echo "-u, upgrade product name, follow same convention with -b, default to sles-11-sp4"
    echo "-l, milestone test repo link which is used to update virt rpms."
    echo "-r, repo to do host upgrade do."
	exit 1
}

while getopts "m:v:b:u:l:r:" OPTIONS
do
    case $OPTIONS in
        m)mode="$OPTARG";;
        v)hypervisor="$OPTARG";;
        b)base="$OPTARG";;
        u)upgrade="$OPTARG";;
        l)milestoneTestRepo="$OPTARG";;
        r)upgradeRepo="$OPTARG";;
        \?)usage;;
        *)usage;;
    esac
done

[ -z "$mode" ] && mode="std"
[ -z "$hypervisor" ] && hypervisor="kvm"
[ -z "$base" ] && base="sles-11-sp3"
[ -z "$upgrade" ] && upgrade="sles-11-sp4"

if [ "$mode" != "std" -a -n "$milestoneTestRepo" ];then
	echo "Error: milestone test repo can only be set when test mode is std." >&2
	usage
fi

if [ -n "$milestoneTestRepo" -a -n "$upgradeRepo" ];then
	echo "Error: there can only be one repo that you really want to upgrade to." >&2
	usage
fi

#when milestoneTestRepo is specially given, we should update virt rpms to this repo after host upgrade, so add phase vhUpdateVirt  after vhPrepAndUpdate
if [ -n "$milestoneTestRepo" ];then
	testPhases="vhUpdateVirt vhPrepAndUpdate vhUpdateVirt vhUpdatePostVerification"
else
	testPhases="vhUpdateVirt vhPrepAndUpdate vhUpdatePostVerification"
fi

shortBase=${base//-/}
shortUpgrade=${upgrade//-/}

case $mode in
	std)vFlag="off"; rareUpdateFlag="on";;
	dev)vFlag="on"; rareUpdateFlag="off";;
esac

if [ -n "$upgradeRepo" ];then
	upgradeParm=" -u $upgradeRepo"
fi

tcfDir=/usr/share/qa/qa_test_virtualization/tcf
linkDir=/usr/share/qa/tcf
toolDir=/usr/share/qa/tools
testNamePrefix="test-VH-Upgrade-$mode-$hypervisor-$shortBase-$shortUpgrade"

#generate tcfs
step=1
for phase in $testPhases;do
	if [ "$phase" = "vhUpdateVirt" ];then
		timer=3600
	elif [ "$phase" = "vhPrepAndUpdate" ];then
		timer=28800
	elif [ "$phase" = "vhUpdatePostVerification" ];then
		timer=12600
	fi
	tcfName="$testNamePrefix-0$step.tcf"
	if [ $step -eq 3 -a "$phase" == "vhUpdateVirt" ];then
		cat > $tcfDir/$tcfName << EOF
timer $timer
fg 1 $phase /usr/share/qa/virtautolib/lib/vh-update.sh -p $phase -t $hypervisor -m ${base}-64 -n ${upgrade}-64 -r off -f $rareUpdateFlag -v $vFlag -l $milestoneTestRepo
wait

EOF
	else
		cat > $tcfDir/$tcfName << EOF
timer $timer
fg 1 $phase /usr/share/qa/virtautolib/lib/vh-update.sh -p $phase -t $hypervisor -m ${base}-64 -n ${upgrade}-64 -r off -f $rareUpdateFlag -v $vFlag $upgradeParm
wait

EOF

	fi
	ln -s $tcfDir/$tcfName $linkDir
	echo "Generated test file: $tcfDir/$tcfName,  link to $linkDir/$tcfName"
	((step++))
done

#generate run file
runName="${testNamePrefix}-run"
cp $toolDir/_generate_vh-update_run_template $toolDir/$runName
chmod +x $toolDir/$runName
echo "Generated test run file: $toolDir/$runName"

