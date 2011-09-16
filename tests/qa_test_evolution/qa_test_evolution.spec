#
# spec file for package qa_evolution (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/

Name:           qa_test_evolution
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Simple evolution tests for ctcs framework
Provides:	qa_evolution
Obsoletes:	qa_evolution
Requires:       strongwind ctcs2
Version:        0.1
Release:        1
Source0:        %name-%version.tar.bz2
Source1:        qa_evolution.tcf
Source2:        test_evolution-run
Source3:	qa_test_evolution.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Test cases for evolution package. Initailly only have a test demo

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
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name
ln -s ../%name/tcf/qa_evolution.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_evolution.8.gz
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
* Fri Aug 12 2011 - llipavsky@suse.cz
- Package rename: qa_evolution -> qa_test_evolution
* Fri Jul 2 2010 - llwang@novell.com
- package created, version 0.1
