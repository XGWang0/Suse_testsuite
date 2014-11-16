#
#****************************************************************************
# spec file for package systemd
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# norootforbuild
#
#***************************************************************************
#

Name:           qa_test_systemd
License:        Freeware
Group:          SuSE internal
Summary:        systemd test
Requires:       ctcs2
BuildRequires:  ctcs2
Version:        0.1
Release:	1
Source0:	compatibility.sh
Source1:        qa_systemd.tcf
Source2:        test_systemd-run
Source3:	qa_test_systemd.8
Source4:	check-unit.sh
Source5:	check-service.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
During Beta7 and Beta8 regression testing, we noticed that systemd upgrade easier to cause system service regression issue(specially relate to sysvinit), such as kdump in bnc882395 and bnc869608, postfix in bnc879960, nfs in bnc860246. So do a basic service activity testing is necessarily. 
We designed 2 test points for systemd service as first step, the automation is implemented.

%prep
#%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 %{S:0} $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_systemd.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/%{name}.8.gz
/usr/share/qa
/usr/share/qa/%name/*

%changelog 
* Fri Jul 25 2014 - bwliu@suse.com
- package created, version 0.1

