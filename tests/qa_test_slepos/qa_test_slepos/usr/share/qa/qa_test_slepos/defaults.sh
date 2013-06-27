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

# qa_slepos-config

# File:		defaults.sh 

# Author:	Tomas Cech <tcech@suse.cz>

# Description:	This file contains configuration, which will
#		be used for this tests and some common functions.

source "$CONF_PATH/local_config.sh"

###################
# object settings #
###################

# country abbrevation
country=pl
# company name
organization=PrazskeKanalizace

#################
# LDAP settings #
#################

# administration DN of LDAP
# this will be part of cn=$admin,o=$organization,c=$country
admin="admin"

# administration password of LDAP
pass="root"

if [ "$ssl"x = yx ]; then
	# use SSL
	#LdapServer="`echo "$admin_server_name.${organization}.${country}" | tr '[A-Z]' '[a-z]'`"
	LdapServer="`echo "$admin_server_name" | tr '[A-Z]' '[a-z]'`"
	LDAP_SERVER="ldaps://$LdapServer/"
else
	# don't use SSL
	LdapServer="$admin_server_IP"
	LDAP_SERVER="ldap://$LdapServer/"
fi


# eDirectory password (can and should be different from LDAP administration password)
# FIXME: not used yet
edir_pass=root2
tree_name=tree_name



info() {
	echo
	echo " * $@"
	echo
}

# write out text and exit with error
die() {
	echo "$@"
	exit 1
}


# this function compares supposed and real output of ldapsearch utility
# it's used for checking LDAP database
check_output() {

# ldapsearch produces output with fixed length of the line
# this will make from multi-line record (where other lines begins with spaces)
# single-line record
sed -i ':a; $!N;s/\n //;ta;P;D' /tmp/ldapsearch-output

RESULT=`diff /tmp/supposed-output /tmp/ldapsearch-output | wc -l`
case $RESULT in
	0) rm /tmp/supposed-output /tmp/ldapsearch-output ; exit 0 ;;
	*) exit 1 ;;
esac
}

# this is general check
# if it result is OK, it also remove files which were set as parameters
do_base_check() {
case $? in
	0)	if [ "${*}" ]; then
			echo "Removing unneeded files..."
			rm -f ${@}
			echo "Removed."
		fi
		echo "Exiting..."
		exit 0 ;;
	1)	exit 1 ;;
	*)	exit 2 ;;
esac
}

# this function arrange machine IP from an IP address and difference
# it takes first three numbers
# then it takes the last one and adds difference
count_machine_IP() {
echo `echo "$2" | sed 's/\([0-9]*\.[0-9]*\.[0-9]*\.\)[0-9]*/\1/'``echo "$2" | sed 's/[0-9]*\.[0-9]*\.[0-9]*\.\([0-9]*\)/\1/' | xargs -i expr {} + "$1" - 1`
}

#this function arrange machine name from mask, basename and order number
create_machine_name() {
length=`echo ${EnumerationMask} | wc -c | xargs -i expr {} - 1`
printf "${WorkstationBaseName}""%0${length}d\n" "$1"
}


image() {
        filename="${image_name}-`echo ${image_version} | sed 's/;\(active\|passive\)//'`"
}


version_parse() {
#	$1	number position (major=1,minor=2,micro=3)
#	$2	parsed version string
echo "$2" | sed "s/\([0-9]*\).\([0-9]*\).\([0-9]*\)/\\$1/"
}

higher_version() {
#	$1	first version string
#	$2	second version string

# if they're empty
if [ -z "$1" ]; then
    if [ -z "$2" ]; then
	die "Error during processing version strings"
    else
	echo "$2"
    fi
elif [ -z "$2" ]; then
    if [ -z "$1" ]; then
	die "Error during processing version strings"
    else
	echo "$1"
    fi

# if they aren't empty
elif [ `version_parse 1 "$1"` -lt `version_parse 1 "$2"` ]; then
    echo "$2"
elif [ `version_parse 1 "$1"` -gt `version_parse 1 "$2"` ]; then
    echo "$1"
else
    if [ `version_parse 2 "$1"` -lt `version_parse 2 "$2"` ]; then
	echo "$2"
    elif [ `version_parse 2 "$1"` -gt `version_parse 2 "$2"` ]; then
	echo "$1"
    else
	if [ `version_parse 3 "$1"` -lt `version_parse 3 "$2"` ]; then
	    echo "$2"
	elif [ `version_parse 3 "$1"` -gt `version_parse 3 "$2"` ]; then
	    echo "$1"
	else
	    echo "$1"
	fi
    fi
fi
}

active_passive() {
echo "$1" | sed 's/[0-9]*.[0-9]*.[0-9]*;\(active\|passive\)/\1/'
}

get_version_number() {
echo "$1" | sed 's/\([0-9]*.[0-9]*.[0-9]*\);\(active\|passive\)/\1/'
}

# this function gets the highest version of active image
get_last_active_version() {
#	$1	image version variable, same format as in LDAP

image_version="$1"
#unset VER LAST
for line in ${image_version};
do
    if [ `active_passive "${line}"` = active ]; then
	VER=`get_version_number "${line}"`
	LAST=`higher_version "${LAST}" "${VER}"`
    fi
done
echo "${LAST}"
}

create_branchserver_name() {
#	$1	branch server name
#	$2	location
#	$3	organizational unit
#	$4	organization
#	$5	country
echo "$1.$2.$3.$4.$5" | tr '[A-Z]' '[a-z]'
}

get_device_IP() {
#	$1	internal IP address
count=0
for addr in `ifconfig | sed -n 's/.*inet addr:\([0-9.]*\).*/\1/p'`
do
	case "${addr}" in
		"127.0.0.1") ;;
		"${internal_ip}") ;;
		*)
			count=$((count + 1))
			echo "${addr}"
			;;
	esac
done
}

C_GREEN="\[\033[01;32m\]"
C_BLUE="\[\033[01;34m\]"
C_NONE="\[\033[00m\]"

