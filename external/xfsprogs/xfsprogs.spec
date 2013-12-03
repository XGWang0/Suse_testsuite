#
# spec file for package xfsprogs
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           xfsprogs
BuildRequires:  e2fsprogs-devel
BuildRequires:  libblkid-devel
BuildRequires:  libtool
BuildRequires:  readline-devel
%define		git_version 7db1e7b
Version:        3.1.8
Release:        0
%if 0%{?suse_version} >= 1010
# hint for ZYPP
Supplements:    filesystem(xfs)
%endif
Provides:       xfsprogs-%{version}
AutoReqProv:    no
Url:            http://oss.sgi.com/projects/xfs/
Summary:        Utilities for managing the XFS file system
License:        GPL-2.0+
Group:          System/Filesystems
Source0:        xfsprogs-%{version}_g%{git_version}.tar.bz2
Patch0:         xfsprogs-docdir.diff
Patch1:         xfsprogs-ppc64.diff
Patch2:		buildfix.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A set of commands to use the XFS file system, including mkfs.xfs.

XFS is a high performance journaling file system which originated on
the SGI IRIX platform.	It is completely multithreaded. It can support
large files and large file systems, extended attributes, and variable
block sizes.It is extent based and makes extensive use of Btrees
(directories, extents, and free space) to aid both performance and
scalability.

Refer to the documentation at http://oss.sgi.com/projects/xfs/ for
complete details.  This implementation is on-disk compatible with the
IRIX version of XFS.



Authors:
--------
    SGI

%package        devel
Requires:       xfsprogs = %version
Url:            http://oss.sgi.com/projects/xfs/
Summary:        XFS Filesystem-specific Static Libraries and Headers
Group:          Development/Libraries/C and C++
Requires:       libuuid-devel
Requires:       xfsprogs
AutoReqProv:    no

%description devel
xfsprogs-devel contains the libraries and header files needed to
develop XFS file system-specific programs.

You should install xfsprogs-devel if you want to develop XFS file
system-specific programs.  If you install xfsprogs-devel, you will also
want to install xfsprogs.



Authors:
--------
    SGI

%package        qa-devel
Requires:       xfsprogs = %version
Requires:       xfsprogs-devel = %{version}
Url:            http://oss.sgi.com/projects/xfs/
Summary:        XFS QA filesystem-specific headers
Group:          Development/Libraries/C and C++

%description qa-devel
xfsprogs-qa-devel contains headers needed to build the xfstests
QA suite.

You should install xfsprogs-qa-devel only if you are interested
in building or running the xfstests QA suite.



Authors:
--------
    SGI

%prep
%setup -q
%patch0
%patch1
%patch2

%build
export OPTIMIZER="-fPIC"
export DEBUG=-DNDEBUG
export LIBUUID=/usr/%{_lib}/libuuid.a
export CFLAGS="$RPM_OPT_FLAGS"
./configure \
	--prefix=%{_prefix} \
	--libdir=/%{_libdir} \
	--includedir=%{_includedir} \
	--mandir=%{_mandir} \
	--datadir=%{_datadir}	\
	--enable-static        \
	--enable-readline=yes	\
	--enable-blkid=yes

# Kill rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?jobs:-j %jobs} 

%install
export DIST_ROOT="$RPM_BUILD_ROOT"
make install
make install-dev
make install-qa
# remove devel stuff from /lib
rm -f -- $RPM_BUILD_ROOT/{%{_lib}/*.{so,a,la},%{_libdir}/*.{la,a}}
rm -f -- $RPM_BUILD_ROOT/%_libdir/libhandle.so
pushd $RPM_BUILD_ROOT%_libdir
	ls ../../%_lib/libhandle.so.[0-9]
	ln -s ../../%_lib/libhandle.so.[0-9] libhandle.so
popd
chmod 755 $RPM_BUILD_ROOT/sbin/fsck.xfs
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root,755)
/sbin/*
/usr/sbin/*
# this is only used by xfs cmds, therefore no urgent need for a shlib package
/%_lib/libhandle.so.*
%doc /usr/share/man/man[58]/*
%doc %_defaultdocdir/%name

%files devel
%defattr(-,root,root,755)
%dir %{_includedir}/xfs
%{_includedir}/xfs/handle.h
%{_includedir}/xfs/jdm.h
%{_includedir}/xfs/linux.h
%ifarch %{multilib_arches}
%{_includedir}/xfs/platform_defs-%{_arch}.h
%endif
%{_includedir}/xfs/platform_defs.h
%{_includedir}/xfs/xfs.h
%{_includedir}/xfs/xfs_fs.h
%{_includedir}/xfs/xqm.h
%_libdir/*.so
/usr/share/man/man3/*

%files qa-devel
%defattr(-,root,root)
%{_includedir}/xfs/bitops.h
%{_includedir}/xfs/cache.h
%{_includedir}/xfs/kmem.h
%{_includedir}/xfs/libxfs.h
%{_includedir}/xfs/libxlog.h
%{_includedir}/xfs/list.h
%{_includedir}/xfs/parent.h
%{_includedir}/xfs/swab.h
%{_includedir}/xfs/xfs_ag.h
%{_includedir}/xfs/xfs_alloc.h
%{_includedir}/xfs/xfs_alloc_btree.h
%{_includedir}/xfs/xfs_arch.h
%{_includedir}/xfs/xfs_attr_leaf.h
%{_includedir}/xfs/xfs_attr_sf.h
%{_includedir}/xfs/xfs_bit.h
%{_includedir}/xfs/xfs_bmap.h
%{_includedir}/xfs/xfs_bmap_btree.h
%{_includedir}/xfs/xfs_btree.h
%{_includedir}/xfs/xfs_btree_trace.h
%{_includedir}/xfs/xfs_buf_item.h
%{_includedir}/xfs/xfs_da_btree.h
%{_includedir}/xfs/xfs_dfrag.h
%{_includedir}/xfs/xfs_dinode.h
%{_includedir}/xfs/xfs_dir2.h
%{_includedir}/xfs/xfs_dir2_block.h
%{_includedir}/xfs/xfs_dir2_data.h
%{_includedir}/xfs/xfs_dir2_leaf.h
%{_includedir}/xfs/xfs_dir2_node.h
%{_includedir}/xfs/xfs_dir2_sf.h
%{_includedir}/xfs/xfs_dir_leaf.h
%{_includedir}/xfs/xfs_dir_sf.h
%{_includedir}/xfs/xfs_extfree_item.h
%{_includedir}/xfs/xfs_ialloc.h
%{_includedir}/xfs/xfs_ialloc_btree.h
%{_includedir}/xfs/xfs_inode.h
%{_includedir}/xfs/xfs_inode_item.h
%{_includedir}/xfs/xfs_inum.h
%{_includedir}/xfs/xfs_log.h
%{_includedir}/xfs/xfs_log_priv.h
%{_includedir}/xfs/xfs_log_recover.h
%{_includedir}/xfs/xfs_metadump.h
%{_includedir}/xfs/xfs_mount.h
%{_includedir}/xfs/xfs_quota.h
%{_includedir}/xfs/xfs_rtalloc.h
%{_includedir}/xfs/xfs_sb.h
%{_includedir}/xfs/xfs_trans.h
%{_includedir}/xfs/xfs_trans_space.h
%{_includedir}/xfs/xfs_types.h
%{_includedir}/xfs/atomic.h
%{_includedir}/xfs/hlist.h
%{_includedir}/xfs/radix-tree.h
%{_includedir}/xfs/xfs_trace.h

%changelog
