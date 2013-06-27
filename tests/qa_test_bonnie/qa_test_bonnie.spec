#
# spec file for package bonnie (Version 1.4)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_bonnie
Url:            http://www.garloff.de/kurt/linux/bonnie
License:        Artistic
Group:          System/Benchmark
AutoReqProv:    on
Summary:        File System Benchmark
Version:        1.4
Release:        354
Source0:        bonnie-%{version}.tar.bz2
Source1:	do_bonnie
Source2:	qa_test_bonnie.8
Source3:	test_bonnie-run
Source4:	bonnie-default.tcf
Patch0:         bonnie-1.4.dif
#Patch:  %{name}-%{version}.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	bonnie bonnie-ctcs2-glue
Obsoletes:	bonnie bonnie-ctcs2-glue
Requires:	ctcs2 >= 0.1.1
#BuildRequires:	linux-kernel-headers  - fails on SLES-10-SP2
#BuildRequires:	kernel-source

%description
Bonnie is a popular performance benchmark that targets various aspects
of Unix file systems.

This subpackage also provides scripts and TCF files to the QA CTCS2 framework.


Authors:
--------
    Tim Bray <tbray@textuality.com>
    Kurt Garloff <garloff@suse.de>
    Vilem Marsik <vmarsik@suse.cz>

%prep
%setup -n bonnie 
%patch0 -p1

%build
make CC=gcc CFLAGS="$RPM_OPT_FLAGS"

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_bonnie/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 744 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/qa_test_bonnie/
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/qa_test_bonnie/tcf/
for A in `ls $RPM_BUILD_ROOT/usr/share/qa/qa_test_bonnie/tcf/`; do ln -s ../qa_test_bonnie/tcf/$A $RPM_BUILD_ROOT/usr/share/qa/tcf/; done
install -m 744 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tools/ 

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_bonnie.8.gz
%doc bonnie.doc README
/usr/bin/bonnie
%{_mandir}/man1/bonnie.1.gz
/usr/share/qa

%changelog -n qa_test_bonnie
* Sat Apr 26 2008 coolo@suse.de
- remove unused header file
* Fri Mar 07 2008 vmarsik@suse.cz
- added a subpackage ctcs2-glue
* Mon May 22 2006 schwab@suse.de
- Don't build as root.
- Don't strip binaries.
* Fri May 19 2006 ro@suse.de
- fix build on ppc64 (define PAGE_MASK if not done)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Apr 04 2002 garloff@suse.de
- Version-1.4:
  * Fix seek benchmark: 1.3 read too large chunks (1MB instead
  of 16k) after every seek, resulting in too low seek numbers.
  bug #15642
* Sun Feb 24 2002 garloff@suse.de
- Compile fix for archs not supporting O_DIRECT (typo)
- Use O_DIRECT from fcntl.h if present.
* Wed Feb 20 2002 garloff@suse.de
- Update to bonnie-1.3:
  * Fixed HTML output (thanks to Rupert Kolb for notfying/patch)
  * Optionally use O_DIRECT (patch by Chris Mason / Andrea Arc.)
* Wed Aug 30 2000 garloff@suse.de
- Update to 1.2:
  * New option -u for getc_/putc_unlocked.
  * Fixed CPU percentage reports if equal or in excess of 100%%.
  * Machine name defaults to hostname now.
- Use BuildRoot.
* Mon Feb 14 2000 garloff@suse.de
- Moved manpage to /usr/share/man
- new options -y, -S, -p
- Add warning if test-size smaller memsize
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Tue Jul 20 1999 garloff@suse.de
- Initial check in of Big Bonnie.
- Added breakhandler to remove temporary files.
