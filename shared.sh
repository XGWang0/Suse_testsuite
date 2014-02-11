#!/bin/bash

export LANG=C

FORCED_VERSION="$VERSION"

[ -r ./config ] && source ./config

# if version was defined externally, use that one
[ -z "$FORCED_VERSION" ] || VERSION="$FORCED_VERSION"

# Where to put built rpms
[ -z "$DESTDIR" ] && DESTDIR="`pwd`/BUILT"
mkdir -p "$DESTDIR" || exit 1

project=QA:Head:Devel
iosc="osc -A https://api.suse.de"

# this function should be implemented in the script, 
# if it needs custom cleanup before failure
# since this file is sourced, all local functions in 
# this file will use the newest definition
# this should be probably fixed to cleaner war!!!
function cleanup
{
		# Nothing - intentionally!!!
		echo "nothing" > /dev/null
}

function assert_command
{
	# checks that the command ($1) is installed. If not, 'exit 1' and report
	if ! which "$1" > /dev/null 2>&1 ; then
		echo "Error: Required command $1 not installed - please install it and try again." >&2
		exit 1
	fi
}
	
function package_prepare
{
	# this must be run in the package directory

	if [ -x ./PACK_PREPARE ] ; then
		# there's custom prepare script!
		./PACK_PREPARE
		[ $? != 0 ] && cleanup && exit 1
	else
		# no custom prepare - try the "pack existing one directory" approach
		tarballname=`ls -l | grep ^d | awk {'print $NF'}`
		version=`grep ^Version: *.spec | awk {'print $2'}`
		version=${version//@@VERSION@@/$VERSION} # from PROJECT/config
		[ -z $tarballname ] || tar --exclude-vcs -jcf $tarballname-$version.tar.bz2 $tarballname
	fi
}

# copies package sources from local directory to the $1
function copy_package_sources
{
	target="$1"
	
	cp * "$target" > /dev/null 2>&1
	rm -f "$target"/PACK_{PREPARE,CLEANUP}
	sed -i "s/@@VERSION@@/$VERSION/g" "$target"/*.spec
}

function package_cleanup
{
	# this must be run in the package directory

	if [ -x ./PACK_CLEANUP ] ; then
		# there's custom cleanup script!

		./PACK_CLEANUP
		[ $? != 0 ] && cleanup && exit 1
	else
		# no custom prepare - try the "pack existing one directory" approach
		tarballname=`ls -l | grep ^d | awk {'print $NF'}`
		version=`grep ^Version: *.spec | awk {'print $2'}`
		version=${version//@@VERSION@@/$VERSION} # from PROJECT/config
		[ -z $tarballname ] || rm -f $tarballname-$version.tar.bz2
	fi
}

# calls osc init, but with support for devel pakckage - if pakckage has 
# its devel associated, initialize it with devel repository
# must be called in the directory, which is to be initialized
# usage osc_init project package
function osc_init 
{
	proj=$1;
	pack=$2;
	
	# check for devel project
	line="`$iosc meta pkg "$proj" "$pack" 2> /dev/null`" || return 1
	line="`echo "$line" | grep '<devel '`" 
	if [ "$line" != "" ] ; then
		if [ "$FORCE_SUBMIT_QA_HEAD" == "yes" ] ; then
			devproj="`echo $line | sed 's/^.*project="\([^"]*\)".*\$/\1/'`"
			echo "INFO: Package $pack (which is normally submitted to $devproj) will be submitted to $proj."
		else
			proj="`echo $line | sed 's/^.*project="\([^"]*\)".*\$/\1/'`"
			pack="`echo $line | sed 's/^.*package="\([^"]*\)".*\$/\1/'`"
		fi
	fi
	
	$iosc init "$proj" "$pack" 2> /dev/null
	# bnc588624 - use checkout instead of init until fixed
		$iosc up
		rm -f *
	# bnc588624 - end 
}
