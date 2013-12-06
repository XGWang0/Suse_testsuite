#
# spec file for package qa_sw_multipath (Version 0.1)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:		qa_test_glibc
License:	GPL v2 or later
Group:		SuSE internal
Summary:	glibc testsuite
Requires:	glibc, gmp, ctcs2
BuildRequires:  gmp-devel
Version:	1.0
Release:	1
%if 0%{?suse_version} == 1010
Source0:	glibc_testsuite-2.4.tar.gz
%endif
%if 0%{?suse_version} == 1110
Source0:	glibc_testsuite-2.11.tar.gz
%endif
Source2:	test_glibc-run
Patch1:         glibc_testsuite-partial-fix-1.patch
Patch2:         tst-leaks2-large-hosts-file-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
glibc testsuite
ripped out from the glibc sources

%prep
%setup -q -n glibc_testsuite
%patch1 -p1
%patch2 -p1

%build
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/%{name}
install -D -m 755 testfiles/gettext-data.mo.de_DE.ISO-8859-1 $RPM_BUILD_ROOT/usr/share/locale/de_DE.ISO-8859-1/LC_MESSAGES/gettext-data.mo
install -D -m 755 testfiles/gettext-data.mo.fr_FR.ISO-8859-1 $RPM_BUILD_ROOT/usr/share/locale/fr_FR.ISO-8859-1/LC_MESSAGES/gettext-data.mo
install -D -m 755 testfiles/tst-gettext-de.mo.de_DE.UTF-8 $RPM_BUILD_ROOT/usr/share/locale/de_DE.UTF-8/LC_MESSAGES/tst-gettext-de.mo
install -D -m 755 testfiles/tst-gettext-de.mo.de_DE.ISO-8859-1 $RPM_BUILD_ROOT/usr/share/locale/de_DE.ISO-8859-1/LC_MESSAGES/tst-gettext-de.mo


#ln -s ../%name/tcf/%name.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a bin $RPM_BUILD_ROOT/usr/share/qa/%name/
cp -a testfiles $RPM_BUILD_ROOT/usr/share/qa/%name/
cp -a tcf $RPM_BUILD_ROOT/usr/share/qa/%name/
ln -s ../%{name}/tcf/%{name}.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_glibc-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_test_glibc.tcf
%dir %{_datadir}/locale/fr_FR.ISO-8859-1
%dir %{_datadir}/locale/de_DE.UTF-8
%dir %{_datadir}/locale/de_DE.ISO-8859-1
%dir %{_datadir}/locale/fr_FR.ISO-8859-1/LC_MESSAGES
%{_datadir}/locale/fr_FR.ISO-8859-1/LC_MESSAGES/gettext-data.mo
%dir %{_datadir}/locale/de_DE.UTF-8/LC_MESSAGES
%{_datadir}/locale/de_DE.UTF-8/LC_MESSAGES/tst-gettext-de.mo
%dir %{_datadir}/locale/de_DE.ISO-8859-1/LC_MESSAGES
%{_datadir}/locale/de_DE.ISO-8859-1/LC_MESSAGES/tst-gettext-de.mo
%{_datadir}/locale/de_DE.ISO-8859-1/LC_MESSAGES/gettext-data.mo

%changelog
