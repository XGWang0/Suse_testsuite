#!BuildIgnore: post-build-checks

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
Requires:       gcc readline-devel zlib-devel sudo           
#Requires:       postgresql93 postgresql93-contrib postgresql-init postgresql93-server
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:       	ctcstools-%{version}.tar.bz2
Source1:        postgresql-9.3.4.tar.bz2
Source2:       	qa_test_pgbench.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
a test script using pgbench to test the IO performance.



Authors:
--------
    Lance Wang (lzwang@suse.com)
    Yong Sun (yosun@suse.com)

%prep
%setup -q -n ctcstools

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8


echo "RPM_BUILD_ROOT=$RPM_BUILD_ROOT"
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 755 pgbench-run.sh $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 pgbench.postinst  $RPM_BUILD_ROOT/usr/share/qa/%{name}/
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf/
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools/
install -m 755 test_pgbench_large-ro-run $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 test_pgbench_large-rw-run $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 test_pgbench_medium-ro-run $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 test_pgbench_medium-rw-run $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 test_pgbench_small-ro-run $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 test_pgbench_small-rw-run $RPM_BUILD_ROOT/usr/share/qa/%{name}/
ln -s ../%{name}/test_pgbench_large-ro-run $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_large-rw-run $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_medium-ro-run $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_medium-rw-run $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_small-ro-run $RPM_BUILD_ROOT/usr/share/qa/tools/
ln -s ../%{name}/test_pgbench_small-rw-run $RPM_BUILD_ROOT/usr/share/qa/tools/
cp %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%{name}/

%post 
/usr/share/qa/%{name}/pgbench.postinst

%preun

%postun
if [ "$1x" == "0x" ]; then
    rm -rf /usr/share/qa/qa_test_pgbench
fi

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_pgbench.8.gz
/usr/share/qa
/usr/share/qa/%{name}
/usr/share/qa/tcf
/usr/share/qa/tools
