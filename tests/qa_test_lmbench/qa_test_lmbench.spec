#
# spec file for package lmbench (Version 3.0_a9)
#

# norootforbuild


Name:           qa_test_lmbench
Url:            http://www.bitmover.com/lmbench/
License:        GPL v2 or later
Group:          SUSE internal
AutoReqProv:    on
Provides:	lmbench lmbench-ctcs2-glue
Obsoletes:	lmbench lmbench-ctcs2-glue
Requires:       coreutils make gcc ctcs2
Version:        3svn1324
Release:        5
Summary:        Some benchmarks
Source0:        lmbench-3.tar.bz2
Source1:        ctcstools.tar.bz2
Source2:        rpmlintrc
Source3:        README
Source4:	qa_test_lmbench.8
#Patch0:         lmbench-%{version}.diff
#Patch1:         lmbench-%{version}-ia64.diff
Patch0:         lmbench-3-automation.diff
Patch1:         lmbench-3-config.diff
Patch2:         lmbench-3-split-testcase.diff
Patch3:         bigger_size_for_filesize.patch
Patch4:         merge_testcases_into_groups.patch
BuildRoot:      %{_tmppath}/%{name}-3-build

%description
lmbench is a series of micro benchmarks intended to measure basic
operating system and hardware system metrics.



Authors:
--------
    Larry McVoy <lm@who.net>

#%package ctcs2-glue
#License:        GPL v2 or later
#Summary:        Let lmbench run via ctcs2
#Group:          SUSE internal
#AutoReqProv:    on
#Requires:       ctcs2 qa_dummy
#Requires:       lmbench = %{version}
#
#%description ctcs2-glue
#This package contains the glue for integrating lmbench into the ctcs
#testing framework.
#
#
#
#Authors:
#--------
#    Yi Xu

%prep
#%setup -q
%setup -q -n lmbench-3 -a1
#%patch0 -p1
#%patch1
find -name "*.orig" -type f | xargs -r rm -fv
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
# install qa_test_lmbench
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/scripts
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/results
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/src
echo $(pwd)
cp -r bin/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/bin
cp scripts/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/scripts
cp results/Makefile $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/results/
cp -r src/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/src
# create directories
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/bin
# install ctcs2 related files in the ctcs2-glue sub packages
cd ctcstools
install -m 744 do_lmbench $RPM_BUILD_ROOT/usr/bin/do_lmbench
install -m 744 test_lmbench-run $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 test_lmbench.bcopy-run    $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 test_lmbench.ctx-run    $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 test_lmbench.file-run    $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 test_lmbench.mem-run    $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 test_lmbench.ops-run    $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 test_lmbench.local-run    $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 test_lmbench.syscall-run    $RPM_BUILD_ROOT/usr/share/qa/tools

#install -m 644 lmbench.tcf $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench

#ln -s ../qa_test_lmbench/lmbench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/lmbench.tcf

ln -s ../tools/test_lmbench-run             $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench-run
ln -s ../tools/test_lmbench.bcopy-run       $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench.bcopy-run
ln -s ../tools/test_lmbench.ctx-run         $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench.ctx-run
ln -s ../tools/test_lmbench.file-run        $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench.file-run
ln -s ../tools/test_lmbench.mem-run         $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench.mem-run
ln -s ../tools/test_lmbench.ops-run         $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench.ops-run
ln -s ../tools/test_lmbench.local-run        $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench.local-run
ln -s ../tools/test_lmbench.syscall-run     $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/test_lmbench.syscall-run

cd ..
chmod +x $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench/scripts/config-test
cp %{S:3} $RPM_BUILD_ROOT/usr/share/qa/qa_test_lmbench

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_lmbench.8.gz
%doc COPYING COPYING-2 README
%dir /usr/share/qa/qa_test_lmbench/
%dir /usr/share/qa/tools/
/usr/share/qa/qa_test_lmbench/README
/usr/bin/do_lmbench
/usr/share/qa/qa_test_lmbench/bin
/usr/share/qa/qa_test_lmbench/scripts
/usr/share/qa/qa_test_lmbench/results
/usr/share/qa/qa_test_lmbench/src
%dir /usr/share/qa
#

/usr/share/qa/tools/test_lmbench-run
/usr/share/qa/tools/test_lmbench.bcopy-run
/usr/share/qa/tools/test_lmbench.ctx-run
/usr/share/qa/tools/test_lmbench.file-run
/usr/share/qa/tools/test_lmbench.mem-run
/usr/share/qa/tools/test_lmbench.local-run
/usr/share/qa/tools/test_lmbench.syscall-run
#
/usr/share/qa/tools/test_lmbench-run
#/usr/share/qa/tcf/lmbench.tcf
#/usr/share/qa/tools/test_lmbench-run
/usr/share/qa/qa_test_lmbench/test_lmbench-run
/usr/share/qa/qa_test_lmbench/test_lmbench.bcopy-run
/usr/share/qa/qa_test_lmbench/test_lmbench.ctx-run
/usr/share/qa/qa_test_lmbench/test_lmbench.file-run
/usr/share/qa/qa_test_lmbench/test_lmbench.mem-run
/usr/share/qa/qa_test_lmbench/test_lmbench.ops-run
/usr/share/qa/qa_test_lmbench/test_lmbench.local-run
/usr/share/qa/qa_test_lmbench/test_lmbench.syscall-run


%dir /usr/share/qa
%dir /usr/share/qa/tcf
%dir /usr/share/qa/tools

%changelog
* Wed Mar 04 2009 vpelcak@suse.cz
- update to svn version
* Fri Nov 07 2008 vpelcak@suse.cz
- minor bugfixes (stdout device and time)
* Fri Sep 19 2008 vpelcak@suse.cz
- package upgrade
- changed package infrastructure
* Tue Nov 27 2007 dmueller@suse.de
- fix rpmlint suppressions
* Thu May 31 2007 yxu@suse.de
- add rpmlintrc file to exclude failure:
- "devel-file-in-non-devel-package" during building
* Tue Apr 03 2007 yxu@suse.de
- added lmbench-ctcts2-glue package
- modified config-run file for automated test under ctcs2
- updated scripts/gnu-os script
* Thu Jun 22 2006 ro@suse.de
- remove selfprovides
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Mar 24 2004 ro@suse.de
- removed .orig files from package
* Sat Jan 10 2004 adrian@suse.de
- add %%defattr
* Mon Feb 17 2003 vbobek@suse.cz
- fixed names of patches
- fixed install section
* Mon Feb 17 2003 ro@suse.de
- don't patch SCCS repository
* Mon Feb 17 2003 vbobek@suse.cz
- updated to version 2.0.4
* Mon Dec 03 2001 cihlar@suse.cz
- update to version 2.0-patch2
* Fri Aug 17 2001 cihlar@suse.cz
- update to version 2.0-patch1
* Wed May 23 2001 schwab@suse.de
- Fix casts.
* Thu May 17 2001 cihlar@suse.cz
- fixed cast warnings on ia64
* Wed Mar 07 2001 cihlar@suse.cz
- update to version 2beta1
* Fri Feb 09 2001 cihlar@suse.cz
- fixed to compile
* Tue Nov 28 2000 cihlar@suse.cz
- update to version 2alpha12
- moved to /var/lib
- added BuildRoot
- fixed copyright and group
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Thu Jul 15 1999 jnroed@suse.de
- new package
