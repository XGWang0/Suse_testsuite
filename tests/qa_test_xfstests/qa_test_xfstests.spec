Name:           qa_test_xfstests
Summary:        XFS regression test suite
Version:        1.1.1
%define         git_version 10298d30e55c
Release:        1
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  autoconf xfsprogs xfsprogs-devel xfsprogs-qa-devel e2fsprogs-devel libacl-devel
BuildRequires:  libattr-devel libaio-devel libtool fdupes automake make m4
Requires:       bash xfsprogs xfsdump perl acl attr bind-utils bc indent quota
Source0:        xfstests-%{version}_g%{git_version}.tar.bz2
Source1:        automation-%{version}.tar.bz2
License:        GPL2+
Vendor:         Silicon Graphics, Inc.
URL:            http://oss.sgi.com/projects/xfs/
Group:          System/Filesystems
Patch3:		no-ltinstall.diff

%description
The XFS regression test suite.  Also includes some support for
acl, attr, dmapi, udf, reiserfs, nfs, btrfs testing.  Contains around 250+ specific tests
for userspace & kernelspace.

%prep
%setup -n xfstests-%{version} -a1
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
#echo prefix=%{_prefix}
#echo manifest
#cat `pwd`/install.manifest
#echo ---
%fdupes %buildroot/%_prefix

install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 automation/run_xfstests.sh $RPM_BUILD_ROOT/usr/share/qa/%{name}/
install -m 755 automation/test_*-run $RPM_BUILD_ROOT/usr/share/qa/tools/
cp -r automation/blacklists/* $RPM_BUILD_ROOT/usr/share/qa/%{name}/xfstests/tests/

%clean
rm -rf $RPM_BUILD_ROOT

#%files -f build/rpm/rpmfiles
%files
%defattr(-, root, root)
/usr/share/qa

%changelog

