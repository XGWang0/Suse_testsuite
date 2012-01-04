# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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

#
# spec file for package qa_cpio (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org
#

# norootforbuild

Name:         qa_test_cpio
BuildRequires: ctcs2
License:      SUSE Proprietary
Group:        SuSE internal
Summary:      Simple cpio test for ctcs framework
Provides:	qa_cpio
Obsoletes:	qa_cpio
Requires:     cpio coreutils perl ctcs2
Version:      0.1
Release:      4
Source0:      %name-%version.tar.bz2
Source1:      qa_cpio.tcf
Source2:      test_cpio-run
Source3:	qa_test_cpio.8
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test case for cpio package. Tests all available archive formats

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
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../%name/tcf/qa_cpio.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_cpio.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools
%doc COPYING

%changelog -n qa_test_cpio
* Mon Jan 30 2006 - kmachalkova@suse.cz
- added qa_dummy to BuildRequired
* Thu Jan 26 2006 - kmachalkova@suse.cz
- added ctcs2 support (tcf file, run script)
- removed binaries from testing archive (package fails to build otherwise)
* Fri Jan 20 2006 - kmachalkova@suse.cz
- package created, version 0.1

