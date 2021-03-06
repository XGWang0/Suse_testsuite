#
# spec file for package qa_test_openssl
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


%define qa_location %{_datadir}/qa/qa_test_openssl

%if 0%{?suse_version} < 1120
%define Ver 0.9.8j
%else
%if 0%{?sle_version} <= 120100 
%define Ver 1.0.1i
%endif
%if 0%{?sle_version} >= 120200
%define Ver 1.0.2h
%endif
%endif

Name:           qa_test_openssl
Version:        %{Ver}
Release:        0
Summary:        Unittests for openssl framework using the system openssl
License:        OpenSSL Open Source License; GPL-3+
Group:          SuSE internal
Source0:        %{name}-%{version}.tar.bz2
Source1:        test_openssl-run
Source2:        qa_test_openssl.8
Source3:        generate_openssl_tests.sh
Source4:        qa_test_openssl_benchmark.sh
Source5:        process_benchmarks.pl
Patch0:         qa_test_openssl-Makefile-%{Ver}.patch
Patch1:         qa_test_openssl-fips_test.patch
Patch2:         dsatest.patch
Patch3:         ecdhtest.patch
Patch4:         ecdsatest.patch
Patch5:         rc4test_remove_cpuid.patch
BuildRequires:  bc
BuildRequires:  ctcs2
BuildRequires:  gcc
BuildRequires:  libopenssl-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  perl
Requires:       bc
Requires:       ctcs2
Requires:       gcc
Requires:       libopenssl-devel
Requires:       make
Requires:       openssl
Requires:       perl
Provides:       qa_openssl
Obsoletes:      qa_openssl
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#everytime is noarch
BuildArch:      noarch

%description
Test cases for openssl package.

%prep
%setup -q
echo -en "#!/bin/bash\napp=\"/usr/share/qa/qa_test_openssl/apps/openssl\"\nif [ ! -f \"\$app\" ];then\n    ln -s /usr/bin/openssl %{qa_location}/apps/\nfi\ncd %{qa_location}/test\nmake \$1\n[[ \$? -eq 0 ]] && exit 0 || exit 1\n" > ./ctcs2_run_test.sh
chmod +x ./ctcs2_run_test.sh

# fix the perl invocations
sed -i -e 's:/usr/local/bin/perl:%{_bindir}/perl:g' util/*.{pl,sh} util/pl/*.pl
sed -i -e 's:/bin/env perl:%{_bindir}/perl:g' util/*.{pl,sh} util/pl/*.pl

%patch0 -p1

%if 0%{?suse_version} >= 1220
%patch1 -p1
%endif

%if 0%{?sle_version} >= 120200
%patch5 -p1
%endif

cat test/Makefile | grep ^test_ | awk -F ':' '{print $1}' | awk -F ' ' '{print $1}' | sort > ./ctcs2_test_list

# Fix missing define
sed -i -e 's:#include <openssl/sha.h>:#include <openssl/sha.h>\n#define OPENSSL_PIC:' test/rc4test.c

# TODO -- is for openssl-1.0.1q
#sed -i -e 's:#include <openssl/ssl.h>:#include <openssl/ssl.h>\n# define SSL3_HM_HEADER_LENGTH                   4:' ssl/clienthellotest.c

%build
cd test
make %{?_smp_mflags}
make tests -j1
make clean -j1

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
install -m 755 -d %{buildroot}%{_datadir}/qa/tcf
install -m 755 -d %{buildroot}%{_datadir}/qa/tools
install -m 755 -d %{buildroot}/%{qa_location}
install -m 755 -d %{buildroot}/%{qa_location}/tcf
install -m 755 %{SOURCE1} %{buildroot}%{_datadir}/qa/tools
install -m 755 %{SOURCE4} %{buildroot}/%{qa_location}
install -m 755 %{SOURCE5} %{buildroot}/%{qa_location}
cp -a * %{buildroot}/%{qa_location}

echo -en "timer 300\nfg 1 clean %{qa_location}/ctcs2_run_test.sh clean\nwait\n\n" > %{buildroot}%{_datadir}/qa/tcf/qa_openssl.tcf
echo -en "timer 300\nfg 1 build %{qa_location}/ctcs2_run_test.sh\nwait\n\n" >> %{buildroot}%{_datadir}/qa/tcf/qa_openssl.tcf
cat %{buildroot}/%{qa_location}/ctcs2_test_list | while read test; do
	echo "timer 300"
	echo -en "fg 1 "
	echo -en "$test %{qa_location}/ctcs2_run_test.sh $test\n"
	echo -en "wait\n\n"
done >> %{buildroot}%{_datadir}/qa/tcf/qa_openssl.tcf
echo -en "timer 300\nfg 1 clean %{qa_location}/ctcs2_run_test.sh clean\nwait\n\n" >> %{buildroot}%{_datadir}/qa/tcf/qa_openssl.tcf
echo -en "timer 6000\nfg 1 openssl_benchmark %{qa_location}/qa_test_openssl_benchmark.sh\nwait\n\n" >> %{buildroot}%{_datadir}/qa/tcf/qa_openssl.tcf


%files
%defattr(-, root, root)
%{_datadir}/qa/
%{_mandir}/man8/qa_test_openssl.8.gz

%changelog
