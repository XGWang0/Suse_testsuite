Source1:	qa_test_fs_stress.8
#
# spec file for package qa_fs_stress (Version 0.1)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

# norootforbuild


Name:           qa_test_fs_stress
License:        GPL v2 or later
#BuildRequires:  ctcs2
Group:          SUSE internal
Summary:        file system stress test
Provides:	qa_fs_stress
Obsoletes:	qa_fs_stress
Requires:       ctcs2
Version:        0.1
Release:        2
Source0:        %{name}-%{version}.tar.bz2
Source1:        fs_stress.tcf
Source2:        test_fs_stress-run
Source3:        qa_test_fs_stress.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
file system stress test

%prep
%setup -n %{name} 

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
cp file_copy $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tcf 
cp %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
ln -s ../../../share/qa/tcf/fs_stress.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_fs_stress.8.gz
/usr/share/qa
/usr/lib/ctcs2
%attr (0755, root, root) /usr/share/qa/tools/test_fs_stress-run
%attr (0755, root, root) /usr/share/qa/tools/file_copy
%changelog
* Wed Apr 01 2009 yxu@suse.de
- initial release
