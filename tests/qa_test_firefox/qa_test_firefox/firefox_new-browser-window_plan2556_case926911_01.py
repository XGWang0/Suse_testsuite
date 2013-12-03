#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Date:        10/25/2010
# Description: Firefox New Browser window Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===New Browser window test===
Step1: Open a new browser window - File | New Window 
Step2: Make sure there are 2 Frame under Firefox application
Step3: File | New Tab to open a new browser tab
Step4: Make sure there are 2 DocumentFrame under Firefox application
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

# Step1: Open a new browser window - File | New Window 
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'New Window'])
sleep(config.SHORT_DELAY)

# Step2: Make sure there are 2 Frame under Firefox application
procedurelogger.expectedResult('Make sure there are 2 Frame under Firefox application')
frames = app.findAllFrames(None)
assert len(frames) == 2, "expected 2 frames, actual is %s" % len(frames)

# Close new frame window
frames[1].keyCombo('<Alt>F4', grabFocus=False)
#quitFirefox(frames[1])
sleep(config.SHORT_DELAY)
assert len(app.findAllFrames(None)) == 1, "new window doesn't closed"

# Step3: File | New Tab to open a new browser tab
menubar.select(['File', 'New Tab'])
sleep(config.SHORT_DELAY)

# Step4: Make sure there are 2 DocumentFrame under Firefox application
procedurelogger.expectedResult('Make sure there are 2 Frame under Firefox application')
#doc_frames = app.findAllDocumentFrames(None, checkShowing=False)
doc_frames = app.findAllInternalFrames(None, checkShowing=False)
assert len(doc_frames) == 2, "expected 2 frames, actual is %s" % len(doc_frames)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
fFrame.assertClosed()

