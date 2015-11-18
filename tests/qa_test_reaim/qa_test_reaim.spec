#
# spec file for package reaim (Version 7.0.1.13)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_reaim
BuildRequires:  libaio-devel automake libtool
Url:            http://sourceforge.net/projects/re-aim-7
License:        GPL v2 or later
Group:          Development/Tools/Other
AutoReqProv:    on
Summary:        Benchmark tool
Version:        7.0.1.13
Release:        102
Source0:        reaim-%{version}.tgz
# For subpackage creation
Source1:        ctcstools-%{version}.tar.bz2
Source2:	README
Source3:	qa_test_reaim.8	
Patch0:          bugfixes.patch
Patch1:         fix-aio.patch
Patch2:         fix-defaults.patch
Patch3:         fix-tst_sig.patch
Patch4:         fix-abs-paths.patch
Patch5:         ready-for-sles8.patch
Patch6:         fix-diskdir.patch
Patch7:         drop-aio.patch
Patch8:         fix-pipe_test.patch
Patch9:         c_macro_problem.patch
Patch10:	diskdir_abuild.patch
Patch11:        fix-sync.patch
Requires:       ctcs2
Provides: 	reaim reaim-ctcs2-glue
Obsoletes:	reaim reaim-ctcs2-glue
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This tool benchmarks overall system speed by mixing measurements of
file system speed and execution speed under VM and CPU pressure.



Authors:
--------
    Various from VA Linux
    Gernot Payer <gpayer@suse.de>

#%package ctcs2-glue
#License:        GPL v2 or later
#Summary:        The let-reaim-be-run-via-ctcs glue
#Group:          Development/Tools/Other
#AutoReqProv:    on
#Requires:       ctcs2 >= 0.1.6
#Requires:       reaim = %{version}
#
#%description ctcs2-glue
#This package contains the glue for integrating reaim into the ctcs
#testing framework.
#
#
#
#Authors:
#--------
#    Various from VA Linux
#    Gernot Payer <gpayer@suse.de>

%prep
#%setup -q -n %{name}-full-%{version} -a1
%setup -q -n reaim-%{version} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
# aio stuff is not written portable => rewrite it for sles8
%if %suse_version < 910
%patch5 -p1
%endif
%patch6 -p1
# drop aio if building for sles7
%if %suse_version < 810
%patch7 -p1
%endif
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%build
./bootstrap
./configure
make

%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/reaim
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/config/reaim
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/reaim
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/qa_test_reaim.8
cp -r data scripts $RPM_BUILD_ROOT/usr/lib/reaim
cp src/reaim data/reaim.config $RPM_BUILD_ROOT/usr/lib/reaim
cp ctcstools/workfile $RPM_BUILD_ROOT/usr/lib/reaim/workfile
cp ctcstools/test_reaim-run $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
chmod +x $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/test_reaim-run
install -m 755 ctcstools/test_reaim_ioperf-run $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 ctcstools/test_reaim_all-run $RPM_BUILD_ROOT/usr/share/qa/tools
cp ctcstools/reaim.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
cp ctcstools/prepare.sh $RPM_BUILD_ROOT/usr/lib/ctcs2/config/reaim
chmod +x $RPM_BUILD_ROOT/usr/lib/ctcs2/config/reaim/prepare.sh
ln -s ../../../reaim/reaim.config $RPM_BUILD_ROOT/usr/lib/ctcs2/config/reaim/reaim.config
ln -s ../../../reaim/workfile $RPM_BUILD_ROOT/usr/lib/ctcs2/config/reaim/workfile
ln -s ../../../reaim/reaim $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/reaim
cp %{S:2} $RPM_BUILD_ROOT/usr/lib/reaim
# now fix file permissions
# no suid root
# no world writable
find $RPM_BUILD_ROOT -type f -print0 | xargs -0 chmod -c o-w,u-s

%files
%defattr(-,root,root)
/usr/lib/reaim
/usr/share/qa
/usr/share/man/man8/%{name}.8.gz

#%files ctcs2-glue
#%defattr(-,root,root)
/usr/lib/ctcs2

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Aug 15 2011 - llipavsky@suse.cz
- Package rename: reaim -> qa_test_reaim
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Thu Feb 15 2007 ehamera@suse.cz
- Lines with two incrementing macros in one term has been splitted.
  (c_macro_problem.patch)
* Mon Jul 17 2006 ehamera@suse.cz
- %%{_libdir} has benn substituted by usr/lib because ctcs expect
  all files in /usr/lib/, not in /usr/lib64/
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Aug 02 2005 gpayer@suse.de
- Installs now to default libdir
* Tue Apr 26 2005 gpayer@suse.de
- Changed address request for sockets in pipe_test.c
* Tue Apr 12 2005 gpayer@suse.de
- Added patch for building reaim for sles7
* Wed Nov 24 2004 gpayer@suse.de
- Fixed low level aio stuff for sles8
- Diskdirs are now created automatically
* Mon Nov 15 2004 gpayer@suse.de
- Added subpackage: ctcs2-glue
- Fixed hard coded absolute paths
* Fri Oct 29 2004 gpayer@suse.de
- Upgraded to version 7.0.1.13
- Fixed missing libaio build dependency
- Fixed various minor bugs
* Fri Sep 03 2004 gpayer@suse.de
- Removed Provide field, which was buggy due to missing documentation
* Wed May 26 2004 gpayer@suse.de
- Initial package
