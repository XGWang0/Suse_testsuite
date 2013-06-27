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


timer=6000

type="$1"

[ "$type" == "" ] && type=standalone

for i in install_* ; do
	# This is intentionally in for of blacklist, so that all newer are tested as well (maybe should be changed in the future?"
	echo $i | grep -q 'nw-65-sp7\|oes-2-fcs\|oes-2-sp1\|rhel-3\|rhel-4-u6\|rhel-4-u7\|rhel-5-fcs\|rhel-5-u1\|rhel-5-u2\|rhel-5-u3\|rhel-5-u4\|sle[ds]-10-sp1\|sle[ds]-10-sp2\|sled-10-sp3\|sle[ds]-10-fcs\|win-vista-fcs\|win-vista-sp1\|win-xp-sp1\|win-xp-sp2\|win-xp-fcs\|win-2k8-' && continue
	cat << EOF
timer $timer
fg 1 $i /usr/share/qa/qa_test_virtualization/$i $type
wait

EOF
done


