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
%define tcf_file          apache2-mod_perl.tcf
Summary:        apache2-mod_perl testsuites
License:        Apache-2.0
Requires:       %{apache_mmn}
Requires:       %{apache_suse_maintenance_mmn}
Requires:       apache2
Requires:       apache2-mod_perl
Requires:       perl = %{perl_version}
Requires:       perl-HTML-Parser
Requires:       perl-Tie-IxHash
Requires:       perl-URI
Requires:       perl-libwww-perl
Requires:       perl(Linux::Pid)
Url:            http://perl.apache.org/
Obsoletes:      mod_perl_2
Conflicts:      mod_perl
Version:        2.0.8
Release:        11.43
Source0:        http://ftp.de.debian.org/debian/pool/main/liba/libapache2-mod-perl2/libapache2-mod-perl2_2.0.8+httpd24-r1449661.orig.tar.gz
Source1:        test_apache2-mod_perl-run
Patch:          apache2-mod_perl-2.0.4-tests.diff
# PATCH-NEEDS-REBASE
Patch1:         lfs-perl-5.14.patch 
Patch2:         avoid-broken-provides.diff
Patch3:         apache24-mod_authz_host.patch
Icon:           mod_perl.xpm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
apache2-mod_perl testsuites


%prep
#%setup -q -n modperl-2.0 -a 1
%setup -q -n httpd24
%patch2 -p1
%patch3 -p1
#%patch1 -p1
find -name ".svn" -type d | xargs rm -rfv

%build
perl Makefile.PL INSTALLDIRS=vendor MP_APXS=`which %{apxs}` MP_APR_CONFIG=/usr/bin/apr-1-config MP_CCOPTS="$(%{apxs} -q CFLAGS)"
make %{?_smp_mflags}
# XXX mod_include/SSI does not include files when they are not named .shtml
mv t/htdocs/includes-registry/test.pl t/htdocs/includes-registry/test.shtml
mv t/htdocs/includes-registry/cgipm.pl t/htdocs/includes-registry/cgipm.shtml
sed 's/\.pl/.shtml/' t/htdocs/includes/test.shtml > tmpfile && mv tmpfile t/htdocs/includes/test.shtml
%ifnarch %arm
#
# Run tests
#
# Don't use sendfile because most systems on which this package will be built don't run a 
# kernel that has it implemented, actually
# (Files smaller than 256 bytes will be delivered via conventional read/write, so most of the tests would pass nevertheless.)
echo -e '\n\nEnableSendfile off' >> t/conf/extra.conf.in
#
# fix for bad_scripts.t in 1.99_12
# [Tue Mar 02 17:28:26 2004] [error] file permissions deny server execution/usr/src/packages/BUILD/modperl-2.0/ModPerl-Registry/t/cgi-bin/r_inherited.pl
if test -e ModPerl-Registry/t/cgi-bin/r_inherited.pl; then chmod +x ModPerl-Registry/t/cgi-bin/r_inherited.pl; fi
#
# 1.99_12_20040302 fix for t/hooks/cleanup.t and t/hooks/cleanup2.t
# [Tue Mar 02 18:38:41 2004] [error] [client 127.0.0.1] can't open /usr/src/packages/BUILD/modperl-2.0/t/htdocs/hooks/cleanup2: Permission denied at /usr/src/packages/BUILD/modperl-2.0/Apache-Test/lib/Apache/TestUtil.pm line 82.
#
# enable more apache modules
# we can't simply use a2enmod, since we are not root.
cat >> t/conf/extra.conf.in <<-EOF
        #LoadModule access_compat_module /usr/%_lib/apache2-prefork/mod_access_compat.so
        LoadModule authn_core_module /usr/%_lib/apache2-prefork/mod_authn_core.so
        LoadModule authz_core_module /usr/%_lib/apache2-prefork/mod_authz_core.so
        LoadModule authz_user_module %{_libdir}/apache2-prefork/mod_authz_user.so
        #LoadModule unixd_module      /usr/%_lib/apache2-prefork/mod_unixd.so
	LoadModule deflate_module    /usr/%_lib/apache2-prefork/mod_deflate.so
	LoadModule proxy_module      /usr/%_lib/apache2-prefork/mod_proxy.so
	LoadModule proxy_http_module /usr/%_lib/apache2-prefork/mod_proxy_http.so
EOF
mkdir -p t/htdocs/hooks
chmod 2770 t/htdocs/hooks
mkdir t/run
%endif
sed -i -e 's#^.*httpd24#    %{qa_dir}/%{name}#g' t/TEST
# Generate tcf file
test_list=`find t -name '*.t' | sed -e 's#^t/##g'`
echo "$test_list" | while read line; do
    test_name=`echo "$line" | sed -e 's/\.t$//g' | tr '/' '-'`
    cat >> %{tcf_file} <<END
timer 300
fg 1 $test_name %{qa_dir}/%{name}/t/TEST $line
wait

END
done


%install
# tcf file
install -m 755 -d $RPM_BUILD_ROOT%{qa_dir}/tcf
install -m 644 %{tcf_file} $RPM_BUILD_ROOT%{qa_dir}/tcf/%{tcf_file}
rm %{tcf_file}
# run script
install -m 755 -d $RPM_BUILD_ROOT%{qa_dir}/tools
install -m 755 %{S:1} $RPM_BUILD_ROOT%{qa_dir}/tools

install -m 755 -d $RPM_BUILD_ROOT%{qa_dir}/%{name}
rm -rf src docs todo
cp -Pr --preserve=mode,timestamps * $RPM_BUILD_ROOT%{qa_dir}/%{name}
find $RPM_BUILD_ROOT%{qa_dir}/%{name} -type d -exec chmod o+rwx {} \;
find $RPM_BUILD_ROOT%{qa_dir}/%{name} -type f -exec chmod o+rw {} \;


%files
%defattr(-,root,root)
%dir %{qa_dir}
%dir %{qa_dir}/tcf
%{qa_dir}/tcf/%{tcf_file}
%dir %{qa_dir}/tools
%{qa_dir}/tools/test_apache2-mod_perl-run
%{qa_dir}/%{name}

%changelog
