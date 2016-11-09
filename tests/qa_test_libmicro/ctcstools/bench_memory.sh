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


OPTS="-E -C 0 -D 30000 -B 10000 -L -S -W"

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
mutex           $OPTS -N "mutex_st"     -I 10
mutex           $OPTS -N "mutex_mt"     -t -I 10        
mutex           $OPTS -N "mutex_T2"     -T 2  -I 100

longjmp         $OPTS -N "longjmp"      -I 10
siglongjmp      $OPTS -N "siglongjmp"   -I 20

cascade_mutex   $OPTS -N "c_mutex_1"    -I 50
cascade_mutex   $OPTS -N "c_mutex_10"   -T 10 -I 5000
cascade_mutex   $OPTS -N "c_mutex_200"  -T 200  -I 2000000
 Obligatory null system call: use very short time
# for default since SuSe implements this "syscall" in userland
#
memset		$OPTS -N "memset_10"	-s 10	-I 10 
memset		$OPTS -N "memset_256"	-s 256	-I 20
memset		$OPTS -N "memset_256_u"	-s 256	 -a 1 -I 20 
memset		$OPTS -N "memset_1k"	-s 1k	 -I 100
memset		$OPTS -N "memset_4k"    -s 4k    -I 250
memset		$OPTS -N "memset_4k_uc" -s 4k    -u -I 400

memset		$OPTS -N "memset_10k"	-s 10k	-I 600	 
#memset		$OPTS -N "memset_1m"	-s 1m	-I 200000
#memset		$OPTS -N "memset_10m"	-s 10m -I 2000000 
#memset		$OPTS -N "memsetP2_10m"	-s 10m -P 2 -I 2000000 

memrand		$OPTS -N "memrand"	-s 128m -B 10000
cachetocache	$OPTS -N "cachetocache" -s 100k -T 2 -I 200

malloc		$OPTS -N "malloc_10"    -s 10    -g 10 -I 50
malloc		$OPTS -N "malloc_100"   -s 100   -g 10 -I 50
malloc		$OPTS -N "malloc_1k"    -s 1k    -g 10 -I 50
malloc		$OPTS -N "malloc_10k"   -s 10k   -g 10 -I 50
malloc		$OPTS -N "malloc_100k"  -s 100k  -g 10 -I 2000

malloc		$OPTS -N "mallocT2_10"    -s 10   -g 10 -T 2 -I 200
malloc		$OPTS -N "mallocT2_100"   -s 100  -g 10 -T 2 -I 200
malloc		$OPTS -N "mallocT2_1k"    -s 1k   -g 10 -T 2 -I 200
malloc		$OPTS -N "mallocT2_10k"   -s 10k  -g 10 -T 2 -I 200
#malloc		$OPTS -N "mallocT2_100k"  -s 100k -g 10 -T 2 -I 10000

memcpy		$OPTS -N "memcpy_10"	-s 10	-I 10 
memcpy		$OPTS -N "memcpy_1k"	-s 1k	-I 50
memcpy		$OPTS -N "memcpy_10k"	-s 10k	-I 800
#memcpy		$OPTS -N "memcpy_1m"	-s 1m   -I 500000
#memcpy		$OPTS -N "memcpy_10m"	-s 10m  -I 5000000

strcpy		$OPTS -N "strcpy_10"	-s 10   -I 5 
strcpy		$OPTS -N "strcpy_1k"	-s 1k   -I 100

strlen		$OPTS -N "strlen_10"	-s 10   -I 5
strlen		$OPTS -N "strlen_1k"	-s 1k   -I 100

strchr		$OPTS -N "strchr_10"	-s 10   -I 5
strchr		$OPTS -N "strchr_1k"	-s 1k   -I 200
strcmp		$OPTS -N "strcmp_10"	-s 10   -I 10
strcmp		$OPTS -N "strcmp_1k"	-s 1k   -I 200

strcasecmp	$OPTS -N "scasecmp_10"	-s 10 -I 50
strcasecmp	$OPTS -N "scasecmp_1k"	-s 1k -I 20000

mutex		$OPTS -N "mutex_st"	-I 10
mutex		$OPTS -N "mutex_mt"	-t -I 10	
mutex		$OPTS -N "mutex_T2"     -T 2  -I 100

cascade_mutex	$OPTS -N "c_mutex_1"	-I 50
cascade_mutex	$OPTS -N "c_mutex_10"	-T 10 -I 5000
cascade_mutex	$OPTS -N "c_mutex_200"	-T 200	-I 2000000

cascade_cond	$OPTS -N "c_cond_1"	-I 100
cascade_cond	$OPTS -N "c_cond_10"	-T 10	-I 3000
cascade_cond	$OPTS -N "c_cond_200"	-T 200	-I 2000000

cascade_lockf	$OPTS -N "c_lockf_1"	-I 1000	
cascade_lockf	$OPTS -N "c_lockf_10"	-P 10 -I 50000
cascade_lockf	$OPTS -N "c_lockf_200"	-P 200 -I 5000000

cascade_flock	$OPTS -N "c_flock"	-I 1000	
cascade_flock	$OPTS -N "c_flock_10"	-P 10   -I 50000
cascade_flock	$OPTS -N "c_flock_200"	-P 200	-I 5000000

cascade_fcntl	$OPTS -N "c_fcntl_1"	-I 2000 	
cascade_fcntl	$OPTS -N "c_fcntl_10"	-P 10 -I 20000
cascade_fcntl	$OPTS -N "c_fcntl_200"	-P 200	-I 5000000

file_lock	$OPTS -N "file_lock"   -I 1000         

fcntl		$OPTS -N "fcntl_tmp"	-I 100	-f $TFILE
fcntl		$OPTS -N "fcntl_usr"	-I 100	-f $VFILE
fcntl_ndelay	$OPTS -N "fcntl_ndelay"	-I 100	

mmap		$OPTS -N "mmap_z8k"	-l 8k   -I 1000		-f /dev/zero
mmap		$OPTS -N "mmap_z128k"	-l 128k	-I 2000		-f /dev/zero
mmap		$OPTS -N "mmap_t8k"	-l 8k	-I 1000		-f $TFILE
mmap		$OPTS -N "mmap_t128k"	-l 128k	-I 1000		-f $TFILE
mmap		$OPTS -N "mmap_u8k"	-l 8k	-I 1000		-f $VFILE
mmap		$OPTS -N "mmap_u128k"	-l 128k	-I 1000		-f $VFILE
mmap		$OPTS -N "mmap_a8k"	-l 8k	-I 200		-f MAP_ANON
mmap		$OPTS -N "mmap_a128k"	-l 128k	-I 200		-f MAP_ANON


mmap		$OPTS -N "mmap_rz8k"	-l 8k	-I 2000 -r	-f /dev/zero
mmap		$OPTS -N "mmap_rz128k"	-l 128k	-I 2000 -r	-f /dev/zero
mmap		$OPTS -N "mmap_rt8k"	-l 8k	-I 2000 -r	-f $TFILE
mmap		$OPTS -N "mmap_rt128k"	-l 128k	-I 20000 -r	-f $TFILE
mmap		$OPTS -N "mmap_ru8k"	-l 8k	-I 2000 -r	-f $VFILE
mmap		$OPTS -N "mmap_ru128k"	-l 128k	-I 20000 -r	-f $VFILE
mmap		$OPTS -N "mmap_ra8k"	-l 8k	-I 2000 -r	-f MAP_ANON
mmap		$OPTS -N "mmap_ra128k"	-l 128k	-I 20000 -r	-f MAP_ANON

mmap		$OPTS -N "mmap_wz8k"	-l 8k	-I 5000 -w	-f /dev/zero
#mmap		$OPTS -N "mmap_wz128k"	-l 128k	-I 50000 -w	-f /dev/zero
mmap		$OPTS -N "mmap_wt8k"	-l 8k	-I 5000 -w	-f $TFILE
#mmap		$OPTS -N "mmap_wt128k"	-l 128k	-I 50000 -w	-f $TFILE
mmap		$OPTS -N "mmap_wu8k"	-l 8k	-I 5000 -w	-f $VFILE
mmap		$OPTS -N "mmap_wu128k"	-l 128k	-I 500000 -w	-f $VFILE
mmap		$OPTS -N "mmap_wa8k"	-l 8k	-I 3000 -w	-f MAP_ANON
#mmap		$OPTS -N "mmap_wa128k"	-l 128k	-I 50000 -w	-f MAP_ANON

munmap		$OPTS -N "unmap_z8k"	-l 8k   -I 500		-f /dev/zero
munmap		$OPTS -N "unmap_z128k"	-l 128k	-I 500		-f /dev/zero
munmap		$OPTS -N "unmap_t8k"	-l 8k	-I 500		-f $TFILE
munmap		$OPTS -N "unmap_t128k"	-l 128k	-I 500		-f $TFILE
munmap		$OPTS -N "unmap_u8k"	-l 8k	-I 500		-f $VFILE
munmap		$OPTS -N "unmap_u128k"	-l 128k	-I 500		-f $VFILE
munmap		$OPTS -N "unmap_a8k"	-l 8k	-I 500		-f MAP_ANON
munmap		$OPTS -N "unmap_a128k"	-l 128k	-I 500		-f MAP_ANON

munmap		$OPTS -N "unmap_rz8k"	-l 8k	-I 1000	-r	-f /dev/zero
munmap		$OPTS -N "unmap_rz128k"	-l 128k	-I 2000 -r	-f /dev/zero
munmap		$OPTS -N "unmap_rt8k"	-l 8k	-I 1000	-r	-f $TFILE
munmap		$OPTS -N "unmap_rt128k"	-l 128k	-I 3000	-r	-f $TFILE
munmap		$OPTS -N "unmap_ru8k"	-l 8k	-I 1000	-r	-f $VFILE
munmap		$OPTS -N "unmap_ru128k"	-l 128k	-I 3000	-r	-f $VFILE
munmap		$OPTS -N "unmap_ra8k"	-l 8k	-I 1000	-r	-f MAP_ANON
munmap		$OPTS -N "unmap_ra128k"	-l 128k	-I 2000	-r	-f MAP_ANON

connection	$OPTS -N "conn_connect"		-B 256 	-c

munmap		$OPTS -N "unmap_wz8k"	-l 8k	-I 1000	-w	-f /dev/zero
#munmap		$OPTS -N "unmap_wz128k"	-l 128k	-I 8000	-w	-f /dev/zero
munmap		$OPTS -N "unmap_wt8k"	-l 8k	-I 1000	-w	-f $TFILE
#munmap		$OPTS -N "unmap_wt128k"	-l 128k	-I 10000	-w	-f $TFILE
munmap		$OPTS -N "unmap_wu8k"	-l 8k	-I 1000	-w	-f $VFILE
munmap		$OPTS -N "unmap_wu128k"	-l 128k	-I 50000	-w	-f $VFILE
munmap		$OPTS -N "unmap_wa8k"	-l 8k	-I 1000	-w	-f MAP_ANON
#munmap		$OPTS -N "unmap_wa128k"	-l 128k	-I 10000	-w	-f MAP_ANON


mprotect	$OPTS -N "mprot_z8k"	-l 8k  -I 300			-f /dev/zero
mprotect	$OPTS -N "mprot_z128k"	-l 128k	-I 500		-f /dev/zero
mprotect	$OPTS -N "mprot_wz8k"	-l 8k	-I 500	-w	-f /dev/zero
mprotect	$OPTS -N "mprot_wz128k"	-l 128k	-I 1000	-w	-f /dev/zero
mprotect	$OPTS -N "mprot_twz8k"  -l 8k   -I 1000 -w -t   -f /dev/zero
mprotect	$OPTS -N "mprot_tw128k" -l 128k -I 2000 -w -t   -f /dev/zero
#mprotect	$OPTS -N "mprot_tw4m"   -l 4m   -w -t -B 1  -f /dev/zero

pipe		$OPTS -N "pipe_pst1"	-s 1	-I 1000	-x pipe -m st
pipe		$OPTS -N "pipe_pmt1"	-s 1	-I 8000	-x pipe -m mt
pipe		$OPTS -N "pipe_pmp1"	-s 1	-I 8000	-x pipe -m mp
pipe		$OPTS -N "pipe_pst4k"	-s 4k	-I 1000	-x pipe -m st
pipe		$OPTS -N "pipe_pmt4k"	-s 4k	-I 8000	-x pipe -m mt
pipe		$OPTS -N "pipe_pmp4k"	-s 4k	-I 8000	-x pipe -m mp

pipe		$OPTS -N "pipe_sst1"	-s 1	-I 1000	-x sock -m st
pipe		$OPTS -N "pipe_smt1"	-s 1	-I 8000	-x sock -m mt
pipe		$OPTS -N "pipe_smp1"	-s 1	-I 8000	-x sock -m mp
pipe		$OPTS -N "pipe_sst4k"	-s 4k	-I 1000	-x sock -m st
pipe		$OPTS -N "pipe_smt4k"	-s 4k	-I 8000	-x sock -m mt
pipe		$OPTS -N "pipe_smp4k"	-s 4k	-I 8000	-x sock -m mp

pipe		$OPTS -N "pipe_tst1"	-s 1	-I 1000	-x tcp  -m st
pipe		$OPTS -N "pipe_tmt1"	-s 1	-I 8000	-x tcp  -m mt
pipe		$OPTS -N "pipe_tmp1"	-s 1	-I 8000	-x tcp  -m mp
pipe		$OPTS -N "pipe_tst4k"	-s 4k	-I 1000	-x tcp  -m st
pipe		$OPTS -N "pipe_tmt4k"	-s 4k	-I 8000	-x tcp  -m mt
pipe		$OPTS -N "pipe_tmp4k"	-s 4k	-I 8000	-x tcp  -m mp

connection	$OPTS -N "conn_accept"		-B 256      -a
.
