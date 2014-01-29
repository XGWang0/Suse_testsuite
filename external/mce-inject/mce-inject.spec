#
# spec file for package mce-inject
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

Name:           mce-inject
Version:        git_25_11_2009
Release:        1
License:        GPL-2.0
Summary:        MCE injection tool
Url:            http://git.kernel.org/pub/scm/utils/cpu/mce/mcelog.git
Group:          System/Benchmark
Source0:        %{name}-%{version}.tar.bz2
Source1:        mce-inject.8
# PATCH-FIX-OPENSUSE fixes-makefile
Patch001:       dont_compile_headers.patch
# PATCH-FIX-OPENSUSE adds-pthread-flag
Patch002:       pthread.patch
BuildRequires:  bison
BuildRequires:  flex
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Machine Check Exception injection tool for linux kernel. Requires a Linux
2.6.31+ kernel with CONFIG_X86_MCE_INJECT enabled and the mce-inject module
loaded (if not built in)

%prep
%setup -q
%patch001 -p1
%patch002 -p1

%build
make

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
export destdir=%{buildroot}
make install

%files
%defattr(-,root,root)
%{_mandir}/man8/mce-inject.8.*
%{_sbindir}/mce-inject

%clean
rm -rf %{buildroot}

%changelog
* Tue Feb 16 2010 chrubis@suse.cz
Created initial package version.
