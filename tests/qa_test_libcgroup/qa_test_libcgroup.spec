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

Name:		qa_test_libcgroup
BuildRequires:	ctcs2 
License:	GPL v2 or later
Group:		SuSE internal
Summary:	libcgroup automated testsuite
Requires:	libcgroup1 libcgroup-devel
Version:	1.0
Release:	1
Source0:	%name.tar.bz2
Source2:	libcgroup-run
Patch0:		64bit.patch
Obsoletes:	qa_libcgroup
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
libcgroup automated testsuite
Includes:
libcgroup upstream tests

%prep
%setup -q -n %{name}
%ifarch ppc64 s390x x86_64
%patch0
%endif

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/%{name}

ln -s ../%name/tcf/qa_libcgroup.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/libcgroup-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_test_libcgroup.tcf

%changelog
