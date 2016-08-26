#
# spec file for package qa_test_bzip2
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


Name:           qa_test_bzip2
Version:        0.2
Release:        0
Summary:        (rd-)qa internal package for testing bzip2
License:        SUSE Proprietary
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          SuSE internal
Url:            http://w3.suse.de/~fseidel/
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_bzip2.tcf
Source2:        test_bzip2-run
Source3:        qa_test_bzip2.8
Requires:       bzip2
Requires:       ctcs2
Requires:       gcc
Requires:       libbz2-devel
Provides:       qa_bzip2
Obsoletes:      qa_bzip2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
this is the first rd-qa internal package following the new rd-qa
internal policies and may be taken as a template for other similar ones

%prep
%setup -q -n %{name}

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}
install -m 755 -d %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/qa/%{name}/tcf
install -m 755 %{SOURCE2} %{buildroot}%{_datadir}/qa/tools
cp -a * %{buildroot}%{_datadir}/qa/%{name}
ln -s ../%{name}/tcf/qa_bzip2.tcf %{buildroot}%{_datadir}/qa/tcf/
find %{buildroot}%{_datadir}/qa/%{name} -depth -type d -name CVS -exec rm -rf {} \;

%files
%defattr(-,root,root)
%{_mandir}/man8/qa_test_bzip2.8%{ext_man}
%{_datadir}/qa
%{_datadir}/qa/%{name}
%{_datadir}/qa/tcf/qa_bzip2.tcf
%{_datadir}/qa/tools/test_bzip2-run
%doc COPYING
%attr(0755,root,root) %{_datadir}/qa/qa_test_bzip2/*.sh

%changelog
%changelog
