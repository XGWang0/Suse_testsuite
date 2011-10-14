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

#===============================================================================
#
#           FILE: basename_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: SUSE Proprietary
#
#        CREATED: 2005-11-09
#        REVISED: 2005-11-09
#
#    DESCRIPTION: "test use of basename"
#   REQUIREMENTS: "needs coreutils, grep, mktemp"
#          USAGE: ./basename_lsb.sh
#
#===============================================================================

if basename --help &>/dev/null; then 

	TMPDIR=`mktemp -d`
	TESTSTRING="$TMPDIR/you_know/some_testing_dirs/hello.world"

	rm -r $TMPDIR
	if basename "$TESTSTRING" .world | grep "^hello$" > /dev/null; then
	    echo "PASSED: basename - basic functions"
	    exit 0		
	else
	    echo "FAILED: basename - basic functions"
	    exit 1	
	fi

else 
	echo "FAILED: ERROR: basename cannot be called"
	exit 1
fi

