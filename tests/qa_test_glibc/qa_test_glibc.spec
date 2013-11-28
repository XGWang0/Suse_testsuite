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

Name:		qa_test_glibc
License:	GPL v2 or later
Group:		SuSE internal
Summary:	glibc testsuite
Requires:	glibc, gmp, ctcs2
BuildRequires:  gmp-devel
Version:	1.0
Release:	1
%if 0%{?suse_version} == 1010
Source0:	glibc_testsuite-2.4.tar.gz
%endif
%if 0%{?suse_version} == 1110
Source0:	glibc_testsuite-2.11.tar.gz
%endif
Source2:	test_glibc-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
glibc testsuite
ripped out from the glibc sources

%prep
%setup -q -n glibc_testsuite

%build
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/%{name}

#ln -s ../%name/tcf/%name.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a bin $RPM_BUILD_ROOT/usr/share/qa/%name/
cp -a testfiles $RPM_BUILD_ROOT/usr/share/qa/%name/
cp -a tcf $RPM_BUILD_ROOT/usr/share/qa/%name/
ln -s ../%{name}/tcf/%{name}.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_glibc-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_test_glibc.tcf

%changelog
