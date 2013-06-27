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
# Date:        11/15/2010
# Description: Firefox Java Plugin Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Java Plugin test===
Step1: Add-on ->Plugins, disable Java(TM) Plug-in
Step2: Unable to load the testpage
Step3: Enable Java(TM) Plug-in
Step4: Load the testpage successful
"""

# imports
import os
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

source_path = '/usr/share/qa/qa_test_firefox/test_source/'
mhtml_page = 'example1.html'

# Step1: Add-on ->Plugins, disable Java(TM) Plug-in
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])

try:
    addon_frame = app.findFrame("Add-ons")
except SearchError:
    addon_frame = pyatspi.findAllDescendants(app, lambda x: x.name == "Add-ons Manager")[1]
sleep(config.SHORT_DELAY)

addon_frame.findListItem("Plugins").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure Jave Plugin in the list')
try:
    java_plugin = addon_frame.findListItem(re.compile('.*Java'))
except SearchError:
    menubar.select(['File', 'Quit'])
    raise Exception, "Java plugin doesn't installed"
    exit(22)
else:
    # Select Java plugin item to make 'Disable' button appear
    java_plugin._accessible.queryAction().doAction(0)
    sleep(config.SHORT_DELAY)
    # Reopen addon frame due to Disable button doesn't accessible sometimes
    menubar.select(['Tools', 'Add-ons'])
    java_plugin.mouseClick(log=False)
    java_plugin.findPushButton("Disable").mouseClick()
    sleep(config.SHORT_DELAY)

pagetabs = fFrame.findAllPageTabs(None)

pagetabs[0].mouseClick()
sleep(config.SHORT_DELAY)

# Step2: Unable to load the testpage
fFrame.findEntry("Search using Google").mouseClick()
sleep(config.SHORT_DELAY)
openURL(fFrame, source_path + mhtml_page)

procedurelogger.expectedResult("the Text widget in example page appears")
example_doc = fFrame.findDocumentFrame("The Animator Applet (1.1) - example 1")
try:
    example_doc.findText(None)
except SearchError:
    pass # expected
else:
    assert False, "Text shouldn't appears when Java plugin disabled"

# Step3: Enable Java(TM) Plug-in
pagetabs[1].mouseClick()
sleep(config.SHORT_DELAY)

#menubar.select(['Tools', 'Add-ons'])
java_plugin.findPushButton("Enable").mouseClick()
sleep(config.SHORT_DELAY)

closeAddOns(fFrame, addon_frame)

# Step4: Load the testpage successful
openURL(fFrame, source_path + mhtml_page)

procedurelogger.expectedResult("the Text widget in example page appears")
example_doc = fFrame.findDocumentFrame("The Animator Applet (1.1) - example 1")
example_doc.findText(None)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
app.assertClosed()

