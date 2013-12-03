#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Date:        04/06/2011
# Description: openVPN connection Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===openVPN connection===
Step1: Download certificates and keys and uncompress
Step2: Left click on the NetworkManager icon, click "VPN Connections", select "Configure VPN..."
Step3: On "VPN" tab page, click "Add", 
Step4: Select "OpenVPN" on "Choose a VPN Connection Type" dialog, click "Create..."
Step5: On "Editing VPN connection 1" dialog setting VPN informations:
        Gateway: <ip>
        Gateway Type: Certificates (TLS)
        User Certificate: client1.crt
        CA Certificate: ca.crt
        Private Key: client1.key
Step6: Click "Advanced...", check "Use LZO data compression", click "OK"
Step7: Click "Apply" to save the settings
Step8: Left click on the NetworkManager icon, click "VPN Connections", select "VPN connection 1"
Step9: Make sure "VPN connection 1" is checked by checking "ifconfig" that "tun0" appears and url load 10.8.0.1 successfully
"""
# imports
import os

from nm_frame import *
from nm_config import *

print doc

# Make sure have openVPN settings
if crt_download_url == "":
    raise Exception, "ERROR: Please config nm_config to give openVPN settings"
    exit(11)

# Make sure have novellvpn packages
openvpn_rpm = os.system('rpm -q openvpn')
if openvpn_rpm != 0:
    raise Exception, "ERROR: missing openvpn packages"
    exit(11)

# Step1: Download certificates and keys and uncompress
crt_tar = crt_download_url.split('/')[-1]

if not os.path.exists(crt_tar):
    # Check crt download url works
    loadURL(crt_download_url)
    sleep(config.SHORT_DELAY)

    os.system('wget %s' % crt_download_url)
    sleep(config.SHORT_DELAY)

if not os.path.exists(user_crt):
    os.system('tar -xvf %s' % crt_tar)
    sleep(config.SHORT_DELAY)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step2: Left click on the NetworkManager icon, click "VPN Connections", select "Configure VPN..."
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenu("VPN Connections").mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Configure VPN')).click(log=True)
sleep(config.SHORT_DELAY)

nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
connection_dialog = nm_editor_app.findDialog("Network Connections")

# Step3: On "VPN" tab page, click "Add"
connection_dialog.findPushButton("Add").mouseClick()
sleep(config.MEDIUM_DELAY)

type_dialog = nm_editor_app.findAllDialogs(None)[1]

# Step4: Select "OpenVPN" on "Choose a VPN Connection Type" dialog, click "Create..."
type_dialog.findMenuItem("OpenVPN", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

type_dialog.findPushButton("Create...").mouseClick()
sleep(config.SHORT_DELAY)

edit_frame = nm_editor_app.findFrame("Editing VPN connection 1")

# Step5: On "Editing VPN connection 1" dialog setting VPN informations:
#        Gateway: <ip>
#        Gateway Type: Certificates (TLS)
#        User Certificate: client1.crt
#        CA Certificate: ca.crt
#        Private Key: client1.key
edit_frame.findText(None, labelledBy="Gateway:").enterText(openvpn_gateway)
sleep(config.SHORT_DELAY)

vpn_tab = edit_frame.findPageTab("VPN")
vpn_buttons = vpn_tab.findAllPushButtons('(None)')
pwd = os.popen("pwd").read().replace('\n', '') + '/'

# Select User Certificate
vpn_buttons[2].mouseClick()
sleep(config.SHORT_DELAY)
crt_dialog = nm_editor_app.findDialog(re.compile('^Choose your'))

if not crt_dialog.findLabel("Location:").showing:
    crt_dialog.findToggleButton("Type a file name").mouseClick()
    sleep(config.SHORT_DELAY)

crt_dialog.findText(None, labelledBy="Location:").enterText(pwd)
crt_dialog.keyCombo("Enter", grabFocus=False)
sleep(config.SHORT_DELAY)

crt_dialog.findTableCell(user_crt).mouseClick()
sleep(config.SHORT_DELAY)
crt_dialog.findPushButton('Open').mouseClick()
sleep(config.SHORT_DELAY)

# Select CA Certificate
vpn_buttons[1].mouseClick()
sleep(config.MEDIUM_DELAY)

crt_dialog = nm_editor_app.findDialog("Choose a Certificate Authority certificate...")

crt_dialog.findText(None, labelledBy="Location:").enterText(pwd)
crt_dialog.keyCombo("Enter", grabFocus=False)
sleep(config.SHORT_DELAY)

crt_dialog.findTableCell(ca_crt).mouseClick()
sleep(config.SHORT_DELAY)
crt_dialog.findPushButton('Open').mouseClick()
sleep(config.SHORT_DELAY)

# Select Private Key
vpn_buttons[0].mouseClick()
sleep(config.MEDIUM_DELAY)

crt_dialog = nm_editor_app.findDialog(re.compile('^Choose your'))

crt_dialog.findText(None, labelledBy="Location:").enterText(pwd)
crt_dialog.keyCombo("Enter", grabFocus=False)
sleep(config.SHORT_DELAY)

crt_dialog.findTableCell(private_key).mouseClick()
sleep(config.SHORT_DELAY)
crt_dialog.findPushButton('Open').mouseClick()
sleep(config.SHORT_DELAY)

# Step6: Click "Advanced...", check "Use LZO data compression", click "OK"
edit_frame.findPushButton("Advanced...").mouseClick()
sleep(config.MEDIUM_DELAY)

adv_dialog = nm_editor_app.findDialog("OpenVPN Advanced Options")
adv_dialog.findCheckBox("Use LZO data compression").mouseClick()
sleep(config.SHORT_DELAY)

adv_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)
adv_dialog.assertClosed()

# Step7: Click "Apply" to save the settings
edit_frame.findPushButton("Apply").mouseClick()
sleep(config.SHORT_DELAY)
edit_frame.assertClosed()

connection_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
nm_editor_app.assertClosed()

# Step8: Left click on the NetworkManager icon, click "VPN Connections", select "VPN connection 1"
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenu("VPN Connections").mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem("VPN connection 1").mouseClick()
sleep(20)

# Step9: Make sure "VPN connection 1" is checked by checking "ifconfig" that "tun0" appears and url load 10.8.0.1 successfully
procedurelogger.expectedResult('Checking "ifconfig" that "tun0" appears')
if os.system('ifconfig |grep tun0') != 0:
    raise Exception, "ERROR: OpenVPN connection fails"
    exit(1)

loadURL("http://%s" % vpn_dns)

# Disconnect VPN connection 1
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenu("VPN Connections").mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Disconnect VPN')).click(log=True)
sleep(config.SHORT_DELAY)

# Delete VNP connection 1
cleanConnection("VPN connection 1", tab="VPN")
sleep(10)

# Clear OpenVPN crt files
os.system('rm -fr *.crt && rm -fr *.key && rm -fr %s' % crt_tar)

