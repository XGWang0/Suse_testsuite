#!BuildIgnore: post-build-checks
#
# spec file for package qa_hazard (Version 0.1)
#
# Copyright (c) 2010 Novell, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.novell.com/
#

# norootforbuild

Name: 		qa_test_hazard
License:        GPL v2 or later
Group:          SuSE internal
Version: 0.1
Release:        5
Summary:        (rd-)qa internal package for training
Provides:	hazard
Obsoletes:	hazard
Requires:	expect ksh qa_keys
Url:            http://qa.suse.de/
Source0:        hazard-%version.tar.bz2
Source1:	qa_test_hazard.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    off

%description
HP hazard only for Novell.
HP Hazard provides automated storage device reliability testing which focuses on
high availability (HA).

Authors:
--------
    Jerry Tang <jtang@novell.com>

%prep
%setup -q -n hazard

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/hazard
cp -a * $RPM_BUILD_ROOT/usr/lib/hazard

if [ -n "`arch|grep alpha`" ];then
	tar -zxf alpha-osf51-server.tar.gz -C $RPM_BUILD_ROOT/usr/lib/hazard
elif [ -n "`arch|grep ia64`" ];then
	tar -zxf ia64-linux24-server.tar.gz -C $RPM_BUILD_ROOT/usr/lib/hazard
else
	tar -zxf i386-linux24-server.tar.gz -C $RPM_BUILD_ROOT/usr/lib/hazard
fi

find $RPM_BUILD_ROOT/usr/lib/hazard -depth -type d -name CVS -exec rm -rf {} \;
sed -i '1s@local/@@'  $RPM_BUILD_ROOT/usr/lib/hazard/coverage.pl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_hazard.8.gz
/usr/lib/hazard

%changelog
* Mon Aug 15 2011 - llipavsky@suse.cz
- Package rename: hazard -> qa_test_hazard
* Thu Nov 15 2010 - jtang@novell.com
- rename the package,version 0.1
* Thu Nov 11 2010 - jtang@novell.com
- remove ctcs2 support,version 0.1
* Thu Oct 14 2010 - jtang@novell.com
- package created automatically,version 0.1
