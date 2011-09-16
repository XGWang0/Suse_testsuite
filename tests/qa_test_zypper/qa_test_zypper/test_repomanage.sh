#!/bin/bash
source testlib.sh
assert_root

NEW_REPO_NAME='qa_test2'

#Add a repo.
assert_result "ar $REPO $REPO_NAME" "Repository '$REPO_NAME' successfully added"

#Rename repo.
assert_result "nr $REPO_NAME $NEW_REPO_NAME" "Repository '$REPO_NAME' renamed to '$NEW_REPO_NAME'."

#List repos.
assert_result "lr" "$NEW_REPO_NAME"
assert_output "lr" "repos"

#Disable repo.
assert_result "mr -d $NEW_REPO_NAME" "Repository '$NEW_REPO_NAME' has been successfully disabled."

#Enable repo.
assert_result "mr -d $NEW_REPO_NAME" "Repository '$NEW_REPO_NAME' has been successfully enabled."

#Remove a repo.
assert_result "rr $NEW_REPO_NAME" "Repository '$NEW_REPO_NAME' has been removed."

#Refresh repos.
assert_result "ref" "All repositories have been refreshed."

echo "Test completed successfully" 
