#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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
# Written by: Calen Chen <cachen@novell.com>
# Date:        07/04/2011
# Description: Nautilus opens Windows Shares Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Nautilus open windows shares===
Step1: Launch Nautilus
Step2: Open the location entry field
Step3: Doing "/sbin/service smb start" 
Step4: Enter smb://<localhost ip>
Step5: Listing of the location should be displayed
"""

# imports
import os
import subprocess

from strongwind import *
from gnome_frame import *

print doc

# Step1: Launch Nautilus
try:
    app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

nFrame = app.findFrame(re.compile('^%s' % os.getenv('USER')))

# Step2: Open the location entry field
location_text = nFrame.findText(None, labelledBy="Location:", checkShowing=False)
if not location_text.showing:
    edit_toggle = nFrame.findToggleButton("Edit").mouseClick()
    sleep(config.SHORT_DELAY)

# Step3: Doing "/sbin/service smb start"
procedurelogger.action('Doing "/sbin/service smb start"')
p = subprocess.Popen('sudo /sbin/service smb start', stdout=subprocess.PIPE, shell=True)
(stdout, stdin) = p.communicate()
done = re.search('done', stdout).group(0)
if done != "done":
    print "smb doesn't started"
    exit(22)

# Step4: Enter smb://127.0.0.1
procedurelogger.action('Enter smb://127.0.0.1')
location_text.text = "smb://127.0.0.1"

location_text.mouseClick()
location_text.keyCombo('enter')
sleep(config.MEDIUM_DELAY)

# Step5: Listing of the location should be displayed
procedurelogger.expectedResult('Listing of the location should be displayed')
nFrame = app.findFrame("Windows shares on 127.0.0.1 - File Browser")
nFrame.findIcon("groups")

# Close nautilus
nFrame.findMenuItem("Close", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
app.assertClosed()


