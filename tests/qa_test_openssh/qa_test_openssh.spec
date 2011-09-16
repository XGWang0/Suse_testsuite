#
# spec file for package qa_openssh (Version 0.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_openssh
License:        BSD 3-Clause; X11/MIT
Group:          SuSE internal
Provides:	qa_openssh
Obsoletes:	qa_openssh
Requires:       mktemp ctcs2 
Version:        0.2
Release:        1
Summary:        (rd-)qa internal package for openssh testing
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_openssh.tcf
Source2:        test_openssh-run
Source3:	qa_test_openssh.8
BuildRoot:      %{_tmppath}/%{name}-build
BuildArch:      noarch

%description
Openssh testsuite. Many functional tests are included.



Authors:
--------
    Cyril Hrubis chrubis@suse.cz

%prep
%setup -n qa_test_openssh

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/${name}
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d -v $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 644 %{S:1} -v $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 %{S:2} -v $RPM_BUILD_ROOT/usr/share/qa/tools
cp -v * $RPM_BUILD_ROOT/usr/share/qa/%{name}/
ln -s ../%{name}/tcf/qa_openssh.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
%{__rm} -rvf $RPM_BUILD_ROOT/usr/share/qa/%{name}/

%files
%defattr(-,root,root)
/usr/share/man/man8/qa_test_openssh.8.gz
/usr/share/qa
/usr/share/qa/%{name}
/usr/share/qa/%{name}/tcf/qa_openssh.tcf
/usr/share/qa/tcf/qa_openssh.tcf
/usr/share/qa/tools/test_openssh-run

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_openssh -> qa_test_openssh
* Wed Jan 02 2008 - mmrazik@suse.cz
- calling "ssh -n" by default to allow integration with ctcs2
- minor spec file cleanup
- upgraded the testsuite to openssh 4.7p1 version
* Mon Aug 13 2007 - jbrunclik@suse.cz
- fixed some of the tests
* Mon Feb 05 2007 - ro@suse.de
- added qa_dummy to buildreq
* Mon Feb 05 2007 - chrubis@suse.cz
- Initial version
