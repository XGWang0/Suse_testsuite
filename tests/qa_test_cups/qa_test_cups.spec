#
# spec file for package qa_test_cups
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           qa_test_cups
Release:        0
Summary:        CUPS automated testsuite
License:        GPL v2; LGPL v2
Group:          SuSE internal
Source1:        test_cups-run
Source2:        qa_test_cups.8
BuildRequires:  ctcs2
BuildRequires:  cups-devel
Requires:       ctcs2
Requires:       cups
Provides:       qa_cups
Obsoletes:      qa_cups
%if 0%{?suse_version} >= 1315
Version:        1.7.5
Source0:        %{name}-%{version}.tgz
BuildArch:	x86_64
%else
Version:        1.0
Source0:        %{name}-%{version}-sle11.tar.bz2
BuildArch:      noarch 
Requires:       cups-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
CUPS automated testsuite
Includes:
IPP compiance tests
Command tests

%prep
%setup -q -n %{name}

%build
make %{?_smp_mflags}

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 755 -d %{buildroot}%{_docdir}/%{name}
ln -s ../%{name}/tcf/qa_cups.tcf %{buildroot}%{_datadir}/qa/tcf/
install -m 755 %{SOURCE1} %{buildroot}%{_datadir}/qa/tools

%if 0%{?suse_version} >= 1315
make install DESTDIR=%{buildroot}%{_datadir}/qa/%{name}

%else cp -a * %{buildroot}%{_datadir}/qa/%{name}
%endif

%files
%defattr(-, root, root)
%{_mandir}/man8/qa_test_cups.8.gz
%dir %{_datadir}/qa
%{_datadir}/qa/%{name}
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_cups-run
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/qa_cups.tcf

%changelog
