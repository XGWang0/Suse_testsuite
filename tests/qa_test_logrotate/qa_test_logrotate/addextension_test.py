#!/usr/bin/python

import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup(addextension=True, compress=True)

# Run logrotate.
rotate_log()

# Verify that the extension was added to the zip file.
zipped_file = TEST_LOG + '.1.log.gz'
assert_exists(zipped_file)
unzip(zipped_file)

# Verify that the extension was added to the log.
rotated_file = TEST_LOG + '.1.log'
assert_exists(rotated_file)
assert_contains('First rotation.', file_name=rotated_file)

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)

