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
PDF:
Step1: Create 'test.pdf' in '~/'
Step2: Open ~/test.pdf
Step3: Make sure test.pdf is opened by Acrobat Reader

Html files:
Step1: Create 'test.html' in '~/'
Step2: Open 'test.html'
Step3: Make sure files are opened by 'firefox'
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
oo_files = ['test.ods', 'test.odt', 'test.odp']

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

## PDF:
# Step1: Create 'test.pdf' in '~/'
procedurelogger.action("Create 'test.pdf' in %s" % data_dir)
file(data_dir + 'test.pdf', 'w')
sleep(config.SHORT_DELAY)

# Step2: Open ~/test.pdf
# Step3: Make sure test.pdf is opened by Acrobat Reader
(opened_app, app) = openFileTest('test.pdf', 'acroread')

# Close acrobat reader
if opened_app.findFrame(None).name != "Adobe Reader":
    opened_app.keyCombo('<Alt>F4', grabFocus=False)
    sleep(config.SHORT_DELAY)
    opened_app.findAlert(None).findPushButton("Yes").mouseClick()
    sleep(config.SHORT_DELAY)
else:
    opened_app.findAlert(None).findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)
    opened_app.keyCombo('<Alt>F4', grabFocus=False)
    sleep(config.SHORT_DELAY)

opened_app.assertClosed()
sleep(config.SHORT_DELAY)

## Html files:
# Step1: Create 'test.html' in '~/'
file(data_dir + 'test.html', 'w')

# Step2: Open 'test.html'
# Step3: Make sure files are opened by 'firefox'
(opened_app, app) = openFileTest('test.html', 'Firefox')

# Close app
opened_app.findFrame(None).findMenuItem("Quit", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
opened_app.assertClosed()

# Remove all created test.* files
subprocess.Popen('rm %stest.*' % data_dir, shell=True)

# Close nautiles
quitApp(app)

app.assertClosed()
