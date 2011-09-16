#!/bin/bash

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
			if [[ "$i" =~ "^\[" ]]
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

ROOTDEV="$(get_tmp_dev)"
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
	if [[ "$i" =~ "^\[" ]]
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
