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
# Date:        10/27/2010
# Description: Firefox Location control Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Location control test===

Step1: File->Open Location
Step2: Make sure URL Location text fileld is focused
Step3: Type a URL"www.google.com" and click Enter
Step4: Make sure the page is opened
Step5: Select any URL from text field to visit
Step6: Make sure the page is opened
"""
# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch Firefox.
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step1: File->Open Location
fFrame.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)

fFrame.findMenuItem(re.compile('^Open Location')).mouseClick()
sleep(config.SHORT_DELAY)

# Step2: Make sure URL Location text field is focused
location_entry = fFrame.findEntry("Search Bookmarks and History")

procedurelogger.expectedResult("Make sure URL Location text field is focused")
assert location_entry.focused == True, "URL location text field is not focused"

# Step3: Type a URL"www.google.com" and click Enter
procedurelogger.action('insert %s' % "www.google.com")
location_entry.text = "www.google.com"
location_entry.keyCombo("enter")
sleep(config.LONG_DELAY)

# Step4: Make sure the page is opened
procedurelogger.expectedResult('Make sure "Google" is loaded')
fFrame.findDocumentFrame("Google")

# Step5: Select any URL from text field to visit
buttons = fFrame.findAutocomplete("Search Bookmarks and History").findAllPushButtons(None)
buttons[-1].mouseClick()
sleep(config.SHORT_DELAY)

fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)

fFrame.keyCombo("Down", grabFocus=False)
sleep(config.SHORT_DELAY)

fFrame.keyCombo("enter", grabFocus=False)
sleep(config.MEDIUM_DELAY)

# Step6: Make sure the page is opened
procedurelogger.expectedResult('Make sure the page is updated')
if fFrame.findDocumentFrame(None).name == "Google":
    raise Exception, "ERROR: Google page shouldn't appears again"
    exit(2)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

