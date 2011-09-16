#
# spec file for package qa_tomboy (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:           qa_test_tomboy
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Simple tomboy tests for ctcs framework
Provides:	qa_tomboy
Obsoletes:	qa_tomboy
Requires:       strongwind ctcs2
Version:        0.1
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_tomboy.tcf
Source2:        test_tomboy-run
Source3:	qa_test_tomboy.8
Source4:	test_local_tomboy-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Test cases for tomboy package.

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_tomboy.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_tomboy.8.gz
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
* Fri Aug 12 2011 - llipavsky@suse.cz
- Package rename: qa_tomboy -> qa_test_tomboy
* Wed Nov 17 2010 - cachen@novell.com
- package created, version 0.1
