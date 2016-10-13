#
# spec file for package qa_test_sharutils
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

%define qa_location %{_datadir}/qa/%{name}
Name:           qa_test_sharutils
Version:        4.6.2
Release:        0
Summary:        Simple sharutils test for ctcs framework
License:        GPL-2.0+
Group:          SUSE internal
Source0:        sharutils-%{version}.tar.bz2
Source1:        qa_sharutils.tcf
Source2:        test_sharutils-run
Source3:        upstream_wrapper.sh
Source4:        qa_test_sharutils.8
Patch0:         %{name}-%{version}-paths.diff
Requires:       ctcs2
Requires:       sharutils
Provides:       qa_sharutils
Obsoletes:      qa_sharutils
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Test case for sharutils package.

Tests from sharutils package (source code) included as well as one
custom testcase for uuencode/decode.

%prep
%setup -q -n sharutils
%patch0

%build

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man8
install -m 755 -d %{buildroot}/%{qa_location}
cp -a * %{buildroot}/%{qa_location}
install -d -m 0755 %{buildroot}%{qa_location}/tcf
install -d -m 0755 %{buildroot}%{_datadir}/qa/tcf
install -d -m 0755 %{buildroot}%{_datadir}/qa/tools
#
#copy the helper script
install -m 0755 %{SOURCE2} %{buildroot}%{_datadir}/qa/tools
install -m 0755 %{SOURCE3} %{buildroot}/%{qa_location}
#
#
cp %{SOURCE1} %{buildroot}/%{qa_location}/tcf
ln -s ../%{name}/tcf/qa_sharutils.tcf %{buildroot}%{_datadir}/qa/tcf/

%files
%defattr(-, root, root)
%{_mandir}/man8/qa_test_sharutils.8%{ext_man}
%{qa_location}
%{_datadir}/qa
%{_datadir}/qa/tcf/qa_sharutils.tcf
%{_datadir}/qa/tools/test_sharutils-run

%changelog
