#! /bin/sh

set -eu

cleanup=true

usage() {
	echo "Usage: $0 [-x] [-n] [-v] [-V] [-h] [<case>]"
	echo ""
	echo "  -x for shell tracing"
	echo "  -n for no cleanup"
	echo "  -v for increased verbosity"
	echo "  -h help"
	echo "  -V version"
}

if [ "${0:0:1}" = "/" ]; then
	SRCDIR=$(dirname $0)
else
	SRCDIR=$PWD/$(dirname $0)
fi

export SRCDIR
. $SRCDIR/svnlib.sh

ARGV="$@"

while getopts xVnvh name ; do
	case $name in
		x) set -x;;
		n) cleanup=false;;
		v) export LOGF="/dev/stdout";;
		h) usage; exit 0;;
		V) echo $SVN_TEST_VERSION; exit 0;;
		*) usage; exit $RES_FAIL_INT;;
	esac
done

shift $((OPTIND - 1))

if [ -n "${1:-}" ]; then
	$cleanup && trap svn_cleanup EXIT

	svn_setup
	[ ! $? -eq 0 ] &&  exit $RES_FAIL_SETUP
	svn_test_all $(hostname -f) /usr/share/doc/packages/vim $1
else
	cases="ssh dav dav_auth"
	rc=0
	for i in $cases; do
		$SRCDIR/svn.sh $ARGV $i
		rc=$(($rc | $?))
	done
	exit $rc
fi
