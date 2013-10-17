Name:           qa_test_xfstests
Summary:        XFS regression test suite
Version:        1.1.1
%define         git_version f6406da
Release:        1
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  autoconf xfsprogs xfsprogs-devel xfsprogs-qa-devel e2fsprogs-devel libacl-devel
BuildRequires:  libattr-devel libaio-devel libtool fdupes
Requires:       bash xfsprogs xfsdump perl acl attr bind-utils bc indent quota
Source0:        xfstests-%{version}_g%{git_version}.tar.bz2
Source1:        automation.tar.bz2
License:        GPL2+
Vendor:         Silicon Graphics, Inc.
URL:            http://oss.sgi.com/projects/xfs/
Group:          System/Filesystems
Patch1:		0001-xfstests-enhance-ltp-fsx-with-a-timeout-option.patch
Patch3:		no-ltinstall.diff

%description
The XFS regression test suite.  Also includes some support for
acl, attr, dmapi, udf, reiserfs, nfs, btrfs testing.  Contains around 250+ specific tests
for userspace & kernelspace.

%prep
%setup -q -a1
%patch1 -p1
%patch3 -p1


%build
export OPTIMIZER="-fPIC"
export CFLAGS="$RPM_OPT_FLAGS -Iinclude"
INSTALL_USER=root
INSTALL_GROUP=root
export INSTALL_USER INSTALL_GROUP
make configure
./configure		\
	--prefix=%{_prefix} \
	--libdir=/%{_libdir} \
	--libexecdir=/usr/%{_lib} \
	--includedir=%{_includedir} \
	--mandir=%{_mandir} \
	--datadir=%{_datadir}	\

make %{?jobs:-j %jobs}

%install
DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
export DIST_ROOT DIST_INSTALL
%makeinstall DIST_ROOT=$RPM_BUILD_ROOT DIST_MANIFEST="$DIST_INSTALL"
make -C build/rpm rpmfiles DESTDIR=$RPM_BUILD_ROOT DIST_MANIFEST="$DIST_INSTALL"
%fdupes %buildroot/%_prefix

%clean
rm -rf $RPM_BUILD_ROOT

%files -f build/rpm/rpmfiles
