#!/bin/bash
source testlib.sh
assert_root

#Refresh repos.
zypper ref

#Update the system.
assert_result "up -y --auto-agree-with-licenses" "Installing" "Nothing to do."
assert_output "up" "update"

assert_output "list-patches" "lp"
assert_output "patch-check" "pchk"

echo "Test completed successfully" 
