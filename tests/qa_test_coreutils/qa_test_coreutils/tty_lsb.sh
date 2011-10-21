#!/bin/bash

#===============================================================================
#
#           FILE: tty_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-11-09
#        REVISED: 2005-11-09
#
#    DESCRIPTION: "test basic functionality of tty" 
#   REQUIREMENTS: "needs coreutils"
#          USAGE: ./tty_lsb.sh
#
#===============================================================================


if tty --help &>/dev/null; then
	
	MY_TTY="/dev/"`ps | grep $$ | awk '{ print $2}'`
	MY_TTY2=`tty`
	
	if [ "$MY_TTY" = "$MY_TTY2" ]; then
	    echo "PASSED: tty base functionality"
	    exit 0
	else
	    echo "PASSED: tty base functionality"
	    exit 1
	fi
else
	echo "FAILED: ERROR: tty cannot be called"
	exit 1
fi


