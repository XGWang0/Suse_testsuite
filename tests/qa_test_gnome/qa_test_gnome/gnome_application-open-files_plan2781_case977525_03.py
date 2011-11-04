#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#


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

