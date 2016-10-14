#
# spec file for package qa_test_newburn
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           qa_test_newburn
Version:        0.5.2
Release:        0
Summary:        Stress test for linux for the ctcs2 test bed
License:        LGPL-2.1+
Group:          System/Benchmark
Source0:        %{name}-%{version}.tar.bz2
Source1:        memtst.tcf
Source2:        qa_test_newburn.8
Source3:        test_newburn-run
Source4:        test_newburn-memtst-run
Requires:       ctcs2
Requires:       kernel-source
Provides:       newburn
Obsoletes:      newburn
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A stress test for linux, which is designed to run inside of ctcs2

%package memtst
Summary:        Newburn memory test
Group:          System/Benchmark
Requires:       ctcs2
Requires:       qa_test_newburn
Provides:       newburn-memtst
Obsoletes:      newburn-memtst

%description memtst
This package contains tcf file to run newburn memory test

%prep
%setup -q -n %{name}

%build
make %{?_smp_mflags} CC="cc %{optflags}" -C memtst.src
cc %{optflags} -o flushb.src/flushb.real -lm flushb.src/flushb.c

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_prefix}/lib/ctcs2/tools
mkdir -p %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn
mkdir -p %{buildroot}%{_datadir}/qa/tcf
(cd memtst.src ; cp memtst maxalloc %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn)
cp blockrdtst blockrdtst-info info_linux messages newburn-generator vmstat-wrapper %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn
cp dmesg kernel newburn timestamp %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn
cp print_disk_info flushb flushb.src/flushb.real %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn
cp loop.sh %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn
chmod +x  %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn/*
ln -s blockrdtst %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn/sblockrdtst
ln -s blockrdtst-info %{buildroot}%{_prefix}/lib/ctcs2/bin/qa_test_newburn/sblockrdtst-info
cp %{SOURCE4} %{buildroot}%{_prefix}/lib/ctcs2/tools
cp %{SOURCE3} %{buildroot}%{_prefix}/lib/ctcs2/tools
chmod 755 %{buildroot}%{_prefix}/lib/ctcs2/tools/test_newburn-run
chmod 755 %{buildroot}%{_prefix}/lib/ctcs2/tools/test_newburn-memtst-run
cp %{SOURCE1} %{buildroot}%{_datadir}/qa/tcf
# now fix file permissions
# no suid root
# no world writable
find %{buildroot} -type f -print0 | xargs -0 chmod -c o-w,u-s

%files
%defattr(-,root,root)
%{_mandir}/man8/qa_test_newburn.8%{ext_man}
%{_prefix}/lib/ctcs2
%exclude %{_prefix}/lib/ctcs2/tools/test_newburn-memtst-run

%files memtst
%defattr(-,root,root)
%{_datadir}/qa/tcf/memtst.tcf
%{_datadir}/qa
%{_prefix}/lib/ctcs2/tools/test_newburn-memtst-run

%changelog
