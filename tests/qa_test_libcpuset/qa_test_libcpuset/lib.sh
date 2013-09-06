#! /bin/sh

# {{{ generic testing scafolding
# {{{ overridable config
CLEANUP=true
LOGF=/dev/null
# }}}

RC_FAIL=11
RC_FAIL_INT=22


# {{{ terminators
die() {
	dief msg_err $@
}

dief() {
	f=$1
	shift
	$f $@
	exit $RC_FAIL_INT
}

fail() {
	msg_fail $@
	exit $RC_FAIL
}
# }}}

# {{{ loggers
msg_err() {
	echo "error: $@" >&2
}
msg_fail() {
	echo "failed: $@" >&2
}
# }}}

cleanup() {
	$CLEANUP || return 0
	is_func cleanup_ && cleanup_
}

is_func() {
	{ type $1 | head -n1 | grep "^${1} is a function$"; } >>$LOGF 2>&1
}

main() {
	usage() {
		echo "Usage: $0 [-x] [-n] [-v] [-V] [-h] [<case>]"
		echo ""
		echo "  -x for shell tracing"
		echo "  -n for no cleanup"
		echo "  -v for increased verbosity"
		echo "  -h help"
		echo "  -V version"
	}

	while getopts xVnvh name ; do
		case $name in
			x) set -x;;
			n) CLEANUP=false;;
			v) export LOGF="/dev/stdout";;
			h) usage; exit 0;;
			V) echo $CPUSET_TEST_VERSION; exit 0;;
			*) dief usage;;
		esac
	done

	shift $((OPTIND - 1))

	[ $# -eq 0 ] && { dief usage; }

	test_=test_$1

	is_func $test_ ||
		{ echo "invalid $1"; dief usage; }

	$test_
	trap cleanup EXIT
	is_func setup_ && setup_
	case_

	[ $? -gt 0 ] && fail "test failed"
	echo "test passed"
}
# }}}

# {{{ testsuite specific helpers
CPUSET_TEST_VERSION=0.1.0
MP=/foo
CPUSET_PATH_MP=/mnt/cpuset

list_cpuset_mp() {
	cat /proc/mounts | while read ln ; do
		echo "$ln" | cut -d " " -f 4 | grep cpuset -q &&
			echo "$ln"
	done

	return 0
}
# }}}
