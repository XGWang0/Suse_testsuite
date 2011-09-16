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

Name:           qa_test_libo
License:        GPL v2 or later
Group:          SuSE internal
AutoReqProv:    on
Version:        0.1
Release:        1
Summary:        qa internal package for libreoffice
Url:            http://www.libreoffice.org/
Source0:        %name-%version.tar.bz2
Source1:	qa_test_libo.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_libo
Obsoletes:	qa_libo
Requires:       qa_libperl

%description
This is a qa_libo test package that can be used to 
test libreoffice through testtool.

Authors:
--------
    Yifan Jiang <yfjiang@novell.com>

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name .svn -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_libo.8.gz
/usr/share/qa/%name

%changelog
* Fri Aug 12 2011 - llipavsky@suse.cz
- Package rename: qa_libo -> qa_test_libo
* Thu May 30 2011 - yfjiang@novell.com
- libreoffice test suite intitiative.
