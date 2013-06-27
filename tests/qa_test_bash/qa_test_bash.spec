#
# spec file for package qa_bash (Version 0.1)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_bash
BuildRequires:  ctcs2 gcc-c++
License:        SUSE Proprietary
Group:          SUSE internal
AutoReqProv:    on
Version:        0.1
Release:        41
Summary:        RD-QA internal package
Source0:        %name-%version.tar.bz2
Source1:        qa_bash.tcf
Source2:        test_bash-run	
Source3:	qa_test_bash.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	qa_bash
Obsoletes:	qa_bash
Requires:       bash diffutils ctcs2

%description
Test of Bash

%prep
rm -rvf $RPM_BUILD_DIR/%{name}-%{version}
tar -xjvf %SOURCE0 -C $RPM_BUILD_DIR

%build
gcc $RPM_BUILD_DIR/%name/data/zecho.c -o $RPM_BUILD_DIR/%name/data/zecho
gcc $RPM_BUILD_DIR/%name/data/recho.c -o $RPM_BUILD_DIR/%name/data/recho
gcc $RPM_BUILD_DIR/%name/data/printenv.c -o $RPM_BUILD_DIR/%name/data/printenv

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
ln -s ../%name/tcf/qa_bash.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cd $RPM_BUILD_DIR
cp -rv %{name} $RPM_BUILD_ROOT/usr/share/qa/

%clean
%{__rm} -rvf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_bash.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_bash -> qa_test_bash
* Tue May 13 2008 mmrazik@suse.cz
- removed x86_64 binaries from the packages (recho et al)
* Mon Feb 18 2008 cihlarov@suse.cz
- added binaries for test, removed from noarch
* Tue Jan 29 2008 cihlarov@suse.cz
- clean build
* Thu Jan 17 2008 cihlarov@suse.cz
- path fixes
* Thu Jan 17 2008 cihlarov@suse.cz
- initial submit
