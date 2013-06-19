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

ARCH=$HOSTTYPE

FREE_SPACE=`df -m / | grep -e "/$" | awk '{print $4}'`
if [ $FREE_SPACE -le 400 ]; then
        echo "no enough space for this test! At least 400MB free space is required!"
        exit 1
fi

FTP_SOURCE=`grep ftp_source /usr/share/qa/qa_test_ftpload/qa_test_ftpload-config |cut -d= -f2`

if [ "$ARCH" != "s390x" ]; then
	ftpload -d /tmp -c 1 $FTP_SOURCE
else
	if [ ! -d /abuild/ftpload_test ] ; then
		mkdir -p /abuild/ftpload_test
	fi 

	ftpload -d /abuild/ftpload_test -c 20 $FTP_SOURCE
fi

log=`ls $LOG_DIR |tail -n 1`

if [ "${log##*.}" == "logerr" ]; then
        echo "ftpload $FTP_SOURCE with failed, please check $LOG_DIR/$log"
        exit 1
elif [ "${log##*.}" == "all" ]; then
        grep "Passed" $LOG_DIR/$log
        if [ $? -eq 0 ]; then
                echo "ftpload $FTP_SOURCE with passed, please check $LOG_DIR/$log"
                exit 0
        else
                exit 1
        fi
fi

