#
# spec file for package tiobench (Version 0.3.3)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_tiobench
Url:            http://sourceforge.net/projects/tiobench
License:        GPL v2 or later
Group:          System/Benchmark
AutoReqProv:    on
Summary:        Portable, robust, fully-threaded I/O benchmark program
Version:        0.3.3
Release:        165
Source0:        tiobench-%{version}.tar.bz2
Source1:        ctcstools-%version.tar.bz2
Source2:	qa_test_tiobench.8
Patch1:         XEN-dom0-problem.patch
Patch2:         invalid_results_format.patch
Patch3:		eatmem.patch
Provides:	tiobench tiobench-ctcs2-glue
Obsoletes:	tiobench tiobench-ctcs2-glue
Requires:	ctcs2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A threaded I/O benchmark for Linux (or any *nix system with POSIX
threads support library).



#%package ctcs2-glue
#Summary:        The let-tiobench-be-run-via-ctcs glue
#Group:          System/Benchmark
#AutoReqProv:    on
#Requires:       ctcs2 >= 0.1.5
#Requires:       tiobench = %{version}
#Requires:       qa_dummy
#
#%description ctcs2-glue
#This package contains the glue for integrating tiobench into the ctcs
#testing framework.



%prep
%setup -q -n tiobench-%{version} -a1
%patch1 -p0
%patch2 -p2
%patch3

%build
make CFLAGS="$RPM_OPT_FLAGS -DLARGEFILES" 

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
# make install
install -D -m 755 tiotest $RPM_BUILD_ROOT/usr/bin/tiotest
install -D -m 755 tiobench.pl $RPM_BUILD_ROOT/usr/bin/tiobench.pl
install -D -m 755 tiosum.pl $RPM_BUILD_ROOT/usr/bin/tiosum.pl
install -D -m 755 eatmem $RPM_BUILD_ROOT/usr/bin/eatmem
install -D -m 644 README $RPM_BUILD_ROOT/usr/share/doc/packages/qa_test_tiobench/README
install -D -m 644 BUGS $RPM_BUILD_ROOT/usr/share/doc/packages/qa_test_tiobench/BUGS
install -D -m 644 COPYING $RPM_BUILD_ROOT/usr/share/doc/packages/qa_test_tiobench/COPYING
install -D -m 644 ChangeLog $RPM_BUILD_ROOT/usr/share/doc/packages/qa_test_tiobench/ChangeLog
install -D -m 644 TODO $RPM_BUILD_ROOT/usr/share/doc/packages/qa_test_tiobench/TODO
# now fix file permissions
# no suid root
# no world writable
find $RPM_BUILD_ROOT -type f -print0 | xargs -0 chmod -c o-w,u-s
#ctcs2-glue
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
install -D -m 755 ctcstools/test_tiobench-run $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/test_tiobench-run
install -D -m 755 ctcstools/tiobench.tcf $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/tiobench.tcf
install -D -m 755 ctcstools/test_tiobench-bench-run $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/test_tiobench-bench-run
install -D -m 755 ctcstools/tiobench-bench.tcf $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/tiobench-bench.tcf
install -D -m 755 ctcstools/eatmem.sh $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/eatmem.sh
ln -sf ../qa_test_tiobench/eatmem.sh $RPM_BUILD_ROOT/usr/share/qa/tools/eatmem.sh
ln -sf ../qa_test_tiobench/tiobench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/tiobench.tcf
ln -sf ../qa_test_tiobench/test_tiobench-run $RPM_BUILD_ROOT/usr/share/qa/tools/test_tiobench-run
ln -sf ../qa_test_tiobench/tiobench-bench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/tiobench-bench.tcf
ln -sf ../qa_test_tiobench/test_tiobench-bench-run $RPM_BUILD_ROOT/usr/share/qa/tools/test_tiobench-bench-run
ln -sf ../share/qa/qa_test_tiobench/eatmem.sh $RPM_BUILD_ROOT/usr/bin/eatmem.sh
ln -sf ../../../share/qa/qa_test_tiobench/tiobench.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/tiobench.tcf
ln -sf ../../../share/qa/qa_test_tiobench/test_tiobench-run $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/test_tiobench-run
ln -sf ../../../share/qa/qa_test_tiobench/tiobench-bench.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/tiobench-bench.tcf
ln -sf ../../../share/qa/qa_test_tiobench/test_tiobench-bench-run $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/test_tiobench-bench-run
find $RPM_BUILD_ROOT -type f -print0 | xargs -0 chmod -c o-w,u-s

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_tiobench.8.gz
/usr/bin/eatmem
/usr/bin/tiotest
/usr/bin/tiobench.pl
/usr/bin/tiosum.pl
/usr/share/doc/packages/qa_test_tiobench

#%files ctcs2-glue
#%defattr(-, root, root)
/usr/bin/eatmem.sh
%dir /usr/lib/ctcs2
%dir /usr/lib/ctcs2/tcf
%dir /usr/lib/ctcs2/tools
/usr/lib/ctcs2/tcf/tiobench.tcf
/usr/lib/ctcs2/tools/test_tiobench-run
/usr/lib/ctcs2/tcf/tiobench-bench.tcf
/usr/lib/ctcs2/tools/test_tiobench-bench-run
%dir /usr/share/qa
%dir /usr/share/qa/tcf
%dir /usr/share/qa/tools
/usr/share/qa
/usr/share/qa/qa_test_tiobench
/usr/share/qa/tcf/tiobench.tcf
/usr/share/qa/tools/test_tiobench-run
/usr/share/qa/tcf/tiobench-bench.tcf
/usr/share/qa/tools/test_tiobench-bench-run
/usr/share/qa/tools/eatmem.sh

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 10 2008 ro@suse.de
- added directories to filelist
* Wed May 30 2007 ehamera@suse.cz
- fixed/workarounded problem on dom0 XEN kernel, which reports 0 time.
  Code is reporting lines like this:
  Random Reads
  2.6.16.46-0.12-xen            1902  4096    1    6.01 1e-10%%     0.649       27.28   0.00000  0.00000 #####
  where 1e-10 means zero and ##### means infinity. It is better than
  fail on 'division by zero' error I mean.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 19 2006 fseidel@suse.de
- reworked for fit in autobuild an packaging guidlines
