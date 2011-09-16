#
# spec file for package ftpload (Version 0.8.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#



Name:           qa_test_ftpload
BuildRequires:  ctcs2
Summary:        ftp download test
Version:        0.1
Release:        1
Provides:	qa_ftpload
Obsoletes:	qa_ftpload
Requires:       wget pure-ftpd ctcs2
Group:          Development/Tools/Other
License:        GPL v2 or later
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        ftpload
Source1:        test_ftpload-run
Source2:        ftpload.tcf
Source3:        ftpload.sh
Source4:	cert_tests.lib
Source5:	qa_test_ftpload.8
BuildArchitectures: noarch

%description
Download ftp://10.11.136.9/400MB for times.

Authors:
--------
    Arthur Guo <aguo@novell.com>

%prep

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/bin/
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8/
cp %{S:0} $RPM_BUILD_ROOT/usr/bin/
cp %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{S:2} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
cp %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name/
cp %{S:4} $RPM_BUILD_ROOT/usr/lib/
cp %{S:5} $RPM_BUILD_ROOT/usr/share/man/man8/
gzip $RPM_BUILD_ROOT/usr/share/man/man8/qa_test_ftpload.8
ln -s ../%name/tcf/ftpload.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
/usr/bin/*
/usr/lib/*
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/ftpload.tcf
/usr/share/qa/tools/test_ftpload-run
/usr/share/man/man8/*

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_ftpload -> qa_test_ftpload
* Fri Feb 25 2011 - aguo@novell.com
- add man page of qa_test_ftpload
* Wed Feb 15 2011 - aguo@novell.com
- create ftpload package.
