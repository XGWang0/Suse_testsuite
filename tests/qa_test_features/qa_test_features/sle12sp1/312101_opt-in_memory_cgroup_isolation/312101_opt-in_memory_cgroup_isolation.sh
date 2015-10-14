#!/bin/bash
# ****************************************************************************
# Copyright © 2015 Unpublished Work of SUSE, Inc. All Rights Reserved.
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

cat << EOF
This is a feature test FATE312101, written in bash and C.

You can do anything here except reboot, please just make sure
that you cleanup after yourself!!!

The test results are determined by the return value of this script:

  0	PASSED
  1	FAILED
 11	INTERNAL ERROR
 22	SKIPPED

So, since this is not a real test, we will wait for three seconds
and than mark this test as skipped.

Happy testing!

EOF

setup_dir=$(dirname $0)
pushd $setup_dir

num_bytes=$(echo "$(grep MemTotal /proc/meminfo | awk '{print $2}') * 1024" | bc)
low_limit_size=$(($num_bytes/3))

ROOT_CGROUP="/dev/memctl/"
CGROUP1="$ROOT_CGROUP/group_1"
CGROUP_SIZE=${num_bytes}
CGROUP_LOW_LIMIT_SIZE=${low_limit_size}


concurent_consumer_bytes=$((${num_bytes}*2/11))

CONCURENT_CONSUMER=true
CONCURENT_CONSUMER_TIMEOUT=30s
CONCURENT_CONSUMER_ANON_PRIV=${concurent_consumer_bytes}
CONCURENT_CONSUMER_ANON_SHARED=${concurent_consumer_bytes}
CONCURENT_CONSUMER_SHM=${concurent_consumer_bytes}


CGROUP_LOG_PATTERN="\<cache\>\|\<rss\>\|\<inactive\|\<active"
SYSTEM_LOG_PATTERN="nr_free_pages\|active\|inactive"
LOG_FILE="/tmp/cgroup1-log-`date +%y%m%d_%H%M%S`"
LOG_TIMEOUT="1s"

dbg()
{
	echo "====>" $*
}

log()
{
	(
		echo $BASHPID > $ROOT_CGROUP/tasks
		echo Start loggin into $LOG_FILE
		while true
		do
			grep "$CGROUP_LOG_PATTERN" $CGROUP1/memory.stat | tr " \n" "::" >> $LOG_FILE
			grep "$SYSTEM_LOG_PATTERN" /proc/vmstat | tr " \n" "::" >> $LOG_FILE
			echo >> $LOG_FILE
			sleep $LOG_TIMEOUT
		done
	) &
}

run_sharks()
{
	dbg "release sharks"
	for i in `seq $1`
	do
		./consumer total_mem=$2 work_mode=2 >/dev/null &
	done
}

run_concurent_consumer()
{
	(
		echo $BASHPID > $ROOT_CGROUP/tasks
		sleep $1
		dbg "Running concurent consumer in the main group"
		./consumer private_anon=$2 shared_anon=$3 shm=$4 work_mode=2
	) &
}

dbg Init memory cgroups
[ -d "$ROOT_CGROUP" ] || mkdir "$ROOT_CGROUP"
mount | grep "${ROOT_CGROUP%/}" 1>/dev/null 2>&1 || mount -t cgroup -omemory cgroup "$ROOT_CGROUP"
[ -d "$CGROUP1" ] || mkdir "$CGROUP1"

echo $CGROUP_SIZE > "$CGROUP1"/memory.limit_in_bytes
echo $CGROUP_LOW_LIMIT_SIZE > "$CGROUP1"/memory.low_limit_in_bytes
echo $$ > "$CGROUP1"/tasks

# page in binaries etc...
dbg "Warm up round"
./consumer

dbg "Wait to calm down"
sleep 10s


# background logging
log

dbg "Wait to settle"
sleep 10s

dbg "Run the big consumer"
./consumer total_mem=1140000000 work_mode=1 &
C_PID=$!

dbg "Wait to settle"
sleep 30s

set -x

[ "i$CONCURENT_CONSUMER" = "itrue" ] && run_concurent_consumer $CONCURENT_CONSUMER_TIMEOUT $CONCURENT_CONSUMER_ANON_PRIV $CONCURENT_CONSUMER_ANON_SHARED $CONCURENT_CONSUMER_SHM

wait
popd
