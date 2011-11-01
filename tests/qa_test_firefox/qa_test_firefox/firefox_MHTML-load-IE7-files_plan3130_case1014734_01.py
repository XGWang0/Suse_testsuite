#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Date:        11/15/2010
# Description: Firefox MHTML Load IE7 Files Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===MHTML Load IE7 Files test===
Step1: Make sure UnMHT extension installed
Step2: Load test page which is MHTML saved in IE7
Step3: Make sure page is loaded in Firefox
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
mhtml_page = 'ie7test_page.mhtml'
plugin_url = 'https://addons.mozilla.org/en-US/firefox/addon/unmht/eula/114681?src=addondetail'

# Step1: make sure UnMHT extension installed
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])

addon_frame = app.findFrame("Add-ons")
addon_frame.findListItem("Extensions").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure UnMHT in extension list')
try: 
    addon_frame.findListItem(re.compile('^UnMHT'))
except SearchError:
    fFrame.findStatusBar(None).mouseClick(log=False)
    sleep(config.SHORT_DELAY)

    openURL(fFrame, plugin_url)

    fFrame.findLink("Accept and Install", checkShowing=False).jump(log=True)
    sleep(config.MEDIUM_DELAY)

    app.findDialog("Software Installation").findPushButton("Install Now").mouseClick()
    sleep(config.LONG_DELAY)

    app.findFrame("Add-ons").findPushButton("Restart Firefox").mouseClick()

    try:
        app.findDialog("Restart Firefox").findPushButton("Restart")
    except LookupError:
        pass
    sleep(config.LONG_DELAY)

    app = cache._desktop.findApplication("Firefox", checkShowing=False)
    fFrame = app.findFrame(None)
    addon_frame = app.findFrame("Add-ons")

addon_frame.altF4()
sleep(config.SHORT_DELAY)

# Step2: Load test page which is MHTML saved in IE7
if os.path.exists(source_path + mhtml_page):
    openURL(fFrame, 'file://' + source_path + mhtml_page)
else:
    raise IOError, source_path + mhtml_page + " doesn't exists"
    exit(11)

# Step3: Make sure page is loaded in Firefox
doc_name = u"河北省重点营运车辆公共服务平台"
doc_name.encode('utf-8')

procedurelogger.expectedResult("Make sure %s page is loaded" % doc_name)
fFrame.findDocumentFrame(doc_name)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

