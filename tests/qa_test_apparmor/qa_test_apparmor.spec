#!BuildIgnore: post-build-checks

# spec file for package qa_apparmor (Version 1325)
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
Name:           qa_test_apparmor
BuildRequires:  apparmor-parser bzip2 gcc libapparmor-devel swig flex bison automake autoconf libtool
Version:        1326
Release:        3
License:        GPL v2
Group:          System/Packages
AutoReqProv:    on
Source0:        tests.tar.bz2
Source1:        qa_apparmor.tcf
Source2:        test_apparmor-run
Source3:        qa_test_apparmor.8
Source4:        test_apparmor-run
Source5:        subdomain-wrapper.sh
Patch0:         qa_apparmor-build_issue_on_sles12
Patch1:         exec_ptrace_regex.patch
Url:            http://www.novell.com/products/apparmor/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        apparmor tests
#BuildArchitectures: noarch
Provides:	qa_apparmor
Obsoletes:	qa_apparmor
Requires:       apparmor-parser apparmor-profiles libapparmor perl bison swig flex ruby
Requires:       qa_lib_ctcs2  


%description
This package contains different types of tests:
- regression tests for apparmor_parser
- regression tests for the kernel module


%prep
%setup -n tests 
%define qa_location /usr/share/qa/qa_test_apparmor
%patch0 -p1
%patch1 -p1


%build
make -C regression/apparmor all
make -C stress/subdomain all


%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tests
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/parser
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/doc/parser
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/doc/apparmor
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/bin/parser
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/bin/profiles
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/bin/subdomain
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/%{qa_location}/
#copy the helper script
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools
#copy  tests
find regression/apparmor/ -maxdepth 2 \( -perm /+x -o -name '*.sh' -o -name '*.inc' \) -exec cp '{}' $RPM_BUILD_ROOT%{qa_location}/tests/ \;
#copy  documentation
cp regression/apparmor/README regression/apparmor/AppArmor.rtf $RPM_BUILD_ROOT%{qa_location}/doc/apparmor
#copy parser documentation 
cp parser/README $RPM_BUILD_ROOT%{qa_location}/doc/parser
#copy parser tests
cp parser/Makefile parser/tst/uservars.conf parser/tst/simple.pl $RPM_BUILD_ROOT%{qa_location}/bin/parser

#
#copy tcf files
cp %{SOURCE1} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../qa_test_apparmor/tcf/qa_apparmor.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_apparmor.tcf
#add subdomain tests
echo "#Subdomain regression tests" >> $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_apparmor.tcf
for test in `make -n -p -C regression/apparmor/ | grep '^TESTS' | cut -d'=' -f 2`; do
	echo "timer 600"
	TEST=`echo $test | tr [a-z] [A-Z]`
	echo "fg 1 ${TEST} /usr/share/qa/qa_test_apparmor/subdomain-wrapper.sh ${test}.sh"
	echo "wait"
	echo
done >> $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_apparmor.tcf
#add parser test
echo "#Parser regression tests" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo "timer 600" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo "fg 1 PARSER_REGRESSION /usr/bin/prove -v /usr/share/qa/qa_test_apparmor/parser/tst/simple.pl" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo "wait" >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
echo >> $RPM_BUILD_ROOT/%{qa_location}/tcf/qa_apparmor.tcf
#add stress test
#
#%define ltp_tcp_cmds_tcf /usr/share/qa/qa_test_ltp/tcf/.tcf
#%define ltp_commands_tcf /usr/share/qa/qa_test_ltp/tcf/comtcp_cmdsmands.tcf


%clean
rm -rvf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_apparmor.8.gz
/usr/share/qa
/usr/share/qa/tcf/qa_apparmor.tcf
#/usr/share/qa/tools/
%exclude %{qa_location}/tcf/qa_apparmor_*.tcf
%exclude /usr/share/qa/tcf/qa_apparmor_*.tcf
%exclude %{qa_location}/bin/profiles
%exclude /usr/share/qa/tools/test_apparmor-profiles-run


%changelog
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_apparmor -> qa_test_apparmor
