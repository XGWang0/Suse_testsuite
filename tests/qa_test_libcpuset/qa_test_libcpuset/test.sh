#! /bin/sh

# {{{ make sure CWD is the same as the script is in, for further
# commands
[ "${0:0:1}" = "/" ] || pref=`pwd`
cd ${pref:-}/$(dirname $0) || { echo "cd failed"; exit 1; }
# }}}

. ./lib.sh

dynamic_mp_case() {
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

	grep ENOENT strace | grep -v lib >>$LOGF
	# Here we should see the attempt to
	# open hardcoded /cpusets to verify the bug 625079
	# or not see it to verify the fix
	# }}}

	return $rc
}

dynamic_mp_setup() {
	# {{{ prep cpuset mountpoints
	for i in $(list_cpuset_mp); do
		umount $i || die "umount $i failed"
	done

	mkdir $MP || die "mkdir $MP failed"
	mount none -t cpuset ${MP} >>$LOGF 2>&1 || die "mount ${MP} failed"
	# }}}

	# {{{ start testing
	cset shield --cpu 1 -k on >>$LOGF 2>&1 || die "cset failed"

	# NOTE: `cset shield` will find current mount with -o cpuset and use
	# that or if no such mountpoint is found, it will mount new one at
	# /cpusets
}

dynamic_mp_cleanup() {
	list_cpuset_mp | while read ln; do
		[ "$(echo $ln | cut -f 2 -d ' ')" = "${MP}" ] &&
			{ umount $MP || msg_fail "umount ${MP} failed"; }
	done

	[ -d ${MP} ] &&
		{ rmdir ${MP} || msg_fail "rmdir ${MP} failed"; }

	return 0
}

test_dynamic_mp() {
	cleanup_() {
		dynamic_mp_cleanup
	}

	case_() {
		dynamic_mp_case
	}

	setup_() {
		dynamic_mp_setup
	}
}

test_dynamic_mp_with_cpuset_mp() {
	cleanup_() {
		dynamic_mp_cleanup

		cat /proc/mounts |
			cut -f 2 -d " " |
			grep $CPUSET_PATH_MP >>$LOGF &&
				umount $CPUSET_PATH_MP

		[ -d $CPUSET_PATH_MP ] && rmdir $CPUSET_PATH_MP

		return 0
	}

	case_() {
		dynamic_mp_case
	}

	setup_() {
		mkdir $CPUSET_PATH_MP || die "mkdir $CPUSET_PATH_MP failed"
		mount --bind -o ro / $CPUSET_PATH_MP >>$LOGF ||
			die "mount $CPUSET_PATH_MP failed"

		dynamic_mp_setup
	}
}

main "$@"
