#!/usr/bin/python

import os, subprocess
from logrotate import *

# Create dummy log and config file.
setup(missingok=True)

# Run logrotate.
rotate_log(missingok=True)

# Delete temporary files created for the test.
cleanup()

# Exit without errors if none were encountered.
exit (0)

