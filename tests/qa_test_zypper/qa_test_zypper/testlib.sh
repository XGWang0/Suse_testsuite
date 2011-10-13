#!/bin/bash

REPO='http://dist.suse.de/ibs/QA:/Head:/Devel/'
REPO_NAME='qa_test'
PACKAGE='qa_sample'
PACKAGE_DESC='(rd-)qa internal package for training'

function failed {
       echo "$1. Test failed"
       exit -1
}

function assert_root {
       [ `id -u` == 0 ] || failed "You must be root to run this test. Exiting..."
       export LANG=C
}

function assert_output {
       r1=`zypper $1`
       r2=`zypper $2`
       [ "$r1" == "$r2" ] || failed "zypper $1 and zypper $2 have different output"
}

function assert_result {
       zypper $1 | grep "$2" > /dev/null
       if [ $? != 0 ]; then
               zypper $1 | grep "$3" > /dev/null
               if [ $? != 0 ]; then
                       failed "There is no $2 or $3 in the result of command: $1"
               fi
       fi
}

function no_result {
    zypper $1 | grep "$2" > /dev/null
    [ $? != 0 ] || failed "Should not exist $2 in the result of command: $1"
}

function assert_file {
    zypper $1 > /dev/null
    [ -e $2 ] || failed "$2 is not exist after execute command: $1"
}

