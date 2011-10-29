#
# spec file for package libmicro (Version 0.4.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_libmicro
License:        Other uncritical OpenSource License ; CDDL
Group:          System/Benchmark
BuildRequires:  kernel-source gcc make
AutoReqProv:    on
Summary:        kernel test suite, micro benchmark
Url:            http://www.opensolaris.org/os/project/libmicro/
Version:        0.4.0
Release:        81
Source0:        libmicro-%{version}.tar.bz2
Source1:        ctcstools.tar.bz2
Source2:	qa_test_libmicro.8
Patch0:         find_binary.patch
Patch1:         removed_undefined_warning.patch
Patch2:		free_histo.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	libmicro libmicro-ctcs2-glue
Obsoletes:	libmicro libmicro-ctcs2-glue
Requires:       ctcs2 >= 0.1.6

%description
LibMicro is intended to measure the performance of various system and
library calls. LibMicro was developed by Bart Smaalders and Phil
Harman.



Authors:
--------
    Various people from OpenSolaris community

#%package ctcs2-glue
#License:        Other uncritical OpenSource License ; CDDL
#Summary:        The let-libmicro-be-run-via-ctcs glue
#Group:          Development/Tools/Other
#AutoReqProv:    on
#Requires:       ctcs2 >= 0.1.6
#Requires:       libmicro = %{version}
#
#%description ctcs2-glue
#This package contains the glue for integrating libmicro into the ctcs
#testing framework.
#
#
#
#Authors:
#--------
#    Patrick Kirsch <pkirsch@suse.de>

%prep
%setup -n libmicro-%{version}
%setup -D -a 1 -n libmicro-%{version}
%patch0 -p1
%patch1 
%patch2 -p1

%build
# This package failed when testing with -Wl,-as-needed being default.
# So we disable it here, if you want to retest, just delete this comment and the line below.
export SUSE_ASNEEDED=0
  	make 

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/lib/libMicro
mkdir -p $RPM_BUILD_ROOT/usr/lib/libMicro/bin
install -m 644 README $RPM_BUILD_ROOT/usr/lib/libMicro
cp bin/* $RPM_BUILD_ROOT/usr/lib/libMicro/bin
cp bin-*/* $RPM_BUILD_ROOT/usr/lib/libMicro/bin
install -m 755 *.sh $RPM_BUILD_ROOT/usr/lib/libMicro/bin
#the sequence is important!
#install -m 755 runtests.sh $RPM_BUILD_ROOT/usr/lib/libMicro	
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
cp ctcstools/test_libmicro-run $RPM_BUILD_ROOT/usr/share/qa/tools
cp ctcstools/libmicro.tcf $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
cp ctcstools/test_libmicro-bench-run $RPM_BUILD_ROOT/usr/share/qa/tools
cp ctcstools/libmicro-bench.tcf $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
ln -s ../%{name}/tcf/libmicro.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/libmicro.tcf
ln -s ../%{name}/tcf/libmicro-bench.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/libmicro-bench.tcf

%files
%defattr(-,root,root)
/usr/share/man/man8/qa_test_libmicro.8.gz
/usr/lib/libMicro
%doc README

#%files ctcs2-glue
#%defattr(-,root,root)
/usr/share/qa

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Aug 12 2011 - llipavsky@suse.cz
- Package rename: libmicro -> qa_test_libmicro
* Fri Jun 19 2009 coolo@novell.com
- disable as-needed for this package as it fails to build with it
* Fri Jul 04 2008 pkirsch@suse.de
- added libmicro-ctcs-glue package, now the tcf is packaged and
  can be run from the SUT without the need of NIS
* Wed May 28 2008 pkirsch@suse.de
- removed warning for bnc#394556,
  thanks to David Binderman
* Mon Mar 17 2008 yxu@suse.de
- retrieve the essential test executing file: bench.sh
- clarify the path for binary in bench.sh
* Fri Jul 13 2007 pkirsch@suse.de
- initial package
