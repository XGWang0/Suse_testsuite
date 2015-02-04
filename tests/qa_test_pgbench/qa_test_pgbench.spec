#!BuildIgnore: post-build-checks

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
Summary:        Using pgbench to test the IO performance
Version:        1.0.0
Release:        5.1
License:        GPL v2
Group:          System/Benchmark
#Url:
Requires:       gcc readline-devel zlib-devel            
#Requires:       postgresql93 postgresql93-contrib postgresql-init postgresql93-server
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source4:       qa_test_pgbench-large.tcf
Source5:       qa_test_pgbench-medium.tcf
Source6:       qa_test_pgbench-small.tcf
Source7:       test_pgbench_medium-run
Source8:       test_pgbench_large-run
Source9:       test_pgbench_small-run
Source10:       simple-pgbench.sh
#Source11:       simple-pgbench.tcf
#Source12:       test_pgbench_small-run
#Source13:       simple-pgbench-run
Source14:       simple-pgbench-new.sh
Source15:       install-pgbench.sh
Source16:       postgresql-9.3.4.tar.bz2
#Patch0:
#BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#BuildArchitectures: noarch

%description
a test script using pgbench to test the IO performance.



Authors:
--------
    Lance Wang (lzwang@suse.com)
    Yong Sun (yosun@suse.com)

%prep

%install
echo $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:7} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:8} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:9} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:10} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 600 %{S:11} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
#install -m 755 %{S:12} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
#install -m 755 %{S:13} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:14} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 %{S:15} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf/
#ln -s ../%{name}/simple-pgbench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%{name}/qa_test_pgbench-small.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%{name}/qa_test_pgbench-medium.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../%{name}/qa_test_pgbench-large.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_small-run $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_medium-run $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_large-run $RPM_BUILD_ROOT/usr/share/qa/tools/



cp %{SOURCE16} $RPM_BUILD_ROOT/usr/share/qa/%{name}/

%post 
/usr/share/qa/%{name}/install-pgbench.sh

%preun

%postun

%files
%defattr(-, root, root)
/usr/share/qa
/usr/share/qa/%{name}
/usr/share/qa/tcf
/usr/share/qa/tools

