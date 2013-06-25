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

# norootforbuild


Name:           mce-inject

Url:            http://git.kernel.org/pub/scm/utils/cpu/mce/mcelog.git
License:        GPL v2
Group:          System/Benchmark
AutoReqProv:    on
Summary:        MCE injection tool
Version:        git_25_11_2009
Release:        1
Source0:         %{name}-%{version}.tar.bz2
Source1:	mce-inject.8
Patch001:	dont_compile_headers.patch
Patch002:	pthread.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	bison flex

%description
Machine Check Exception injection tool for linux kernel. Requires a Linux
2.6.31+ kernel with CONFIG_X86_MCE_INJECT enabled and the mce-inject module
loaded (if not built in)

Authors:
--------
	Andi Kleen
	Ying Huang

%prep
%setup
%patch001 -p1
%patch002 -p1

%build
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
export destdir=$RPM_BUILD_ROOT
make install

%files
%defattr(-,root,root)
%{_mandir}/man8/mce-inject.8.*
%{_sbindir}/mce-inject

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Feb 16 2010 chrubis@suse.cz
 Created initial package version.
