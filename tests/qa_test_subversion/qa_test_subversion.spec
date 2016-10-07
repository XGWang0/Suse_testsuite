#
# spec file for package qa_test_subversion
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           qa_test_subversion
Version:        0.1.2
Release:        0
Summary:        Simple subversion tests for ctcs framework
License:        SUSE Proprietary
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          SuSE internal
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_subversion.tcf
Source2:        test_subversion-run
Source3:        qa_test_subversion.8
BuildRequires:  ctcs2
Requires:       apache2
Requires:       ctcs2
Requires:       grep
Requires:       subversion
Requires:       subversion-server
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%if 0%{?suse_version} >= 1100
Requires:       vim-base
%else
Requires:       vim
%endif

%description
Test cases for subversion

%prep
%setup -q -n %{name}

%build

%install
# TODO: make this work from the makefile
install -m 755 -d %{buildroot}%{_mandir}/man8/
install -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/qa/%{name}/tcf
ln -s ../%{name}/tcf/qa_subversion.tcf %{buildroot}%{_datadir}/qa/tcf/
install -m 755 %{SOURCE2} %{buildroot}%{_datadir}/qa/tools
cp -a * %{buildroot}%{_datadir}/qa/%{name}
chmod 755 %{buildroot}%{_datadir}/qa/%{name}/svn.sh
find %{buildroot}%{_datadir}/qa/%{name} -depth -type d \( -name CVS -or\
 -name .svn \) -exec rm -rf {} \;

%files
%defattr(-, root, root)
%dir %{_datadir}/qa
%{_datadir}/qa/%{name}
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_subversion-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_subversion.tcf
%{_mandir}/man8/qa_test_subversion.8%{ext_man}
%doc LICENSE

%changelog
%changelog
