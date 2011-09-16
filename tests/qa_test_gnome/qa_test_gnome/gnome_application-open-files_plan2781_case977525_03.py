#!/usr/bin/env python

##############################################################################
# Written by:  Calen Chen <cachen@novell.com>
# Date:        06/21/2011
# Description: Some types of files should be opened by corresponding 
#              applications Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Some types of files should be opened by corresponding applications===
Compressed files:
Step1: Create 'test.tar.gz', 'test.tar.bz2', 'test.zip' in '~/'
Step2: Open 'test.tar.gz', 'test.tar.bz2', 'test.zip'
Step3: Make sure files are opened by 'fileroller'
"""

# imports
from strongwind import *
from gnome_frame import *
import os
import subprocess

print doc

who = os.getenv("USER")
if who == "root":
    data_dir = "/%s/" % who
else:
    data_dir = "/home/%s/" % who
comp_files = ['test.tar.gz', 'test.tar.bz2', 'test.zip']

def openFileTest(file_name, app_name):
    '''
    Open specified file by specified application, then close the application
    '''
    # Launch nautilus
    app = launchNautilus('/usr/bin/nautilus', 'nautilus')
    nFrame = app.findFrame("%s - File Browser" % who)

    # Open file
    openAction(nFrame.findIcon(file_name))
    sleep(config.LONG_DELAY)

    # Make sure file are opened by the expected application
    procedurelogger.expectedResult("%s is opened by %s" % (file_name, app_name))
    opened_app = cache._desktop.findApplication(app_name, checkShowing=None)
    sleep(config.MEDIUM_DELAY)

    cache.addApplication(opened_app)

    return opened_app, app

# Remove all created test.* files
subprocess.Popen('rm %stest.*' % data_dir, shell=True)
sleep(config.SHORT_DELAY)

## Compressed files:
# Step1: Create 'test.tar.gz', 'test.tar.bz2', 'test.zip' in '~/'
for i in comp_files:
    procedurelogger.action("Create %s in %s" % (i, data_dir))
    file(data_dir + i, 'w')
    sleep(config.SHORT_DELAY)

    # Step2: Open 'test.tar.gz', 'test.tar.bz2', 'test.zip'
    # Step3: Make sure files are opened by 'fileroller'
    (opened_app, app) = openFileTest(i, 'file-roller')

    # Close app
    quitApp(opened_app)

# Remove all created test.* files
subprocess.Popen('rm %stest.*' % data_dir, shell=True)

# Close nautiles
quitApp(app)

app.assertClosed()
