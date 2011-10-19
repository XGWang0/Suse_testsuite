#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# Date:        07/27/2011
# Description: Nautilus open FTP Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Nautilus open FTP===
Step1: Launch Nautilus
Step2: Open the location text entry filed
Step3: Enter ftp://<location> to connect anonymously
Step4: Make sure listing of the location should be displayed
"""

# imports
from strongwind import *
from gnome_frame import *
from gnome_config import *
import os
import subprocess

print doc

location = ftp_server

if location == "":
    print "SKIP: Please give ftp_server setting in gnome_config.py and run test again"
    exit(22)

# Step1: Launch Nautilus
try:
    app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# Just an alias to make things shorter.
nFrame = app.findFrame(re.compile('^%s' % os.getenv('USER')))
menubar = nFrame.findMenuBar(None)

# Step2: Open the location text entry filed
location_text = nFrame.findText(None, labelledBy="Location:", checkShowing=False)
if not location_text.showing:
    edit_toggle = nFrame.findToggleButton("Edit").mouseClick()
    sleep(config.SHORT_DELAY)

# Step3: Enter ftp://<location> to connect anonymously
procedurelogger.action('Enter %s' % "ftp://" + location)
location_text.text = "ftp://" + location

location_text.mouseClick()
location_text.keyCombo('enter')
sleep(config.SHORT_DELAY)

try:
    ftp_dialog = app.findDialog(None)
except:
    pass
else:
    ftp_dialog.findRadioButton("Connect anonymously").mouseClick()
    sleep(config.SHORT_DELAY)
    ftp_dialog.findPushButton("Connect").mouseClick()
    sleep(config.MEDIUM_DELAY)

# Step4: Make sure listing of the location should be displayed
procedurelogger.expectedResult("Make sure ftp connection is list in ")
ftp_cell = nFrame.findSplitPane(None).findTableCell("ftp on %s" % location)

assert nFrame.name == "/ on %s - File Browser" % location, \
                         "Nautilus frame name should be %s, but now is %s" % \
                          ("/ on %s - File Browser", nFrame.name)

# Unmount ftp connection
ftp_cell.mouseClick(log=False)
sleep(config.SHORT_DELAY)
ftp_cell.mouseClick(button=3)
sleep(config.SHORT_DELAY)

app.findAllWindows(None)[-1].findMenuItem("Unmount").mouseClick()
sleep(config.SHORT_DELAY)

# Quit nautilus
menubar.findMenuItem("Close", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
nFrame.assertClosed()

