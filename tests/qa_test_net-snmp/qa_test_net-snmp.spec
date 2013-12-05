#
# spec file for package qa_net-snmp (Version 5.4.2)
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
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


Name:           qa_test_net-snmp
BuildRequires:  bzip2
Version:        5.4.3
Release:        2
License:        GPL v2 or later; BSD
Group:          System/Packages
AutoReqProv:    on
Source0:        %{name}-%{version}.tar.bz2
Source1:        get_qa_test_net-snmp
Source2:        qa_net-snmp.tcf
Source3:        TESTCONF-suse.sh
Source4:        test_net-snmp-run
Source5:        run-test-wrapper.sh
Source6:        generate_tcf.sh
Source7:	qa_test_net-snmp.8
Patch0:		T141snmpv2cvacmgetfail.patch
Patch1:		add_source_file_path.patch
Url:            http://sourceforge.net/projects/net-snmp
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        SNMP testsuite
BuildArch:      noarch
Provides:	qa_net-snmp
Obsoletes:	qa_net-snmp
Requires:       net-snmp net-snmp-devel
Provides:	qa_net-snmp
Obsoletes:	qa_net-snmp
Requires:       ctcs2 perl

%description
This package contains testsuite for net-snmp package together with a
tcf file (test control file).

The testsuite contains several testcases for testing the basic
functionality provided by net-snmp package.



Authors:
--------
    Wes Hardaker <hardaker@users.sourceforge.net>

%prep
%setup -n qa_test_net-snmp
%define qa_location /usr/share/qa/qa_test_net-snmp
%patch0 -p1
%patch1 -p0

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:7} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}
#
cp -rv * $RPM_BUILD_ROOT/%{qa_location}
cp %{SOURCE3} $RPM_BUILD_ROOT/%{qa_location}/testing
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
cp %{SOURCE2} $RPM_BUILD_ROOT/%{qa_location}/tcf
ln -s ../qa_test_net-snmp/tcf/qa_net-snmp.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 0755 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/%{qa_location}

%clean
rm -rvf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_net-snmp.8.gz
/usr/share/qa
/usr/share/qa/tcf/qa_net-snmp.tcf
/usr/share/qa/qa_test_net-snmp/

%changelog
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Thu Aug 11 2011 - llipavsky@suse.cz
- Package rename: qa_net-snmp -> qa_test_net-snmp
