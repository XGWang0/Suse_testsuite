#!/usr/bin/python

import os
import re

dirName = "/thisdir"

# Make sure we are on i*86 (I know, this makes no sense, but it is only for demo purposes)
if not re.match("^i.86$", os.popen("arch", "r").read()):
    print "You are not running i*86, so skipping this test."
    exit(22)

# See if dirName doesn't yet exist
if os.path.exists(dirName):
    print "Oops! %s already was there. No idea what to do now. Bye!" % dirName
    exit(11)

# Create dirName
try:
    os.mkdir(dirName) #default mode is "0777"
except:
    pass 

# Now make sure dirName exists
if os.path.exists(dirName):
    print "Yes! %s was successfully created!" % dirName
    exit(0)
else:
    print "Oops! %s could not be created. That is unfortunate. Perhaps either you are not root, or your file system is really messed up. Bye!" % dirName
    exit (1);
