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


#
# This script generates installation testcase for each install "description" in virtautolib
#

function usage
{
	cat << EOF >&2 
Usage:
	$0 [-d path_to_autoinstallation_dir] [-t disk_type]

Where:
	path_to_autoinstallation_dir root directory of autoinstallation 
	                             descriptions
	Default: /usr/share/qa/virtautolib/data/autoinstallation

Disk_type:
	Could be "., file, iscsi, nbd, npiv, phy, tap:aio, tap:qcow, tap:qcow2 and vmdk"
EOF
	exit 1
}

while getopts "t:h:d:" OPTIONS
do
	case $OPTIONS in
		t) case "$OPTARG" in
			.|file|iscsi|nbd|npiv|phy|tap:aio|tap:qcow|tap:qcow2|vmdk)
			disktype="$OPTARG";;
			*) usage;;
		   esac;;
		d) [ -z $OPTARG ] && dir="/usr/share/qa/virtautolib/data/autoinstallation" || dir=$OPTARG;;
		h) usage;;
		*) usage;;
	esac
done

cd "$dir" || exit 1

tmpf=`mktemp`
find \( -name .svn -prune \) -o \( -not -name .svn -type f -print \) > $tmpf

cd - > /dev/null

cat $tmpf | while read line
do
	os="`echo $line | awk -F/ '{ print $2; }'`"
	rel="`echo $line | awk -F/ '{ print $3; }'`"
	sp="`echo $line | awk -F/ '{ print $4; }'`"
	arch="`echo $line | awk -F/ '{ print $5; }'`"
	vtype="`echo $line | awk -F/ '{ print $6; }'`"
	#beware, there is a static sometimes (only sometimes) here!
	static="`echo $line | awk -F/ '{ print $7; }'`"
	scenario="`echo $line | awk -F/ '{ print $NF; }'`"

	if [ "$scenario" != "$static" -a "$os" != "nw" ] ; then
		#TODO - add static support - is this really needed here?
		continue
	fi

	# TODO re-add nfs in the future - currently some issues
	for method in iso net # ftp http iso # nfs
	do
		if [ -z $disktype ]; then
			NAME="$os-$rel-$sp-$arch-$vtype-$scenario-$method"
			DEFINITION="$os-$rel-$sp-$arch-$vtype-$scenario-$method"
			VMINST_ARGS="-o $os -r $rel -p $sp -c $arch -t $vtype -n $scenario -m $method"
		else
			tmpdisktype=`echo $disktype|cut -d: -f2`
			NAME="$os-$rel-$sp-$arch-$vtype-$scenario-$method-$tmpdisktype"
			DEFINITION="$os-$rel-$sp-$arch-$vtype-$scenario-$method-$tmpdisktype"
			VMINST_ARGS="-o $os -r $rel -p $sp -c $arch -t $vtype -n $scenario -m $method -D $disktype"
		fi

		# meaningless cases
		[ "$os" != "win" -a "$vtype" == "fv" -a "$method" == "iso" ] && continue
		[ "$os" == "win" -a "$vtype" != "fv" ] && continue
		[ "$os" == "win" -a "$method" != "iso" ] && continue
		[ "$os" == "nw" -a "$method" != "iso" ] && continue
		[ "$os" == "rhel" -a "$method" == "iso" ] && continue
		[ "$os" == "sles" -a "$rel" = "9" -a "$method" == "iso" ] && continue

		[ "$os" == "oes" -a "$method" == "iso" ] && continue

		# FIXME enable this again - opensuse are highly unreliable and unsupported, work to fix them
		[ "$os" == "os" ] && continue

		cat _install.template | sed "s/@VMINST_ARGS@/$VMINST_ARGS/g" | sed "s/@DEFINITION@/$DEFINITION/g" > install_$NAME
		chmod 755 install_$NAME
	done
done

rm $tmpf

