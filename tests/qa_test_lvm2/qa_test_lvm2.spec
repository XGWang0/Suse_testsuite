#
# spec file for package qa_lvm (Version 0.1)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_lvm2
License:        GPL v2
Group:          SuSE internal
Summary:        lvm2 regression tests for ctcs framework
Provides:	qa_lvm2
Obsoletes:	qa_lvm2
Requires:       lvm2 ctcs2 grep git
Version:        0.1
Release:        2
Source0:        %{name}-%{version}.tar.bz2
Source1:	qa_lvm2.tcf
Source2:        test_lvm2-run
Source3:	qa_test_lvm2.8
Source4:	test_lvm2_2_02_98-run
Source5:	test_lvm2_source-run
Source6:	qa_test_lvm2_shell.tar.bz2
Source7:        qa_test_lvm2_2_02_120.tar.bz2
Source8:        qa_lvm2_2_02_120.tcf
Source9:        test_lvm2_2_02_120-run
Patch1:		dmeventd_lvmetad_test.path
Patch2:         lvchange-raid_none_writemostly.path
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Regression tests for Logical Volume Manager

Authors:
--------
    Dinar Valeev <dvaleev@novell.com>

%prep
%define qa_location /usr/share/qa/%{name}
%setup -n %{name} -a6 -q
%patch1 -p0
%patch2 -p0
# For lvm2-2.02.120 or later
%setup -c -n "%{name}_2_02_120" -a7 -T -q

%build
pushd $RPM_BUILD_DIR/%{name}/lib
cc harness.c -o harness
cc not.c -o not
chmod +x *
ln -s not should  
rm *.c
popd
# For lvm2-2.02.120 or later
pushd $RPM_BUILD_DIR/%{name}_2_02_120/qa_test_lvm2/test/lib
cc %{optflags} -o harness harness.c
cc %{optflags} -o not not.c
ln -s not should
ln -s not fail
ln -s not invalid
test -f /sbin/dmeventd && ln -s /sbin/dmeventd dmeventd
test -f /etc/lvm/profile/thin-performance.profile && ln -s /etc/lvm/profile/thin-performance.profile thin-performance.profile
rm *.c
popd

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/%{name}
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
cd $RPM_BUILD_DIR/%{name}
ln -s ../%name/tcf/qa_lvm2.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:5} $RPM_BUILD_ROOT/usr/share/qa/tools
install -d $RPM_BUILD_ROOT/usr/share/qa/%name
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
mv $RPM_BUILD_ROOT/usr/share/qa/%name/qa_test_lvm2-2_02_98 $RPM_BUILD_ROOT/usr/share/qa/qa_test_lvm2_shell

cd $RPM_BUILD_ROOT/usr/share/qa/qa_test_lvm2_shell/test/lib
cc harness.c -o harness
cc not.c -o not
chmod +x *
ln -s not should
# For lvm2-2.02.120 or later
cp -ar $RPM_BUILD_DIR/%{name}_2_02_120/qa_test_lvm2 $RPM_BUILD_ROOT/usr/share/qa/%{name}_2_02_120
install -m 644 %{S:8} $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:9} $RPM_BUILD_ROOT/usr/share/qa/tools/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_lvm2.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%{_datadir}/qa/qa_test_lvm2_shell
%{_datadir}/qa/%{name}_2_02_120
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_lvm2-run
%{_datadir}/qa/tools/test_lvm2_2_02_98-run
%{_datadir}/qa/tools/test_lvm2_source-run
%{_datadir}/qa/tools/test_lvm2_2_02_120-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_lvm2.tcf
%{_datadir}/qa/tcf/qa_lvm2_2_02_120.tcf
%attr(0755,root,root) /usr/share/qa/%name/*.sh


%changelog
* Tue Sep 08 2015 - jtzhao@suse.com
- Upgrade qa_test_lvm2 using upstream tests(lvm2-2.02.120)
- Add new lvm2 tests to test list of SLE 12 SP1
