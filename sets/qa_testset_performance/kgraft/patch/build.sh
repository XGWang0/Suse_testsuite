#!/bin/bash

zypper -n install -l kernel-syms kgraft-devel rpm-build
if test $? -ne 0; then
    echo "Failed to install kernel-syms or kgraft-devel"
    exit 1
fi

rpmbuild --define="_sourcedir $PWD" kgraft-patch-getpid-qa.spec -ba
if test $? -ne 0; then
   echo "Failed to build the rpm package"
fi

mname=$(uname -m)
pushd /usr/src/packages/RPMS/${mname}
for filename in kgraft-patch-getpid-qa*.rpm;do
    echo "Installing ${filename}"
    zypper -n install -l ${filename}
    if test $? -ne 0;then
        echo "Faile to install ${filename}"
	continue
    fi
    pushd /proc
    for PID in [0-9]*; do
       if test "X$(cat ${PID}/kgr_in_progress)" == X1; then
           kill -STOP ${PID}
           kill -CONT ${PID}
       fi
    done
    unset PIDS
    for PID in [0-9]*; do
        if test "X$(cat ${PID}/kgr_in_progress)" == X1; then
            COMM="$(cat ${PID}/comm)"
            echo "$COMM (${PID}) still in progress:"
	    cat ${PID}/stack
	    echo -e "======================\n"
            PIDS="$PIDS $PID"
        fi
    done
    if test -z "${PIDS}"; then
	echo "NO prcess is kgr_in_progress"
    else
        echo "Some process still is kgr_in_progress"
        echo "Manully fixed by yourself"
        break
    fi
    popd
done
popd
