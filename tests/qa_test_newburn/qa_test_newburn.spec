#
# spec file for package newburn (Version 0.4)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_newburn
License:        LGPL v2.1 or later
Group:          System/Benchmark
AutoReqProv:    on
Summary:        Stress test for linux for the ctcs2 test bed
Version:        0.5.2
Release:        1
Provides:	newburn
Obsoletes:	newburn
Requires:       ctcs2 kernel-source
Source0:        %{name}-%{version}.tar.bz2
Source1:        memtst.tcf
Source2:	qa_test_newburn.8
Source3:	test_newburn-run
Source4:	test_newburn-memtst-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A stress test for linux, which is designed to run inside of ctcs2



Authors:
--------
    Various people from VA Linux


%package memtst
Summary:        Newburn memory test  
Group:          System/Benchmark
AutoReqProv:    on
Provides:	newburn-memtst
Obsoletes:	newburn-memtst
Requires:       qa_test_newburn ctcs2

%description memtst
This package contains tcf file to run newburn memory test


%prep
%setup -n %{name}

%build
make -C memtst.src
make -C flushb.src

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/qa_test_newburn
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
(cd memtst.src ; cp memtst maxalloc $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/qa_test_newburn)
cp blockrdtst blockrdtst-info info_linux messages newburn-generator vmstat-wrapper $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/qa_test_newburn
cp dmesg kernel newburn timestamp $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/qa_test_newburn
cp print_disk_info flushb flushb.src/flushb.real $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/qa_test_newburn
ln -s blockrdtst $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/qa_test_newburn/sblockrdtst
ln -s blockrdtst-info $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/qa_test_newburn/sblockrdtst-info
cp %{S:4} $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
cp %{S:3} $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
chmod 755 $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/test_newburn-run
chmod 755 $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/test_newburn-memtst-run
cp %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tcf
# now fix file permissions
# no suid root
# no world writable
find $RPM_BUILD_ROOT -type f -print0 | xargs -0 chmod -c o-w,u-s

%files
%defattr(-,root,root)
/usr/share/man/man8/qa_test_newburn.8.gz
/usr/lib/ctcs2
%exclude /usr/lib/ctcs2/tools/test_newburn-memtst-run
%exclude /usr/lib/ctcs2/bin/qa_test_newburn/memtst


%files memtst
%defattr(-,root,root)
/usr/share/qa/tcf/memtst.tcf
/usr/lib/ctcs2/tools/test_newburn-memtst-run
/usr/lib/ctcs2/bin/qa_test_newburn/memtst

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Nov 05 2010 aguo@novell.com
- fix bnc#651257 - newburn cannot generate tcf file
- fix some cannot find file errors
* Thu Jul 29 2010 llipavsky@suse.cz
- moved fix bnc#626573 - newburn test doesn't start to ctcs2
* Thu Jul 29 2010 llipavsky@suse.cz
- fix bnc#626573 - newburn test doesn't start
* Thu Jun 17 2010 llwang@novell.com
- fix BZ612507, change this package into internal source model
* Fri Nov 21 2008 yxu@suse.de
- bnc445112-memtst-fix.patch applied
* Wed Oct 15 2008 dgollub@suse.de
- added bnc398429-newburn-asm_page_h.diff:
  asm/page.h is obsolate in 2.6.27(-rcX) (bnc#398429)
* Sat Apr 26 2008 coolo@suse.de
- fix build
* Wed Jan 16 2008 pkirsch@suse.de
- patch for compressing logfiles (BB*) after run
* Thu Aug 09 2007 olh@suse.de
- remove PAGE_SIZE usage
* Tue Mar 06 2007 pkirsch@suse.de
- added default values for ia64, because there is no fdisk
  available and few testcases do not run, see bug #250541
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 17 2006 fseidel@suse.de
- fixed blockrdtst-info
* Thu Oct 13 2005 ories@suse.de
- initial submission
- test_newburn-run will look for absolute paths
