#!/bin/sh
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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

# make sure chgrp is reasonable

if test "$VERBOSE" = yes; then
  set -x
  chgrp --version
fi

. helpers/envvar-check
. helpers/lang-default
. helpers/group-names

pwd=`pwd`
tmp=basic.$$
trap 'status=$?; cd $pwd; rm -rf $tmp && exit $status' 0
trap '(exit $?); exit' 1 2 13 15

framework_failure=0
mkdir $tmp || framework_failure=1
cd $tmp || framework_failure=1

if test $framework_failure = 1; then
  echo 'failure in testing framework' 1>&2
  (exit 1); exit 1
fi

fail=0

set _ $groups; shift
g1=$1
g2=$2
mkdir d
touch f f2 d/f3
chgrp $g1 f || fail=1
chgrp $g2 f || fail=1
chgrp $g2 f2 || fail=1
chgrp -R $g1 d || fail=1

# Don't let verbose output interfere.
test "$VERBOSE" = yes && set +x

(
  chgrp -c $g1 f
  chgrp -c $g2 f
  chgrp -c $g2 f
  chgrp --verbose '' f
  chgrp --verbose $g1 f
  chgrp --verbose $g1 f
  chgrp --verbose --reference=f2 f
  chgrp -R --verbose $g2 d
  chgrp -R --verbose $g1 d
  chgrp -R -c $g2 d
  chgrp -R -c $g1 d
  chgrp -c $g2 d

  rm -f f
  touch f
  ln -s f symlink
  chgrp $g1 f
  chgrp -h $g2 symlink

  # This should not change the group of f.
  chgrp -h -c $g2 symlink
  chown --from=:$g1 -c :$g2 f

  # This *should* change the group of f.
  # Though note that the diagnostic is misleading in that
  # it says the `group of `symlink'' has been changed.
  chgrp -c $g1 symlink
  chown --from=:$g1 -c :$g2 f

  # If -R is specified without -H or L, -h is assumed.
  chgrp -h $g1 f symlink
  chgrp -R $g2 symlink
  chown --from=:$g1 -c :$g2 f

  # chown() must not be optimized away even when
  # the file's owner and group already have the desired value.
  touch f g
  chgrp $g1 f g
  chgrp $g2 g
  sleep 1
  chgrp $g1 f

  # The following no-change chgrp command is supposed to update f's ctime,
  # but on OpenBSD, it appears to be a no-op for some file system types
  # (at least NFS) so g's ctime is more recent.  This is not a big deal;
  # this test works fine when the files are on a local file system (/tmp).
  chgrp '' f
  ls -c -t f g

) 2>&1 | sed "
  s/' to .*[^0-9:].*/' to SOMENAME/
  s/\([ :]\)$g1$/\1G1/
  s/\([ :]\)$g2$/\1G2/
" > actual

cat <<\EOF > expected
changed group of `f' to G1
changed group of `f' to G2
ownership of `f' retained
changed group of `f' to G1
group of `f' retained as G1
changed group of `f' to SOMENAME
changed group of `d/f3' to G2
changed group of `d' to G2
changed group of `d/f3' to G1
changed group of `d' to G1
changed group of `d/f3' to G2
changed group of `d' to G2
changed group of `d/f3' to G1
changed group of `d' to G1
changed group of `d' to G2
changed ownership of `f' to :G2
changed group of `symlink' to G1
changed ownership of `f' to :G2
changed ownership of `f' to :G2
f
g
EOF

cmp expected actual \
  || { diff expected actual 1>&2; fail=1; }

(exit $fail); exit $fail

