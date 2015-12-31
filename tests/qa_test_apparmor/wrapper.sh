#!/bin/bash
#this file is a simple test wrapper since subdomain regression tests must
#be executed within the subdomain directory. This script can be executed
#from anywhere
cd `dirname "$0"`
script_dir=`dirname "$1"`
script_name=`basename "$1"`
pushd "$script_dir" > /dev/null
./${script_name}
ret=$?
popd > /dev/null
exit $ret
