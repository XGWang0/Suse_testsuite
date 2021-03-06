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
Source2:	    qa_test_tiobench.8
Patch1:         XEN-dom0-problem.patch
Patch2:         invalid_results_format.patch
Patch3:		    eatmem.patch
# bnc#835355 tiobench compiling conflict on aligned_alloc
Patch4:         tiobench-remove-conflict-on-aligned_alloc.patch
Patch5:     tiobench-add-sync-option.patch
Patch6:     ctcs2_remove_backspace.patch
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
%patch4 -p1
%patch5 -p1
%patch6 -p1

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

pushd ctcstools > /dev/null
for name in *; do
    case $name in
        *.tcf)
            install -D -m 644 ${name} $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/
            ln -sf ../qa_test_tiobench/${name} $RPM_BUILD_ROOT/usr/share/qa/tcf/
            ln -sf ../../../share/qa/qa_test_tiobench/${name} $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/
            ;;
        *-run)
            install -D -m 755 ${name} $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/
            ln -sf ../qa_test_tiobench/${name} $RPM_BUILD_ROOT/usr/share/qa/tools/
            ln -sf ../../../share/qa/qa_test_tiobench/${name} $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/
            ;;
    esac
    install -D -m 755 ${name} $RPM_BUILD_ROOT/usr/share/qa/qa_test_tiobench/
    ln -sf ../share/qa/qa_test_tiobench/eatmem.sh $RPM_BUILD_ROOT/usr/bin/
done
popd > /dev/null

find $RPM_BUILD_ROOT -type f -print0 | xargs -0 chmod -c o-w,u-s

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_tiobench.8.gz
/usr/bin/eatmem
/usr/bin/tiotest
/usr/bin/tiobench.pl
/usr/bin/tiosum.pl
/usr/share/doc/packages/qa_test_tiobench
/usr/bin/eatmem.sh
/usr/lib/ctcs2
/usr/lib/ctcs2/tcf
/usr/lib/ctcs2/tools
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools

#%files ctcs2-glue
#%defattr(-, root, root)

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
