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
Image files:
Step1: Create 'test.png', 'test.gif', 'test.jpg' in '~/'
Step2: Open 'test.png', 'test.gif', 'test.jpg'
Step3: Make sure files are opened by 'Eye of Gnome'
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
img_files = ['test.png', 'test.gif', 'test.jpg']

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

## Image files:
# Step1: Create 'test.png', 'test.gif', 'test.jpg' in '~/'
for i in img_files:
    procedurelogger.action("Create %s in %s" % (i, data_dir))
    f = file(data_dir + i, 'w')
    sleep(config.SHORT_DELAY)

    # Step2: Open 'test.png', 'test.gif', 'test.jpg'
    # Step3: Make sure files are opened by 'Eye of Gnome'
    (opened_app, app) = openFileTest(i, 'eog')

    # Close app
    opened_app.findFrame(None).findMenuItem("Close", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    opened_app.assertClosed()

# Remove all created test.* files
subprocess.Popen('rm %stest.*' % data_dir, shell=True)

# Close nautiles
quitApp(app)

app.assertClosed()
