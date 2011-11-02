#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/26/2010
# Description: Firefox Externally handled content Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Externally handled content test===
Step1: Browser to http://www.python.org/ftp/python/2.7/Python-2.7.tgz
Step2: Since mozilla can't handle this file internally, it should launch 
an Opening dialog
Step3: Select Open with default application(File Roller), make sure Download Manager appears
Step4: Cancel download and close Download Manager
Step5: Browser to http://www.python.org/ftp/python/2.7/Python-2.7.tgz again
Step6: Select Save File, make sure Download Manager appears
Step7: Cancel download and close Download Manager

NOTES:
Some different Steps with the test cases in Plan2556:
(1) use new web url to instead http://www.mozilla.org/quality/smoketests/test.zip that doesn't works
(2) Add more tests for "Open" and "Save File" actions
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

try:
  app = launchApp("/usr/bin/firefox", "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: Open browser to http://www.python.org/ftp/python/2.7/Python-2.7.tgz
url_entry = fFrame.findEntry("Search Bookmarks and History")
url_entry.text = "http://www.python.org/ftp/python/2.7/Python-2.7.tgz"
sleep(config.SHORT_DELAY)
url_entry.keyCombo("enter")

# Step2: Since mozilla can't handle this file internally, it should open the Save As dialog
opening_dialog = app.findDialog("Opening Python-2.7.tgz")

# Step3: Select Open with default application(File Roller)
opening_dialog.findRadioButton("Open with").mouseClick()
sleep(config.SHORT_DELAY)

opening_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

# Enter name of file to save to... dialog appears but it doesn't accessible in SP2,
# press key enter to close the dialog
opening_dialog.keyCombo('enter')
sleep(config.SHORT_DELAY)

# Make sure Download Manager appears
download_frame = app.findFrame(re.compile('Downloads$'))
sleep(config.SHORT_DELAY)

## BUG: Cancel button has wrong position and press action interface implementated in SP2 
# Step4: Cancel the download and close Download Manager
#download_frame.findPushButton("Cancel", checkShowing=False).mouseClick(log=True)
#sleep(config.MEDIUM_DELAY)
(x, y) = (462, 50)
pyatspi.Registry.generateMouseEvent(x, y, 'b1dc')
sleep(config.SHORT_DELAY)

download_frame.findPushButton("Clear List").press(log=True)
sleep(config.SHORT_DELAY)

download_frame.altF4()

# Step5: Browser to http://www.python.org/ftp/python/2.7/Python-2.7.tgz again
url_entry = fFrame.findEntry("Search Bookmarks and History")
url_entry.text = "http://www.python.org/ftp/python/2.7/Python-2.7.tgz"
sleep(config.SHORT_DELAY)
url_entry.keyCombo("enter")

opening_dialog = app.findDialog("Opening Python-2.7.tgz")

# Step6: Select Save File
opening_dialog.findRadioButton("Save File").mouseClick()
sleep(config.SHORT_DELAY)

opening_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

opening_dialog.keyCombo('enter')
sleep(config.MEDIUM_DELAY)

# Make sure Download Manager appears
download_frame = app.findFrame(re.compile('Downloads$'))
sleep(config.MEDIUM_DELAY)

# Step7: Cancel and close Download frame
#download_frame.findPushButton("Cancel", checkShowing=False).mouseClick(log=True)
#sleep(config.SHORT_DELAY)
(x, y) = (462, 50)
pyatspi.Registry.generateMouseEvent(x, y, 'b1dc')
sleep(config.SHORT_DELAY)

download_frame.findPushButton("Clear List").press(log=True)
sleep(config.SHORT_DELAY)

download_frame.altF4()

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

