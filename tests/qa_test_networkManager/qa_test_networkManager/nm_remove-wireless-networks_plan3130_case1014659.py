#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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


##############################################################################
# Written by: Felicia Mu<fxmu@novell.com>
#             Calen Chen <cachen@novell.com>
# Date:       02/17/2011
# Description: Remove wireless network Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Remove Wireless Networks===
Step1: Click "Wireless" page tab.
Step2: Click "Add" button.
Step3: On the "Editing Wireless connection 1" dialog, input "wireless-test" in the elect the "Connection name:" Edit.
Step4: Input "wireless-test" in the "SSID:" Edit.
Step5: Click "Apply" button.
Step6: On the "Network connections" dialog, select the "wireless-test" table cell.
Step7: Click "delete" button, the "Question" dialog is shown.
Step8: On the new dialog, click "delete" button.
"""
# imports
from nm_frame import *

print doc

# open the label sample application
try:
  app = launchDialog("/usr/bin/nm-connection-editor", "nm-connection-editor")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter

nDialog = app.findDialog("Network Connections");

# Step1: Click "Wireless" page tab.
newtab = nDialog.findNewItem("PageTab", "Wireless")
sleep(config.SHORT_DELAY)

nDialog.clickItem("PageTab", "Wireless")
sleep(config.SHORT_DELAY)

# Step2: Click "Add" button.
nDialog.clickItem("PushButton", "Add")
sleep(config.SHORT_DELAY)

addFrame= app.findFrame("Editing Wireless connection 1")

# Step3: On the "Editing Wireless connection 1" dialog, input "wireless-test" in the elect the "Connection name:" Edit.
addFrame.findText(None).enterText("wireless-test")
sleep(config.SHORT_DELAY)

# Step4: Input "wireless-test" in the "SSID:" Edit.
addFrame.findText(None, labelledBy="SSID:").enterText("wireless-test")
sleep(config.SHORT_DELAY)

# Step5: Click "Apply" button.
addFrame.clickItem("PushButton", "Apply")
sleep(config.SHORT_DELAY)
addFrame.assertClosed()

# Step6: On the "Network connections" dialog, select the "wireless-test" table cell.
wireless_test = newtab.findTableCell("wireless-test", checkShowing=False)

procedurelogger.action('Select "wireless-test" on the wireless list')
wireless_test.grabFocus()
sleep(config.SHORT_DELAY)

# Step7: Click "delete" button, the "Question" dialog is shown.
nDialog.clickItem("PushButton", "Delete")
sleep(config.SHORT_DELAY)
alertdialog = app.findAlert(None);

# Step8: On the new dialog, click "delete" button.
alertdialog.clickItem("PushButton", "Delete")
sleep(config.SHORT_DELAY)

# Step9: Make sure "wireless-test" is removed from list
procedurelogger.expectedResult('"wireless-test" is removed from list')
try:
    wireless_test.showing
except LookupError:
    pass # expected!
else:
    print "wireless-test still on the list"

nDialog.clickItem("PushButton", "Close")
app.assertClosed()
sleep(config.MEDIUM_DELAY)

