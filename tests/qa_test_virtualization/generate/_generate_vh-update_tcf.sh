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
# This script generates vh-update tcfs for all supported hypervisor/product
#

for hypervisor in xen kvm;do 
	for arch in 32 64;do
		for product in sles-11-sp3 sles-11-sp4;do
			if [ "$product" = "sles-11-sp3" ];then
				upProduct="sles-11-sp4"
			elif [ "$product" = "sles-11-sp4" ];then
				if [ "$arch" = "32" ];then
					continue
				fi
				upProduct="sles-12-sp1"
			fi
			for mode in standard devel;do
				if [ "$mode" = "standard" ];then
					vFlag="off"
				elif [ "$mode" = "devel" ];then
					vFlag="on"
				fi
				for phase in vhUpdateVirt vhPrepAndUpdate vhUpdatePostVerification;do
					if [ "$phase" = "vhUpdateVirt" ];then
						timer=3600
					elif [ "$phase" = "vhPrepAndUpdate" ];then
						timer=7200
					elif [ "$phase" = "vhUpdatePostVerification" ];then
						timer=3600
					fi
					cat << EOF
timer $timer
fg 1 $phase /usr/share/qa/virtautolib/lib/vh-update.sh -p $phase -t $hypervisor -m ${product}-${arch} -n ${upProduct}-${arch} -r off -f on -v $vFlag
wait

EOF
				done
			done
		done
	done
done
