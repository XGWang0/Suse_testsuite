#
# spec file for package qa_openssh_fips (Version 0.1)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_openssh_fips
License:        BSD
Group:          SuSE internal
Provides:	qa_openssh_fips
Obsoletes:	qa_openssh_fips
Requires:       mktemp ctcs2 
Version:        0.2
Release:        1
Summary:        (rd-)qa internal package for openssh testing
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_openssh_fips.tcf
Source2:        test_openssh_fips-run
Source3:	qa_test_openssh_fips.8
Patch1:         fips-patchset.patch
BuildRoot:      %{_tmppath}/%{name}-build
BuildArch:      noarch

%description
Openssh testsuite. Many functional tests are included.



Authors:
--------
    Cyril Hrubis chrubis@suse.cz

%prep
%setup -n qa_test_openssh_fips
%patch1 -p4

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
ln -s ../%{name}/tcf/qa_openssh_fips.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
%{__rm} -rvf $RPM_BUILD_ROOT/usr/share/qa/%{name}/

%files
%defattr(-,root,root)
/usr/share/man/man8/qa_test_openssh_fips.8.gz
/usr/share/qa
/usr/share/qa/%{name}
/usr/share/qa/%{name}/tcf/qa_openssh_fips.tcf
/usr/share/qa/tcf/qa_openssh_fips.tcf
/usr/share/qa/tools/test_openssh_fips-run
%attr(0755,root,root) /usr/share/qa/%name/prepare.sh
%attr(0755,root,root) /usr/share/qa/%name/runtests.sh
%attr(0755,root,root) /usr/share/qa/%name/scp-ssh-wrapper.sh
%attr(0755,root,root) /usr/share/qa/%name/sshd-log-wrapper.sh

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_openssh_fips -> qa_test_openssh_fips
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
