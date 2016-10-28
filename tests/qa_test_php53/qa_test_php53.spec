#
# spec file for package qa_test_php53
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


%define qa_location %{_datadir}/qa/qa_test_php53
%define qa_server_location /srv/www/htdocs/php53-tests
Name:           qa_test_php53
Version:        5.3.29
Release:        0
Summary:        PHP5 test suite
License:        PHP
Group:          System/Packages
Url:            http://www.php.net
Source0:        php-%{version}.tar.bz2
Source1:        test_php53-run
Source2:        qa_test_php53.8
Source3:        apache2-php5-prepare.sh
Source4:        test_php53-server-run
Source5:        expected_fail.list
Source6:        source_skipped.list
Patch0:         server-test-config.patch
Requires:       ctcs2
Requires:       mysql
Requires:       php53 >= 5.3.0
Requires:       php53-bcmath
Requires:       php53-bz2
Requires:       php53-calendar
Requires:       php53-ctype
Requires:       php53-dom
Requires:       php53-exif
Requires:       php53-gd
Requires:       php53-gettext
Requires:       php53-gmp
Requires:       php53-iconv
Requires:       php53-mbstring
Requires:       php53-mcrypt
Requires:       php53-mysql
Requires:       php53-shmop
Requires:       php53-soap
Requires:       php53-sqlite
Requires:       php53-sysvmsg
Requires:       php53-sysvsem
Requires:       php53-sysvshm
Requires:       php53-tokenizer
Requires:       php53-wddx
Requires:       php53-xsl
Requires:       php53-zlib
Provides:       qa_test_php5
Obsoletes:      qa_test_php5
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
%if 0%{?suse_version} <= 1030
Requires:       php53-mhash
%endif

%description
This package contains wide range of PHP5 tests. These tests include
basic language constructs (operators, control flow, etc), object
oriented language constructs (classes, etc), basic functions tests
(strlen, "function" construct, etc), php extensions (java, mbstring,
etc).

%package server
Summary:        PHP5 test suite
License:        Other uncritical OpenSource License
Group:          System/Packages
Requires:       %{name} = %{version}
Requires:       apache2-mod_php53
Provides:       qa_php5-server
Obsoletes:      qa_php5-server

%description server
This package contains wide range of PHP5 tests. These tests include
basic language constructs (operators, control flow, etc), object
oriented language constructs (classes, etc), basic functions tests
(strlen, "function" construct, etc), php extensions (java, mbstring,
etc).

%prep
%setup -q -n php-%{version}
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
find . -name *.phpt|grep -vf %{SOURCE5}|grep -vf %{SOURCE6}|sort > ./ctcs2_test_order

%patch0 -p1

%install
install -m 755 -d %{buildroot}%{_mandir}/man8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8
gzip %{buildroot}%{_mandir}/man8/%{name}.8
cd ..
install -d -m 0755 %{buildroot}%{qa_location}
install -m 755 %{SOURCE3} %{buildroot}%{qa_location}
install -d -m 0755 %{buildroot}%{qa_server_location}
install -m 755 %{SOURCE5} %{buildroot}%{qa_location}
install -m 755 %{SOURCE6} %{buildroot}%{qa_location}

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
touch %{buildroot}%{qa_location}/tcf/qa_php53.tcf
touch %{buildroot}%{qa_location}/tcf/qa_php53-server.tcf
ln -s ../qa_test_php53/tcf/qa_php53.tcf %{buildroot}%{_datadir}/qa/tcf/
ln -s ../qa_test_php53/tcf/qa_php53-server.tcf %{buildroot}%{_datadir}/qa/tcf/
install -m 755 %{SOURCE1} %{buildroot}%{_datadir}/qa/tools
install -m 755 %{SOURCE4} %{buildroot}%{_datadir}/qa/tools

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
%{_mandir}/man8/qa_test_php53.8%{ext_man}
%{_datadir}/qa/
%{_datadir}/qa/tcf/qa_php53.tcf
%{_datadir}/qa/tools
%exclude %{_datadir}/qa/tcf/qa_php53-server.tcf
%exclude %{_datadir}/qa/tools/test_php53-server-run
%exclude %{qa_location}/tcf/qa_php53-server.tcf
%exclude %{qa_location}/server-tests-config.php
%exclude %{qa_location}/server-tests.php

%files server
%defattr(-, root, root)
%{qa_server_location}
%{_datadir}/qa/tcf/qa_php53-server.tcf
%{_datadir}/qa/tools/test_php53-server-run
%{qa_location}/tcf/qa_php53-server.tcf
%{qa_location}/server-tests-config.php
%{qa_location}/server-tests.php

%changelog
%changelog
