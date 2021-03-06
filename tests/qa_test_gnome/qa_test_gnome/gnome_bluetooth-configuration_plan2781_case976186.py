#!/usr/bin/env python
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
# Date:        08/08/2011
# Description: GUI for Bluetooth configuration test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===GUI For Bluetooth Configuration===
Step1: Launch "bluetooth-properties" 
Step2: Check the box "Make computer discoverable"
Step3: Launch "bluetooth-sendto" to send file to another device
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

file_path = '/%s/bluetooth_test' % os.getenv('USER')      

# Step1: Launch "bluetooth-properties" 
try:
    app = launchApp("/usr/bin/bluetooth-properties", "bluetooth-properties")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# just an alias to make things shorter
bpFrame = app.bluetoothPropertiesFrame

# Step2: Check the box "Make computer discoverable"
try:
    bpFrame.findLabel("No Bluetooth adapters present")
except SearchError:
    pass
else:
    bpFrame.findPushButton("Close").mouseClick()
    print "This machine doesn't support bluetooth adapter"
    exit(22)
    
make_checkbox = bpFrame.findCheckBox("Make computer discoverable")
if not make_checkbox.checked:
    make_checkbox.mouseClick()
    sleep(config.SHORT_DELAY)

bpFrame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
app.assertClosed()

# Step3: Launch "bluetooth-sendto" to send file to another device
# Touch a test file
if not os.path.exists(file_path):
        os.system('touch %s' % file_path)

# Lanuch bluetooth-sendto
send_app = launchApp("/usr/bin/bluetooth-sendto", "bluetooth-sendto", window='Dialog')
bsDialog = send_app.bluetoothSendtoDialog

# Select a file to send
if not bsDialog.findLabel("Location:").showing:
    bsDialog.findToggleButton("Type a file name").mouseClick()
    sleep(config.SHORT_DELAY)

bsDialog.findText(None, labelledBy="Location:").enterText(file_path)
sleep(config.SHORT_DELAY)

bsDialog.findPushButton("Open").mouseClick()
sleep(config.SHORT_DELAY)

bsDialog.assertClosed()

# Select the first computer device to send to
dsDialog = send_app.findDialog("Select Device to Send To")

dsDialog.findComboBox("All types").findMenuItem("Computer", checkShowing=False).click(log=True)
sleep(config.MEDIUM_DELAY)

dsDialog.findTable(None).findTableCell(None).mouseClick()
sleep(config.SHORT_DELAY)

dsDialog.findPushButton("Send To").mouseClick()
sleep(config.SHORT_DELAY)

dsDialog.assertClosed()

ftDialog = send_app.findDialog("File Transfer")

try:
    ftDialog.findIcon("Warning")
except SearchError:
    sleep(config.LONG_DELAY)
    send_app.assertClosed()
else:
    warning_label = ftDialog.findAllLabels(None)[-1].name
    # Quit app
    ftDialog.findPushButton("Close").mouseClick()
    sleep(config.SHORT_DELAY)
    raise Exception, "ERROR: Fails to sending file via bluetooth, because %s" % warning_label
    exit(2)


