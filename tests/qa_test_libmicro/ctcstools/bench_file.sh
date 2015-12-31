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
close		$OPTS -N "close_bad"		-B 32		-b
close		$OPTS -N "close_tmp"		-B 32		-f $TFILE
close		$OPTS -N "close_usr"		-B 32		-f $VFILE
close		$OPTS -N "close_zero"		-B 32		-f /dev/zero

chdir		$OPTS -N "chdir_tmp"	-I 2000		$TDIR1 $TDIR2
chdir		$OPTS -N "chdir_usr"	-I 2000		$VDIR1 $VDIR2

chdir		$OPTS -N "chgetwd_tmp"	-I 3000	-g $TDIR1 $TDIR2
chdir		$OPTS -N "chgetwd_usr"	-I 3000	-g $VDIR1 $VDIR2

realpath	$OPTS -N "realpath_tmp" -I 3000		-f $TDIR1
realpath	$OPTS -N "realpath_usr"	-I 3000	-f $VDIR1

lseek		$OPTS -N "lseek_t8k"	-s 8k	-I 50	-f $TFILE
lseek		$OPTS -N "lseek_u8k"	-s 8k	-I 50	-f $VFILE

open		$OPTS -N "open_tmp"		-B 256		-f $TFILE
open		$OPTS -N "open_usr"		-B 256		-f $VFILE
open		$OPTS -N "open_zero"		-B 256		-f /dev/zero

dup		$OPTS -N "dup"			-B 512   

recurse		$OPTS -N "recurse"		-B 512

read		$OPTS -N "read_t1k"	-s 1k			-f $TFILE
read		$OPTS -N "read_t10k"	-s 10k			-f $TFILE
read		$OPTS -N "read_t100k"	-s 100k			-f $TFILE

read		$OPTS -N "read_u1k"	-s 1k			-f $VFILE
read		$OPTS -N "read_u10k"	-s 10k			-f $VFILE
read		$OPTS -N "read_u100k"	-s 100k			-f $VFILE

read		$OPTS -N "read_z1k"	-s 1k			-f /dev/zero 
read		$OPTS -N "read_z10k"	-s 10k			-f /dev/zero 
read		$OPTS -N "read_z100k"	-s 100k			-f /dev/zero 
read		$OPTS -N "read_zw100k"	-s 100k	         -w	-f /dev/zero 

write		$OPTS -N "write_t1k"	-s 1k			-f $TFILE
write		$OPTS -N "write_t10k"	-s 10k			-f $TFILE
write		$OPTS -N "write_t100k"	-s 100k			-f $TFILE

write		$OPTS -N "write_u1k"	-s 1k			-f $VFILE
write		$OPTS -N "write_u10k"	-s 10k			-f $VFILE
write		$OPTS -N "write_u100k"	-s 100k			-f $VFILE

write		$OPTS -N "write_n1k"	-s 1k	-I 100 -B 0	-f /dev/null 
write		$OPTS -N "write_n10k"	-s 10k	-I 100 -B 0	-f /dev/null 
write		$OPTS -N "write_n100k"	-s 100k	-I 100 -B 0	-f /dev/null 

writev		$OPTS -N "writev_t1k"	-s 1k			-f $TFILE
writev		$OPTS -N "writev_t10k"	-s 10k		        -f $TFILE
writev		$OPTS -N "writev_t100k"	-s 100k			-f $TFILE

writev		$OPTS -N "writev_u1k"	-s 1k			-f $VFILE
writev		$OPTS -N "writev_u10k"	-s 10k			-f $VFILE
writev		$OPTS -N "writev_u100k"	-s 100k			-f $VFILE

writev		$OPTS -N "writev_n1k"	-s 1k	-I 100 -B 0	-f /dev/null 
writev		$OPTS -N "writev_n10k"	-s 10k	-I 100 -B 0	-f /dev/null 
writev		$OPTS -N "writev_n100k"	-s 100k	-I 100 -B 0	-f /dev/null 

pread		$OPTS -N "pread_t1k"	-s 1k	-I 300		-f $TFILE
pread		$OPTS -N "pread_t10k"	-s 10k	-I 1000		-f $TFILE
pread		$OPTS -N "pread_t100k"	-s 100k	-I 10000	-f $TFILE

pread		$OPTS -N "pread_u1k"	-s 1k	-I 300		-f $VFILE
pread		$OPTS -N "pread_u10k"	-s 10k	-I 1000		-f $VFILE
pread		$OPTS -N "pread_u100k"	-s 100k	-I 10000	-f $VFILE

pread		$OPTS -N "pread_z1k"	-s 1k	-I 300		-f /dev/zero 
pread		$OPTS -N "pread_z10k"	-s 10k	-I 1000		-f /dev/zero 
pread		$OPTS -N "pread_z100k"	-s 100k	-I 2000	-f /dev/zero 
pread		$OPTS -N "pread_zw100k"	-s 100k	-w -I 10000	-f /dev/zero 

pwrite		$OPTS -N "pwrite_t1k"	-s 1k	-I 500		-f $TFILE
pwrite		$OPTS -N "pwrite_t10k"	-s 10k	-I 1000		-f $TFILE
pwrite		$OPTS -N "pwrite_t100k"	-s 100k	-I 10000	-f $TFILE

pwrite		$OPTS -N "pwrite_u1k"	-s 1k	-I 500		-f $VFILE
pwrite		$OPTS -N "pwrite_u10k"	-s 10k	-I 1000		-f $VFILE
pwrite		$OPTS -N "pwrite_u100k"	-s 100k	-I 20000	-f $VFILE

pwrite		$OPTS -N "pwrite_n1k"	-s 1k	-I 100		-f /dev/null 
pwrite		$OPTS -N "pwrite_n10k"	-s 10k	-I 100		-f /dev/null 
pwrite		$OPTS -N "pwrite_n100k"	-s 100k	-I 100		-f /dev/null 
.
