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
# Date:        10/27/2010
# Description: Firefox Preferences Save Home Page Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Preferences Save Home Page test===

Step1: Select Edit->Preferences
Step2: Come to Main tab,"Startup" section
Step3: Make sure that "Show my home page" is selected(by default) as 
"When Firefox starts", under the "Startup" section
Step4: In the "Home page" section, enter http://www.mozilla.org/quality/
Step5: Click Close  to save the changes and dismiss the Preferences dialog
Step6: Click the Home link icon in the Navigation Toolbar
Step7: Make sure http://www.mozilla.org/quality/ is loaded in current browser
Step8: Exit and relaunch the browser
Step9: The home page that loads should now be http://www.mozilla.org/quality/
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

web_url = "http://www.mozilla.org/quality/"

# Step1: Select Edit->Preferences
menubar = fFrame.findMenuBar(None)
menubar.select(["Edit", "Preferences"])

preferences_frame = app.findFrame("Firefox Preferences")

# Step2: Come to Main tab,"Startup" section
preferences_frame.findAllListItems(None)[0].mouseClick()
sleep(config.SHORT_DELAY)

# Step3: Make sure that "Show my home page" is selected(by default) as 
# "When Firefox starts", under the "Startup" section
procedurelogger.expectedResult('Make sure "Show my home page" is selected')
# if not selected here will return SearchError
preferences_frame.findMenuItem("Show my home page")

# Step4: In the "Home page" section, enter http://www.mozilla.org/quality/
procedurelogger.action('insert %s' % web_url)
page_entry = preferences_frame.findEntry("Home Page:")
page_entry.mouseClick()
sleep(config.SHORT_DELAY)
page_entry.text = web_url
sleep(config.SHORT_DELAY)

# Step5: Click Close to save the changes and dismiss the Preferences dialog
preferences_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.assertClosed()

# Step6: Click the Home link icon in the Navigation Toolbar
fFrame.findPushButton("Home").mouseClick()
sleep(config.LONG_DELAY)

# Step7: Make sure http://www.mozilla.org/quality/ is loaded in current browser
procedurelogger.expectedResult('Make sure %s is loaded' % web_url)
fFrame.findDocumentFrame(re.compile('^QMO'))

# Step8: Exit browser
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

# Relaunch browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

# Step9: The home page that loads should now be http://www.mozilla.org/quality/
procedurelogger.expectedResult('Make sure %s is loaded' % web_url)
fFrame.findDocumentFrame(re.compile('^QMO'))

# Restore to Default
fFrame.findMenuItem("Preferences", checkShowing=False).click(log=True)
app.findFrame("Firefox Preferences").findPushButton("Restore to Default").mouseClick()
sleep(config.SHORT_DELAY)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

