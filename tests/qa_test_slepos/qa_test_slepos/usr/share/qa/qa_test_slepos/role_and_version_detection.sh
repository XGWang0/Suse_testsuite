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

# get version - NLPOS9 or SLEPOS10 or SLEPOS11
if [ -f /etc/slepos-release ]; then
	pos_version="`sed -n '/VERSION/s/[^=]*= //p' /etc/slepos-release`"
else
	pos_version="`cat /etc/SuSE-release | sed -n 's/VERSION = //p'`"
fi

# get patchlevel 0, 1 ...
if [ -f /etc/slepos-release ]; then
	pos_patchlevel="`sed -n '/PATCHLEVEL/s/[^=]*= //p' /etc/slepos-release`"
else
	pos_patchlevel="`cat /etc/SuSE-release | sed -n 's/PATCHLEVEL = //p'`"
fi

if [ -z "$pos_patchlevel" ]; then
	pos_patchlevel=0
fi

# This will select correct function namespace.
# It's not wrong - computer can be Admin, Branch and Image server at the same time
unset on_admin on_branch on_image

if which posInitLdap.sh &> /dev/null; then
	# I am on Admin server
	on_admin=yes
fi

if which posInitBranchserver.sh &> /dev/null; then
	# I am on Branch server
	on_branch=yes
	BRANCH_SERVER_CONFIG="$CONF_PATH/branch_server-$HOSTNAME.sh"
fi

if [ "$pos_version" = "9" ]; then
	if which xscr  &> /dev/null; then
		# I am on Image server
		on_image=yes
	fi
else
	if which kiwi &> /dev/null; then
		# I am on Image server
		on_image=yes
	fi
fi

