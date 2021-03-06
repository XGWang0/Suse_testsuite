#
# spec file for package qa_indent (Version 2.2.9)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_indent
License:        Copyright mention
Group:          SuSE internal
Summary:        Simple indent tests for ctcs framework
Provides:	qa_indent
Obsoletes:	qa_indent
Requires:       indent coreutils diffutils ctcs2
Version:        2.2.9
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_indent.tcf
Source2:        test_indent-run
Source3:	qa_test_indent.8
Patch0:         %name-%version-exitcode.diff
Patch1:         %name-%version-add_blankline.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for indent package. Tests different indentations of source text.

%prep
%setup -q -n %{name}
%patch0
%patch1

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
ln -s ../%name/tcf/qa_indent.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
find $RPM_BUILD_ROOT/usr/share/qa/%name -depth -type d -name CVS -exec rm -rf {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_indent.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tcf/
/usr/share/qa/tools
%attr(0755,root,root) /usr/share/qa/%name/*.sh
%attr(0755,root,root) /usr/share/qa/%name/regression/TEST
%attr(0755,root,root) /usr/share/qa/%name/regression/TIME

%changelog -n qa_test_indent
* Tue Jul 25 2006 - mmrazik@suse.cz
- testsuite from upstream added
* Fri Jan 27 2006 - kmachalkova@suse.cz
- added ctcs2 support (tcf file, run script)
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 20 2006 - kmachalkova@suse.cz
- package created, version 0.1


