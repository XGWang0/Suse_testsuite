#! /bin/sh

RC_FAIL=11
RC_FAIL_INT=22

MP=/foo

cleanup() {
	list_cpuset_mp | while read ln; do
		[ "$(echo $ln | cut -f 2 -d ' ')" = "${MP}" ] &&
			{ umount $MP || msg_fail "umount ${MP} failed"; }
	done

	[ -d ${MP} ] &&
		{ rmdir ${MP} || msg_fail "rmdir ${MP} failed"; }

	return 0
}

die() {
	echo "error: $@" >&2
	cleanup
	exit $RC_FAIL_INT
}

msg_fail() {
	echo "failed: $@" >&2
}

fail() {
	msg_fail $@
	cleanup
	exit $RC_FAIL
}

list_cpuset_mp() {
	cat /proc/mounts | while read ln ; do
		echo "$ln" | cut -d " " -f 4 | grep cpuset -q &&
			echo "$ln"
	done

	return 0
}


####################

# {{{ make sure CWD is the same as the script is in, for further
# commands
[ "${0:0:1}" = "/" ] || pref=`pwd`
cd ${pref:-}$(dirname $0) || die "cd failed"
# }}}

trap cleanup EXIT

# {{{ prep cpuset mountpoints
for i in $(list_cpuset_mp); do
	umount $i || die "umount $i failed"
done

mount none -t cpuset ${MP} || die "mount failed"
# }}}

# {{{ start testing
cset shield --cpu 1 -k on || die "cset failed"

# NOTE: `cset shield` will find current mount with -o cpuset and use
# that or if no such mountpoint is found, it will mount new one at
# /cpusets

# {{{ choose pid to move
pid=$(cset proc -l system \
	| sort -R \
	| sed "s/ \+/\t/g" \
	| cut -f 3 \
	| head -n1)
# }}}

# {{{ do the actual test - cpuset_move()
strace ./move_pid $pid /user 2> strace
# {{{ since suse strace ends rc=0 even if the child did not, we have to
# find it in the trace
tail -n 1 strace | grep -q "exit_group(0)" &&
	rc=0 ||
	rc=$(tail -n 1 strace | sed 's/^exit_group(\([0-9]\+\)).*/\1/')
# }}}

grep ENOENT strace | grep -v lib
# Here we should see the attempt to
# open hardcoded /cpusets to verify the bug 625079
# or not see it to verify the fix
# }}}

# }}}

# {{{ print results
[ $rc -gt 0 ] && fail "test failed"
echo "test passed"
# }}}
