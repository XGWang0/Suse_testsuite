#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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

. bind.rc

backup_config
install_config "primary"

$BINDCTRL restart

sleep 10

QUERY_1=`grep primary_query_1 qa_test_bind-config |cut -d = -f2`
MATCH_1=`grep primary_match_1 qa_test_bind-config |cut -d = -f2`
RESULT_1=$(dig @127.0.0.1 $QUERY_1 | grep -E "(^$QUERY_1.*$MATCH_1)")

echo "query for '$QUERY_1' resulted in '$RESULT_1'"

QUERY_2=`grep primary_query_2 qa_test_bind-config |cut -d = -f2`
MATCH_2=`grep primary_match_2 qa_test_bind-config |cut -d = -f2`
RESULT_2=$(dig @127.0.0.1 -x $QUERY_2 | grep -E "^$MATCH_2")

echo "query for '$QUERY_2' resulted in '$RESULT_2'"

if [ -n "$RESULT_1" -a -n "$RESULT_2" ]; then
   echo "PASSED: bind - Primary DNS"
   RC=0
else 
   echo "FAILED: bind - Primary DNS"
   RC=1
fi
   
restore_config

exit $RC

