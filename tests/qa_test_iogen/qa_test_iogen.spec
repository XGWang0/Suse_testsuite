# ****************************************************************************
#
# spec file for package qa_test_iogen
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# norootforbuild

# ****************************************************************************
#

Name:           qa_test_iogen
License:        BSD
Group:          IO benchmark
Summary:        iogen test
Requires:       ctcs2
BuildRequires:  ctcs2
Version:        3.1
Release:	1
Source0:        %name-%version.tar.bz2
Source1:        qa_iogen.tcf
Source2:        test_iogen-run
Source3:        %name.8
Source4:        do_iogen
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
An I/O generator. It forks child processes that each run a mix of reads and writes.
It is by not a performance measuring tool since it tries to recreate the worst case
scenario I/O. 


%prep
%setup -q -n %{name}

%build
make all

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/bin
install -m 744 iogen $RPM_BUILD_ROOT/usr/bin
ln -s ../%name/tcf/qa_iogen.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/bin/iogen
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/%name/do_iogen
/usr/share/qa/tcf/qa_iogen.tcf
/usr/share/qa/tools/test_iogen-run
/usr/share/man/man8/%name.8.gz

%changelog 
* Wed Nov 07 2012 - yxu@suse.de
- package created, version 3.1

