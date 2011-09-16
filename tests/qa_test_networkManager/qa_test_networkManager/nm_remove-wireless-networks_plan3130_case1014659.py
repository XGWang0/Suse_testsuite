#!/usr/bin/env python

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
