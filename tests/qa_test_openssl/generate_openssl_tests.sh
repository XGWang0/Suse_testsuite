#!/bin/bash
# Created by <tchvatal@suse.cz>
# Distribute under GPL-3 or later.

print_help() {
	echo "Usage:"
	echo "    $0 <VERSION>"
	exit 0
}

extract_item() {
	if [[ -z ${1} ]]; then
		echo "No file specified to unpack"
		exit 1
	fi

	tar -xzpf "${WORKDIR}/${TARBALL}" "${TARBALL%.tar.*}"/${1}
	if [[ $? -ne 0 ]]; then
		echo "Failed to extract \"${1}\" from \"${TARBALL}\""
		exit 1
	fi

}

extract_tests() {
	local items="test util Makefile.shared e_os.h apps/openssl.cnf apps/CA.sh apps/server2.pem certs"
	local i

	pushd "${PACKAGE}" > /dev/null

	for i in ${items}; do
		extract_item ${i}
	done
	mv "${TARBALL%.tar.*}"/* ./ && rm -rf "${TARBALL%.tar.*}"

	popd > /dev/null
}

fix_test_symlinks() {
	local f
	local symlinks=""
	local slink
	pushd "${PACKAGE}" > /dev/null

	for f in test/*; do
		slink=`readlink $f`
        slink=${slink#$OLD_NAME_VER}
		if [[ ${slink} = ..* ]]; then
			extract_item ${slink/..\/}
		fi
	done
    for i in ${items}; do
        extract_item ${i}
    done

    cp "${TARBALL%.tar.*}"/* ./ && rm -rf "${TARBALL%.tar.*}"

	popd > /dev/null
}

fix_test_executable() {
	pushd "${PACKAGE}" > /dev/null
	mkdir apps/ &> /dev/null
	ln -s /usr/bin/openssl apps/openssl
	popd > /dev/null
}

fix_test_symlinks_after() {
    local f
    local symlinks=""
    local slink
    local plink

    pushd "${PACKAGE}" > /dev/null
    for f in test/*;do
        slink=`readlink $f`
        plink=${slink#$OLD_NAME_VER}
        if [[ ${plink} = ..* ]]; then
            ln -s -f ${plink} ${f}
        fi
    done

    popd > /dev/null

}

forgotten_items() {
    local items="ssl/ssl_locl.h crypto/constant_time_locl.h"
    local i

    pushd "${PACKAGE}" > /dev/null

    for i in ${items}; do
            extract_item ${i}
    done

    cp -n -r "${TARBALL%.tar.*}"/* ./ && rm -rf "${TARBALL%.tar.*}"
    
    popd > /dev/null
}

if [[ -z ${1} ]]; then
	print_help
fi
VERSION=${1}
PACKAGE="qa_test_openssl-${VERSION}"
OLD_NAME_VER="openssl-${VERSION}/"
TARBALL="openssl-${VERSION}.tar.gz"
WORKDIR=$(pwd)

if [[ ! -f "${WORKDIR}/${TARBALL}" ]]; then
	echo "Unable to locate ${TARBALL}, please fetch it."
	exit 1
fi

[[ -d ${PACKAGE} ]] && rm -rf ${PACKAGE}

mkdir -p "${PACKAGE}"

extract_tests
fix_test_symlinks
fix_test_executable
fix_test_symlinks_after
forgotten_items


tar cjf "${PACKAGE}".tar.bz2 "${PACKAGE}"
rm -rf "${PACKAGE}"
echo "Tarball created:"
echo "    `md5sum ${PACKAGE}.tar.bz2`"
