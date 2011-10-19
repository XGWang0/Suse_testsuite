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
# Written by: Calen Chen <cachen@novell.com>
# Date:        11/01/2010
# Description: Firefox Lockdown save media Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Lockdown save media test===
Step1: Open browser to "about:config"
Step2: Search for config.lockdown.savemedia table cell, change value to "true"
Step3: Browser to "http://www.google.com"
Step4: Right clicking on "google" image on page
Step5: Make sure Save as button is inactive (greyed out)

NOTE:
(1) Context menu raised by right clicking doesn't accessible, so Step5 will be 
replaced by right click image and press key 'down' and 'enter' to navigate 
the save as item and make sure the action doesn't launch save dialog
(2) I assume "savemedia" has been replaced by "savepage"
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: Open browser to "about:config"
openURL(fFrame, "about:config")

config_frame = app.findFrame(re.compile('^about:config'))

# Insert config.lockdown.savemedia into Filter: entry
config_frame.findPushButton("I'll be careful, I promise!").mouseClick()
sleep(config.SHORT_DELAY)

config_frame.findEntry("Filter:").mouseClick()
sleep(config.SHORT_DELAY)

config_frame.findEntry("Filter:").typeText("config.lockdown.savepage")

# Step2: Search for config.lockdown.savemedia table cell
try:
    config_frame.findTableCell("config.lockdown.savepage")
except SearchError:
    fFrame.altF4() # Close firefox and exit as SKIPPED
    exit(22)
else:
    doubleClick(config_frame.findTableCell("false"))

# Change value to "true"
procedurelogger.expectedResult("Make sure value is changed to true")
config_frame.findTableCell("true")

# Step3: Browser to "http://www.google.com"
url = "http://www.google.com"
openURL(fFrame, url)

procedurelogger.expectedResult("Make sure %s is opened" % url)
doc_frame = app.findDocumentFrame("Google")

# Step4: Right clicking on "google" image on page
doc_frame.findImage("Google").mouseClick(button=3)
sleep(config.SHORT_DELAY)

# press key 'down' and 'enter' to navigate the save as item 
fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)
fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)
fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)
fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)

fFrame.keyCombo("enter", grabFocus=False)
sleep(config.SHORT_DELAY)

# Step5: Make sure the action doesn't launch save dialog
procedurelogger.expectedResult("Make sure the action doesn't launch save dialog")
try:
    app.findDialog("Save Image")
except SearchError:
    pass # expected
else:
    assert False, "Save Image dialog sholdn't appears"

# Change config.lockdown.savemedia to false
openURL(fFrame, "about:config")
config_frame = app.findFrame(re.compile('^about:config'))

config_frame.findPushButton("I'll be careful, I promise!").mouseClick()
sleep(config.SHORT_DELAY)

config_frame.findEntry("Filter:").mouseClick()
sleep(config.SHORT_DELAY)

config_frame.findEntry("Filter:").typeText("config.lockdown.savepage")

# change value
doubleClick(config_frame.findTableCell("config.lockdown.savepage"))

procedurelogger.expectedResult("Make sure value is changed to false")
config_frame.findTableCell("false")

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

