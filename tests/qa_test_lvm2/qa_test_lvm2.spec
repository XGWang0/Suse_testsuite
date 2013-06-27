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
BuildRequires:  ctcs2
License:        GPL v2
Group:          SuSE internal
Summary:        lvm2 regression tests for ctcs framework
Provides:	qa_lvm2
Obsoletes:	qa_lvm2
Requires:       lvm2 ctcs2 grep
Version:        0.1
Release:        1
Source0:        %{name}-%{version}.tar.bz2
Source1:	qa_lvm2.tcf
Source2:        test_lvm2-run
Source3:	qa_test_lvm2.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Regression tests for Logical Volume Manager

Authors:
--------
    Dinar Valeev <dvaleev@novell.com>

%prep
%setup -q -n %{name}

%build
pushd $RPM_BUILD_DIR/%{name}/lib
cc harness.c -o harness
cc not.c -o not
ln -s not should  
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
ln -s ../%name/tcf/qa_lvm2.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_lvm2.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_lvm2-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_lvm2.tcf

%changelog
