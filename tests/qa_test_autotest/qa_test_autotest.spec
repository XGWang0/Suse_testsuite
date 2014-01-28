#
# spec file for package autotest (Version 0.12.0)
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


Name:           qa_test_autotest
License:        MIT; Apache 2.0; GPLv2; LGPLv3
Group:          Development/Tools/Other
Provides:	autotest
Obsoletes:	autotest
Requires:       kernel-source gcc gcc-c++ make python postgresql automake autoconf patch
BuildRequires:	ctcs2
AutoReqProv:    on
Summary:        Kernel test suite
Url:            https://github.com/autotest
Version:        0.13.1
Release:        1
Source0:        autotest-autotest-%{version}.tar.gz
Source1:        autotest_quick.tcf
Source2:        test_autotest-run
Source3:        autotest-autotest-%{version}.rpmlintrc
Source4:        qa_test_autotest.8
Source5:	qa_test_autotest-config
Source6:	pre-kvm.sh
Source7:	fio-2.0.3.tar.gz
Source8:    autotest_bench.tcf
Source9:    autotest_no_bench.tcf
Patch0: 	fio.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Autotest with the packed tests/suites is used for kernel testing. This
harness especially is used for testing the mainline kernel.



Authors:
--------
    Various people from test.kernel.org

%prep

%setup -n autotest-autotest-2b0da9d

%patch0 -p1
%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/autotest
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tools
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/config/autotest
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
mkdir -p $RPM_BUILD_ROOT/usr/lib/ctcs2/bin/autotest
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:5} $RPM_BUILD_ROOT/usr/lib/ctcs2/config/autotest
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 %{S:6} $RPM_BUILD_ROOT/usr/lib/autotest
cp -a client/* $RPM_BUILD_ROOT/usr/lib/autotest
cp %{S:7} $RPM_BUILD_ROOT/usr/lib/autotest/tests/fio/
cp %{S:1} $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/
cp %{S:8} $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/
cp %{S:9} $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf/
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools

%files
%defattr(0755,root,root)
/usr/share/man/man8/qa_test_autotest.8.gz
/usr/lib/autotest
/usr/lib/ctcs2
/usr/share/qa/

#%doc README

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Nov 22 2011 jtang@suse.com
- update the autotest testsuite
* Mon Oct 21 2011 cachen@suse.com
- add configuration file for iso url setting
* Tue Jun 01 2010 lidongyang@novell.com
- upgrade to upstream 0.12.0
* Mon Feb 09 2009 yxu@suse.de
- turned off cpu_hotplug test, bnc#386714
* Mon Jan 19 2009 yxu@suse.de
- truncate autotest_quick.tcf
- fix typo in autotest.tcf
* Thu Oct 09 2008 yxu@suse.de
- fix for bnc #430680
- included "setup_modules.py" in the list of files to be installed
* Tue Jun 17 2008 pkirsch@suse.de
- changed every python2.4 call to generic python, to be
  more universal and bypass build constraints
* Tue Jun 17 2008 pkirsch@suse.de
- switched to mainline svn version 1686
- edited nearly all patches, due to changed API
- some test suites still does not work out of the box
* Tue May 06 2008 yxu@suse.de
- added autotest-cpu_hotplug tcf file
- renamed the old autotest-cpu_hotplug tcf file to autotest-cyclictest
  according to its content (autotest-cyclictest test)
* Wed Mar 12 2008 yxu@suse.de
- build the package for some more distros: e.g. sles9, sles10
* Fri Feb 15 2008 pkirsch@suse.de
- added common_lib in spec_file, due to autotest mainline changes
* Mon Jan 28 2008 pkirsch@suse.de
- updated to svn 1208 from mainline
- added get_blktrace.patch
* Fri Oct 12 2007 pkirsch@suse.de
- corrected disktest.py to use diskfree for used diskspace
* Fri Sep 14 2007 pkirsch@suse.de
- enabled posgresql testsuite
* Tue Sep 11 2007 pkirsch@suse.de
- corrected kernelbuild and sparse testcases to run with
  SUSE
* Tue Sep 11 2007 pkirsch@suse.de
- set all working directorys to /abuild
* Mon Aug 27 2007 pkirsch@suse.de
- correct max run time of tests to 1d
* Fri Jul 13 2007 pkirsch@suse.de
- initial package
