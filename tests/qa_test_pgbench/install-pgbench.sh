#!/bin/bash
BASE_ROOT=/usr/share/qa/qa_test_pgbench/

function _exit {
    local _ret=$1
    shift
    echo "$@"
    exit $_ret
}

cd $BASE_ROOT

if test -f postgresql-9.3.4.tar.bz2;then
    TAR_DIR=/usr/share/qa/qa_test_pgbench/postgresql-9.3.4
else
    echo "[system]can't find postgres package!"
fi

mkdir -p $BASE_ROOT/postgres
if test -d  $BASE_ROOT/postgres; then
   INSTALL_ROOT=$BASE_ROOT/postgres
else 
   echo "[system]created install dir faild!" 
fi

tar -xvf postgresql-9.3.4.tar.bz2
if test $? -ne 0; then
   _exit 1 "[postgres] unzip postgres and create dir failed!"
else
   echo "[postgres] unzip postgres and create dir successfully!"
fi

cd $TAR_DIR

./configure --prefix=$INSTALL_ROOT
if test $? -ne 0;then
    rm -rf $INSTALL_ROOT
    rm -rf $TAR_DIR
    _exit 1 "[SYSTEM] configure postgres failed!"
else
    echo "[SYSTEM] configure postgres completely "
fi

make
if test $? -ne 0;then
    rm -rf $INSTALL_ROOT
    rm -rf $TAR_DIR
    _exit 1 "[SYSTEM] build postgres failed!"
else
    echo "[SYSTEM] build postgres completely "
fi


make install
if test $? -ne 0;then
    rm -rf $INSTALL_ROOT
    rm -rf $TAR_DIR
    _exit 1 "[SYSTEM] make install postgres failed!"
else
    echo "[SYSTEM] make install postgres completely "
fi


