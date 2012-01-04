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
# Date:        04/07/2011
# Description: Create New Wireless Network Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Network Manager test==
===Create New Wireless Network===
System A:
Step1: Left click on the NetworkManager icon and select Create New Wireless Network 
Step2: Specify an ad-hoc network named "NewTest", Select security method 'None', 
Click the Create button
Step3: Make sure the connection to "NewTest" successful
Step4: SSH connect to System B, using iwconfig connect to "NewTest" wireless
Step5: Make sure System A could ping System B successful
"""
# imports
import os
from strongwind import *
from nm_frame import *
from nm_config import *

print doc

# Make sure have machine settings
if sys1_eth0_ip == "" or sys2_eth0_ip == "":
    raise Exception, "ERROR: Please config nm_config to give machine settings"
    exit(11)

# Get nm-applet application layer
nm_applet_app = nmAppletApp()

# Step1: Left click on the NetworkManager icon, click "Create New Wireless Network"
nm_panel = nmPanel()

nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findMenuItem(re.compile('^Create New Wireless')).mouseClick()
sleep(config.SHORT_DELAY)

create_dialog = nm_applet_app.findDialog("Create New Wireless Network")

# Step2: Specify an ad-hoc network named "NewTest", Select security method "None"
create_dialog.findText(None).typeText('NewTest')
sleep(config.SHORT_DELAY)

# Click the "Create" button
create_dialog.findPushButton("Create").mouseClick()
sleep(config.SHORT_DELAY)

create_dialog.assertClosed()
sleep(30)

# Step3: Make sure the connection to "NewTest" successful
checkInfo(acc_name=['NewTest',])

# Get wireless connection IP of "NewTest"
sys1_wlan0_ip = os.popen("ifconfig wlan0 |grep 'inet addr' |awk '{print $2}'").read().replace('addr:', '').split('\n')[0]

# Step4: SSH connect to System B, using iwconfig connect to "NewTest" wireless
procedurelogger.action('SSH connect to System B, using iwconfig connect to "NewTest" wireless')
os.system("ssh %s iwconfig wlan0 essid off" % sys2_eth0_ip)
os.system("ssh %s ifconfig wlan0 down" % sys2_eth0_ip)
os.system("ssh %s iwconfig wlan0 mode ad-hoc essid \"NewTest\"" % sys2_eth0_ip)

ip_list = sys1_wlan0_ip.split('.')
ip_list[3] = str(int(ip_list[3]) + 5)
sys2_wlan0_ip = '.'.join(ip_list)
os.system("ssh %s ifconfig wlan0 up %s" % (sys2_eth0_ip, sys2_wlan0_ip))
sleep(10)

# Step5: Make sure System A could ping System B successful
procedurelogger.expectedResult("Make sure System A could ping System B successful")
if os.system('ping -c 3 %s' % sys2_wlan0_ip) != 0:
     raise Exception, "ERROR: Fails to ping System B %s" % sys2_wlan0_ip
     exit(1)

# Clean wireless on System A
cleanConnection("NewTest")

# Clean wireless on System B
os.system("ssh %s iwconfig wlan0 essid off" % sys2_eth0_ip)

