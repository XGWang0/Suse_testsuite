#
# spec file for package qa_test_lha
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

Name: qa_test_lha
Version: 0.8
Release: 0
Summary: Testsuite for lha package containing CLI tests.
License: GPL-2.0+
Group: System/Benchmark
Source: %{name}-%{version}.tar.bz2
#Source1: GNUmakefile
#Source2: make-tcf
#Source3: %{name}.8
#Source4: %{name}.changes
#Source5: test_%{name}-run
BuildRequires: make
Requires: cram
Requires: qa_lib_ctcs2
Requires: qa_tools
BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch

%description
Testsuite containing set of files used for testing %{name} packaged into CTCS2.

%prep
%setup -q -n %{name}

%build
make

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root)
%{_mandir}/man8/%name.8.gz
%dir /usr/share/qa
%dir /usr/share/qa/%name
/usr/share/qa/%name/*
/usr/share/qa/tcf
/usr/share/qa/tools

%changelog
