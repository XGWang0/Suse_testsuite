# ****************************************************************************
# Copyright © 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# spec file for package qa_sample (Version 0.1)
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild
%define hiworkload hiworkload-0.1

Name:           qa_test_kgraft
BuildRequires:  ctcs2
License:        GPL-2.0+
Group:          SuSE internal
AutoReqProv:    on
Version:        1.0
Release:        1
Summary:        kGraft functional tests
Source0:        %name-%version.tar.bz2
Source1:        qa_kgraft.tcf
Source2:        test_kgraft-run
Source3:        qa_test_kgraft.8
Source4:        hiworkload-0.1.tar.gz
ExclusiveArch:	x86_64 s390x ppc64le
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_kgraft
Obsoletes:	qa_kgraft
Requires:       ctcs2, bash, gcc, make, kernel-syms

%description
This is an integration bit for kGraft test suite.

Authors:
--------
    Libor Pechacek <lpechacek@suse.cz>

%prep
%setup -T -b 4 -q -n %{hiworkload}
%setup -T -b 0 -q -n %{name}

%build
pushd ../%{hiworkload}
./configure --prefix=/usr/share/qa/%name
popd

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
pushd ../%{hiworkload}
%make_install
popd
ln -s ../%name/tcf/qa_kgraft.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;
find  $RPM_BUILD_ROOT/usr/share/qa/%name -type f ! -name "COPYING" | xargs chmod +x

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_kgraft.tcf
/usr/share/qa/tools/test_kgraft-run
/usr/share/man/man8/*
%doc COPYING

%changelog
