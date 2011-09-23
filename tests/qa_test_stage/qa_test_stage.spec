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

Name:           qa_test_stage
License:        GPL v2 or later
Group:          SuSE internal
AutoReqProv:    on
Version:        0.1
Release:        1
Summary:        qa internal package for stage test 
Source0:        %name-%version.tar.bz2
Source1:        qa_test_stage.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_stage
Obsoletes:	qa_stage
Requires:       expect qa_tools qa_lib_config perl-libwww-perl

%description
This is a stage test package that can be used to test new rpm

Authors:
--------
    Jerry Tang <jtang@novell.com>

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755  * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name .svn -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)  
/usr/share/man/man8/qa_test_stage.8.gz
/usr/share/qa/%name

%changelog
* Thu May 30 2011 - jtang@novell.com
- stage test init.
