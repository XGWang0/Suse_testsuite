#
# spec file for package qa_test_php
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


%define php php5
%define ver 5.5.9
%define qa_location %{_datadir}/qa/qa_test_php
%define qa_server_location /srv/www/htdocs/php-tests
%if 0%{?suse_version} < 1130
%define php php5
%define ver 5.2.14
%endif
%if 0%{?suse_version} == 1320
%define php php
%define ver 7.0.3
%endif
Name:           qa_test_php
Version:        %{ver}
Release:        0
Summary:        PHP test suite
License:        PHP
Group:          System/Packages
Url:            http://www.php.net
Source0:        php-%{version}.tar.bz2
Source1:        test_php-run
Source2:        qa_test_php.8
Source3:        apache2-php-prepare.sh
Source4:        test_php-server-run
Patch0:         server-test-config-%{ver}.patch
Patch1:         syntax_fix.patch
#Provides:	qa_php5
Requires:       ctcs2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
#Obsoletes:	qa_php5
%if 0%{?suse_version} == 1320
Requires:       mysql
Requires:       php7 >= 7.0.3
Requires:       php7-bcmath
Requires:       php7-bz2
Requires:       php7-ctype
Requires:       php7-dom
Requires:       php7-exif
Requires:       php7-gd
Requires:       php7-gettext
Requires:       php7-gmp
Requires:       php7-iconv
Requires:       php7-mbstring
Requires:       php7-mcrypt
Requires:       php7-mysql
Requires:       php7-shmop
Requires:       php7-soap
Requires:       php7-sysvmsg
Requires:       php7-sysvsem
Requires:       php7-sysvshm
Requires:       php7-tokenizer
Requires:       php7-wddx
Requires:       php7-xsl
Requires:       php7-zip
%endif
%if 0%{?suse_version} < 1320
Requires:       mysql
Requires:       php5 >= 5.0.0
Requires:       php5-bcmath
Requires:       php5-bz2
Requires:       php5-calendar
Requires:       php5-ctype
Requires:       php5-dom
Requires:       php5-exif
Requires:       php5-gd
Requires:       php5-gettext
Requires:       php5-gmp
Requires:       php5-iconv
Requires:       php5-mbstring
Requires:       php5-mcrypt
Requires:       php5-mysql
Requires:       php5-shmop
Requires:       php5-soap
Requires:       php5-sysvmsg
Requires:       php5-sysvsem
Requires:       php5-sysvshm
Requires:       php5-tokenizer
Requires:       php5-wddx
Requires:       php5-xsl
Requires:       php5-zlib
%endif
%if 0%{?suse_version} <= 1030
Requires:       php5-dbase
Requires:       php5-mhash
%endif
%if 0%{?suse_version} <= 1130
Requires:       php5-sqlite
%endif

%description
This package contains wide range of PHP tests. These tests include
basic language constructs (operators, control flow, etc), object
oriented language constructs (classes, etc), basic functions tests
(strlen, "function" construct, etc), php extensions (java, mbstring,
etc).

%package server
Summary:        PHP test suite
License:        Other uncritical OpenSource License
# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"
Group:          System/Paearch_for_tests $php_dirsearch_for_tests $php_dirkages
Requires:       %{name} = %{version}
Requires:       apache2-mod_php7

%description server
This package contains wide range of PHP5 tests. These tests include
basic language constructs (operators, control flow, etc), object
oriented language constructs (classes, etc), basic functions tests
(strlen, "function" construct, etc), php extensions (java, mbstring,
etc).

%prep
%setup -q -n php-%{version}

%if 0%{?suse_version} <= 1130
%patch1 -p1
%endif
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
find . -name *.phpt |sort > ./ctcs2_test_order

%patch0 -p1

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
cd ..
install -d -m 0755 %{buildroot}%{qa_location}
install -m 755 %{SOURCE3} %{buildroot}%{qa_location}
install -d -m 0755 %{buildroot}%{qa_server_location}

cp php.gif %{buildroot}/%{qa_location}
cp run-tests.php %{buildroot}/%{qa_location}
cp ctcs2_test_order %{buildroot}/%{qa_location}
cp server-tests.php %{buildroot}/%{qa_location}
cp server-tests-config.php %{buildroot}/%{qa_location}
cp -r ext sapi tests Zend %{buildroot}/%{qa_location}
cp -r ext sapi tests Zend %{buildroot}/%{qa_server_location}

install -d -m 0755 %{buildroot}%{qa_location}/tcf
install -d -m 0755 %{buildroot}%{_datadir}/qa/tcf
install -d -m 0755 %{buildroot}%{_datadir}/qa/tools
touch %{buildroot}%{qa_location}/tcf/qa_php.tcf
touch %{buildroot}%{qa_location}/tcf/qa_php-server.tcf
ln -s ../qa_test_php/tcf/qa_php.tcf %{buildroot}%{_datadir}/qa/tcf/
ln -s ../qa_test_php/tcf/qa_php-server.tcf %{buildroot}%{_datadir}/qa/tcf/
install -m 755 %{SOURCE1} %{buildroot}%{_datadir}/qa/tools
install -m 755 %{SOURCE4} %{buildroot}%{_datadir}/qa/tools

%post
TEST_ENV="TEST_PHP_EXECUTABLE=%{_bindir}/%{php} REPORT_EXIT_STATUS=1 TEST_PHP_SRCDIR=%{qa_location} TEST_PHP_DETAILED=1 NO_INTERACTION=1"

cat -n %{qa_location}/ctcs2_test_order | grep -v '[0-9]*[ ]*#' | while read test_num line; do
    echo "timer 300"
    echo -en "fg 1 "
    printf PHPTEST%%0.4d $test_num
    echo -en " env $TEST_ENV %{_bindir}/%{php} -d 'open_basedir=' -d 'output_buffering=0' -d 'memory_limit=-1' %{qa_location}/run-tests.php %{qa_location}/$line \n"
    echo -en "wait\n\n"
done > %{qa_location}/tcf/qa_php.tcf

%post server
cat -n %{qa_location}/ctcs2_test_order | grep -v '[0-9]*[ ]*#' | while read test_num line; do
    echo "timer 300"
    echo -en "fg 1 "
    printf PHPSERVER%%0.4d $test_num
    echo -en " %{_bindir}/%{php} -d 'open_basedir=' -d 'output_buffering=0' -d 'memory_limit=-1' %{qa_location}/server-tests.php -c %{qa_location}/server-tests-config.php -d %{qa_location}/$line \n"
    echo -en "wait\n\n"
done > %{qa_location}/tcf/qa_php-server.tcf

%files
%defattr(-, root, root)
%{_mandir}/man8/qa_test_php.8%{ext_man}
%{_datadir}/qa/
%{_datadir}/qa/tcf/qa_php.tcf
%{_datadir}/qa/tools
%exclude %{_datadir}/qa/tools/test_php-server-run
%exclude %{_datadir}/qa/tcf/qa_php-server.tcf
%exclude %{qa_location}/tcf/qa_php-server.tcf
%exclude %{qa_location}/server-tests-config.php
%exclude %{qa_location}/server-tests.php

%files server
%defattr(-, root, root)
%{qa_server_location}
%{_datadir}/qa/tools/test_php-server-run
%{_datadir}/qa/tcf/qa_php-server.tcf
%{qa_location}/tcf/qa_php-server.tcf
%{qa_location}/server-tests-config.php
%{qa_location}/server-tests.php

%changelog
%changelog
