#!/bin/sh
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#


# Parameters:
# $1
#    The test directory; typically (but not always) it is the same
#    as the name of the core utility being tested.
# $2
#    The name of the test program.
# $3 (optional)
#    The name of the core utility if it differs from the directory name.
# $4 (optional)
#    Additional flag; currently can be only "no-root" which means the test
#    should not be run as root, but as the common user.

if [ $# -ne 2 -o $# -ne 3 -o $# -ne 4 ]; then
	echo "Usage: $0 \$TESTDIR \$TESTPROG [\$UTILTY] [\$FLAG]"
	echo "see \"Parameters\" in $0 for details"
	exit 1
fi

# Read the parameters.
TESTDIR=$1
TESTPROG=$2
UTILITY=$3
FLAG=$4

# Take the utility name from the directory name if not specified explicitly.
if [ -z "$UTILITY" ] ; then
    UTILITY=$1
fi

# Some tests fail in output comparison due to language differences
export LANG=

# Enable messages to be printed so we know more about what happens.
VERBOSE=yes
export VERBOSE

# Some tests require Perl; tell them where to find it.
PERL=perl
export PERL

# The directory where the tests search for data files and helpers.
# Before the test is run, we change to its directory,
# so this is only "."
srcdir=.
export srcdir

# Determine the directory where this script resides; there are some important
# symlinks and helpers.
MYDIR=`dirname $0`
if ! echo $MYDIR | grep -e '^/.*' ; then
    MYDIR=`pwd`/$MYDIR
fi

# Change to the test directory.
cd "$MYDIR/orig_test_suite/$TESTDIR"

#BUILD_SRC_DIR="`cd $MYDIR/orig_test_suite/src; pwd -P`"
BUILD_SRC_DIR="`pwd -P`"
export BUILD_SRC_DIR

# Add it to the path so that the tests can see the symlinks.
PATH="$PATH:$MYDIR:$BUILD_SRC_DIR"
export PATH

PACKAGE_VERSION="`rpm -q coreutils | cut -d- -f2`"
export PACKAGE_VERSION

# The PROG environment variable is needed by some tests
# to contain the name of the utility being tested.
PROG="$UTILITY"
export PROG

# Allow expensive tests to be run as well (they are not that expensive).
RUN_EXPENSIVE_TESTS="yes"
export RUN_EXPENSIVE_TESTS

# Provide a separate temporary partition for tests that need one.
CANDIDATE_TMP_DIRS='/tmp/qa_coreutils_mnt /tmp /var/tmp /usr/tmp /var/lib/nobody'
export CANDIDATE_TMP_DIRS

# Provide a separate full partition for tests that need one.
FULL_PARTITION_TMPDIR='/tmp/qa_coreutils_full_mnt'
export FULL_PARTITION_TMPDIR

# For some reason the testsuite does neither find the groups 'nobody' is in nor can it deal with group names
COREUTILS_GROUPS="`LANG= id nobody | grep -o groups.* | grep -o '[0-9][0-9]*'`"
COREUTILS_GROUPS="`echo $COREUTILS_GROUPS`"
export COREUTILS_GROUPS

# Some tests need a controling tty and cannot be run in non-interactive mode. Skip them.
INTERACTIVE_TEST_DIR="stty"
for tdir in $INTERACTIVE_TEST_DIR; do
    if [ "$TESTDIR" == $tdir ] ; then
        echo skip $TESTDIR/$TESTPROG, because we are not interactive
        exit 0
    fi
done

# Tests should be run as root. They switch to user 'nobody' where needed.
# Some test can't even be performed if we are not root
RUN_AS_ROOT="test/test-tests rm/fail-2eperm rm/no-give-up"
export RUN_AS_ROOT

if [ "$EUID" != "0" ] ; then
    for test in $RUN_AS_ROOT; do
        if [ "$TESTDIR/$TESTPROG" = $test ] ; then
            echo skip $test, because we are not root
            exit 0
        fi
    done
    ./$TESTPROG
    exit $?
fi

if [ "$FLAG" == "no-root" ] ; then
    su nobody -c ./$TESTPROG
else
    ./$TESTPROG
fi
exit $?




