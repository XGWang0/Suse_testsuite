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
# Description: Firefox Novell Moonlight Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Novell Moonlight test===

Step1: Make sure Silverlight Plug-In appears in Plugins list
Step2: Visit the following URL
Silverlight3 http://www.belindaperez.com/demo/deepu/SimpleImageScroller.html
Silverlight3 http://www.innoveware.com/ql3/QuakeLight.html
Silverlight2 http://net35.ccs.neu.edu/home/cobracar/DiggSample.html
Step3: Make sure websites be showed correctly. the website should not show 
"Install Microsoft Sliverlight".
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

# Step1: Make sure Silverlight Plug-In appears in Plugins list
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])
sleep(config.MEDIUM_DELAY)

try:
    addon_frame = app.findFrame("Add-ons")
except SearchError:
    addon_frame = pyatspi.findAllDescendants(app, lambda x: x.name == "Add-ons Manager")[1]
sleep(config.SHORT_DELAY)

addon_frame.findListItem("Plugins").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure Silverlight Plug-In exists')
addon_frame.findListItem(re.compile('^Silverlight Plug-In'), checkShowing=False)

closeAddOns(fFrame, addon_frame)

# Step2: Visit the following URL
# Launch http://www.belindaperez.com/demo/deepu/SimpleImageScroller.html
# that is Silverlight3
openURL(fFrame, "http://www.belindaperez.com/demo/deepu/SimpleImageScroller.html")

# Step3: Make sure websites be showed correctly. the website should not show 
# "Install Microsoft Sliverlight".
procedurelogger.expectedResult('%s document frame appears' % \
                                                  "SimpleImageScrollerDemo")
links=fFrame.findAllLinks(None)
for i in links:
    if i.name == "Get Microsoft Silverlight":
        assert False, "the website should not show Install Microsoft Sliverlight"

# Add new tab to launch http://www.innoveware.com/ql3/QuakeLight.html
# that is Silverlight3
menubar.select(['File', 'New Tab'])
sleep(config.SHORT_DELAY)

openURL(fFrame, "http://www.innoveware.com/ql3/QuakeLight.html")

# Make sure websites be showed correctly. the website should not show 
# "Install Microsoft Sliverlight".
procedurelogger.expectedResult('%s document frame appears' % \
                                                  "QuakeLight")
fFrame.findDocumentFrame(re.compile('^QuakeLight'))

links=fFrame.findAllLinks(None)
for i in links:
    if i.name == "Get Microsoft Silverlight":
        assert False, "the website should not show Install Microsoft Sliverlight"

# Add new tab to Launch http://net35.ccs.neu.edu/home/cobracar/DiggSample.html
# that is Silverlight2
menubar.select(['File', 'New Tab'])
sleep(config.SHORT_DELAY)

openURL(fFrame, "http://net35.ccs.neu.edu/home/cobracar/DiggSample.html")

# Make sure websites be showed correctly. the website should not show 
# "Install Microsoft Sliverlight".
'''
procedurelogger.expectedResult('%s document frame appears' % \
                                                  "DiggSearch")
fFrame.findDocumentFrame(re.compile('^Digg'))

links=fFrame.findAllLinks(None)
for i in links:
    if i.name == "Get Microsoft Silverlight":
        assert False, "the website should not show Install Microsoft Sliverlight"
'''
# Close application
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
quitMultipleTabs(app)
app.assertClosed()

