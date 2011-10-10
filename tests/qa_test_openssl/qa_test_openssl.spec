#
# spec file for package qa_gzip (Version 0.1)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild
%define qa_location /usr/share/qa/qa_test_openssl

Name:           qa_test_openssl
License:        GNU General Public License (GPL)
Group:          SuSE internal
Summary:        Unittests for openssl framework using the system openssl
Provides:	qa_openssl
Obsoletes:	qa_openssl
Requires:       make openssl bc ctcs2 libopenssl-devel
BuildRequires:  make openssl bc ctcs2 libopenssl-devel
Version:        1.0.0e
Release:        2
Source0:        %name-%version.tar.bz2
Source1:        qa_openssl.tcf
Source2:        test_openssl-run
Source3:        qa_test_openssl.8
Source4:	generate_openssl_tests.sh
Source5:	generate_openssl_tests_makefile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for openssl package.



%prep
%setup -q -n %{name}-%{version}
cat test/Makefile |grep ^test_ | awk -F ':' '{print $1}' | awk -F ' ' '{print $1}' > ./ctcs2_test_list

echo -en "#!/bin/bash\ncd %{qa_location}/test\nmake \$1\n[[ \$? -eq 0 ]] && exit 0 || exit 1\n" > ./ctcs2_run_test.sh
chmod +x ./ctcs2_run_test.sh

%build
cd test
make

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/%{qa_location}
install -m 755 -d $RPM_BUILD_ROOT/%{qa_location}/tcf
install -m 644 %{S:1} $RPM_BUILD_ROOT/%{qa_location}/tcf
install -m 755 %{S:2} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/%{qa_location}

%post
cat %{qa_location}/ctcs2_test_list | while read test; do
	echo "timer 300"
	echo -en "fg 1 "
	echo -en "$test %{qa_location}/ctcs2_run_test.sh $test\n"
	echo -en "wait\n\n"
done > %{qa_location}/tcf/qa_openssl.tcf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/qa
%{qa_location}
/usr/share/qa/tcf/qa_openssl.tcf
/usr/share/qa/tools/test_openssl-run
/usr/share/man/man8/qa_test_openssl.8.gz

%changelog
