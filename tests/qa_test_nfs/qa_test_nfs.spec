#
# spec file for package qa_nfs (Version 0.2)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_nfs
BuildRequires:  libqainternal
License:        SUSE Proprietary
Group:          System/Packages
Summary:        Basic NFS tests for nfsv3 and nfsv4
%if 0%{?sles_version} == 10
Provides:	qa_nfs
Obsoletes:	qa_nfs
Requires:       limal-nfs-server nfs-utils libqainternal ctcs2
%else
Provides:	qa_nfs
Obsoletes:	qa_nfs
Requires:       nfs-kernel-server nfs-client libqainternal ctcs2
%endif
AutoReqProv:    on
Version:        0.2
Release:        2
Source0:        %name-%version.tar.bz2
Source1:        test_nfs-run
Source2:        test_nfs-v4-run
Source3:	qa_test_nfs.8
Source4:	qa_nfs.tcf
Source5:	qa_nfs-v4.tcf
Patch0:		    start_stop.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%define qa_location /usr/share/qa/%{name}

%description
Basic NFS tests for nfsv3 and nfsv4. Including: [nfs_start_stop] Start
and stop nfs daemon.

[nfs_mount_umount] Mount and umount directories with various params.

[nfs_read] Read text and binary data and make simple directory tree
with folders, files and links and check them.

[nfs_write] The same as nfs_read, but writes to mounted dir and check
with local dir.

[nfs_dontwrite] Try write to mounted dir with no permision, mounted as
ro etc.

[nfs_usermapping_*] Mount directories with params root_squash,
no_root_squash and all_squash and check correct granting and denying
for root and user.


%prep
%setup -n %{name}
%patch0 -p 1

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}
cp -rv * $RPM_BUILD_ROOT/%{qa_location}
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 0644 %{S:4} $RPM_BUILD_ROOT%{qa_location}/tcf
install -m 0644 %{S:5} $RPM_BUILD_ROOT%{qa_location}/tcf
ln -s ../%name/tcf/qa_nfs.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
ln -s ../%name/tcf/qa_nfs-v4.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/qa/tools

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)   
/usr/share/man/man8/qa_test_nfs.8.gz
%{qa_location}
/usr/share/qa
/usr/share/qa/tcf/qa_nfs.tcf
/usr/share/qa/tools/test_nfs-run

%changelog
* Wed Oct 13 2010 csxia@novell.com
	change the dependency of nfs-client to nfs-utils in Requires filed for SLES code 10 
	since there is no such rpm:nfs-client
* Thu Dec 17 2009 csxia@novell.com
	start_stop.diff 
* Mon Jun 09 2008 michalsrb@gmail.com
- initial release
