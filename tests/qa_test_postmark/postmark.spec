#
# spec file for package postmark (Version 1.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:		qa_test_postmark
License:	Artistic License
Group:		System/Benchmark
AutoReqProv:	on
Version:	1.51
Release:	1
Summary:	A filesystem benchmarking tool
URL:		http://fsbench.filesystems.org/
Source0:	%{name}-%{version}.tar.bz2
Source1:	test_postmark-run
Source2:	qa_postmark.tcf
Source3:	input
Source4:	qa_test_postmark.8
BuildRoot:	%{_tmppath}/%{name}-%{version}-build


%description
Existing file system benchmarks are deficient in portraying
performance in the ephemeral small-file regime used by Internet
software, especially:
                * electronic mail
                * netnews
                * web-based commerce
PostMark is a new benchmark to measure performance for this class of
application.


Authors:
--------
        NetApp

%prep
%setup

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:4} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 755  $RPM_BUILD_ROOT/usr/bin
install -d -m 755  $RPM_BUILD_ROOT/usr/share/qa
install -d -m 755  $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 755  $RPM_BUILD_ROOT/usr/share/qa/tools
install -d -m 755  $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -d -m 755  $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 postmark $RPM_BUILD_ROOT/usr/bin
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/%{name}/
ln -s ../%name/tcf/qa_postmark.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_postmark.8.gz
/usr/bin/postmark
/usr/share/qa
/usr/share/qa/tcf
/usr/share/qa/tools
/usr/share/qa/%{name}
/usr/share/qa/%{name}/tcf
/usr/share/qa/tcf/qa_postmark.tcf
/usr/share/qa/%{name}/tcf/qa_postmark.tcf
/usr/share/qa/tools/test_postmark-run
/usr/share/qa/%{name}/input


%changelog
