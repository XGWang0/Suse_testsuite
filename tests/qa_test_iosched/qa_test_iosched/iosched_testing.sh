#!/bin/bash
# ****************************************************************************
# Copyright © 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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

export TIOCALL="/usr/bin/tiotest -t 2 -c -f 512 -r 4000 -b 4096 -d /tmp "

#default to root-device
export ROOTDEV="$(egrep '.*dev.* / ' /proc/mounts | cut -d' ' -f1)"

export BLOCK=""

export CURRENT=""

declare -a SCHEDULERS
export SCHEDULERS=()


#we need to be root
if [ "$UID" -ne "0" ]
then
	echo "ERROR: you need to be root to run this test" >&2
	exit 2;
fi

if ! [ -x "/usr/bin/tiotest" ]
then
	echo "ERROR: tiotest/tiobench needs to be installed" >&2
	exit 2;
fi


#get block device and scheduler-name
function set_scheduler ()
{
	if [ -d "/sys/block/$1" ]
	then
		echo "$2" > /sys/block/$1/queue/scheduler
	else
		echo "Internal error: $1 is no blockdevice under /sys/block" >&2
		exit 2
	fi
}

#needs block-device
function get_current_scheduler ()
{
	if [ -d "/sys/block/$1" ]
	then
		for i in $(< /sys/block/$1/queue/scheduler)
		do
			if [ $(echo $i | grep -e "^\[") ]
			then
				echo "$(echo $i|tr -d '\[\]')"
			fi
		done
	else
		echo "Internal error: $1 is no blockdevice under /sys/block" >&2
		exit 2
	fi
}

#will print device the /tmp dir is mounted to
function get_tmp_dev ()
{
	for i in $(cut -d' ' -f2 /proc/mounts)
	do
		echo "${#i}:$i"
	done |sort -g |cut -d':' -f2 | while read DATA
	do
		if [[ "/tmp" =~ "^$DATA" ]]
		then
			echo -en "$(egrep ".*dev.* $DATA " /proc/mounts|cut -d' ' -f1)"
			return 0
			break
		fi
	done
}

if [ -z "$(get_tmp_dev)" ]; then
	#if get_tmp_dev() cannot get a result, check root dev
	ROOTDEV=`df -l | grep "/$" | cut -d' ' -f1 | sed -e 's/[0-9]//g'`
else
	ROOTDEV="$(get_tmp_dev)"
fi

BLOCK="${ROOTDEV##*/}"

#get blockdevice
for i in /sys/block/*
do
	j="${i##*/}"
	if [[ "$BLOCK" =~ "^$j" ]]
	then
		BLOCK="$j"
	fi
done

echo "Running test on $ROOTDEV (which is blockdevice $BLOCK):"

#get schedulers available
for i in $(< /sys/block/$BLOCK/queue/scheduler)
do
	#if [[ "$i" =~ "^\[" ]]
	if [ `echo $i | grep -e "^\["` ]
	then
		CURRENT="$(echo $i|tr -d '\[\]')"
		SCHEDULERS=(${SCHEDULERS[@]} $CURRENT)
	else
		SCHEDULERS=(${SCHEDULERS[@]} $i)
	fi

done

## NOW lets do the work

declare -a READRATES
declare -a WRITERATES
declare -a LATENCIES

for i in ${SCHEDULERS[@]}
do
	echo "Setting scheduler to:$i"
	set_scheduler $BLOCK $i
	sleep 1
	if [ "$(get_current_scheduler $BLOCK)" == "$i" ]
	then
		echo "Changing scheduler succeeded.."
		echo "Starting tiobench on /tmp .."
		export TFILE="$(mktemp)"
		$TIOCALL >$TFILE

		LATENCY="$(cat $TFILE | perl -ne 's/^\| Total\s+\|\s*([0-9\.]+) ms.+$/\1/ and print')"
		WRITERATE="$(cat $TFILE | perl -ne 's/^\| Write\s+[^\|]+\|[^\|]+\|\s*([0-9\.]+) MB.+$/\1/ and print')"
		READRATE="$(cat $TFILE | perl -ne 's/^\| Read\s+[^\|]+\|[^\|]+\|\s*([0-9\.]+) MB.+$/\1/ and print')"
		
		echo "=>$i:Read-Rate/MB/s:$READRATE"
		echo "=>$i:Write-Rate/MB/s:$WRITERATE"
		echo "=>$i:Avg.Latency/ms:$LATENCY"
		
		LATENCIES=(${LATENCIES[@]} "$LATENCY:$i")
		READRATES=(${READRATES[@]} "$READRATE:$i")
		WRITERATES=(${WRITERATES[@]} "$WRITERATE:$i")

		rm -f "$TFILE"
	else
		echo "Failure on changing scheduler. Exiting"
		exit 1
	fi
done

echo "Summary for read-speeds:"
for i in "${READRATES[@]}"
do
	echo "$i"
done | sort -g

echo "Summary for write-speeds:"
for i in "${WRITERATES[@]}"
do
	echo "$i"
done | sort -g

echo "Summary for latencies:"
for i in "${LATENCIES[@]}"
do
	echo "$i"
done | sort -g

