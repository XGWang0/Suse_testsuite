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

Name:           kgraft-patch-getpid-qa
Version:        1
Release:        1
License:        GPL-2.0
Summary:        Kgraft test patch for QA test
Group:          System/Kernel
Source1:        kgraft-patch-getpid-qa.c
Source2:        Makefile
Source3:        Module.supported
BuildRequires:  kernel-syms kgraft-devel
%kgraft_module_package

%description
This is a test Kgraft patch. This is used for QA ACAPII Team
before there is a recognized one.

%prep
%setup -Tc
for sourcefile in %{S:1} %{S:2} %{S:3}; do
 cp ${sourcefile} .
done

%build
set -- *
for flavor in %flavors_to_build; do
	mkdir -p "obj/$flavor"
	cp "$@" "obj/$flavor"
	make -C %{kernel_source $flavor} M="$PWD/obj/$flavor" modules
done

%install
export INSTALL_MOD_DIR=kgraft
export INSTALL_MOD_PATH=%buildroot
for flavor in %flavors_to_build; do
	make -C %{kernel_source $flavor} M="$PWD/obj/$flavor" modules_install
done

%changelog

