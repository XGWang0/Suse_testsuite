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

Name:		qa_test_python
License:	GPL v2 or later
Group:		SuSE internal
Summary:	python testsuite
Version:	2.7.7
Release:	2
%if 0%{?suse_version} <= 1110
Source0:    testsuite-python2.6.tar.gz
%else
Source0:    testsuite-python2.7.tar.gz
%endif
Source2:	test_python-run
BuildArch:	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:	python >= 2.6, python-curses, python-gdbm, python-opengl, python-httplib2, python-openssl, ctcs2, python-devel

%description
python testsuite
ripped out from the python 2.6 (SLE11 SP2 GM) and python 2.7 (SLE12)sources

%prep
%if 0%{?suse_version} <= 1110
%setup -q -n testsuite-python2.6
%else
%setup -q -n testsuite-python2.7
%endif

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT%{_docdir}/%{name}

#ln -s ../%name/tcf/%name.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a Lib $RPM_BUILD_ROOT/usr/share/qa/%name/
cp -a tcf $RPM_BUILD_ROOT/usr/share/qa/%name/
ln -s ../%{name}/tcf/%{name}.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_python-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_test_python.tcf

%changelog
