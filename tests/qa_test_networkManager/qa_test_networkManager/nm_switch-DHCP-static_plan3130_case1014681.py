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
# Written by: Calen Chen <cachen@novell.com>
# Date:        02/23/2011
# Description: Switch static IP address and DHCP Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Switch static IP address and DHCP===
Change DHCP to Static address:
Step1: Right click on the NetworkManager icon, select "Edit Connections"
Step2: On "Wired" tab page, select "System eth0", click Edit
Step3: Exit the test if Root Authenticate dialog pops up, Enter root password manually and 
enable "Remember authorization", then rerun the test
Step4: Click "IPv4 Settings" tab page, select "Manual" method
Step5: Click the Add button and enter a local IP address, Netmask and Gateway, i.e. 147.2.207.143, 255.255.255.0, and 147.2.207.254, DNS Servers is 147.2.136.75,137.65.1.1 those are setting in nm_config
Step6: Click Apply
Step7: Left click on the NetworkManager icon and select "System eth0" wired network to reload
Step8: Make sure Network connection is successful to open url i.e. www.google.com
Step9: Right click on the NetworkManager icon, select Connection Information
Step10: Make sure IP Address is 147.2.207.143

Change Static address to DHCP:
Step1: Right click on the NetworkManager icon, select "Edit Connections"
Step2: On "Wired" tab page, select "System eth0", click Edit
Step3: Click "IPv4 Settings" tab page, select "Automatic (DHCP)" method
Step4: Click Apply
Step5: Left click on the NetworkManager icon and select "System eth0" wired network to reload
Step6: Make sure Network connection is successful to open url i.e. www.google.com
Step7: Right click on the NetworkManager icon, select Connection Information
Step8: Make sure IP Address is 147.2.207.143
"""
# imports
from nm_frame import *
from nm_config import *

print doc

# Make sure have Static network settings
if static_ip=="":
    raise Exception, "ERROR: Please config nm_config to give static network settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Change DHCP to Static address:
# Step1: Right click on the NetworkManager icon, select "Edit Connections"
nm_panel = nmPanel()

nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Edit Connections')).click(log=True)
sleep(config.SHORT_DELAY)

nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
connection_dialog = nm_editor_app.findDialog("Network Connections")

# Step2: On "Wired" tab page, select "System eth0", click Edit
connection_dialog.findTableCell("System eth0").mouseClick()
sleep(config.SHORT_DELAY)

connection_dialog.findPushButton(re.compile('^Edit')).mouseClick()
sleep(config.SHORT_DELAY)

# Step3: Exit the test if Root Authenticate dialog pops up, Enter root password manually and 
# enable "Remember authorization", then rerun the test
try:
    editing_frame = nm_editor_app.findFrame("Editing System eth0")
except SearchError:
    authenticate = cache._desktop.findApplication('polkit-gnome-manager', checkShowing=False)
    authen_dialog = authenticate.findDialog("Authenticate")
    authen_dialog.findPasswordText(None).typeText(sys1_root_pwd)
    sleep(config.SHORT_DELAY)

    authen_dialog.findCheckBox("Remember authorization").mouseClick()
    sleep(config.SHORT_DELAY)

    authen_dialog.findPushButton("Authenticate").mouseClick()
    sleep(config.SHORT_DELAY)

# Step4: Click "IPv4 Settings" tab page, select "Manual" method
ipv4_tab = editing_frame.findPageTab("IPv4 Settings")
sleep(config.SHORT_DELAY)
ipv4_tab.mouseClick()
sleep(config.SHORT_DELAY)

if ipv4_tab.findComboBox(None).name == "Manual":
    editing_frame.findMenuItem("Automatic (DHCP)", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)

editing_frame.findMenuItem("Manual", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Step5: Click the Add button and enter a local IP address, Netmask and Gateway, i.e. 147.2.207.143, 255.255.255.0, and 147.2.207.254, DNS Servers is 147.2.136.75,137.65.1.1 those are setting in nm_config
editing_frame.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

address_cells = ipv4_tab.findAllTableCells(None)
address_list = [static_ip, static_mask, static_gateway]

def insert(x, y):
    x.typeText(y)
map(insert, address_cells, address_list)
sleep(config.SHORT_DELAY)

for i in ipv4_tab.findAllTexts(None):
    i.enterText(static_dns)
#ipv4_tab.findAllTexts(None)[-1].enterText(static_dns)

# Step6: Click Apply
editing_frame.findPushButton(re.compile('^Apply')).mouseClick()
sleep(config.SHORT_DELAY)
# Sometimes need root authenticate
try:
    authenticate = cache._desktop.findApplication('polkit-gnome-manager', checkShowing=False)
except SearchError:
    pass
else:
    authen_dialog = authenticate.findDialog("Authenticate")
    authen_dialog.findPasswordText(None).typeText(sys1_root_pwd)
    sleep(config.SHORT_DELAY)
    authen_dialog.findPushButton("Authenticate").mouseClick()
    sleep(config.SHORT_DELAY)

editing_frame.assertClosed()

connection_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
nm_editor_app.assertClosed()

# Step7: Left click on the NetworkManager icon and select "System eth0" wired network to reload
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem("System eth0").mouseClick()
sleep(20)

# Step8: Make sure Network connection is successful to open url i.e. www.google.com
loadURL('http://www.google.com/')

# Step9: Right click on the NetworkManager icon, select Connection Information
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Connection Information')).click(log=True)
sleep(config.SHORT_DELAY)

info_dialog = nm_applet_app.findDialog("Connection Information")

# Step10: Make sure IP Address is 147.2.207.143
procedurelogger.expectedResult("Connect with IP: %s" % static_ip)
info_dialog.findLabel(static_ip)

info_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
info_dialog.assertClosed()

# Change Static address to DHCP:
# Step1: Right click on the NetworkManager icon, select "Edit Connections"
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Edit Connections')).click(log=True)
sleep(config.SHORT_DELAY)

nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
connection_dialog = nm_editor_app.findDialog("Network Connections")

# Step2: On "Wired" tab page, select "System eth0", click Edit
connection_dialog.findTableCell("System eth0").mouseClick()
sleep(config.SHORT_DELAY)

connection_dialog.findPushButton(re.compile('^Edit')).mouseClick()
sleep(config.SHORT_DELAY)
editing_frame = nm_editor_app.findFrame("Editing System eth0")

# Step3: Click "IPv4 Settings" tab page, select "Automatic (DHCP)" method
ipv4_tab = editing_frame.findPageTab("IPv4 Settings")
sleep(config.SHORT_DELAY)
ipv4_tab.mouseClick()
sleep(config.SHORT_DELAY)

editing_frame.findMenuItem("Automatic (DHCP)", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Step4: Click Apply
editing_frame.findPushButton(re.compile('^Apply')).mouseClick()
sleep(config.SHORT_DELAY)
# Sometimes need root authenticate
try:
    authenticate = cache._desktop.findApplication('polkit-gnome-manager', checkShowing=False)
    authen_dialog = authenticate.findDialog("Authenticate")
    authen_dialog.findPasswordText(None).typeText(sys1_root_pwd)
    sleep(config.SHORT_DELAY)
    authen_dialog.findPushButton("Authenticate").mouseClick()
    sleep(config.SHORT_DELAY)
except SearchError:
    pass
editing_frame.assertClosed()

connection_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
nm_editor_app.assertClosed()

# Step5: Left click on the NetworkManager icon and select "System eth0" wired network to reload
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem("System eth0").mouseClick()
sleep(20)

# Step6: Make sure Network connection is successful to open url i.e. www.google.com
loadURL('http://www.google.com/')

# Step7: Right click on the NetworkManager icon, select Connection Information
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Connection Information')).click(log=True)
sleep(config.SHORT_DELAY)

info_dialog = nm_applet_app.findDialog("Connection Information")

# Step8: Make sure IP Address is not 147.2.207.143
procedurelogger.expectedResult("IP Address is not %s" % static_ip)
try:
    info_dialog.findLabel(static_ip)
except SearchError:
    pass
else:
    raise Exception, "IP Address should not be %s" % static_ip
    exit(1)

info_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
info_dialog.assertClosed()

