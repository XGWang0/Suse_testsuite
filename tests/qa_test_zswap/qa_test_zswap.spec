#
# spec file for package qa_test_zswap
#
# Copyright (c) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

Name:           qa_test_zswap
Version:        1.0
Release:        0
License:        GPL v2
Summary:        zswap testsuite
Group:          SuSE internal
Source:         %{name}-%{version}.tar.xz
Source1:        zswap.tcf
Source2:        test_zswap-run
BuildRequires:  gcc
Requires:       python-setuptools
Provides:       qa_zswap
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Testsuite for zswap. Zswap is a Linux kernel feature providing a compressed write-back cache for swapped pages. Instead of moving memory pages to a swap device when they are to be swapped out, zswap performs their compression and then stores them into a memory pool dynamically allocated inside system's RAM.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/qa/%{name}/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT%{_datadir}/qa/%{name}/tcf/
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/qa/tcf
ln -s ../%{name}/tcf/zswap.tcf $RPM_BUILD_ROOT%{_datadir}/qa/tcf/
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/qa/tools
install -m 755 %{S:2} $RPM_BUILD_ROOT%{_datadir}/qa/tools

%post
easy_install-2.7 pexpect

%preun
rm -f %{_datadir}/qa/%{name}/*.pyc %{_datadir}/qa/%{name}/*.pyo

%files
%defattr(-,root,root)
%dir %{_datadir}/qa
%{_datadir}/qa/%{name}
%dir %{_datadir}/qa/tcf
%{_datadir}/qa/tcf/zswap.tcf
%dir %{_datadir}/qa/tools
%{_datadir}/qa/tools/test_zswap-run

%changelog
* Wed Nov 02 2016 - jtzhao@suse.com
- Initial commit
