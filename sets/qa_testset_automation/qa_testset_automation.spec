#
# spec file for package qa_testset_automation
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


Name:           qa_testset_automation
Version:        1.0
Release:        0
Summary:        A test Framework for QA APACII
License:        GPL-2.0+
Group:          testset
Source0:        automation-%{version}.tar.bz2
Requires:       qa_db_report
Requires:       qa_lib_config
Requires:       qa_lib_ctcs2
Requires:       qa_lib_internalapi
Requires:       qa_lib_keys
Requires:       qa_lib_perl
Requires:       qa_tools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
qa_testset_automation is a collection of tools.

%prep
%setup -q -n automation

%build

%install
%if 0%{?suse_version} == 1110
%define sle_release SLE11
%else if 0%{?suse_version} == 1315
%define sle_release SLE12
%endif

pushd qaset
make TARGET_RELEASE=%{sle_release} DEST=%{buildroot} install
popd
cp -a perfcom %{buildroot}%{_datadir}/qa

%files
%defattr(-, root, root)
%if 0%{?suse_version} == 1110
%{_initddir}/qaset
%else if 0%{?suse_version} == 1315
%{_prefix}/lib/systemd/system/multi-user.target.wants
%{_prefix}/lib/systemd/system/qaperf.service
%endif
%{_datadir}/qa
%{_datadir}/qa/qaset
%{_datadir}/qa/perfcom

%changelog
