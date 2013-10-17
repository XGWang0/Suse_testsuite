#!/bin/sh

force=false

[ -z "$1" ] && {
	echo point me to the git repo
	exit 1
}

dir="$1"

set -e

pwd=`pwd`
cd "$dir"

. VERSION
PKG_VERSION=${PKG_MAJOR}.${PKG_MINOR}.${PKG_REVISION}
gitsha=$(git log --format='%h' -n 1)

out=xfstests-${PKG_VERSION}_g${gitsha}.tar.bz2

[ -f "$pwd/$out" ] || force=true

if ! $force && head $pwd/xfstests.changes | grep -q $gitsha; then
	echo "already there"
	exit 1
fi

( cd $pwd ; oosc rm -f xfstests-*.bz2 )

git archive --format=tar --prefix=xfstests-$PKG_VERSION/ HEAD | bzip2 --best > $pwd/$out

cd $pwd
oosc add $out

sed -i -e 's/^\(.*define.*git_version\s\+\).*/\1'$gitsha/ xfstests.spec

ed xfstests.changes <<EOF
0a
-------------------------------------------------------------------
`date` - $LOGNAME@suse.cz

- update to git $gitsha

.
w
EOF
