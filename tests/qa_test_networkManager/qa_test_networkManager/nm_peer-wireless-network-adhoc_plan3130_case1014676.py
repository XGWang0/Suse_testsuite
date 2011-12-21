#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Written by: Calen Chen <cachen@novell.com>
# Date:        01/17/2011
# Description: Peer Wireless Network Ad-Hoc Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Peer Wireless Network Ad-Hoc test===
Step1: Left click on the NetworkManager icon and select Create New Wireless Network 
Step2: Specify an adhoc network name 'adhoc_test', Select security method 'None', 
Click the Create button
Step3: Right click on the NetworkManager icon, select Edit Connections
Step4: Select the Wireless tab, select the adhoc network 'adhoc_test' and click the edit button
Step5: Select the Ipv4 Settings tab select the Manual method in the drop down
Step6: Click the Add button and enter a local IP address, Netmask and Gateway, i.e. 192.168.0.1, 255.255.255.0, and 192.168.0.254 respectively, 
Leave DNS Servers and Search Domains blank
Step7: Click Apply
Step8: Left click on the NetworkManager icon and select Connect to Hidden Wireless Network
Step9: Select adhoc network 'adhoc_test' on the connection dropdown and click Connect
Step10: Right click on the NetworkManager icon, select Connection Information
Step11: Click 'adhoc_test' Page Tab, make sure IP is 192.168.0.1
Step12: Left click on the NetworkManager icon, make sure 'adhoc_test' radiobutton is checked
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

old_apps = cache._desktop.findAllApplications(None)

# Step1: Left click on the NetworkManager icon and select Create New Wireless Network 
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Create New Wireless')).mouseClick()
sleep(config.SHORT_DELAY)

create_dialog = nm_applet_app.findDialog("Create New Wireless Network")

# Step2: Specify an adhoc network name 'adhoc_test', Select security method 'None', Click the Create button
create_dialog.findText(None).typeText('adhoc_test')
sleep(config.SHORT_DELAY)

create_dialog.findPushButton("Create").mouseClick()
sleep(config.SHORT_DELAY)

new_apps = cache._desktop.findAllApplications(None)
if len(new_apps) == len(old_apps):
    pass
else:
    authenticate = cache._desktop.findApplication('polkit-gnome-manager', checkShowing=False)
    authen_dialog = authenticate.findDialog("Authenticate")
    authen_dialog.findPasswordText(None).typeText(sys1_root_pwd)
    sleep(config.SHORT_DELAY)

    authen_dialog.findCheckBox("Remember authorization").mouseClick()
    sleep(config.SHORT_DELAY)

    authen_dialog.findPushButton("Authenticate").mouseClick()
    sleep(config.SHORT_DELAY)

create_dialog.assertClosed()
sleep(20)

# Step3: Right click on the NetworkManager icon, select Edit Connections
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Edit Connections')).click(log=True)
sleep(config.SHORT_DELAY)

nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
connection_dialog = nm_editor_app.findDialog("Network Connections")

# Step4: Select the Wireless tab, select the adhoc network 'adhoc_test' and click the edit button
connection_dialog.findPageTab("Wireless").mouseClick()
sleep(config.SHORT_DELAY)

connection_dialog.findTableCell("adhoc_test").mouseClick()
sleep(config.SHORT_DELAY)

connection_dialog.findPushButton("Edit").mouseClick()
sleep(config.SHORT_DELAY)

editing_frame = nm_editor_app.findFrame("Editing adhoc_test")

# Step5: Select the Ipv4 Settings tab select the Manual method in the drop down
ipv4_tab = editing_frame.findPageTab("IPv4 Settings")
ipv4_tab.mouseClick()
sleep(config.SHORT_DELAY)

editing_frame.findMenuItem("Manual", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Step6: Click the Add button and enter a local IP address, Netmask and Gateway, i.e. 192.168.0.1, 255.255.255.0, and 192.168.0.254 respectively, Leave DNS Servers and Search Domains blank
editing_frame.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

address_cells = ipv4_tab.findAllTableCells(None)
address_list = ['192.168.0.1', '255.255.255.0', '192.168.0.254']

def insert(x, y):
    x.typeText(y)
map(insert, address_cells, address_list)
sleep(config.SHORT_DELAY)

# Step7: Click Apply
editing_frame.findPushButton("Apply").mouseClick()
sleep(config.SHORT_DELAY)

# Make sure only one "adhoc_test" on the list
adhocs = connection_dialog.findAllTableCells("adhoc_test")

if len(adhocs) != 1:
    connection_dialog.findPushButton("Close").mouseClick()
    sleep(config.SHORT_DELAY)
    raise Exception, "Edit wireless action shouldn't create a new adhoc_test"
    exit(1)

connection_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.assertClosed()

# Step8: Left click on the NetworkManager icon and select Connect to Hidden Wireless Network
nm_panel = nmPanel()
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Connect to Hidden')).click(log=True)
sleep(config.SHORT_DELAY)

connect_dialog = nm_applet_app.findDialog("Connect to Hidden Wireless Network")

# Step9: Select adhoc network 'adhoc_test' on the connection dropdown and click Connect
connect_dialog.findAllMenuItems("adhoc_test", checkShowing=False)[-1].click(log=True)
sleep(config.MEDIUM_DELAY)

connect_dialog.findPushButton("Connect").mouseClick()
sleep(30)

# Step10: Right click on the NetworkManager icon, select Connection Information
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Connection Information')).click(log=True)
sleep(config.SHORT_DELAY)

info_dialog = nm_applet_app.findDialog("Connection Information")

# Step11: Click 'adhoc_test' Page Tab, make sure IP is 192.168.0.1
info_dialog.findPageTab("adhoc_test").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Connect to test with IP: 192.168.0.1")
info_dialog.findLabel("192.168.0.1")

info_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
info_dialog.assertClosed()

# Step12: Left click on the NetworkManager icon, make sure 'adhoc_test' radiobutton is checked
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)
adhocs = nm_applet_app.findWindow(None).findAllCheckMenuItems("adhoc_test", checkShowing=False)

procedurelogger.expectedResult("Make sure 'adhoc_test' is checked")
assert adhocs[0].checked == True, "Network doesn't connect to test"

# Make sure only one "adhoc_test" on the wireless list
procedurelogger.expectedResult('Make sure only one "adhoc_test" on the wireless list')
if len(adhocs) != 1:
    nm_panel.mouseClick(log=False)
    sleep(config.SHORT_DELAY)
    raise Exception, "Edit wireless action shouldn't create new adhoc_test"
    exit(1)

# Remove test connection
nm_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)

cleanConnection("adhoc_test")

