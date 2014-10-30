#
# spec file for package kgraft-patch-getpid
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%define QA_KGRAFT_PATH_ROOT /usr/share/qa/qa_test_kgraft_patch

Name:           qa-kgraft-patch
Version:        1
Release:        1
License:        GPL-2.0
Summary:        Kgraft patches for QA test
Group:          System/Kernel
Source0:        qa-kgraft-patch.tar.xz
Source1:        qa-kgr-install-modules.sh
Source2:        qa-kgr-uninstall-modules.sh
Source3:        qa-kgr-try-finish-patching.sh
Source4:        qa-kgr-regen-initrd
Source200:      qa-kgr-patch-sys-getpid
Source201:      qa-kgr-patch-sys-read
Source202:      qa-kgr-patch-sys-write
Source203:      qa-kgr-patch-sys-fsync
BuildRequires:  kernel-syms kgraft-devel
#do not use kgraft_module_package
#Because QA needs to insmod manully!

%description
This is used for QA Team.

%prep -T
# nothing to be prepared

%build
# build the modules locally

%install
QA_KGRAFT_PATH_ROOT=${RPM_BUILD_ROOT}/%{QA_KGRAFT_PATH_ROOT}
install -d ${QA_KGRAFT_PATH_ROOT}
install %{S:0} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:1} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:2} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:3} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:4} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:200} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:201} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:202} ${QA_KGRAFT_PATH_ROOT}
install -m 755 %{S:203} ${QA_KGRAFT_PATH_ROOT}

%post
%{QA_KGRAFT_PATH_ROOT}/qa-kgr-install-modules.sh

%preun
%{QA_KGRAFT_PATH_ROOT}/qa-kgr-uninstall-modules.sh
pushd %{QA_KGRAFT_PATH_ROOT}
rm -rf  qa-kgraft-patch > /dev/null

%files
%defattr(-, root, root)
%{QA_KGRAFT_PATH_ROOT}


%changelog
