Source1:	qa_test_process_stress.8
#
# spec file for package qa_process_stress (Version 0.1)
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


Name:           qa_test_process_stress
#BuildRequires:  ctcs2
License:        SUSE Proprietary
Group:          SUSE internal
Summary:        process stress test from LTP
Provides:	qa_process_stress
Obsoletes:	qa_process_stress
Requires:       ctcs2 ltp
Version:        0.1
Release:        2
Source0:        %{name}-%{version}.tar.bz2
Source1:        qa_test_process_stress.8
Source2:        test_process_stress-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
process stress test from LTP

%prep
%setup -n %{name} 

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:1} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf
cp do_process_stress $RPM_BUILD_ROOT/usr/share/qa/tools
cp process_stress.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf 
cp %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
chmod 755 $RPM_BUILD_ROOT/usr/share/qa/tools/test_process_stress-run
ln -s ../../../share/qa/tcf/process_stress.tcf $RPM_BUILD_ROOT/usr/lib/ctcs2/tcf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_process_stress.8.gz
/usr/share/qa
/usr/lib/ctcs2
%changelog
* Tue Mar 01 2011 llwang@novell.com
- modify loop condition
* Wed Apr 01 2009 yxu@suse.de
- initial release
