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

#
# spec file for package qa_test_lsb (Version 1.0)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_lsb
#BuildRequires:  bzip2 gcc
Version:        2.0
Release:        3
License:        SUSE Proprietary
Group:          SuSE internal
Autoreqprov:    on
Source0:        %{name}-%{version}.tar.bz2
Source1:        test_lsb-run
Source2:	qa_test_lsb.8
Url:            http://www.linuxbase.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        The LSB test suite adapted for automatic runs.
BuildArch:      noarch
Obsoletes:	qa_lsb
Requires:       perl wget lsb xorg-x11-Xvfb xorg-x11-fonts-100dpi
Requires:	foomatic-filters
Requires:	libqt4 libqt4-sql libqt4-sql-sqlite libqt4-x11 libqt4-qt3support

%description
This is the testsuite for the Linux Standard Base (LSB).

This is only the automatic testing driver. The respective tests are in
appropriate lsb-* packages, which are produced by the LSB committee.



Authors:
--------
    Jiri Dluhos <jdluhos@suse.com>

%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
#install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
#ln -s ../%name/tcf/qa_lsb.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
install -d -m 0755 $RPM_BUILD_ROOT/etc/lsb-release.d

%post
if [ ! -e "/etc/lsb-release.d/core-4.0-noarch" ] ; then
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/core-4.0-noarch
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/desktop-4.0-noarch
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/graphics-4.0-noarch
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/core-4.0-`uname -m`
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/desktop-4.0-`uname -m`
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/graphics-4.0-`uname -m`
fi
if [ ! -e "/etc/lsb-release.d/core-4.1-noarch" ] ; then
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/core-4.1-noarch
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/desktop-4.1-noarch
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/graphics-4.1-noarch
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/core-4.1-`uname -m`
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/desktop-4.1-`uname -m`
	touch $RPM_BUILD_ROOT/etc/lsb-release.d/graphics-4.1-`uname -m`
fi


%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/%{name}.8.gz
/usr/share/qa
/usr/share/qa/%name/
/usr/share/qa/tcf/
/usr/share/qa/tools/
%attr(0755, root, root) /usr/share/qa/tools/test_lsb-run
#/usr/share/qa/tools/lsb-run
/etc/lsb-release.d/
%doc COPYING


%changelog -n qa_lsb
* Wed Jan 18 2012 - aguo@suse.com
- remove qa_dummy dependency
* Mon Jul 19 2010 - jdluhos@suse.cz
- brand new version based on new upstream version
* Fri Feb 02 2007 - ro@suse.de
- remove self-provides from package
* Fri Sep 22 2006 - ro@suse.de
- use ExclusiveArch instead of BuildArch
* Thu Aug 31 2006 - jdluhos@suse.cz
- removed third-party packages from dependencies as they trigger
  errors in autobuild; they can be downloaded automatically
* Wed Apr 26 2006 - jdluhos@suse.cz
- initial release

