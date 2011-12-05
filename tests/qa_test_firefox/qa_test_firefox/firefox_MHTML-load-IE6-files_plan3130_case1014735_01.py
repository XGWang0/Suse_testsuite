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
# Date:        11/10/2010
# Description: Firefox MHTML Load IE6 Files Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===MHTML Load IE6 Files test===
Step1: make sure UnMHT extension installed
Step2: Load test page which served by IIS in Firefox
Step3: Make sure page is loaded
Step4: Unzip mhtml_apache.zip which served by Apache
Step5: Load test page in Firefox
Step6: Make sure page is loaded
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
mhtml_apache = source_path + 'mhtml_apache.zip'
IIS_page = 'NOVELL Worldwide.mht'
apache_page = 'Kaltura Community Edition Server - Home Page.htm'
plugin_url = 'https://addons.mozilla.org/en-US/firefox/addon/unmht/eula/114681?src=addondetail'

# Step1: make sure UnMHT extension installed
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Add-ons'])
sleep(config.MEDIUM_DELAY)

try:
    addon_frame = app.findFrame("Add-ons")
except SearchError:
    addon_frame = pyatspi.findAllDescendants(app, lambda x: x.name == "Add-ons Manager")[1]
sleep(config.SHORT_DELAY)

addon_frame.findListItem("Extensions").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure UnMHT in extension list')
try: 
    addon_frame.findListItem(re.compile('^UnMHT'))
except SearchError:
    fFrame.findStatusBar(None).mouseClick(log=False)
    sleep(config.SHORT_DELAY)

    closeAddOns(fFrame, addon_frame)
    sleep(config.SHORT_DELAY)

    openURL(fFrame, plugin_url)
    sleep(config.LONG_DELAY)

    pyatspi.findDescendant(fFrame, lambda x: x.name == "Add to Firefox").mouseClick()
    sleep(config.MEDIUM_DELAY)

    if pyatspi.findDescendant(fFrame, lambda x: x.name == "Allow") != None:
        pyatspi.findDescendant(fFrame, lambda x: x.name == "Allow").mouseClick()
        sleep(config.MEDIUM_DELAY)

    app.findDialog("Software Installation").findPushButton("Install Now").mouseClick()
    sleep(config.LONG_DELAY)

    try:
        addon_frame.findPushButton("Restart Firefox").mouseClick()
    except SearchError:
        pyatspi.findDescendant(fFrame, lambda x: x.name == "Restart Now").mouseClick()

    try:
        app.findDialog("Restart Firefox").findPushButton("Restart")
    except LookupError:
        pass
    sleep(config.LONG_DELAY)

    app = cache._desktop.findApplication("Firefox", checkShowing=False)
    fFrame = app.findFrame(None)
else:
    closeAddOns(fFrame, addon_frame)
    sleep(config.SHORT_DELAY)

# Step2: Load test page which served by IIS in Firefox
if os.path.exists(source_path + IIS_page):
    openURL(fFrame, 'file://' + source_path + IIS_page)
else:
    raise IOError, source_path + IIS_page + " doesn't exists"
    exit(11)

# Step3: Make sure page is loaded
procedurelogger.expectedResult("Make sure %s page is loaded" % IIS_page)
fFrame.findDocumentFrame(re.compile('^NOVELL: Worldwide'))

# Step4: Unzip mhtml_apache.zip which served by Apache
procedurelogger.action("Unzip mhtml_apache.zip which served by Apache")
if os.path.exists(mhtml_apache):
    os.system('unzip -o %s -d %s' % (mhtml_apache, source_path))
else:
    raise IOError, mhtml_apache + " doesn't exists"
    exit(11)

sleep(config.MEDIUM_DELAY)

# Step5: Load test page in Firefox
if os.path.exists(source_path + apache_page):
    openURL(fFrame, 'file://' + source_path + apache_page)
    sleep(config.SHORT_DELAY)
    fFrame.keyCombo("enter", grabFocus=False)
    sleep(config.SHORT_DELAY)
else:
    raise IOError, source_path + apache_page + " doesn't exists"
    exit(11)

# Step6: Make sure page is loaded
procedurelogger.expectedResult("Make sure %s page is loaded" % apache_page)
fFrame.findDocumentFrame("Kaltura Community Edition Server - Home Page")

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

