#!/bin/sh

[ -z "$1" ] && {
	echo point me to the git repo
	exit 1
}
force=${2:-false}

dir="$1"

set -e

pwd=`pwd`
cd "$dir"

make dist

. VERSION
PKG_VERSION=${PKG_MAJOR}.${PKG_MINOR}.${PKG_REVISION}
gitsha=$(git log --format='%h' -n 1)

if ! $force; then
if head $pwd/xfsprogs.changes | grep -q $gitsha; then
	echo "already there"
	exit 1
fi
fi

out=xfsprogs-${PKG_VERSION}_g${gitsha}.tar.bz2
zcat xfsprogs-${PKG_VERSION}.tar.gz | bzip2 --best > $pwd/$out

cd $pwd

set +e
oosc rm xfsprogs-*.bz2
oosc add $out

sed -i -e 's/^\(.*define.*git_version\s\+\).*/\1'$gitsha/ xfsprogs.spec

ed xfsprogs.changes <<EOF
0a
-------------------------------------------------------------------
`date` - $LOGNAME@suse.cz

- update to git $gitsha

.
w
EOF
