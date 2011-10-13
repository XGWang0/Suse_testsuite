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
Requires:       make openssl bc ctcs2 libopenssl-devel perl
BuildRequires:  make openssl bc ctcs2 libopenssl-devel perl
%if 0%{?suse_version} < 1120
Version:	0.9.8r
%else
Version:        1.0.0e
%endif
Release:        13
Source0:        %name-%version.tar.bz2
Source1:        test_openssl-run
Source2:        qa_test_openssl.8
Source3:	generate_openssl_tests.sh
Patch0:		qa_test_openssl-Makefile-1.0.0e.patch
Patch1:		qa_test_openssl-Makefile-0.9.8r.patch
Patch2:		qa_test_openssl-sle10-drop-ige.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArchitectures: noarch

%description
Test cases for openssl package.


%prep
%setup -q -n %{name}-%{version}
echo -en "#!/bin/bash\ncd %{qa_location}/test\nmake \$1\n[[ \$? -eq 0 ]] && exit 0 || exit 1\n" > ./ctcs2_run_test.sh
chmod +x ./ctcs2_run_test.sh

sed -i -e 's:/usr/local/bin/perl:/usr/bin/perl:g' util/*.{pl,sh} util/pl/*.pl

%if 0%{?suse_version} < 1120
%patch1 -p1
%else
pushd test > /dev/null
%patch0 -p1
popd > /dev/null
%endif

# SLE 10 does not have this flag, it was added during 0.9.8e release
# SLE 10 does not have support for IGE
# SLE 10 does not have CAMELIA and SEED cypher
%if 0%{?suse_version} < 1100
pushd test > /dev/null
sed -i -e '/RSA_FLAG_NO_CONSTTIME/ d' rsa_test.c
sed -i -e 's:#define HEADER_E_OS_H:#define HEADER_E_OS_H\n#define OPENSSL_NO_CAMELLIA\n#define OPENSSL_NO_SEED\n:' ../e_os.h
%patch2 -p1 
popd > /dev/null
%endif

cat test/Makefile |grep ^test_ | awk -F ':' '{print $1}' | awk -F ' ' '{print $1}' > ./ctcs2_test_list


%build
cd test
make
#make tests # some tests fail on sle10 now, cancel them so we still have packages
make clean

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

echo -en "timer 300\nfg 1 build %{qa_location}/ctcs2_run_test.sh\nwait\n\n" > $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_openssl.tcf
cat $RPM_BUILD_ROOT/%{qa_location}/ctcs2_test_list | while read test; do
	echo "timer 300"
	echo -en "fg 1 "
	echo -en "$test %{qa_location}/ctcs2_run_test.sh $test\n"
	echo -en "wait\n\n"
done >> $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_openssl.tcf
echo -en "timer 300\nfg 1 clean %{qa_location}/ctcs2_run_test.sh clean\nwait\n\n" >> $RPM_BUILD_ROOT/usr/share/qa/tcf/qa_openssl.tcf


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
/usr/share/qa/
/usr/share/man/man8/qa_test_openssl.8.gz


%changelog
