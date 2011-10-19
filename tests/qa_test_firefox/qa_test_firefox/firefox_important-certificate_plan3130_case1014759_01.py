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
# Date:        10/21/2010
# Description: Firefox Certificate Test
##############################################################################

class PluginError(Exception):
    "Raised when plugin doesn't exist"
    pass

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Certificate test===
Only valid if we get centralized certificate store in Firefox (Check certificates and certificates chain in Edit-Preference-Advanced-Encryption-View Certificates)

Step1: load http://sf.net and Add https://sf.net to Security Exception.
Step2: open Edit->Preference->Advanced->Encryption->View Certificates
Step3: make sure there are Root Certificates that Firefox trusts under Authorities
Step4: make sure sourceforge.net certificate under Servers
"""
# imports
import os
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

# First to make sure sourceforge.net certificate doesn't exist
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

server_tab = certificate_dialog.findPageTab("Servers")
server_tab.switch(log=True)
sleep(config.SHORT_DELAY)

try:
    source_cell = server_tab.findTableCell("sourceforge.net")
except SearchError:
    pass
else:
    # Clear sourceforge.net certificate
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

# Step1: load http://sf.net
web = "https://sf.net"
openURL(fFrame, web)

procedurelogger.expectedResult('%s frame appears' % "Untrusted Connection")
sf_frame = fFrame.findDocumentFrame("Untrusted Connection")

# Add https://sf.net to Security Exception
sf_frame.findAllHeadings(None)[-1].mouseClick()
sleep(config.SHORT_DELAY)
sf_frame.findPushButton(re.compile('^Add Exception'), checkShowing=False).press(log=True)
sleep(config.MEDIUM_DELAY)
security_dialog = app.findDialog("Add Security Exception")

checkbox = security_dialog.findCheckBox("Permanently store this exception")
if checkbox.checked:
    checkbox.mouseClick()
    sleep(config.SHORT_DELAY)
else:
    pass

security_dialog.findPushButton("Confirm Security Exception").mouseClick()
sleep(config.LONG_DELAY)

# ensure that it loads the same https://sourceforge.net as above.
procedurelogger.expectedResult('Ensure https://sourceforge.net page appears')
source_frame = fFrame.findDocumentFrame(re.compile('^SourceForge.net:'))
assert source_frame.showing == True, \
                             "SourceForge.net page doesn't appears"

# Step2: open Edit->Preference->Advanced->Encryption->View Certificates
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

# Step3: make sure there are Root Certificates that Firefox trusts under Authorities
certificate_dialog.findPageTab("Authorities").switch(log=True)
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('make sure there are Root Certificates that Firefox trusts')
authorities_pane = certificate_dialog.findScrollPane(None, labelledBy="Authorities")
assert len(authorities_pane.findAllTableCells(None)) > 0, "should list Root Certificates"

# Step4: make sure sourceforge.net certificate under Servers
certificate_dialog.findPageTab("Servers").switch(log=True)
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('make sure sourceforge.net certificate exists')
source_cell = certificate_dialog.findTableCell("sourceforge.net")

# Clear sourceforge.net certificate
source_cell.mouseClick()
sleep(config.SHORT_DELAY)
certificate_dialog.findPushButton(re.compile('^Delete')).mouseClick()
sleep(config.SHORT_DELAY)
delete_dialog = app.findDialog("Delete Server Certificate Exceptions")
delete_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)
delete_dialog.assertClosed()

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

