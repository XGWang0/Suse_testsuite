#!/bin/sh
#
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms
# of the Common Development and Distribution License
# (the "License").  You may not use this file except
# in compliance with the License.
#
# You can obtain a copy of the license at
# src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing
# permissions and limitations under the License.
#
# When distributing Covered Code, include this CDDL
# HEADER in each file and include the License file at
# usr/src/OPENSOLARIS.LICENSE.  If applicable,
# add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your
# own identifying information: Portions Copyright [yyyy]
# [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

BIN="/usr/lib/libMicro/bin"
bench_version=0.4.0
libmicro_version=`$BIN/tattle -V`

case $libmicro_version in
$bench_version)
	;;
*)
	echo "ERROR: libMicro version doesn't match 'bench' script version"
	exit 1
esac

TMPROOT=/tmp/libmicro.$$
VARROOT=/var/tmp/libmicro.$$
mkdir -p $TMPROOT
mkdir -p $VARROOT
trap "rm -rf $TMPROOT $VARROOT" 0 2

TFILE=$TMPROOT/data
IFILE=$TMPROOT/ifile
TDIR1=$TMPROOT/0/1/2/3/4/5/6/7/8/9
TDIR2=$TMPROOT/1/2/3/4/5/6/7/8/9/0
VFILE=$VARROOT/data
VDIR1=$VARROOT/0/1/2/3/4/5/6/7/8/9
VDIR2=$VARROOT/1/2/3/4/5/6/7/8/9/0


OPTS="-E -C 200 -L -S -W"

dd if=/dev/zero of=$TFILE bs=1024k count=10 2>/dev/null
dd if=/dev/zero of=$VFILE bs=1024k count=10 2>/dev/null
mkdir -p $TDIR1 $TDIR2
mkdir -p $VDIR1 $VDIR2

touch $IFILE

ARCH=`arch`

# produce benchmark header for easier comparisons

hostname=`uname -n`

if [ -f /usr/sbin/psrinfo ]; then
	p_count=`psrinfo|wc -l`
	p_mhz=`psrinfo -v | awk '/operates/{print $6 "MHz"; exit }'`
	p_type=`psrinfo -vp 2>/dev/null | awk '{if (NR == 3) {print $0; exit}}'` 
fi

if [ -f /proc/cpuinfo ]; then
	p_count=`egrep processor /proc/cpuinfo | wc -l`
	p_mhz=`awk -F: '/cpu MHz/{printf("%5.0f00Mhz\n",$2/100); exit}' /proc/cpuinfo`
	p_type=`awk -F: '/model name/{print $2; exit}' /proc/cpuinfo`
fi

printf "!Libmicro_#:   %30s\n" $libmicro_version
printf "!Options:      %30s\n" "$OPTS"
printf "!Machine_name: %30s\n" $hostname
printf "!OS_name:      %30s\n" `uname -s`
printf "!OS_release:   %30s\n" `uname -r`
printf "!OS_build:     %30.18s\n" "`uname -v`"
printf "!Processor:    %30s\n" `uname -m`
printf "!#CPUs:        %30s\n" $p_count
printf "!CPU_MHz:      %30s\n" $p_mhz
printf "!CPU_NAME:     %30s\n" "$p_type"
printf "!IP_address:   %30s\n" `getent hosts $hostname | awk '{print $1}'`
printf "!Run_by:       %30s\n" $LOGNAME
printf "!Date:	       %30s\n" "`date '+%D %R'`"
printf "!Compiler:     %30s\n" `$BIN/tattle -c`
printf "!Compiler Ver.:%30s\n" "`$BIN/tattle -v`"
printf "!sizeof(long): %30s\n" `$BIN/tattle -s`
printf "!extra_CFLAGS: %30s\n" "`$BIN/tattle -f`"
printf "!TimerRes:     %30s\n" "`$BIN/tattle -r`"
 
mkdir -p $TMPROOT/bin
cp $BIN/exec_bin $TMPROOT/bin/$A

while read A B
do
	# $A contains the command, $B contains the arguments
	# we echo blank lines and comments
	# we ship anything which fails to match *$1* (useful
	# if we only want to test one case, but a nasty hack)

	case $A in
	""|"#"*)
		echo "$A $B"
		continue
		;;
	*$1*)
		;;
	*)
		continue
	esac

	if [ ! -f $TMPROOT/bin/$A ]
	then
		cp $BIN/$A $TMPROOT/bin/$A
	fi
	(cd $TMPROOT && eval "$BIN/$A $B")
done <<.
#
# Obligatory null system call: use very short time
# for default since SuSe implements this "syscall" in userland
#
getsockname	$OPTS -N "getsockname"	-I 100
getpeername	$OPTS -N "getpeername"	-I 100

socket		$OPTS -N "socket_u"		-B 256
socket		$OPTS -N "socket_i"		-B 256		-f PF_INET

socketpair	$OPTS -N "socketpair"		-B 256

setsockopt	$OPTS -N "setsockopt"		-I 200

bind		$OPTS -N "bind"			-B 100

listen		$OPTS -N "listen"		-B 100

connection	$OPTS -N "connection"		-B 256 

poll		$OPTS -N "poll_10"	-n 10	-I 500
poll		$OPTS -N "poll_100"	-n 100	-I 1000
poll		$OPTS -N "poll_1000"	-n 1000	-I 5000

poll		$OPTS -N "poll_w10"	-n 10	-I 500		-w 1
poll		$OPTS -N "poll_w100"	-n 100	-I 2000		-w 10
poll		$OPTS -N "poll_w1000"	-n 1000	-I 40000	-w 100

select		$OPTS -N "select_10"	-n 10	-I 500
select		$OPTS -N "select_100"	-n 100	-I 1000
select		$OPTS -N "select_1000"	-n 1000	-I 5000

select		$OPTS -N "select_w10"	-n 10	-I 500		-w 1
select		$OPTS -N "select_w100"	-n 100	-I 2000		-w 10
select		$OPTS -N "select_w1000"	-n 1000	-I 40000        -w 100

connection	$OPTS -N "conn_accept"		-B 256      -a

close_tcp	$OPTS -N "close_tcp"		-B 32  
.