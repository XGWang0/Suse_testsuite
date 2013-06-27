#!/bin/bash
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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

# source REPO, REPO_NAME, PACKAGE, PACKAGE_DESC variables
source qa_test_zypper-config

function failed {
       echo "$1. Test failed"
       exit -1
}

function assert_root {
       [ `id -u` == 0 ] || failed "You must be root to run this test. Exiting..."
       export LANG=C
}

function assert_output {
       r1=`zypper $1`
       r2=`zypper $2`
       [ "$r1" == "$r2" ] || failed "zypper $1 and zypper $2 have different output"
}

function assert_result {
       zypper $1 | grep "$2" > /dev/null
       if [ $? != 0 ]; then
               zypper $1 | grep "$3" > /dev/null
               if [ $? != 0 ]; then
                       failed "There is no $2 or $3 in the result of command: $1"
               fi
       fi
}

function no_result {
    zypper $1 | grep "$2" > /dev/null
    [ $? != 0 ] || failed "Should not exist $2 in the result of command: $1"
}

function assert_file {
    zypper $1 > /dev/null
    [ -e $2 ] || failed "$2 is not exist after execute command: $1"
}


