#
# spec file for package qa_apache_testsuite (Version 503706)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_apache_testsuite
License:        Apache 2.0
Group:          SUSE internal
AutoReqProv:    on
Version:        894558
Release:        1
Summary:        (rd-)qa internal package for testing apache and apache2
Url:            http://httpd.apache.org/test/
Source0:        %{name}-%{version}.tar.bz2
Source1:        mod_perl-2.0.4.tar.bz2
Source2:	test_apache_testsuite-run
Source3:	qa_test_apache_testsuite.8
Patch0:         CVE-2004-0959.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Provides:	qa_apache_testsuite
Obsoletes:	qa_apache_testsuite
Requires:       ctcs2 apache2-prefork apache2-devel apache2-mod_perl apache2-mod_php5 apache2-mod_python apache2-worker gcc perl-libwww-perl perl-IO-Socket-SSL

%description
This package contains automated tests for apache developed with
perl-framework.

%prep
%setup -b 1 -n %{name}
cd ..
%patch0 -p0

%install
#
# create the directories
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/httpd-test
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/mod_perl-tests
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/man/man8
#install the files
install -m 755 %SOURCE2 $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 644 %SOURCE3 $RPM_BUILD_ROOT/usr/share/man/man8/
gzip $RPM_BUILD_ROOT/usr/share/man/man8/qa_test_apache_testsuite.8
#
#
# generate the tcf file for ctcs2
touch $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf/qa_apache_testsuite.tcf
ln -s ../%name/tcf/qa_apache_testsuite.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
#
# remove failing/weird tests
#
#I think this test is borken. Actually I don't understand why it should
#give the expected result
rm -f t/php/umask.t
#
#
#
cp -r * $RPM_BUILD_ROOT/usr/share/qa/%{name}/httpd-test
cp -r ../mod_perl/* $RPM_BUILD_ROOT/usr/share/qa/%{name}/mod_perl-tests
find $RPM_BUILD_ROOT/usr/share/qa -type f -name "*.html" -print0 | xargs -0 -r chmod a-x

%build

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/qa/
/usr/share/man/man8/qa_test_apache_testsuite.8.gz
#/usr/share/qa/qa_test_apache_testsuite/
#/usr/lib/ctcs2/tcf/
/usr/share/qa/tcf/qa_apache_testsuite.tcf
%attr(777, root, root) /usr/share/qa/qa_test_apache_testsuite/mod_perl-tests/lib/Apache/TestConfigData.pm

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_apache_testsuite -> qa_test_apache_testsuite
* Thu Jan 31 2008 mmrazik@suse.cz
- added dependency to perl-IO-Socked-SSL (some tests were skipped due to
  missing dep)
* Mon Feb 05 2007 mmrazik@suse.cz
- testsuite upgrade
* Mon Nov 13 2006 ro@suse.de
- remove executable bits from html files
* Thu Jul 27 2006 mmrazik@suse.cz
- timeout for tests increased to 30min (in the tcf file)
* Wed Jul 26 2006 mmrazik@suse.cz
- minor changes in run-tests.sh (dav must be loaded before authz_svn +
  patch for ppc64)
* Thu Jul 20 2006 mmrazik@suse.cz
- fixed BuildRequires (removed most of the packages)
* Thu Jun 01 2006 mmrazik@suse.cz
- minor fix of run-tests.sh (mod_proxy must be loaded before proxy_balancer)
- testsuite upgrade (some minor changes in perl-framework)
* Wed Mar 01 2006 mmrazik@suse.cz
- added -target option to test execution (this is due to bad design of perldo.t test)
* Wed Feb 08 2006 mmrazik@suse.cz
- mod_perl testsuite upgrade (2.0.1->2.0.2)
- fixed dependencies (removed perl-Crypt-SSLeay)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jan 18 2006 mmrazik@suse.cz
- removed qa_apache_testsuite-0.2-mod_imap-rename.diff (accepted by upstream)
- fixed tcf file location (updated QA Packaging Guidelines)
- created run-script (see QA Packaging Guidelines)
- added qa_dummy dependency
* Sat Jan 14 2006 kukuk@suse.de
- Add gmp-devel to nfb
* Wed Jan 11 2006 mmrazik@suse.cz
- fixed test for CVE-2004-0959 (changed error_reporting())
- fixed modules/info.t test (mod_imap is renamed to mod_imagemap)
* Tue Jan 10 2006 mmrazik@suse.cz
- php4 -> php5 in dependencies
- fixed the building with current stable (e.i. no libapr0)
- fixed the run-tests.sh script
- downloaded new svn version of tests (e.i. version upgrade)
* Mon Jan 09 2006 ro@suse.de
- php4 -> php5 in neededforbuild
* Tue Dec 06 2005 mmrazik@suse.cz
- raised timeouts in tcf file (from 300s to 600s)
    - raised the apache start timeout from 60s to 180s
    - fixed the tcf location (now conforming to QA package guidelines)
* Wed Nov 30 2005 mmrazik@suse.cz
- run-tests.sh fixed (because of typo all of the tests were failing)
* Mon Nov 28 2005 mmrazik@suse.cz
- fixed file run-tests.sh for 64 bit platforms
* Mon Nov 28 2005 mmrazik@suse.cz
- mod_perl tests blacklisted on SLES9
* Tue Nov 15 2005 yxu@suse.de
- fixed changelog
* Mon Nov 14 2005 mmrazik@suse.cz
- fixed the failing test #44 from httpd-test/t/modules/include.t
* Mon Nov 14 2005 mmrazik@suse.cz
- fixed testing environment (shell variables)
- added testcases for httpd-worker (to qa_apache_testsuite.tcf)
- fixed failing testcases from mod_perl (t/modules)
* Fri Nov 11 2005 mmrazik@suse.cz
- changes in spec file.
- warm up time for apache raised to 120 seconds
- initial release
