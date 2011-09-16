#!/bin/bash
source testlib.sh
assert_root

assert_file "--root /tmp se" "/tmp/var/cache/zypp/solv/"
assert_file "-R /tmp/var se" "/tmp/var/var/cache/zypp/solv/"
rm -rf /tmp/var

no_result "--disable-system-resolvables se" "^i"

echo "Test completed successfully"
