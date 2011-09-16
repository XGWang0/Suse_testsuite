Source1:	qa_test_sched_stress.8
#
# spec file for package qa_sched_stress (Version 0.1)
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


Name:           qa_test_sched_stress
#BuildRequires:  ctcs2
License:        GPL v2 or later
Group:          SUSE internal
Summary:        sched stress test from LTP
Provides:	qa_sched_stress
Obsoletes:	qa_sched_stress
Requires:       ctcs2 ltp
Version:        0.1
Release:        2
Source0:         %{name}-%{version}.tar.bz2
Source1:        test_sched_stress-run
Source2:        qa_test_sched_stress.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
sched stress test from LTP

%prep
%setup -n %{name} 

%build

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%{name}
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
cp do_sched_stress $RPM_BUILD_ROOT/usr/share/qa/%name
cp sched_stress.tcf $RPM_BUILD_ROOT/usr/share/qa/%{name}/tcf
cp %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
chmod 755 $RPM_BUILD_ROOT/usr/share/qa/tools/test_sched_stress-run $RPM_BUILD_ROOT/usr/share/qa/%name/do_sched_stress
ln -s ../%{name}/tcf/sched_stress.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_sched_stress.8.gz
/usr/share/qa
%changelog
* Wed Apr 01 2009 yxu@suse.de
- initial release
