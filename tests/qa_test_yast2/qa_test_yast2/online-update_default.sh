#!/bin/bash

#################################################################################
#                                                                               #
#     SUSE/Novell confidential Testscript                                       #
#     Only for internal use, distribution prohibited                            #
#                                                                               #
#     Name:                   online-update_default.sh                          #
#                                                                               #
#     Date of creation:       01.09.2005                                        #
#                                                                               #
#     Author:                 Frank Seidel <fseidel@suse.de>                    #
#     Maintainer:             Frank Seidel <fseidel@suse.de>                    #
#     Reviewer:               <REVIEWER>                                        #
#                                                                               #
#     Description             Tests a default-run (take over all suggestions)   #
#                             of online_update. But this only works with qt     #
#                             gui, as this test includes a dirty x-hack         #
#                                                                               #
#################################################################################

#MAXTIMEDIFF is used as maximum timedifference (in secs) since end of this
#macro and the (by yast2 itself) recorded last update
MAXTIMEDIFF="300"

#check if we are root
if [ $UID -gt 0 ]
then
	echo "ERROR: this script needs to be run as root (with x-access)" >&2
	exit 1
else
	echo "Starting YaST2 ... online_update"
	/usr/lib/YaST2/bin/y2base -l /tmp/qa_yast2_onlineupdate_default.log online_update qt --macro /usr/share/qa/qa_test_yast2/macros/you_default2.ycp
	RCODE="$?";

	#check if yast was ok with this run
	if [ $RCODE -gt 0 ]
	then
		echo "FAILED - with returncode $RCODE"
		exit 1;
	else
		#get unixtime of last onlineupdate
		LASTUPDATE="$(date -d "$(tail -1 /var/lib/YaST2/you/youlog |cut -d' ' -f -2)" +%s)";
		ENDTIME="$(date +%s)";
		DIFFTIME=$[ENDTIME-LASTUPDATE];
		
		#see if it really was done in the last time
		if [ $DIFFTIME -lt $MAXTIMEDIFF ]
		then
			echo "PASSED - yast onlineupdate reported no errors and youlog seems ok"
			exit 0;
		else
			echo "FAILED - last update was too long ago (not this run probably).. $DIFFTIME secs.";
			exit 1;
		fi
	fi
fi
