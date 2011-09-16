#!BuildIgnore: post-build-checks
#
# spec file for package qa_libo (Version 0.1)
#
# Copyright (c) 2011 Novell, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_cts
License:        GPL v2 or later
Group:          SuSE internal
AutoReqProv:    on
Version:        0.1
Release:        1
Summary:        qa internal package for HA cts
Url:            http://www.libreoffice.org/
Source0:        %name-%version.tar.bz2
Source1:        qa_test_cts.8
Source2:        00-qa_test_cts-sharestorage-server
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_cts
Obsoletes:	qa_cts
Requires:       expect ksh qa_keys qa-config

%description
This is a HA test package that can be used to 
test base function of HA.

Authors:
--------
    Jerry Tang <jtang@novell.com>

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d $RPM_BUILD_ROOT/etc/qa
install -m 644 %{S:2} $RPM_BUILD_ROOT/etc/qa
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755  * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name .svn -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)  
/usr/share/man/man8/qa_test_cts.8.gz
/usr/share/qa/%name
/etc/qa/00-qa_test_cts-sharestorage-server

%changelog
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_cts -> qa_test_cts
* Thu May 30 2011 - jtang@novell.com
- HA cts test suite intitiative.
