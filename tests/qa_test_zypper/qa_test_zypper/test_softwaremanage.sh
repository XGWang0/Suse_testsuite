#!/bin/bash
source testlib.sh
assert_root

#test_softwaremanage

assert_output "install $PACKAGE" "in $PACKAGE"
assert_output "remove $PACKAGE" "rm $PACKAGE"
assert_output "verify $PACKAGE" "ve $PACKAGE"
assert_output "source-install $PACKAGE" "si $PACKAGE"
assert_output "install-new-recommends" "inr"

echo "Test completed successfully" 
