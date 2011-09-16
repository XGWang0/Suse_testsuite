#!/bin/bash
source testlib.sh
assert_root

#Search for a package.
assert_result "se $PACKAGE" $PACKAGE_DESC
assert_output "se $PACKAGE" "search $PACKAGE"

#Show package information.
assert_result "if $PACKAGE" "Information for package qa_sample"
assert_output "if $PACKAGE" "info $PACKAGE"

#patch-info

#Show pattern info.
assert_result "pattern-info base" "Information for pattern base"

#Search for a pattern.
assert_result "se --type pattern base" "Base System"

assert_output "patches" "pch"
assert_output "packages" "pa"
assert_output "patterns" "pt"
assert_output "products" "pd"
#assert_output "what-provides" "wp"

echo "Test completed successfully" 
