#
# spec file for package interbench (Version 0.1)
#

Name:         qa_test_interbench
Url:          http://users.on.net/~ckolivas/interbench/
License:      GPL v2 or later
# Group:        SuSE internal
Group:        System/Benchmark
Summary:      Interbench benchmark
Provides:	interbench interbench-ctcs2-glue
Obsoletes:	interbench interbench-ctcs2-glue
Requires:     coreutils ctcs2
Version:      0.30
Release:      1
Source0:      interbench-%version.tar.bz2
Source1:      test_interbench-run
Source2:      ctcstools-%version.tar.bz2
Source3:      README
Source4:        qa_test_interbench.8
Patch0:       strcmp.dif
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
This benchmark application is designed to benchmark interactivity in Linux.
It is designed to measure the effect of changes in Linux kernel design or system
configuration changes such as cpu, I/O scheduler and filesystem changes and
options. With careful benchmarking, different hardware can be compared.

Authors:
Con Kolivas <kernel@kolivas.org>

#%package ctcs2-glue
#License:        Other uncritical OpenSource License
#Summary:        The let-interbench-be-run-via-ctcs glue
#Group:          Development/Tools/Other
#AutoReqProv:    on
#Requires:       ctcs2 >= 0.1.6
#Requires:       interbench = %{version}
#
#%description ctcs2-glue
#This package contains the glue for integrating interbench into the ctcs
#testing framework.
#
#Authors:
#Michal Srb <michalsrb@gmail.com>

%prep
%setup -q -n interbench
%setup -q -a 2 -n interbench
%patch0 -p1

%build
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../%name/tcf/interbench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
mv readme.interactivity $RPM_BUILD_ROOT/usr/share/qa/%name
mv readme $RPM_BUILD_ROOT/usr/share/qa/%name
mv interbench $RPM_BUILD_ROOT/usr/bin/interbench
cp -a ctcstools/* $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_interbench.8.gz
/usr/bin/interbench
#
#%files ctcs2-glue
#%defattr(-, root, root)
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools
%attr(0755,root,root) /usr/share/qa/%name/do_interbench

%changelog
* Mon Aug 15 2011 - llipavsky@suse.cz
- Package rename: interbench -> qa_test_interbench
* Tue Aug 12 2008 - vpelcak@suse.cz
- updated to version 0.30
* Fri Jul 18 2008 - michalsrb@gmail.com
- package created, version 0.1
