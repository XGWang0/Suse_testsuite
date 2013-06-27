# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#

#
# spec file for package suse-cert (Version 0.8.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#



Name:           qa_test_suse-cert
BuildRequires:  gcc-c++ hwinfo-devel
Summary:        SLES9/SLES10 Certification tests
Version:        0.8.1
Release:        184
Provides:	suse-cert
Obsoletes:	suse-cert
Requires:       hwinfo-devel coreutils bonnie cdrecord mkisofs wget e2fsprogs util-linux build mgetty pure-ftpd python
Group:          Development/Tools/Other
License:        SUSE Proprietary
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         scripts.tar.bz2
Source1:        templates.tar.bz2
Source2:        sources.tar.bz2
Source3:        configs.tar.bz2
Source4:		suse-cert.tcf
Source5:		test_suse-cert-run
Source6:		ftpload.sh
Source7:	qa_test_suse-cert.8
Source8:	qa_test_suse-cert-config
Patch:          suse-cert-hwinfo.dif

%description
All tests and tools for SLES9/SLES10/SLED10 certifications are included
in this package. Those tests are meant to be run from the System Test
Kit via TestConsole.



Authors:
--------
    Klaus G. Wagner <kgw@suse.de>
    Thomas Siedentopf <tsieden@suse.de>
    Olli Ries <ories@suse.de>
    Gerald Bringhurst <gbringhurst@suse.de>

%prep
%setup -c suse-cert -a0 -a1 -a2 -a3 
%patch

%build
make -C src all

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:7} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
#fixme?
mkdir -p $RPM_BUILD_ROOT/usr/lib
mv bin/cert_tests.lib $RPM_BUILD_ROOT/usr/lib 
mkdir -p $RPM_BUILD_ROOT/usr/bin
# remove old CVS file
# get rid of these mvs asap!
mv bin/do_floppy_wrapper $RPM_BUILD_ROOT/usr/bin/do_floppy
mv bin/do_floppy $RPM_BUILD_ROOT/usr/bin/do_floppy_internal
mv bin/* $RPM_BUILD_ROOT/usr/bin 
mv src/eatmemry src/mkcertconf src/lssl src/lsnod $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/cert/templates
mkdir -p $RPM_BUILD_ROOT/usr/share/cert/configs
cp -a configs/* $RPM_BUILD_ROOT/usr/share/cert/configs
cp -a templates/* $RPM_BUILD_ROOT/usr/share/cert/templates
mkdir -p $RPM_BUILD_ROOT/var/opt/novell/NovellTestKits
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/bonnie/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
cp %{S:4} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
cp %{S:5} $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{S:6} $RPM_BUILD_ROOT/usr/share/qa/%name
cp %{S:8} $RPM_BUILD_ROOT/usr/share/qa/%name
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/suse-cert.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
/usr/share/man/man8/qa_test_suse-cert.8.gz
%dir /var/opt/novell/NovellTestKits
%dir /var/opt/novell
/usr/bin/*
%dir /usr/share/cert
%dir /usr/share/cert/templates
/usr/share/cert/templates/*
%dir /usr/share/cert/configs
/usr/share/cert/configs/*
/usr/lib/cert_tests.lib
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/suse-cert.tcf
/usr/share/qa/tools/test_suse-cert-run
/usr/share/qa/qa_test_suse-cert/ftpload.sh

%changelog
* Tue Oct 25 2011 - cachen@suse.com
- add configuration file
* Mon Nov 8 2010 - aguo@novell.com
- add suse-cert.tcf test_suse-cert-run and ftpload.sh so suse-cert can be implemented by ctcs2
* Tue Aug 3 2010 - yxu@novell.com  
- removed -f option of hostname command in cert_tests.lib file   
* Wed Mar 12 2008 yxu@suse.de
- renamed eatmem to eatmemry to resolve conflict with the eatmem file in the package tiobench
- submited this package to all distros
* Tue Jan 31 2006 ro@suse.de
- try to adapt to current hwinfo
* Thu Jan 26 2006 ro@suse.de
- converted nfb to buildreq
* Tue Dec 06 2005 gbringhurst@suse.de
-  Fixed buildcrunch to continually build packages for the set time
  for the test. (e.g. 24 hours for the full server, 8 hours for reduced)
  the fix is documented in "start_get_ps" in buildcrunch.
  also fixed MYTMPDIR variable in function check_mount to ${MYTMPDIR}
* Tue Nov 15 2005 gbringhurst@suse.de
- fixed buildcrunch, to catch bad fs4 mounts.  Wil verify
  if a valid mount can be done and do a preliminary check
  for packages.  This will allow a quick FAIL if no valid mount
  point can be made. geb
* Mon Oct 24 2005 gbringhurst@suse.de
- Reverting back to suse-cert v0.8, same as version that
  shipped with SCK v4.2.6.   v0.9 still has issues with
  cpustress and not terminating with a BAD IP for fs4.
  There is also a problem with the time that the bonnie
  test runs (should be 3.5 hours).   One test ran 13 hours
  and another ran 34 hours(one was a i386 box the other was
  a x86_64).   We will be using version 0.8.0 of qa_test_suse-cert
  for this kit.  The only issue we had with the 0.8 kit was
  with cpustress reporting FALSE positive.   This will be handled
  via 'doc' and a shipping script which will validate the mount point.
* Fri Oct 21 2005 gbringhurst@novell.com
- submitting version 9.0.1 of suse-cert.  This has fixes for
  false positive results on 'buildcrunch' for CPUSTRESS.
* Tue Oct 18 2005 gbringhurst@suse.de
- reference back to a previous kit, had to make sure that
- this was suse-cert that was used in the 4.2.6 kit.
-- updated to version 5.0
-  * validation of kit for autobuild.
* Wed Oct 12 2005 gbringhurst@suse.de
- updated to version 5.0
  * validation of kit for autobuild.
* Tue Mar 08 2005 ories@suse.de
- added fixes for
  * 70900 (race between buildcrunch & get_ps)
  * 71225 (OES CD set layout changed => configure_fs4 offset handling needs adjustment)
* Fri Feb 04 2005 ories@suse.de
- one more NLD related bugfix
* Thu Feb 03 2005 ories@suse.de
- fix nld core cd set array assignment
* Tue Feb 01 2005 ories@suse.de
- fix typo in configure_fs4 (#50262)
* Mon Jan 24 2005 ories@suse.de
- mkcertconf: ppc64: type fix (char -> unsigned char) (#49992, #50001)
- do_cdrec: added cdrecord's -dao option for DVD tests (#49743)
- removed obsolete testcrunch script, verified with all .def files
* Mon Jan 17 2005 ories@suse.de
- added new log file layout to do_bonnie
- kgw added media detection to do_cdrom
* Mon Jan 10 2005 ories@suse.de
- testcrunch:
  Added (sort of a) race detector to sigchldhandler()
  Array $sdirs[] now simply traversed by means of index $total
  Cleaned up code for initial build launches a bit.
  Updated obsolete contents of $testcrunchinfo
- do_bonnie:
  Some code cleanup in: functions autodetect_eatmem,
  autodetect_ramdisk, adjust_values
  Fixed: log bug in fct. adjust_values
  Added: needed preliminary definition of tidy_up()
  Added: some cosmetics (more log messages, comments,...)
- some cleanup in various log templates
* Sat Dec 04 2004 ories@suse.de
- provide symlink /media/tc/raid1 -> $WORKDIR to make the RAID test more
  convenient for RAID only systems
* Thu Nov 25 2004 ories@suse.de
- bugfix: configure ppp connection on FS4 as well
- bugfix: do cdrec image fillup in correct directory
* Tue Sep 28 2004 ories@suse.de
- fixed broken directory layout
* Wed Sep 22 2004 ories@suse.de
- improved bonnie wrapper - less math thus better scaling
- eatmem does not print messages anymore
- moved config file to certify_sys.conf
- added parted output, email notification, get_ps
- more sanity checks
* Fri Sep 17 2004 ories@suse.de
- removed compiled binaries
* Fri Sep 17 2004 ories@suse.de
- install missing eatmem
* Fri Sep 17 2004 ories@suse.de
- dropped ramdisk for bonnie #43303
- various bugfixes
* Mon Sep 06 2004 ories@suse.de
- fixes for #44274, #44548, #44589 (still disabled), #44712, #44713
- provides build- & testcrunch (hack for b3)
- configure_pkg/sut starts tclink, cleanup in do_cdrec, fixed
  typos in ftpload
- don't start pppd per default
- testcrunch traps sigterm
* Mon Aug 30 2004 ories@suse.de
- fixes for #44399, #44404, #44406
- ftpload starts pppd when serial option is set
- activated hwinfo in configure_sut
- misc
* Fri Aug 27 2004 ories@suse.de
- added configure scripts for FS4 & SUT
- removed obsolete do_all_* tests
* Mon Aug 23 2004 ories@suse.de
- initial version

