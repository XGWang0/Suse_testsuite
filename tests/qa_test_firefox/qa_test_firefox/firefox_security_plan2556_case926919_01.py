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
# Date:        10/18/2010
# Description: Firefox Security Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Security test===
Step1: Open browser to http://www.opensuse.org/en/. The Lock icon at the bottom right side of the browser window should appear unlocked.
Step2: Go to a secure site, say, https://bugzilla.novell.com
Step3: Verify that the Lock icon at the bottom right side of the browser window appears locked.
Step4: Visit https://sf.net and ensure that the "Untrusted Connection" page appears.
Step5: Add https://sf.net to Security Exception.
Step6: Click "Confirm Security Exception" to visit the site
Step7: ensure that it loads the same https://sourceforge.net as above.

NOTE: 
There are some different steps with TestCase926919 in TestPlan2556:
(1) In step1, use https://bugzilla.novell.com to instead http://sourceforge.net
(2) In step2, no Warning Dialog comes up
(3) In step5, "Untrusted Connection" page appears to instead error dialog
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Step1: Open browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Load http://www.opensuse.org/en/
web = "http://www.opensuse.org/en/"
openURL(fFrame, web)

procedurelogger.expectedResult('%s frame appears' % web)
fFrame.findDocumentFrame(re.compile('^openSUSE.org'))

# Clear the existing Certificates
menubar = fFrame.findMenuBar(None)
menubar.select(['Edit', 'Preferences'])
sleep(config.SHORT_DELAY)

preferences_frame = app.findFrame("Firefox Preferences")
preferences_frame.findListItem("Advanced").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPageTab("Encryption").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPushButton("View Certificates").press(log=True)
sleep(config.SHORT_DELAY)

certificate_dialog = app.findDialog("Certificate Manager")
servers_tab = certificate_dialog.findPageTab("Servers")
servers_tab.switch(log=True)
sleep(config.SHORT_DELAY)

try:
    source_cell = servers_tab.findTableCell("sourceforge.net")
except SearchError:
    pass # expected
else:
    source_cell.mouseClick()
    sleep(config.SHORT_DELAY)
    certificate_dialog.findPushButton(re.compile('^Delete')).mouseClick()
    sleep(config.SHORT_DELAY)
    delete_dialog = app.findDialog("Delete Server Certificate Exceptions")
    delete_dialog.findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)
    delete_dialog.assertClosed()
certificate_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.assertClosed()

# There is no Lock icon at the bottom right side of the browser
procedurelogger.action('Find Lock icon at the bottom right side')
procedurelogger.expectedResult('There is no Lock icon in %s web' % "www.opensuse.org")

buttons = fFrame.findStatusBar(None).findAllPushButtons(None)
button_names = [i.name for i in buttons]
name1 = "bugzilla.novell.com"
name2 = "Authenticated by DigiCert Inc"
assert (name1 not in button_names) or (name2 not in button_names), \
                                     "Lock icon shouldn't appears in statusbar"

# Step2: Go to a secure site, say, https://bugzilla.novell.com
entry = fFrame.findEntry("Search Bookmarks and History")
entry.text = "https://bugzilla.novell.com"
entry.mouseClick()
sleep(config.SHORT_DELAY)
fFrame.keyCombo("enter", grabFocus=False)
sleep(20)

# Step3: Verify that the Lock icon at the bottom right side of the browser window appears locked.
procedurelogger.action('Find Lock icon at the bottom right side')
procedurelogger.expectedResult('There is Lock icon in %s web' % "bugzilla.novell.com")

buttons = fFrame.findStatusBar(None).findAllPushButtons(None)
button_names = [i.name for i in buttons]
assert (name1 in button_names) or (name2 in button_names), \
                                     "Lock icon should appears in statusbar"

# Step4: Visit https://sf.net 
entry.mouseClick()
entry.text = "https://sf.net "
sleep(config.SHORT_DELAY)
fFrame.keyCombo("enter", grabFocus=False)
sleep(20)

# ensure that the "Untrusted Connection" page appears.
procedurelogger.expectedResult('Untrusted Connection page appears')
sf_frame = fFrame.findDocumentFrame("Untrusted Connection")

# Step5: Add https://sf.net to Security Exception.
sf_frame.findAllHeadings(None)[-1].click(log=True)
sleep(config.SHORT_DELAY)
sf_frame.findPushButton(re.compile('^Add Exception'), checkShowing=False).press(log=True)
sleep(20)
security_dialog = app.findDialog("Add Security Exception")

# uncheck "Permanently store this exception"
checkbox = security_dialog.findCheckBox("Permanently store this exception")
if checkbox.checked:
    checkbox.mouseClick()
    sleep(config.SHORT_DELAY)
else:
    pass

# Step6: Click "Confirm Security Exception" to visit the site
security_dialog.findPushButton("Confirm Security Exception").mouseClick()
sleep(20)

# Step7: ensure that it loads the same https://sourceforge.net as above.
procedurelogger.expectedResult('Ensure https://sourceforge.net page appears')
source_frame = fFrame.findDocumentFrame(re.compile('^SourceForge.net:'))
assert source_frame.showing == True, \
                             "SourceForge.net page doesn't appears"

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

