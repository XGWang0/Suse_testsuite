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
# Date:        10/19/2010
# Description: Firefox Sidebar Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Sidebar test===
Step1: Load http://www.mozilla.org/
Step2: Click on View -> Sidebar to open and close the Sidebar
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

# Step1: Load http://www.mozilla.org/
web = "http://www.mozilla.org/"
openURL(fFrame, web)

procedurelogger.expectedResult('mozilla.org frame appears')
fFrame.findDocumentFrame("Home of the Mozilla Project")


# Step2: Click on View -> Sidebar to open each Sidebar
sidebar_menu = fFrame.findMenu("Sidebar", checkShowing=False)
for i in range(sidebar_menu.childCount):
    fFrame.findMenu("View").mouseClick()
    sleep(config.SHORT_DELAY)
    sidebar_menu.mouseClick()
    sleep(config.SHORT_DELAY)
    sidebar_menu.getChildAtIndex(i).mouseClick()
    sleep(config.SHORT_DELAY)
    procedurelogger.expectedResult('%s Sidebar appears' % \
                                     sidebar_menu.getChildAtIndex(i).name)
    sidebar = fFrame.findInternalFrame(sidebar_menu.getChildAtIndex(i).name)

# Close Sidebar
for i in range(sidebar_menu.childCount):
    if sidebar_menu.getChildAtIndex(i).checked:
        sidebar_name = sidebar_menu.getChildAtIndex(i).name
        sidebar_menu.getChildAtIndex(i).click(log=True)
        sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('%s Sidebar disappears' % \
                             sidebar_name)
if sidebar.showing:
    raise Exception, "Sidebar shouldn't appears"
    exit(1)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

