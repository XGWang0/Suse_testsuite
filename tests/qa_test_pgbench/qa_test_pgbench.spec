#
# spec file for package sysbench (Version 0.4.8)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_pgbench
Summary:        
Version:        
Release:        
License:        
Group:          
Url:            
Requires:       postgresql93 postgresql93-contrib postgresql-init postgresql93-server
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source10:       simple-pgbench.sh
Source11:       simple-pgbench.tcf
Source12:       simple-pgbench-run
#Patch0:
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#BuildArchitectures: noarch

%description
a test script using pgbench to test the IO performance.



Authors:
--------
    Lance Wang (lzwang@.suse.com)

%prep

%install
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 755 %{S:10} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 600 %{S:11} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:12} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%{name}/simple-pgbench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/simple-pgbench-run $RPM_BUILD_ROOT/usr/share/qa/tools/

%post 

%preun

%postun

%files
%defattr(-, root, root)
%dir /usr/share/qa/%{name}
%dir /usr/share/qa/tcf
%dir /usr/share/qa/tools
