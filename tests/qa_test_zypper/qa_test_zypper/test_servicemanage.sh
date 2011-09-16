#!/bin/bash
source testlib.sh
assert_root

#Add a service.
assert_result "as $REPO $REPO_NAME" "Service '$REPO_NAME' has been successfully added."

#Disable service.
assert_result "ms -d $REPO_NAME" "Service '$REPO_NAME' has been sucessfully disabled."

#Enable service.
assert_result "ms -e $REPO_NAME" "Service '$REPO_NAME' has been sucessfully enabled."

#List services.
assert_result "ls" $REPO_NAME
assert_output "services" $REPO_NAME

#Refresh services.
assert_result "refs" "All services have been refreshed."
assert_output "refs" "refresh-services"

#Remove a service.
assert_result "rs $REPO_NAME" "Service '$REPO_NAME' has been removed."

echo "Test completed successfully" 
