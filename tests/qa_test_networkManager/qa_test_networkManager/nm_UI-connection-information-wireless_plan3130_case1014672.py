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
# Date:       03/25/2011
# Description: Wireless UI Connection Information Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Wired UI Connection Information===
Step1: Left click NetworkManager icon, click wireless1_name wirelese to connect
Step2: Right click NetworkManager icon, Click "Connection Information" to launch dialog
Step3: Choose wireless1_name tab page
Step4: Make sure wired connection informations shows the same as ifconfig
"""
# imports
import os
from nm_frame import *
from nm_config import *

print doc

# Make sure have Wireless settings
if wireless1_name=="":
    raise Exception, "ERROR: Please config nm_config to give Wireless settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Left click NetworkManager icon, click wireless1_name wirelese to connect
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless1_name).mouseClick()
sleep(20)
authenWireless(wireless1_pwd)

# Step2: Right click NetworkManager icon, Click "Connection Information" to launch dialog
nm_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem("Connection Information").click(log=True)
sleep(config.SHORT_DELAY)

info_dialog = nm_applet_app.findDialog("Connection Information")

# Step3: Choose wireless1_name tab page
wired_tab = info_dialog.findPageTab("Auto %s" % wireless1_name)

wired_tab.mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Make sure wireless connection informations shows the same as system as UI
labels = wired_tab.findAllLabels(None)

label_list = []
for i in labels:
  label_list.append(i.name)
label_list.remove('')

UI_info_dict = dict(zip(label_list[1::2], label_list[0::2]))

# Get all informations from system
expect_info_dict = {}
ip = os.popen("ifconfig wlan0 |grep 'inet addr' |awk '{print $2}'").read().replace('addr:', '').split('\n')[0]
expect_info_dict["IP Address:"] = ip

broadcase = os.popen("ifconfig wlan0 |grep 'inet addr' |awk '{print $3}'").read().replace('Bcast:', '').split('\n')[0]
expect_info_dict["Broadcast Address:"] = broadcase

mask = os.popen("ifconfig wlan0 |grep 'inet addr' |awk '{print $4}'").read().replace('Mask:', '').split('\n')[0]
expect_info_dict["Subnet Mask:"] = mask

hwaddr = os.popen("ifconfig wlan0 |grep 'HWaddr' |awk '{print $5}'").read().split('\n')[0]
expect_info_dict["Hardware Address:"] = hwaddr

os.system('ifconfig eth0 down')
sleep(config.LONG_DELAY)
route = os.popen("route |grep 'default' |awk '{print $2}'").read().replace('\n', '')
expect_info_dict["Default Route:"] = route

driver = os.popen("hwinfo --netcard |grep -2 'Device File: wlan0'").read().split("\n")[0].replace('  Driver: "', '').replace('"', '')
expect_info_dict["Driver:"] = driver

dns1 = os.popen("cat /etc/resolv.conf |grep nameserver").read().split(' ')[1].replace('\n', '')
expect_info_dict["Primary DNS:"] = dns1
sleep(config.SHORT_DELAY)
os.system('ifconfig eth0 up')
sleep(20)

speed = os.popen("iwconfig wlan0 |grep Rate").read().replace('  ','').split('=')[1].replace(' Tx-Power', '')
expect_info_dict["Speed:"] = speed

procedurelogger.action("Diff Connection Informations from UI shows with the system get")
procedurelogger.expectedResult("Wireless connection informations shows the same as system as UI")
for i in expect_info_dict.items():
    if i in UI_info_dict.items():
        pass
    else:
        info_dialog.findPushButton("Close").mouseClick()
        sleep(config.SHORT_DELAY)
        nm_applet_app.assertClosed()
        raise Exception, "ERROR: Different information %s with in UI Connection Information dialog shows" % str(i)

# Close dialog
info_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
nm_applet_app.assertClosed()


