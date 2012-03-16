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
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        03/07/2012
# Description: Communication Channels: Redundant Channel setup test
##############################################################################

from strongwind import *
from yast2_cluster_config import *
from yast2_cluster_frame import *

doc="""
Actions:

STEP1: Launch yast2 cluster
STEP2: Set up Communication Channels (udp, 147.2.207.0, 226.94.1.2, 5406, Auto Generate Node ID)
STEP3: Enable and set up Redundant Channel (147.2.212.0, 226.94.1.3, 5407)
STEP4: Set up rrp mode to "passive"

Expected:

STEP1: communication channel informations are in corosync.conf
STEP2: rrp_mode shows "passive" in corosync.conf
"""

print doc

conf_path = "/etc/corosync/corosync.conf"

###### Actions:
# STEP1: Launch yast2 cluster
app = launchYastApp("yast2 -gtk cluster&", "y2base")

yFrame = app.findFrame(re.compile('^Cluster - Communication'))

# STEP2: set up Communication Channels 
# (udp, 147.2.207.0, 226.94.1.2, 5406, Auto Generate Node ID)
yFrame.findMenuItem(transport_type, checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

channel_texts = yFrame.findPanel("Channel").findAllTexts(None)
channel_info = [bind_net_addr_1, multicast_addr_1, multicast_port_1]

def insert(x, y):
    x.text = y
map(insert, channel_texts, channel_info)
sleep(config.SHORT_DELAY)

if not yFrame.findCheckBox("Auto Generate Node ID").checked:
    yFrame.findCheckBox("Auto Generate Node ID").mouseClick()
    sleep(config.SHORT_DELAY)

# STEP3: Enable and set up Redundant Channel (147.2.212.0, 226.94.1.3, 5407)
redundant_cbox = yFrame.findCheckBox("Redundant Channel")
if not redundant_cbox.checked:
    redundant_cbox.mouseClick()
    sleep(config.SHORT_DELAY)

parent_panel = redundant_cbox.parent
redundant_texts = parent_panel.getChildAtIndex(0).findAllTexts(None)
channel_info = [bind_net_addr_2, multicast_addr_2, multicast_port_2]

def insert(x, y):
    x.text = y
map(insert, redundant_texts, channel_info)
sleep(config.SHORT_DELAY)

# STEP4: Set up rrp mode to "passive"
yFrame.findMenuItem(rrp_mode, checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:

# STEP1: communication channel informations are in corosync.conf
procedurelogger.action("Checking communication channel informations")

procedurelogger.expectedResult("communication channel informations are in %s" % conf_path)
for m in channel_info:
    checkInfo(m, conf_path)

# STEP2: rrp_mode shows "passive" in corosync.conf
procedurelogger.expectedResult("rrp_mode shows %s in %s" % (rrp_mode, conf_path))
checkInfo("rrp_mode:\t%s" % rrp_mode, conf_path)

