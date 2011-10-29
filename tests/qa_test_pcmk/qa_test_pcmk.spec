#
# spec file for package qa_pcmk (Version 0.1)
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           qa_test_pcmk
BuildRequires:  ctcs2
License:	GPL v2.1 or later
Group:          SuSE internal
Summary:	Pacemaker internal test suite
Provides:	qa_pcmk
Obsoletes:	qa_pcmk
Requires:	pacemaker
Version:	1.0
Release:	1
Source0:	%name-%version.tar.bz2
Source1:	test_pcmk-run
Source2:        qa_test_pcmk.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch

%description
Pacemaker internal testsuite.

Uses crm_simulate to emulate different scenarios

Authors:
--------
    Dinar Valeev <dvaleev@novell.com>

%prep
%setup -q -n %name

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%name/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools

ln -s ../%name/tcf/qa_pcmk.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools

cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_pcmk.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%name
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_pcmk-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_pcmk.tcf

%changelog


