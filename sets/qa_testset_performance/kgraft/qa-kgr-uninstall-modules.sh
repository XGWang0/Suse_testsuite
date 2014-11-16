#!/bin/bash

HOST_CPU=$(uname -m)
QA_KGRAFT_PATH_ROOT=/usr/share/qa/qa_test_kgraft_patch
pushd ${QA_KGRAFT_PATH_ROOT}

pushd ${QA_KGRAFT_PATH_ROOT}
if test ! -d qa-kgraft-patch; then
    return
fi
pushd qa-kgraft-patch
for flavor in $(ls /usr/src/linux-obj/${HOST_CPU} 2>/dev/null); do
    krel=$(make -s -C /usr/src/linux-obj/${HOST_CPU}/$flavor kernelrelease)
    pushd "$PWD/obj/$flavor"
    for module in *.ko; do
        rm /lib/modules/${krel}/kgraft/${module}
    done
    popd
done
popd
popd
