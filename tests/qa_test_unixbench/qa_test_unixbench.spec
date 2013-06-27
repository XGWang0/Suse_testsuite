#
# spec file for package unixbench (Version 4.0.1)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           qa_test_unixbench
License:        GPL v2
Group:          System/Benchmark
AutoReqProv:    on
Version:        4.0.1
Release:        9
Summary:        A byte Unix benchmarks
Url:            http://ftp.tux.org/pub/benchmarks/System/unixbench/
Source0:        unixbench-%{version}.tar.bz2
Source1:        COPYING
Source2:        LICENSE
Source3:        qa_test_unixbench-rpmlintrc
Source4:	qa_test_unixbench.8
Source5:	test_unixbench-run
Source6:	qa_unixbench.tcf
Patch0:         unixbench-fix_Run_nomake.diff
Patch1:         unixbench-fix_context_x86_64.diff
Patch2:         unixbench-fix_execl_no_such_file.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#BuildArchitectures: noarch
#ExclusiveArch: %ix86
#Authors:
#--------------
#	David C Niemi

%description
The design flaw was that the benchmarks timed a fixed number of loops;
if there were too few loops, the times were too small to be reliable.
Perhaps we could have increased the number of loops and been safe for
another few years (months?).
for test`



Authors:
--------
    David C Niemi

%prep 
%setup -n unixbench-%version
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/testdir
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/tmp
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/results
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/pgms
install -m 755 ./Run $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/Run
install -m 755 ./pgms/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/pgms/.
install -m 755 ./testdir/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/testdir/.
install -m 755 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/tools/
install -m 644 %{S:6} $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_unixbench.8.gz
%doc COPYING LICENSE
%dir /usr/share/qa
%dir /usr/share/qa/tools
%dir /usr/share/qa/tcf
%dir /usr/share/qa/qa_test_unixbench
%dir /usr/share/qa/qa_test_unixbench/pgms
%dir /usr/share/qa/qa_test_unixbench/testdir
/usr/share/qa/qa_test_unixbench/Run
/usr/share/qa/qa_test_unixbench/pgms/*
/usr/share/qa/qa_test_unixbench/testdir/*
/usr/share/qa/tcf/qa_unixbench.tcf
/usr/share/qa/tools/test_unixbench-run


%changelog
* Fri Nov 28 2008 ro@suse.de
- make it build for the moment, install location needs
  to be modified
* Fri Nov 21 2008 ro@suse.de
- added directory to filelist to fix build
* Fri Nov 14 2008 fhe@suse.de
- change the unixbench installation location
* Tue Oct 28 2008 fhe@suse.de
- fix the bug when run context1 on x86_64 machine with patch unixbench-fix_context_x86_64.diff
  for the data type "int" and "unsigned long" have different size when on x86_64 machine.
- fix the bug when run execl when the work dir is very long or deep with unixbench-fix_execl_no_such_file.diff
  for the variable path_str stands for the absolute path of the execl program, the ori value is not big enough for sometest environment.
* Wed Sep 03 2008 fhe@suse.de
- add the LICENSE and COPYING files
* Tue Sep 02 2008 fhe@suse.de
- clear the license
* Mon Aug 04 2008 fhe@suse.de
-fix the Run bug  when we start we no need to make the source code at all
* Wed Jul 30 2008 fhe@suse.de
-initial release
