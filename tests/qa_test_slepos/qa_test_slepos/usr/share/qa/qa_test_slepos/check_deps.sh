#!/bin/sh
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

all_exe_files() {
	echo $PATH | \
	tr ':' '\n' | \
	while read dir; do
		[ -d "$dir" ] && \
		[ $(ls -1A "$dir" | wc -l) -gt 0 ] && \
		echo "$dir"
	done | \
	sed 's@$@/*@'
}

check_deps() {
	PATHS_TO_CHECK="/lib/ /usr/lib"
	if [ -d /lib64 ]; then
		PATHS_TO_CHECK="$PATHS_TO_CHECK /lib64"
	fi
	if [ -d /usr/lib64 ]; then
		PATHS_TO_CHECK="$PATHS_TO_CHECK /usr/lib64"
	fi
	FILES_TO_CHECK="`all_exe_files`
`find $PATHS_TO_CHECK -type f -o -type l`"
#	FILES_TO_CHECK="`find /usr/lib/xulrunner-1.9.0.6/`"
	OLD_LANG="$LANG"
	LANG=en
	for FILE in $FILES_TO_CHECK; do
		if [ -L "$FILE" ] && [ ! -e "$FILE" ]; then
			echo "$FILE is broken link"
		elif [ -f "$FILE" ] && [ -x "$FILE" ] && [ `filesize "$FILE"` -ne 0 ]; then
			LDDOUT="`ldd "$FILE"`"
			case $? in
				0)
				if echo "$LDDOUT" | grep '=> not found' &> /dev/null; then
					LIB=`ldd "$FILE" | grep 'not found' | sort -u | cut -d\  -f1 | sed 's/\t//'`
					grep "/${LIB}$" <<< "$FILES_TO_CHECK" &> /dev/null || echo "$FILE is missing $LIB"
				fi ;;
				1)
				continue ;;
				*)
				echo "other error with file $FILE" ;;
			esac
			
		fi
	done
	LANG="$OLD_LANG"
}

check_deps

