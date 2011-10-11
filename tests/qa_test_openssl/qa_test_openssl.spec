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
%if 0%{?suse_version} < 1120
Version:	0.9.8r
%else
Version:        1.0.0e
%endif
Release:        5
Source0:        %name-%version.tar.bz2
Source1:        test_openssl-run
Source2:        qa_test_openssl.8
Source3:	generate_openssl_tests.sh
Patch0:		qa_test_openssl-Makefile-1.0.0e.patch
Patch1:		qa_test_openssl-Makefile-0.9.8r.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for openssl package.


%prep
%setup -q -n %{name}-%{version}
echo "SLES: %{?sles_version}"
cat test/Makefile |grep ^test_ | awk -F ':' '{print $1}' | awk -F ' ' '{print $1}' > ./ctcs2_test_list

echo -en "#!/bin/bash\ncd %{qa_location}/test\nmake \$1\n[[ \$? -eq 0 ]] && exit 0 || exit 1\n" > ./ctcs2_run_test.sh
chmod +x ./ctcs2_run_test.sh

%if 0%{?suse_version} < 1120
%patch1 -p1
%else
cd test
%patch0 -p1
%endif


%build
cd test
make
make tests


%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tcf
install -m 755 -d $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 -d $RPM_BUILD_ROOT/%{qa_location}
install -m 755 -d $RPM_BUILD_ROOT/%{qa_location}/tcf
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
cp -a * $RPM_BUILD_ROOT/%{qa_location}
touch $RPM_BUILD_ROOT/%{qa_location}/qa_openssl.tcf
ln -s $RPM_BUILD_ROOT/%{qa_location}/qa_openssl.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/


%post
echo -en "timer 300\nfg 1 build %{qa_location}/ctcs2_run_test.sh\nwait\n\n" > %{qa_location}/tcf/qa_openssl.tcf
cat %{qa_location}/ctcs2_test_list | while read test; do
	echo "timer 300"
	echo -en "fg 1 "
	echo -en "$test %{qa_location}/ctcs2_run_test.sh $test\n"
	echo -en "wait\n\n"
done >> %{qa_location}/tcf/qa_openssl.tcf


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
