# vim: ft=apache
#
# spec file for package qa_test_apache2-mod_perl
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           qa_test_apache2-mod_perl
BuildRequires:  apache-rpm-macros
BuildRequires:  apache2-devel
BuildRequires:  db-devel
BuildRequires:  ed
BuildRequires:  netcfg
BuildRequires:  pcre-devel
BuildRequires:  perl
BuildRequires:  perl-BSD-Resource
BuildRequires:  perl-Compress-Zlib
BuildRequires:  perl-Tie-IxHash
BuildRequires:  perl-libwww-perl
BuildRequires:  sudo
%if 0%{sles_version} == 9
BuildRequires:  openldap2-devel
%endif
%define apxs /usr/sbin/apxs
%define apache apache2
%define apache_libexecdir %(%{apxs} -q LIBEXECDIR)
%define apache_sysconfdir %(%{apxs} -q SYSCONFDIR)
%define apache_includedir %(%{apxs} -q INCLUDEDIR)
%define apache_serverroot %(%{apxs} -q PREFIX)
%define apache_mmn        %(MMN=$(%{apxs} -q LIBEXECDIR)_MMN; test -x $MMN && $MMN)
%define qa_dir		  /usr/share/qa
%define test_user	  nobody
%define tcf_file          apache2-mod_perl.tcf
Summary:        Apache mod perl testsuites
License:        Apache-2.0
Group:          SuSE internal
Requires:       %{apache_mmn}
Requires:       %{apache_suse_maintenance_mmn}
Requires:       apache2
Requires:       perl = %{perl_version}
Requires:       perl-HTML-Parser
Requires:       perl-Tie-IxHash
Requires:       perl-URI
Requires:       perl-libwww-perl
Requires:       perl(Linux::Pid)
Url:            http://perl.apache.org/
Obsoletes:      qa_test_apache_testsuite
Version:        2.0.9
Release:        0
Source0:        mod_perl-2.0.9.tar.gz
Source1:        test_apache2_mod_perl-run
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
apache2 mod_perl testsuites

%prep
%setup -q -n mod_perl-2.0.9

%build
perl Makefile.PL INSTALLDIRS=vendor MP_APXS=`which %{apxs}` MP_APR_CONFIG=/usr/bin/apr-1-config MP_CCOPTS="$(%{apxs} -q CFLAGS)"
make %{?_smp_mflags}
sed -ie 's#.*/mod_perl-%{version}#    %{qa_dir}/%{name}#g' t/TEST
# Generate tcf file
mkdir tcf
test_list=`find t -name '*.t' | sed -e 's#^t/##g' | sort -h` 
echo "$test_list" | while read line; do
    test_name=`echo "$line" | sed -e 's/\.t$//g' | tr '/' '-'`
    cat >> tcf/%{tcf_file} <<END
timer 300 
fg 1 $test_name %{qa_dir}/%{name}/t/TEST -apxs \`which apxs\` -httpd \`which httpd\` -verbose $line
wait

END
done

%install
install -m 755 -d %{buildroot}%{qa_dir}
install -m 755 -d %{buildroot}%{qa_dir}/tools
install -m 755 %{S:1} %{buildroot}%{qa_dir}/tools
install -m 755 -d %{buildroot}%{qa_dir}/%{name}
mv * %{buildroot}%{qa_dir}/%{name}
install -m 755 -d %{buildroot}%{qa_dir}/tcf
ln -s ../%{name}/tcf/%{tcf_file} %{buildroot}%{qa_dir}/tcf/

%clean
rm -rf $RPM_BUILD_ROOT

%post
chown -R %{test_user}.%{test_user} %{qa_dir}/%{name}/*

%files
%defattr(-,root,root)
%dir %{qa_dir}
%{qa_dir}/%{name}
%dir %{qa_dir}/tools
%{qa_dir}/tools/test_apache2_mod_perl-run
%dir %{qa_dir}/tcf
%{qa_dir}/tcf/%{tcf_file}

%changelog
