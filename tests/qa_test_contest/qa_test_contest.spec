#
# spec file for package contest (Version 0.61)
#

Name:         qa_test_contest
Url:          http://users.on.net/~ckolivas/qa_test_contest/
License:      GPL2
# Group:        SuSE internal
Group:        System/Benchmark
Summary:      contest benchmark
Provides:	contest contest-ctcs2-glue
Obsoletes:	contest contest-ctcs2-glue
Requires:     coreutils ctcs2
Version:      0.61
Release:      1
Source0:      contest-%version.tar.bz2
Source1:      test_contest-run
Source2:      ctcstools.tar.bz2
Source3:      README
Source4:        qa_test_contest.8
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
This program is designed to test system responsiveness by running kernel
compilation under a number of different load conditions. It is designed to
compare different kernels, not different machines. It uses real workloads
you'd expect to find for short periods in every day machines but sustains
them for the duration of a kernel compile to increase the signal to noise
ratio.

Authors:
Con Kolivas <kernel@kolivas.org>

#%package ctcs2-glue
#License:        Other uncritical OpenSource License
#Summary:        The let-contest-be-run-via-ctcs glue
#Group:          Development/Tools/Other
#AutoReqProv:    on
#Requires:       ctcs2 >= 0.1.6
#Requires:       contest = %{version}
#
#%description ctcs2-glue
#This package contains the glue for integrating contest into the ctcs
#testing framework.
#
#Authors:
#Michal Srb <michalsrb@gmail.com>

%prep
%setup -q -n contest-%{version}
%setup -q -a 2 -n contest-%{version}

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
ln -s ../%name/tcf/contest.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
mv README $RPM_BUILD_ROOT/usr/share/qa/%name
mv contest $RPM_BUILD_ROOT/usr/bin/contest
cp -a ctcstools/* $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_contest.8.gz
/usr/bin/contest

#%files ctcs2-glue
#%defattr(-, root, root)
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
* Wed Aug 13 2008 - vpelcak@suse.cz
- package created, version 0.61
