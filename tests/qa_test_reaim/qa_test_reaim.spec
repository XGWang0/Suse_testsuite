#
# spec file for package qa_test_reaim
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


Name:           qa_test_reaim
Version:        7.0.1.13
Release:        0
Summary:        Benchmark tool
License:        GPL-2.0+
Group:          Development/Tools/Other
Url:            http://sourceforge.net/projects/re-aim-7
Source0:        reaim-%{version}.tgz
# For subpackage creation
Source1:        ctcstools-%{version}.tar.bz2
Source2:        README
Source3:        qa_test_reaim.8
Patch0:         bugfixes.patch
Patch1:         fix-aio.patch
Patch2:         fix-defaults.patch
Patch3:         fix-tst_sig.patch
Patch4:         fix-abs-paths.patch
Patch5:         ready-for-sles8.patch
Patch6:         fix-diskdir.patch
Patch7:         drop-aio.patch
Patch8:         fix-pipe_test.patch
Patch9:         c_macro_problem.patch
Patch10:        diskdir_abuild.patch
Patch11:        fix-sync.patch
Patch12:        change-times.patch
BuildRequires:  automake
BuildRequires:  libaio-devel
BuildRequires:  libtool
Requires:       ctcs2
Provides:       reaim
Provides:       reaim-ctcs2-glue
Obsoletes:      reaim
Obsoletes:      reaim-ctcs2-glue
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This tool benchmarks overall system speed by mixing measurements of
file system speed and execution speed under VM and CPU pressure.

%prep
#%setup -q -n %{name}-full-%{version} -a1
%setup -q -n reaim-%{version} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
# aio stuff is not written portable => rewrite it for sles8
%if 0%{?suse_version} < 910
%patch5 -p1
%endif
%patch6 -p1
# drop aio if building for sles7
%if 0%{?suse_version} < 810
%patch7 -p1
%endif
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
autoreconf -fiv
%configure
make %{?_smp_mflags} CFLAGS="%{optflags} -lm -ffloat-store -D_GNU_SOURCE -DSHARED_OFILE"

%install
mkdir -p %{buildroot}%{_prefix}/lib/reaim
mkdir -p %{buildroot}%{_prefix}/lib/ctcs2/tools
mkdir -p %{buildroot}%{_prefix}/lib/ctcs2/config/reaim
mkdir -p %{buildroot}%{_prefix}/lib/ctcs2/tcf
mkdir -p %{buildroot}%{_prefix}/lib/ctcs2/bin/reaim
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_datadir}/qa/tools
install -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/qa_test_reaim.8
cp -r data scripts %{buildroot}%{_prefix}/lib/reaim
cp src/reaim data/reaim.config %{buildroot}%{_prefix}/lib/reaim
cp ctcstools/workfile %{buildroot}%{_prefix}/lib/reaim/workfile
cp ctcstools/test_reaim-run %{buildroot}%{_prefix}/lib/ctcs2/tools
chmod +x %{buildroot}%{_prefix}/lib/ctcs2/tools/test_reaim-run
install -m 755 ctcstools/test_reaim_ioperf-run %{buildroot}%{_datadir}/qa/tools
install -m 755 ctcstools/test_reaim_all-run %{buildroot}%{_datadir}/qa/tools
cp ctcstools/reaim.tcf %{buildroot}%{_prefix}/lib/ctcs2/tcf
cp ctcstools/prepare.sh %{buildroot}%{_prefix}/lib/ctcs2/config/reaim
chmod +x %{buildroot}%{_prefix}/lib/ctcs2/config/reaim/prepare.sh
ln -s ../../../reaim/reaim.config %{buildroot}%{_prefix}/lib/ctcs2/config/reaim/reaim.config
ln -s ../../../reaim/workfile %{buildroot}%{_prefix}/lib/ctcs2/config/reaim/workfile
ln -s ../../../reaim/reaim %{buildroot}%{_prefix}/lib/ctcs2/bin/reaim
cp %{SOURCE2} %{buildroot}%{_prefix}/lib/reaim
# now fix file permissions
# no suid root
# no world writable
find %{buildroot} -type f -print0 | xargs -0 chmod -c o-w,u-s

%files
%defattr(-,root,root)
%{_prefix}/lib/reaim
%{_datadir}/qa
%{_mandir}/man8/%{name}.8%{ext_man}

#%files ctcs2-glue
#%defattr(-,root,root)
%{_prefix}/lib/ctcs2

%changelog
%changelog
