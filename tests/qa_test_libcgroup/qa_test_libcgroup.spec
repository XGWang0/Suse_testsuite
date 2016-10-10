#
# spec file for package qa_test_libcgroup
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


Name:           qa_test_libcgroup
Version:        1.0
Release:        0
Summary:        libcgroup automated testsuite
License:        GPL-2.0+
Group:          SUSE internal
Source0:        %{name}-%{version}.tar.bz2
Source2:        libcgroup-run
BuildRequires:  ctcs2
Requires:       gcc-c++
Requires:       libcgroup-devel
Obsoletes:      qa_libcgroup
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
libcgroup automated testsuite
Includes:
libcgroup upstream tests

%prep
%setup -q -n %{name}

%build

%install
install -m 755 -p -d %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 755 -p -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -p -d %{buildroot}%{_datadir}/qa/tools
install -m 755 -p -d %{buildroot}%{_docdir}/%{name}

ln -s ../%{name}/tcf/qa_test_libcgroup.tcf %{buildroot}%{_datadir}/qa/tcf/
install -m 755 %{SOURCE2} %{buildroot}%{_datadir}/qa/tools
cp -a * %{buildroot}%{_datadir}/qa/%{name}

%files
%defattr(-, root, root)
%dir %{_datadir}/qa
%{_datadir}/qa/%{name}
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/libcgroup-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_test_libcgroup.tcf
%attr(0755,root,root) %{_datadir}/qa/%{name}/common-test.sh
%attr(0755,root,root) %{_datadir}/qa/%{name}/src/config.status
%attr(0755,root,root) %{_datadir}/qa/%{name}/src/*.sh

%changelog
