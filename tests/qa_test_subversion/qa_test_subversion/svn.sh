#! /bin/sh

set -eu

cleanup=true
log=

usage() {
	echo "Usage: $0 [-x] [-n] [-v] [-h]"
	echo ""
	echo "  -x for shell tracing"
	echo "  -n for no cleanup"
	echo "  -v for increased verbosity"
	echo "  -h guess what"
	echo ""
	echo "Interpretation"
	echo " exit code != 0 => FAILURE"
	echo " each subtest will print if it PASSED, but not if it FAILED."
}

. svnlib.sh

while [ $# -gt 0 ]; do
	case ${1:-} in
		"-x")	set -x; shift ;;
		"-n") cleanup=false; shift;;
		"-v") export LOGF="/dev/stdout"; shift;;
		"-h") usage; exit 0;;
		*) usage; exit 1;;
	esac
done

$cleanup && trap svn_cleanup EXIT

svn_setup
svn_test_all $(hostname -f) /usr/share/doc/packages/vim ${log}
