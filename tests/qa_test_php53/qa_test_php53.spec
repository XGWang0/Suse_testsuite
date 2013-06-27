#
# spec file for package qa_php5 (Version 5.3.26)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           qa_test_php53
%define qa_location /usr/share/qa/qa_test_php53
%define qa_server_location /srv/www/htdocs/php53-tests
Version:        5.3.26
Release:        1
License:        PHP
Group:          System/Packages
AutoReqProv:    on
Url:            http://www.php.net
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Summary:        PHP5 test suite
Source0:        php-%{version}.tar.bz2
Source1:        test_php53-run
Source2:	qa_test_php53.8
Source3:	apache2-php5-prepare.sh
Source4:	test_php53-server-run
Source5:	expected_fail.list
Source6:	source_skipped.list
Patch0:		server-test-config.patch
BuildArch:      noarch
Provides:	qa_test_php5
Obsoletes:	qa_test_php5
Requires:       php53 >= 5.3.0 php53-wddx php53-ctype php53-mbstring php53-bz2 php53-bcmath php53-ctype php53-exif php53-gd php53-gettext php53-gmp php53-mcrypt php53-shmop php53-sysvshm php53-sysvsem php53-zlib php53-calendar php53-iconv php53-tokenizer php53-dom php53-soap mysql php53-sysvmsg php53-xsl php53-mysql php53-sqlite
Requires:       ctcs2
%if %suse_version <= 1030
Requires:       php53-mhash
%endif

%description
This package contains wide range of PHP5 tests. These tests include
basic language constructs (operators, control flow, etc), object
oriented language constructs (classes, etc), basic functions tests
(strlen, "function" construct, etc), php extensions (java, mbstring,
etc).



Authors:
--------
    Andrei Zmievski <andrei@ispi.net>
    Danny Heijl <Danny.Heijl@cevi.be>
    Frank M. Kromann <fmk@swwwing.com>
    Rasmus Lerdorf <rasmus@php.net>
    Sam Ruby <rubys@us.ibm.com>
    Sascha Schumann <sascha@schumann.cx>
    Stefan Roehrich <sr@linux.de>
    Thies C. Arntzen <thies@digicol.de>
    Uwe Steinmann <steinm@php.net>

%package server
License:        Other uncritical OpenSource License
Summary:        PHP5 test suite
Group:          System/Packages
Provides:	qa_php5-server
Obsoletes:	qa_php5-server
Requires:       %{name} = %{version} apache2-mod_php53

%description server
This package contains wide range of PHP5 tests. These tests include
basic language constructs (operators, control flow, etc), object
oriented language constructs (classes, etc), basic functions tests
(strlen, "function" construct, etc), php extensions (java, mbstring,
etc).



Authors:
--------
    Andrei Zmievski <andrei@ispi.net>
    Danny Heijl <Danny.Heijl@cevi.be>
    Frank M. Kromann <fmk@swwwing.com>
    Rasmus Lerdorf <rasmus@php.net>
    Sam Ruby <rubys@us.ibm.com>
    Sascha Schumann <sascha@schumann.cx>
    Stefan Roehrich <sr@linux.de>
    Thies C. Arntzen <thies@digicol.de>
    Uwe Steinmann <steinm@php.net>

%prep
%setup -n php-%{version} -q
cd ..

search_for_tests() {
        local sub
        if [ $(basename $1) = "tests" ]
        then
                test_dir=${1#*php-%{version}}
                mkdir -p $qa_dir/${test_dir%/tests}
                cp -r $php_dir/$test_dir $qa_dir/$test_dir
                return
        fi
        for sub in $1/*
        do
                if [ -d $sub ]
                then
                        search_for_tests $sub
                fi
        done
}

php_dir=$(pwd)/php-%{version}
qa_dir=$(pwd)
search_for_tests $php_dir
cp $php_dir/*.php $qa_dir
cp $php_dir/README.TESTING* $qa_dir
cp $php_dir/php.gif $qa_dir

rm -rf $php_dir/*

find . -name *win32* | xargs rm
find . -name *.phpt|grep -vf %{S:5}|grep -vf %{S:6}|sort > ./ctcs2_test_order

%patch0 -p1

%install
install -m 755 -d $RPM_BUILD_ROOT/usr/share/man/man8
install -m 644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man8
gzip $RPM_BUILD_ROOT/usr/share/man/man8/%{name}.8
cd ..
install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}
install -m 755 %{S:3} $RPM_BUILD_ROOT%{qa_location}
install -d -m 0755 $RPM_BUILD_ROOT%{qa_server_location}
install -m 755 %{S:5} $RPM_BUILD_ROOT%{qa_location}
install -m 755 %{S:6} $RPM_BUILD_ROOT%{qa_location}

cp php.gif $RPM_BUILD_ROOT/%{qa_location}
cp run-tests.php $RPM_BUILD_ROOT/%{qa_location}
cp ctcs2_test_order $RPM_BUILD_ROOT/%{qa_location}
cp server-tests.php $RPM_BUILD_ROOT/%{qa_location}
cp server-tests-config.php $RPM_BUILD_ROOT/%{qa_location}
cp -r ext sapi tests Zend $RPM_BUILD_ROOT/%{qa_location}
cp -r ext sapi tests Zend $RPM_BUILD_ROOT/%{qa_server_location}

install -d -m 0755 $RPM_BUILD_ROOT%{qa_location}/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tcf
install -d -m 0755 $RPM_BUILD_ROOT/usr/share/qa/tools
touch $RPM_BUILD_ROOT%{qa_location}/tcf/qa_php53.tcf
touch $RPM_BUILD_ROOT%{qa_location}/tcf/qa_php53-server.tcf
ln -s ../qa_test_php53/tcf/qa_php53.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
ln -s ../qa_test_php53/tcf/qa_php53-server.tcf $RPM_BUILD_ROOT/usr/share/qa/tcf/
install -m 755 %{S:1} $RPM_BUILD_ROOT/usr/share/qa/tools
install -m 755 %{S:4} $RPM_BUILD_ROOT/usr/share/qa/tools

%clean
rm -rvf $RPM_BUILD_ROOT

%post
TEST_ENV="TEST_PHP_EXECUTABLE=%{_bindir}/php REPORT_EXIT_STATUS=1 TEST_PHP_SRCDIR=%{qa_location} TEST_PHP_DETAILED=1 NO_INTERACTION=1"

cat -n %{qa_location}/ctcs2_test_order | grep -v '[0-9]*[ ]*#' | while read test_num line; do
    echo "timer 300"
    echo -en "fg 1 "
    printf PHPTEST%%0.4d $test_num 
    echo -en " env $TEST_ENV %{_bindir}/php -d 'open_basedir=' -d 'output_buffering=0' -d 'memory_limit=-1' %{qa_location}/run-tests.php %{qa_location}/$line \n"
    echo -en "wait\n\n"
done > %{qa_location}/tcf/qa_php53.tcf

%post server
cat -n %{qa_location}/ctcs2_test_order | grep -v '[0-9]*[ ]*#' | while read test_num line; do
    echo "timer 300"
    echo -en "fg 1 "
    printf PHPSERVER%%0.4d $test_num 
    echo -en " %{_bindir}/php -d 'open_basedir=' -d 'output_buffering=0' -d 'memory_limit=-1' %{qa_location}/server-tests.php -c %{qa_location}/server-tests-config.php -d %{qa_location}/$line \n"
    echo -en "wait\n\n"
done > %{qa_location}/tcf/qa_php53-server.tcf

%files
%defattr(-, root, root)
/usr/share/man/man8/qa_test_php53.8.gz
/usr/share/qa/
/usr/share/qa/tcf/qa_php53.tcf
/usr/share/qa/tools
%exclude /usr/share/qa/tcf/qa_php53-server.tcf
%exclude /usr/share/qa/tools/test_php53-server-run
%exclude %{qa_location}/tcf/qa_php53-server.tcf
%exclude %{qa_location}/server-tests-config.php
%exclude %{qa_location}/server-tests.php

%files server
%defattr(-, root, root)
%{qa_server_location}
/usr/share/qa/tcf/qa_php53-server.tcf
/usr/share/qa/tools/test_php53-server-run
%{qa_location}/tcf/qa_php53-server.tcf
%{qa_location}/server-tests-config.php
%{qa_location}/server-tests.php

%changelog
* Tue Nov 22 2011 - jtang@suse.com
- Rename 
* Tue Nov 08 2011 - jtang@suse.com
- Create new version
* Wed Aug 17 2011 - llipavsky@suse.cz
- Remove qa_dummy dependency
* Wed Aug 10 2011 - llipavsky@suse.cz
- Package rename: qa_php5 -> qa_test_php5
* Mon Aug 04 2008 ro@suse.de
- drop mhash requires for >= 11.0
* Thu Jan 10 2008 mmrazik@suse.cz
- start apache2 automaticaly before running the tests
* Wed Nov 08 2006 mmrazik@suse.cz
- build failures fixed (removed executable permission for some txt files)
* Thu Oct 19 2006 ro@suse.de
- drop php5-mysqli from requires (does not exist)
* Thu Jun 22 2006 ro@suse.de
- remove selfprovides
* Wed Feb 01 2006 mmrazik@suse.cz
- php 5.1.2 upgrade
- php5 CLI test support
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jan 18 2006 mmrazik@suse.cz
- fixed tcf location (updated QA Packaging Guidelines)
- created run-script (/usr/share/qa/tools/test_php5-run)
* Mon Jan 09 2006 mmrazik@suse.cz
- fixed dependencies
 - fixed environment for some tests (moving some files to /srv/www/htdocs/...)
* Thu Jan 05 2006 mmrazik@suse.cz
- initial release
