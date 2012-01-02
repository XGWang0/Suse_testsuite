#
# spec file for package unixbench (Version 4.0.1)
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
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench
#mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/src
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/testdir
#mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/old-doc
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/tmp
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/results
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/pgms
install -m 755 ./Run $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/Run
#install -m 755 ./COPYING $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/COPYING
#install -m 755 ./LICENSE $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/LICENSE
install -m 755 ./pgms/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/pgms/.
#install -m 755 ./src/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/src/.
install -m 755 ./testdir/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/testdir/.
#install -m 755 ./old-doc/* $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/old-doc/.
#install -m 755 ./tmp $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/tmp/.
#install -m 755 ./results $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/results/.
#if [ ! -d $RPM_BUILD_ROOT/usr/bin ];
#then
#	mkdir -p $RPM_BUILD_ROOT/usr/bin
#fi
#ln -sf  $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench/Run  $RPM_BUILD_ROOT/usr/bin/unixbench-run 

%clean
rm -rf $RPM_BUILD_ROOT/usr/share/qa/qa_test_unixbench
#rm -rf $RPM_BUILD_ROOT/usr/share/qa/unixbench-run

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_unixbench.8.gz
%doc COPYING LICENSE
%dir /usr/share/qa
/usr/share/qa/qa_test_unixbench
#

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
