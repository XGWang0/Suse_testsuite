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
	local items="test"											
	local i																					

	pushd "${PACKAGE}" > /dev/null

	for i in ${items}; do
		extract_item ${i}
	done
	mv "${TARBALL%.tar.*}"/* ./ && rm -rf "${TARBALL%.tar.*}"

	popd > /dev/null
}

cleanup_files() {
	pushd "${PACKAGE}" > /dev/null
	# first move the tests subfolder into the folder itself
	mv test/* ./
	rm -rf test/
	# remove header/c files as they are done by unittest in the pkg
	rm -rf *.{c,h,am,in}
	chmod +x *.sh
	# fix binaries that are called to use the system ones
	sed -i -e 's:${TOOLS}:/usr/bin:' common.sh
	popd > /dev/null
}

if [[ -z ${1} ]]; then
	print_help
fi
VERSION=${1}
PACKAGE="qa_test_tiff-${VERSION}"
TARBALL="tiff-${VERSION}.tar.gz"
WORKDIR=$(pwd)

if [[ ! -f "${WORKDIR}/${TARBALL}" ]]; then
	echo "Unable to locate ${TARBALL}, please fetch it."
	exit 1
fi

[[ -d ${PACKAGE} ]] && rm -rf ${PACKAGE}

mkdir -p "${PACKAGE}"
extract_tests
cleanup_files

tar cjf "${PACKAGE}".tar.bz2 "${PACKAGE}"
rm -rf "${PACKAGE}"
echo "Tarball created:"
echo "    `md5sum ${PACKAGE}.tar.bz2`"
