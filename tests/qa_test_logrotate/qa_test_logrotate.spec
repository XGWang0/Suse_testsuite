#
# spec file for package qa_logrotate_test (Version 0.1)
#
# Copyright (c) 2010 Novell, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name:           qa_test_logrotate
BuildRequires:  ctcs2
License:        GPL v2 or later
Group:          SuSE internal
AutoReqProv:    on
Version:        0.11
Release:        1
Summary:        QA package for testing logrotate
Url:            http://qa.suse.de/
Source0:        %name-%version.tar.bz2
Source1:        qa_logrotate_test.tcf
Source2:        test_logrotate-run
Source3:        qa_test_logrotate.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_logrotate_test
Obsoletes:	qa_logrotate_test
Requires:       ctcs2

%description
Tests the following features of logrotate: addextension, compression, copy_log, dateformat, force_rotate, ifempty, log_order, log_size, no_force_rotate, notifempty, and remove_old_logs.

Authors:
--------
    David Mulder <dmulder@suse.com>

%prep
%setup -q -n %{name}

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
ln -s ../%name/tcf/qa_logrotate_test.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_logrotate_test.tcf
/usr/share/qa/tools/test_logrotate-run
/usr/share/man/man8/*

%changelog
* Tue Aug 02 2011 - dmulder@suse.com
- Created this package for testing logrotate.
