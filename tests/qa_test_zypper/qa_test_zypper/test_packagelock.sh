#!/bin/bash
source testlib.sh
assert_root

#Add a lock.
assert_result "al $PACKAGE" "Specified lock has been successfully added."
assert_output "addlock $PACKAGE" "al $PACKAGE"

#Remove a lock.
assert_result "rl $PACKAGE" "1 lock has been successfully removed."
#assert_output "removelock $PACKAGE" "rl $PACKAGE"

#List locks.
assert_output "locks" "ll"

#Clean locks.
assert_result "cl" "Removed"
assert_output "cleanlocks" "cl"

echo "Test completed successfully" 
