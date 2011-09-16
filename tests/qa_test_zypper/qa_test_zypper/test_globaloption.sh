#!/bin/bash
source testlib.sh
assert_root

assert_output "--help" "-h"
assert_result "-h" "Usage:"

assert_output "--version" "-V"
# Not support zypper 0.x.x, so assert output has zypper [1-9]
assert_result "-V" "zypper [1-9]"

cp /etc/zypp/zypp.conf ~/zypp.conf
assert_output "zypper --config ~/zypp.conf se $PACKAGE" "zypper -c ~/zypp.conf se $PACKAGE"
assert_result "zypper --config ~/zypp.conf se $PACKAGE" "Loading repository data..."
rm -f ~/zypp.conf

assert_output "--quiet se $PACKAGE" "-q se $PACKAGE"
no_result "-q se $PACKAGE" "Loading repository data"

assert_output "--verbose se $PACKAGE" "-v se $PACKAGE"
assert_result "-v se $PACKAGE" "Checking whether to refresh metadata for"

# TODO: Currently, zypper -A se and zypper se have same output. So later you can add zypper --no-abbrev test here if necessary...

# TODO: Add zypper --table-style test here

# TODO: Add zypper --rug-compatible test here

assert_result "--non-interactive in $PACKAGE" "Installing: $PACKAGE"
assert_result "-n rm $PACKAGE" "Removing $PACKAGE"

assert_output "--xmlout se $PACKAGE" "-x se $PACKAGE"
assert_result "-x se $PACKAGE" "xml version="

# TODO: add --reposd-dir, -D; --cache-dir, -C; --raw-cache-dir test here.

echo "Test completed successfully"
