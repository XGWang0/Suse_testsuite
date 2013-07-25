#
# spec file for package qa_findutils (Version 0.1)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_findutils
BuildRequires:  findutils findutils-locate
License:        GPL v2 or later
Group:          SuSE internal
Summary:        Findutils tests for ctcs framework
Provides:	qa_findutils
Obsoletes:	qa_findutils
Requires:       findutils-locate findutils dejagnu coreutils ctcs2 grep diffutils mktemp
Version:        0.1
Release:        15
Source0:        %name-%version.tar.bz2
Source1:        qa_findutils.tcf
Source2:        test_findutils-run
Source3:	qa_test_findutils.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for findutils package.
* test find
* test xargs

%prep
%setup -q -n %{name}

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../%name/tcf/qa_findutils.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;
find $RPM_BUILD_ROOT/usr/share/qa/%name -type d -o -type f -a ! -name "*.tcf" | xargs chmod +x
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_findutils.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/
/usr/share/qa/tools/
#/usr/share/qa/tcf/qa_findutils.tcf
#/usr/share/qa/tools/test_findutils-run


%changelog -n qa_test_findutils
* Tue Aug 08 2006 - jdluhos@suse.cz
- Added three tests from the original test suite; one of them
  (locate) does not work yet as it needs a special utility
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 19 2006 - kmachalkova@suse.cz
- fixed relative/absolute path issue in run-script
* Wed Jan 18 2006 - mmrazik@suse.cz
- fixed tcf location (updated Packaging Guidelines)
- fixed run-script location (updated Packaging Guidelines)
* Tue Jan 17 2006 - kmachalkova@suse.cz
- added support for ctcs2 (tcf file,...)
- additional tests for some other 'find' and 'xargs' switches
* Thu Aug 18 2005 - kmachalkova@suse.cz
- package created, version 1.1
