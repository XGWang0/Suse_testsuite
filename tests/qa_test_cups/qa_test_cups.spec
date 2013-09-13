#
# spec file for package qa_sw_multipath (Version 0.1)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:		qa_test_cups
BuildRequires:	ctcs2
License:	GPL v2; LGPL v2
Group:		SuSE internal
Summary:	CUPS automated testsuite
Provides:	qa_cups
Obsoletes:	qa_cups
Requires:	ctcs2 cups cups-devel
Version:	1.0
Release:	1
Source0:	%name-%version-sle11.tar.bz2
Source1:	test_cups-run
Source2:	qa_test_cups.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:	noarch

%description
CUPS automated testsuite
Includes:
IPP compiance tests
Command tests

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/%{name}

ln -s ../%name/tcf/qa_cups.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_cups.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_cups-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_cups.tcf

%changelog
* Thu Dec 09 2010 dvaleev@novell.com
- Initial version
