# ****************************************************************************
#
# spec file for package qa_test_iperf (Version 2.0.5)
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# norootforbuild
#
# ****************************************************************************
#

Name:           qa_test_iperf
License:        Restricted Shareware
Group:          network benchmark
Summary:        iperf test
Requires:       ctcs2 gcc gcc-c++
BuildRequires:  ctcs2 gcc gcc-c++
Version:        2.0.5
Release:	1
Source0:        iperf-%version.tar.bz2
Source1:	%{name}.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Iperf was developed as an alternative for measuring maximum TCP and UDP bandwidth performance. 
Iperf allows the tuning of various parameters and UDP characteristics. 
Iperf reports bandwidth, delay jitter, datagram loss.

%prep
%setup -q -n %{name}

%build
./configure
make 

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/usr/bin/
install -m 755 src/iperf $RPM_BUILD_ROOT/usr/bin/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/%{name}.8.gz
/usr/bin/iperf

%changelog 
* Mon Nov 26 2012 - yxu@suse.de
- package created, version 2.0.5

