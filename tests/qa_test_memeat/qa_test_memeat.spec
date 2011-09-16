#
# spec file for package memeat (Version 0.1)
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


Name:           qa_test_memeat
#BuildRequires:  ctcs2
License:        No license agreement found in package
Group:          SUSE internal
AutoReqProv:    on
Version:        0.1
Release:        224
Summary:        rd-qa-kernel internal package for easy memstressing
Source:         memeat-%{version}.tar.bz2
Source1:	qa_test_memeat.8
Source2:	memeat.tcf
Source3:	test_memeat-run
Patch0:         %{name}-%{version}-noloop.diff
Patch1:         %{name}-%{version}-memfree-fallback.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       memeat
Obsoletes:      memeat

#ExclusiveArch: %ix86

%description
Contains an easy program that eats up nearly all available (low) mem of
the system and does read and write operations on it.



Authors:
--------
    Andi Kleen <ak@suse.de>

%prep
%setup -q -n memeat-%{version}
%patch0 -p1
%patch1 -p1

%build
make clean
make CFLAGS="$RPM_OPT_FLAGS" all

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/qa_test_memeat
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/qa_test_memeat/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/qa_test_memeat/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/bin
cp -v memeat memeat.sh $RPM_BUILD_ROOT/usr/share/qa/qa_test_memeat/
cp -v %{S:2} $RPM_BUILD_ROOT/usr/share/qa/qa_test_memeat/tcf/
cp -v %{S:3} $RPM_BUILD_ROOT/usr/share/qa/qa_test_memeat/tools/
chmod 775 $RPM_BUILD_ROOT/usr/share/qa/qa_test_memeat/tools/test_memeat-run
ln -s ../share/qa/qa_test_memeat/memeat $RPM_BUILD_ROOT/usr/bin/memeat
ln -s ../share/qa/qa_test_memeat/memeat.sh $RPM_BUILD_ROOT/usr/bin/memeat.sh
ln -s ../qa_test_memeat/tcf/memeat.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/memeat.tcf
ln -s ../../../share/qa/qa_test_memeat/tcf/memeat.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/memeat.tcf
ln -s ../qa_test_memeat/tools/test_memeat-run $RPM_BUILD_ROOT/usr/share/qa/tools/test_memeat-run
ln -s ../../../share/qa/qa_test_memeat/tools/test_memeat-run $RPM_BUILD_ROOT/usr/lib/ctcs2/tools/test_memeat-run

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_memeat.8.gz
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools
/usr/share/qa/qa_test_memeat
/usr/share/qa/tcf/memeat.tcf
/usr/share/qa/tools/test_memeat-run
/usr/lib/ctcs2
/usr/lib/ctcs2/tcf
/usr/lib/ctcs2/tools
/usr/lib/ctcs2/tcf/memeat.tcf
/usr/lib/ctcs2/tools/test_memeat-run
/usr/bin/memeat
/usr/bin/memeat.sh

%changelog
* Wed Oct 15 2008 mmrazik@suse.cz
- Fallback to MemFree if LowFree is not available (bnc#398434)
* Mon Mar 10 2008 ro@suse.de
- added directories to filelist
* Thu Apr 05 2007 yxu@suse.de
- add a counter to let memeat loop finish
* Tue Jan 24 2006 fseidel@suse.de
- initial release
