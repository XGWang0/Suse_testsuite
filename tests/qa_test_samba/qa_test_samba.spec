#
# spec file for package qa_samba (Version 0.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_samba
License:        GPL v2 or later
Group:          SuSE internal
Summary:        (rd-)qa internal package for testing samba
Provides:	qa_samba
Obsoletes:	qa_samba
Requires:       samba samba-client samba-winbind ctcs2 expect libqainternal
BuildRequires:  gcc make
AutoReqProv:    on
Version:        0.2.4
Release:        146
Source0:        %name-%version.tar.bz2
Source1:        qa_samba.tcf
Source2:        README
Source3:        test_samba-run
Source4:	qa_test_samba.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Test cases for samba packages (implemented so far): - start daemon
   and check that it started

- stop daemon and check that it stopped

- verify pidfile handling

- create user

- delete user

- test smbcontrol

- show shares

- file access (linux to linux only)

- file access with ACL (linux to linux only)



Authors:
--------
    Lukas Lipavsky <llipavsky@suse.cz>

%prep
%setup -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:2} $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}
install -m 755 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_samba.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name .svn -exec rm -rf {} \;
( cd $RPM_BUILD_ROOT/usr/share/qa/%name/src/file-access/ && make install )
( cd $RPM_BUILD_ROOT/usr/share/qa/%name/src/file-access-acl/ && make install )
rm -fr $RPM_BUILD_ROOT/usr/share/qa/%name/src

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_samba.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/qa_samba.tcf
/usr/share/qa/tools/test_samba-run
%config /usr/share/qa/%name/config
%{_docdir}/%{name}
%doc %{_docdir}/%{name}/README

%changelog
* Wed Aug 10 09:35:02 GMT 2011 - llipavsky@suse.cz
- Package rename: qa_samba -> qa_test_samba
* Tue Jan 22 2008 llipavsky@suse.cz
- Unify versions for sles9-all, sles10-all and stable-all
* Tue Jul 24 2007 llipavsky@suse.cz
- changed to alder format suitable for sles9
* Wed Jan 17 2007 llipavsky@suse.cz
- fixed some minor bugs (ADMIN$ share, group handling, etc)
* Mon Nov 06 2006 llipavsky@suse.cz
- Increased timeout for long test, fixed test interruption before
  they are completed
* Fri Nov 03 2006 lukas@suse.cz
- fixed permissions problem that prevented successful build
* Wed Nov 01 2006 llipavsky@suse.cz
- fixed building problem which caused file-access tests to fail
* Mon Aug 21 2006 llipavsky@suse.cz
- added file access (with and without acl) tests
* Wed Jul 12 2006 llipavsky@suse.cz
- fixed to comply QA Packaging Guidelines
* Mon Jul 10 2006 llipavsky@suse.cz
- initial release
