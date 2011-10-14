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

#
# spec file for package qa_coreutils (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_coreutils
#BuildRequires:  ctcs2 
License:		SUSE Proprietary
Group:          SUSE internal
Summary:        Coreutils tests for ctcs framework
AutoReqProv:    off
Provides:	qa_coreutils
Obsoletes:	qa_coreutils
Requires:       coreutils ctcs2 gawk diffutils mktemp
Version:        0.1
Release:        191
Source0:        %name-%version.tar.bz2
Source1:        qa_coreutils.tcf
Source2:        test_coreutils-run
Source3:	qa_test_coreutils.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Test cases for coreutils package. Tests the following components:

basename, bool, cat, com, csplit, cut, dirname, expand, expr, md5sum,
sort, touch, tr, tty, uniq, wc

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
ln -s ../%name/tcf/qa_coreutils.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_coreutils.8.gz
%dir /usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools
#/usr/lib/ctcs2/tcf/qa_coreutils.tcf
#%dir /usr/lib/ctcs2/tools
#/usr/lib/ctcs2/tools/test_coreutils-run

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_coreutils -> qa_test_coreutils
* Wed Apr 16 2008 mmrazik@suse.cz
- leap_year.sh test added (bnc#355921)
- changed the exit code of du/basic test (now it silently passed if the
  test is skipped)
* Wed Jan 16 2008 mmrazik@suse.cz
- fixed 000prepare.sh to be less error prone (not using losetup
  /dev/loop0 directly but using the -o loop mount option)
* Mon Jan 14 2008 mmrazik@suse.cz
- timeout for single tests raised to 1200 seconds
- fixed orig_misc_nice test to be explicitely executed with nice
  level 0
* Tue Aug 07 2007 jbrunclik@suse.cz
- added more original tests to the tcf file
* Tue Aug 07 2007 jbrunclik@suse.cz
- fixed some of the original tests
* Tue Aug 01 2006 jdluhos@suse.cz
- added a virtual partition (via a loop device) for tests that need
  a directory on a different partition
* Mon Jul 31 2006 jdluhos@suse.cz
- replaced the many wrapper scripts by a single one; fixed
  root/non-root running for tests that need it; added the remaining
  original tests
* Fri Jul 28 2006 jdluhos@suse.cz
- added symlinks to selected coreutils binaries, as needed
  by tests; about 4 more tests now work correctly
* Thu Jul 27 2006 jdluhos@suse.cz
- path fixes, most of the already added tests are working now
* Mon Jul 24 2006 jdluhos@suse.cz
- first phase of adding the original upstream test suite (from the
  coreutils package)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 19 2006 kmachalkova@suse.cz
- fixed relative/absolute path issue in run-script
* Wed Jan 18 2006 mmrazik@suse.cz
- fixed tcf and run-script location (update Packaging Guidelines)
* Tue Dec 13 2005 kmachalkova@suse.cz
- source tarball renamed
* Thu Dec 08 2005 kmachalkova@suse.cz
- package created, version 0.1

