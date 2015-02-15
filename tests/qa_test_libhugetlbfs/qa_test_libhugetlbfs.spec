#
# spec file for package libhugetlbfs (Version 0.1)
#

Name:         qa_test_libhugetlbfs
Url:          http://libhugetlbfs.sourceforge.net/
License:      GPL v2 or later
# Group:        SuSE internal
Group:        Kernel/Function
Summary:      Kernel, libhugetlbfs
Requires:     ctcs2 glibc glibc-devel libhugetlbfs
Version:      2.17
Release:      1
Source0:      libhugetlbfs-%version.tar.gz
Source1:      test_libhugetlbfs-run
Source2:      qa_test_libhugetlbfs.8
Source3:      qa_test_libhugetlbfs.tcf
Patch0:       err_output.patch
Patch1:       ppc64le.patch
Patch2:	      s390ppc64.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
The testsuite contains tests both for the library's features and for the underlying kernel hugepage functionality 

%prep
%setup -q -n libhugetlbfs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make clean
make -i

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 %{S:3} $RPM_BUILD_ROOT/usr/share/qa/tcf
mkdir -p $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
install -d $RPM_BUILD_ROOT/usr/share/qa/%name
cp -a * $RPM_BUILD_ROOT/usr/share/qa/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_libhugetlbfs.8.gz
/usr/share/qa
/usr/share/qa/%name
/usr/share/qa/tools

%changelog
* Wed Nov 6 2013 - cachen@suse.com
- package created
