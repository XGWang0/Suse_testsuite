#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_siege_defaultrun.sh
#        VERSION: 0.1
#         AUTHOR: Frank Seidel <fseidel@suse.de>
#       REVIEWER: 
#        LICENSE: some License, e.g. GPL
#
#        CREATED: 2005-10-13
#        REVISED: 2005-10-13
#
#    DESCRIPTION: "uses siege to load local webserver"
#   REQUIREMENTS: "requires running webserver on localhost:80"
#          USAGE: ./qa_siege_defaultrun.sh [optional-Timestring(like '24H')]
#
#===============================================================================

#<Declarations>
USERS="500"
TIME="64M"


TCDIR="/usr/share/qa/qa_test_siege"
SIEGEBIN="/usr/share/qa/qa_test_siege/siege/bin/siege"
FAILED="0"
#</Declarations>



#<main>
	#Look for optional time-argument
	if [ $# -gt 0 ]
	then
		echo "STATUS: taking optional time-string >${1}<"
		TIME="$1"
	else
		echo "STATUS: taking default time-setting of $TIME"
	fi


	#Start siege itself
	if [ -x "$SIEGEBIN" ]
	then
		# siege-run may already have copied the config file
		if [ ! -f ~/.siegerc ]
		then
			${TCDIR}/siege/bin/siege.config || exit 1
		fi
		$SIEGEBIN -c $USERS --time=$TIME || FAILED="1"
	else
		echo "ERROR: $SIEGEBIN not executable" >&2
		exit 1
	fi


	#result-overview
	if [ $FAILED -ge 1 ]
	then
		echo "FAILED: siege had an error :(" >&2
		exit 1
	else
		echo "PASSED: siege run was ok :)"
		exit 0
	fi

#</main>
