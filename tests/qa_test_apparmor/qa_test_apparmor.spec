#
# spec file for package qa_apparmor (Version 1325)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           qa_test_apparmor
BuildRequires:  apparmor-parser bzip2 gcc libapparmor-devel ltp-ctcs2-glue qa_bind qa_postfix  libapparmor-devel
Version:        1325
Release:        3
License:        GPL v2
Group:          System/Packages
AutoReqProv:    on
Source0:        tests-%{version}.tar.bz2
#Source1:        regression-tests-6381.tar.bz2
Source3:        qa_apparmor.tcf
Source4:        subdomain-wrapper.sh
Source5:        test_apparmor-run
Source6:	qa_test_apparmor.8
Source7:        test_apparmor-profiles-run
Source8:        get_Apparmor_Tests
Patch0:         qa_apparmor-parser-path.patch
Patch2:         qa_apparmor-disable_ptrace_on_ppc.patch
Patch3:         qa_apparmor-clone.patch
Patch4:         qa_apparmor-disable_clone_on_ia64.patch
Patch5:         immunix.patch
Patch6:         qa_apparmor-linux-vdso.patch
Patch7: 		wrong-cflag-in_makefile.diff
Patch8:         qa_apparmor-mount-sh.patch
Patch9:         bug-804628.patch
Patch10:        qa_apparmor-build_issue_on_sles11sp1.patch 
#Patch6:         qa_apparmor-dirent.patch
Url:            http://www.novell.com/products/apparmor/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        apparmor tests
#BuildArchitectures: noarch
Provides:	qa_apparmor
Obsoletes:	qa_apparmor
Requires:       apparmor-parser apparmor-profiles libapparmor perl 
Requires:       qa_lib_ctcs2  

%description
This package contains different types of tests:

- regression tests for apparmor_parser

- regression tests for the kernel module



%package profiles
License:        Other uncritical OpenSource License
Provides:	qa_apparmor-profiles
Obsoletes:	qa_apparmor-profiles
Requires:       %{name} = %{version} qa_test_bind qa_test_ltp qa_test_postfix
Summary:        apparmor profile tests
Group:          System/Packages

%description profiles
This package contains tcf files for apparmor profile testing.

Currently the following profiles are tested: - postfix

- bind

- ldd

- tcp commands (ping, netstat, traceroute)



%prep
%setup -n tests
%define qa_location /usr/share/qa/qa_test_apparmor
%patch0 -p1
#this is soooo ugly :) the test should be fixed...
%ifarch ppc ppc64
%patch2 -p1
%endif
%patch3 -p1
%ifarch ia64
%patch4 -p1
%endif
%patch5
%patch6 -p1
%patch7 -p1
%patch8 -p5
%patch9 -p1
%patch10 -p1
%build
make -C regression/subdomain all
make -C stress/subdomain all

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:6} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/bin/subdomain
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/bin/parser
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/bin/stress
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/bin/profiles
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/doc/subdomain
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/doc/parser
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
#
#copy the helper script
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 0755 %{SOURCE7} $RPM_BUILD_ROOT/usr/share/qa/tools
#copy subdomain tests
find regression/subdomain/ -maxdepth 2 \( -perm /+x -o -name '*.sh' -o -name '*.inc' \) -exec cp '{}' $RPM_BUILD_ROOT%{qa_location}/bin/subdomain \;
#copy subdomain documentation
cp regression/subdomain/README regression/subdomain/AppArmor.rtf $RPM_BUILD_ROOT%{qa_location}/doc/subdomain
#copy subdomain test wrapper
install -m 0755 %{SOURCE4} $RPM_BUILD_ROOT/%{qa_location}/bin
#copy parser documentation 
cp parser/README $RPM_BUILD_ROOT%{qa_location}/doc/parser
#copy parser tests
cp parser/Makefile parser/simple.pl parser/uservars.conf $RPM_BUILD_ROOT%{qa_location}/bin/parser
cp -R parser/simple_tests/ $RPM_BUILD_ROOT%{qa_location}/bin/parser
#copy stress tests
cp -R stress/subdomain/ $RPM_BUILD_ROOT%{qa_location}/bin/stress
#
#copy tcf files
cp %{SOURCE3} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../qa_test_apparmor/tcf/qa_apparmor.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
#add subdomain tests
echo "#Subdomain regression tests" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
for test in `make -n -p -C regression/subdomain | grep '^TESTS' | cut -d'=' -f 2`; do
	echo "timer 600"
	TEST=`echo $test | tr [a-z] [A-Z]`
	echo "fg 1 ${TEST} /usr/share/qa/qa_test_apparmor/bin/subdomain-wrapper.sh ${test}.sh"
	echo "wait"
	echo
done >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
#add parser test
echo "#Parser regression tests" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo "timer 600" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo "fg 1 PARSER_REGRESSION /usr/bin/prove -v /usr/share/qa/qa_test_apparmor/bin/parser/simple.pl" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo "wait" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
#add stress test
#
%define ltp_tcp_cmds_tcf /usr/share/qa/qa_test_ltp/tcf/tcp_cmds.tcf
%define ltp_commands_tcf /usr/share/qa/qa_test_ltp/tcf/commands.tcf
ln -s ../qa_test_bind/tcf/qa_bind.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_apparmor-bind.tcf
ln -s ../../qa_test_bind/tcf/qa_bind.tcf $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-bind.tcf
ln -s ../qa_test_postfix/tcf/qa_postfix.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_apparmor-postfix.tcf
ln -s ../../qa_test_postfix/tcf/qa_postfix.tcf $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-postfix.tcf
#add ping and netstat tests from ltp
#this grep is stupid :(
echo "timer 600" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
grep ping01 %ltp_tcp_cmds_tcf >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
echo "wait" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
#
echo "timer 600" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
grep netstat01 %ltp_tcp_cmds_tcf >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
echo "wait" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
#
echo "timer 600" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
grep " ldd " %ltp_commands_tcf >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
echo "wait" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor-ltp.tcf
ln -s ../qa_test_apparmor/tcf/qa_apparmor-ltp.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_apparmor.8.gz
/usr/share/qa
/usr/share/qa/tcf/qa_apparmor.tcf
/usr/share/qa/qa_test_apparmor
/usr/share/qa/tools/
%exclude %{qa_location}/tcf/qa_apparmor-*.tcf
%exclude /usr/share/qa/tcf/qa_apparmor-*.tcf
%exclude %{qa_location}/bin/profiles
%exclude /usr/share/qa/tools/test_apparmor-profiles-run

%files profiles
%defattr(-, root, root)
%{qa_location}/tcf/qa_apparmor-*.tcf
%{qa_location}/bin/profiles
/usr/share/qa/tools/test_apparmor-profiles-run
/usr/share/qa/tcf/qa_apparmor-*.tcf
%exclude /usr/share/qa/tcf/qa_apparmor.tcf

%changelog
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_apparmor -> qa_test_apparmor
