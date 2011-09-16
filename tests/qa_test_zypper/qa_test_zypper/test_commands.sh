#!/bin/bash
source testlib.sh
assert_root

assert_output "help" "?"
assert_result "help" "Usage:"

assert_result "versioncmp 2.0 1.1" "newer"
assert_result "vcmp 1.0 1.1" "older"

assert_output "targetos" "tos"
assert_result "tos" "^sle\|^open"

assert_result "licenses" "SUMMARY"

echo se zoo | zypper sh | grep zoo > /dev/null
[ $? == 0 ] || failed "zypper sh failed"

echo se zoo | zypper shell | grep zoo > /dev/null
[ $? == 0 ] || failed "zypper shell failed"

echo "Test completed successfully"
