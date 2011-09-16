#
# spec file for package interbench (Version 0.1)
#

Name:         qa_test_kernbench
Url:          http://freshmeat.net/projects/qa_test_kernbench/
License:      GPL2
# Group:        SuSE internal
Group:        System/Benchmark
Summary:      kernbench benchmark
Provides:	kernbench kernbench-ctcs2-glue
Obsoletes:	kernbench kernbench-ctcs2-glue
Requires:     coreutils kernel-source make gcc gawk ctcs2
Version:      0.41
Release:      1
Source0:      kernbench-%{version}.tar.bz2
Source1:      test_kernbench-run
Source2:      ctcstools-%version.tar.bz2
Source3:      README
Source4:	qa_test_kernbench.8
Patch0:       maxload.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
This is a cpu throughput benchmark originally devised and used by Martin J.
Bligh. It is designed to compare kernels on the same machine, or to compare
hardware. To compare hardware you need to be running the same architecture
machines (eg i386), the same userspace binaries and run kernbench on the same
kernel source tree.

It runs a kernel at various numbers of concurrent jobs: 1/2 number of cpus, 
optimal (default is 4xnumber of cpus) and maximal job count. Optionally it can
also run single threaded. It then prints out a number of useful statistics
for the average of each group of runs and logs them to kernbench.log

You need more than 2Gb of ram for this to be a true throughput benchmark or
else you will get swapstorms.

Ideally it should be run in single user mode on a non-journalled filesystem.
To compare results it should always be run in the same kernel tree.

Authors:
Con Kolivas <kernel@kolivas.org>

#%package ctcs2-glue
#License:        Other uncritical OpenSource License
#Summary:        The let-kernbench-be-run-via-ctcs glue
#Group:          Development/Tools/Other
#AutoReqProv:    on
#Requires:       ctcs2 >= 0.1.6, gawk
#Requires:       kernbench = %{version}
#
#%description ctcs2-glue
#This package contains the glue for integrating kernbench into the ctcs
#testing framework.
#
#Authors:
#Michal Srb <michalsrb@gmail.com>

%prep
%setup -q -n kernbench-%{version}
%setup -q -a 2 -n kernbench-%{version}
%patch0 -p1

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../%name/tcf/kernbench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
mv README $RPM_BUILD_ROOT/usr/share/qa/%name
mv kernbench $RPM_BUILD_ROOT/usr/bin/kernbench
cp -a ctcstools/* $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_kernbench.8.gz
/usr/bin/kernbench
#
#%files ctcs2-glue
#%defattr(-, root, root)
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
* Wed Aug 13 2008 - vpelcak@suse.cz
- package created, version 0.41
