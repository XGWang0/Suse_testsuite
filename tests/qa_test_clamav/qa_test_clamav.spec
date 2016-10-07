#
# spec file for package qa_test_clamav
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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

#!BuildIgnore: post-build-checks-malwarescan

Name:           qa_test_clamav
Version:        0.6
Release:        0
Summary:        (rd-)qa internal package for testing clamav
License:        SUSE Proprietary
Group:          SUSE internal
Url:            http://www.clamav.net/
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_clamav.tcf
Source2:        test_clamav-run
Source3:        README
Source4:        qa_test_clamav.8
Requires:       clamav
Requires:       ctcs2
Provides:       qa_clamav
Obsoletes:      qa_clamav
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
test suite for clamav and freshclam testing

%prep
%setup -q -n %{name}

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man8
install -m 755 -d %{buildroot}%{_datadir}/qa
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 755 %{SOURCE2} %{buildroot}%{_datadir}/qa/tools
install -m 755 %{SOURCE3} %{buildroot}%{_datadir}/qa/%{name}/
cp -a * %{buildroot}%{_datadir}/qa/%{name}
ln -s ../%{name}/tcf/qa_clamav.tcf %{buildroot}%{_datadir}/qa/tcf/

%files
%defattr(0755,root,root)
%{_mandir}/man8/qa_test_clamav.8%{ext_man}
%{_datadir}/qa/
%{_datadir}/qa/%{name}
%{_datadir}/qa/%{name}/README
%{_datadir}/qa/tcf/qa_clamav.tcf
%{_datadir}/qa/tools/test_clamav-run
%doc COPYING

%changelog
