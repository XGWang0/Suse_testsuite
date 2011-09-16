#
# spec file for package qa_sw_multipath (Version 0.1)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_multipath
BuildRequires:  ctcs2
License:        GPL v2 or later
Group:          SuSE internal
Summary:        Simple multipath tests for ctcs framework
Provides:	qa_multipath
Obsoletes:	qa_multipath
Requires:       multipath-tools open-iscsi ctcs2 grep dt
Version:        1.2
Release:        1
Source0:        %name-%version.tar.bz2
Source2:        test_sw_multipath-run
Source3:	README.target
Source4:	README.tests
Source5:	example.test
Source6:	test_hw_multipath-run
Source7:	qa_test_multipath.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch
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
install -m 644 %{S:3} $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 %{S:4} $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 %{S:5} $RPM_BUILD_ROOT%{_docdir}/%{name}

ln -s ../%name/tcf/qa_sw_multipath.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%name/tcf/qa_hw_multipath.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

install -m 755 %{S:2} %{S:6} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_multipath.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_sw_multipath-run
%{_datadir}/qa/tools/test_hw_multipath-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_sw_multipath.tcf
%{_datadir}/qa/tcf/qa_hw_multipath.tcf
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README.target
%doc %{_docdir}/%{name}/README.tests
%doc %{_docdir}/%{name}/example.test

%changelog
