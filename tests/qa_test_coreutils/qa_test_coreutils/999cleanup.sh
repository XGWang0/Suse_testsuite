#!/bin/sh

# Clear the temporary directory.
rm -rf /tmp/qa_test_coreutils

# Remove the temporary virtual partition.
umount /tmp/qa_coreutils_mnt
rm -rf /tmp/qa_coreutils_mnt
rm /tmp/qa_coreutils_tmpfs

# Remove the temporary full partition.
umount /tmp/qa_coreutils_full_mnt
rm -rf /tmp/qa_coreutils_full_mnt
rm /tmp/qa_coreutils_full_tmpfs

# Always succeed.
exit 0


