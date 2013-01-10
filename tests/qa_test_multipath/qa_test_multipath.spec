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
# spec file for package qa_sw_multipath (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_multipath
BuildRequires:  ctcs2
License:        SUSE Proprietary
Group:          SuSE internal
Summary:        Simple multipath tests for ctcs framework
Provides:	qa_multipath
Obsoletes:	qa_multipath
Requires:       multipath-tools open-iscsi ctcs2 grep dt
Version:        1.3
Release:        1
Source0:        %name-%version.tar.bz2
Source2:        test_sw_multipath-run
Source3:	README.target
Source4:	README.tests
Source5:	example.test
Source6:	test_hw_multipath-run
Source7:	qa_test_multipath.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:	noarch
Obsoletes:	qa_sw_multipath

%description
Test cases for multipath software and hardware tests

* ACTIVE/ACTIVE

* ACTIVE/PASSIVE

* path recovery

* flow control

* path_checker tests (dio, tur)

* HW tests for EMC,NETAPP,HP,IBM

Authors:
--------
    Dinar Valeev <dvaleev@novell.com>

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:7} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 %{S:3} .
install -m 644 %{S:4} .
install -m 644 %{S:5} .

ln -s ../%name/tcf/qa_sw_multipath.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_hw_multipath.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

install -m 755 %{S:2} %{S:6} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../tools/test_sw_multipath-run $RPM_BUILD_ROOT/usr/share/qa/tools/test_multipath-run
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc README.target README.tests example.test COPYING
/usr/share/man/man8/qa_test_multipath.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_multipath-run
%{_datadir}/qa/tools/test_sw_multipath-run
%{_datadir}/qa/tools/test_hw_multipath-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_sw_multipath.tcf
%{_datadir}/qa/tcf/qa_hw_multipath.tcf

%changelog
