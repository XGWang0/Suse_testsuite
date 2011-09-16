#!/bin/sh
set -x

# Copy all the tests to /tmp and make the directory writable.
mkdir -p /tmp/qa_test_coreutils || exit 1
cp -r /usr/share/qa/qa_test_coreutils/* /tmp/qa_test_coreutils || exit 1
chown -R nobody /tmp/qa_test_coreutils || exit 1

# Create a small virtual partition for tests that need one.
dd if=/dev/zero of=/tmp/qa_coreutils_tmpfs bs=1k count=65535 || exit 1
yes | mkfs -t ext2 /tmp/qa_coreutils_tmpfs || exit 1
mkdir /tmp/qa_coreutils_mnt || exit 1
mount -t ext2 -o loop /tmp/qa_coreutils_tmpfs /tmp/qa_coreutils_mnt || exit 1
chown -R nobody.users /tmp/qa_coreutils_mnt || exit 1

# Create a full virtual partition for tests that need one.
dd if=/dev/zero of=/tmp/qa_coreutils_full_tmpfs bs=1k count=1024 || exit 1
yes | mkfs -t ext2 /tmp/qa_coreutils_full_tmpfs || exit 1
mkdir /tmp/qa_coreutils_full_mnt || exit 1
mount -t ext2 -o loop /tmp/qa_coreutils_full_tmpfs /tmp/qa_coreutils_full_mnt || exit 1
dd if=/dev/zero of=/tmp/qa_coreutils_full_mnt/zero
chown -R nobody.users /tmp/qa_coreutils_full_mnt || exit 1

# Always succeed.
exit 0
