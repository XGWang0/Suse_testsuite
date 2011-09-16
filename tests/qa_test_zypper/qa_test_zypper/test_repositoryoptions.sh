#!/bin/bash
source testlib.sh
assert_root

assert_result "--no-gpg-checks --gpg-auto-import-keys ar $REPO $REPO_NAME" "Repository '$REPO_NAME' successfully added"

assert_result "--disable-repositories se $PACKAGE" "No packages found"
assert_result "sd $REPO_NAME" "has been removed"

assert_result "--plus-repo $REPO se $PACKAGE" $PACKAGE_DESC
assert_result "-p $REPO se $PACKAGE" $PACKAGE_DESC

assert_result "--no-refresh --no-cd --no-remote -q se $PACKAGE" "No packages found"

echo "Test completed successfully"
