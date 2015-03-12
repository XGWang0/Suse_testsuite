#!/bin/bash

HOST_CPU=$(uname -m)
QA_KGRAFT_PATH_ROOT=/usr/share/qa/qa_test_kgraft_patch

DEBUG=N

if test "X${DEBUG}" == "XY"; then
    :
else
    QA_FLAGS='QA_TEST_DELETE_IT=Y'
fi

pushd ${QA_KGRAFT_PATH_ROOT}
tar xf qa-kgraft-patch.tar.xz
pushd qa-kgraft-patch
set -- *
#export INSTALL_MOD_PATH=%buildroot
export INSTALL_MOD_DIR=kgraft
for flavor in $(ls /usr/src/linux-obj/${HOST_CPU} 2>/dev/null); do
	mkdir -p "obj/$flavor"
	cp "$@" "obj/$flavor"
	make -C /usr/src/linux-obj/${HOST_CPU}/${flavor} M="$PWD/obj/$flavor" ${QA_FLAGS} modules
    make -C /usr/src/linux-obj/${HOST_CPU}/${flavor} M="$PWD/obj/$flavor" ${QA_FLAGS} modules_install
done
popd
popd

depmod
