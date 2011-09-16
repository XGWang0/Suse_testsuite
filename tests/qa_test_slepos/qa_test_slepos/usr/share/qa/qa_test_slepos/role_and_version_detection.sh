#!/bin/bash

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
