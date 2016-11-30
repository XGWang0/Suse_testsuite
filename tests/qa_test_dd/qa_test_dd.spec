#
# spec file for package qa_test_dd
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


Name:           qa_test_dd
Version:        0.1
Release:        0
Summary:        dd performance test
License:        GPL-2.0+
Group:          System/Benchmark
Url:            http://qa.suse.de/
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_dd.tcf
Source2:        test_dd-run
Source3:        qa_test_dd.8
Requires:       ctcs2
Provides:       qa_dd
Obsoletes:      qa_dd
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This is a I/O performance test package.

%prep
%setup -q -n %{name}

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 755 %{SOURCE2} %{buildroot}%{_datadir}/qa/tools
install -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
cp -a * %{buildroot}%{_datadir}/qa/%{name}
ln -s ../%{name}/tcf/qa_dd.tcf %{buildroot}%{_datadir}/qa/tcf/
find  %{buildroot}%{_datadir}/qa/%{name} -type f ! -name "COPYING" | xargs chmod +x

%files
%defattr(-,root,root)
%{_datadir}/qa
%{_datadir}/qa/%{name}
%{_datadir}/qa/tcf/qa_dd.tcf
%{_datadir}/qa/tools/test_dd-run
%{_mandir}/man8/*

%changelog
