#!/bin/bash

RPM_PACKAGE_NAME=qa-kgraft-patch

tar -c -J -f ${RPM_PACKAGE_NAME}.tar.xz ${RPM_PACKAGE_NAME}

zypper -n install -l kernel-syms kgraft-devel rpm-build
if test $? -ne 0; then
    echo "Failed to install kernel-syms or kgraft-devel"
    exit 1
fi

rpmbuild --define="_sourcedir $PWD" ${RPM_PACKAGE_NAME}.spec -ba
if test $? -ne 0; then
   echo "Failed to build the rpm package"
   exit 1
fi

mname=$(uname -m)
pushd /usr/src/packages/RPMS/${mname}
for filename in ${RPM_PACKAGE_NAME}*.rpm;do
    echo "Installing ${filename}"
    zypper -n install -l ${filename}
    if test $? -ne 0;then
        echo "Faile to install ${filename}"
	    continue
    fi
done
popd
