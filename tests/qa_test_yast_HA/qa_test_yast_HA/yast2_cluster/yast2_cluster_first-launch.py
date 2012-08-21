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
# Description: First time to launch basic cluster setup test
##############################################################################

from yast2_cluster_config import *
from yast2_test_frame import *

doc="""
Actions:

STEP1: backup the old /etc/corosync/corosync.conf to initialize the first start up
STEP2: set up Communication Channels (udp, 147.2.207.0, 226.94.1.2, 5406, Auto Generate Node ID)
STEP3: set up Security as default (disable)
STEP4: set up Service as default (Booting off, start openais now, enable mgmtd)
STEP5: set up Configure Csync2 as default
STEP6: set Configure conntrackd as default

Expected:

STEP1: /etc/corosync/corosync.conf is created
STEP2: communication channel informations are in corosync.conf
STEP3: secauth shows in corosync.conf is "off"
STEP4: use_mgmtd shows in corosync.conf is "yes"; openais process is running; mgmtd process is running
STEP5: "group ha_group" is created in /etc/csync2/csync2.cfg
"""

print doc

conf_path = "/etc/corosync/corosync.conf"

bind_net_addr_1 = bind_net_addr_1
multicast_addr_1 = multicast_addr_1
multicast_port_1 = multicast_port_1

UItest = autoUITest()

###### Actions:
# Stop openais
sleep(config.SHORT_DELAY)

os.system("rcopenais stop")

# STEP1: backup the old /etc/corosync/corosync.conf to initialize the first start up
os.system("mv %s %s.bak 2>/dev/null" % (conf_path, conf_path))

# Launch yast2 cluster
app = UItest.launchYastApp("yast2 -gtk cluster&", "y2base")

if app._accessible.childCount > 1:
    app.findDialog(None).findPushButton("Install").mouseClick()
    sleep(90)

yFrame = app.findFrame(re.compile('^Cluster - Communication'))

# STEP2: set up Communication Channels 
# (udp, 147.2.207.0, 226.94.1.2, 5406, Auto Generate Node ID)
yFrame.findMenuItem("udp", checkShowing=False).click(log=True)
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

yFrame.findPushButton("Next").mouseClick()
sleep(config.SHORT_DELAY)

# STEP3: set up Security as default (disable)
yFrame = app.findFrame(re.compile('^Cluster - Security'))

yFrame.findPushButton("Next").mouseClick()
sleep(config.SHORT_DELAY)

# STEP4: set up Service as default (Booting off, start openais now, enable mgmtd)
yFrame = app.findFrame(re.compile('^Cluster - Service'))

yFrame.findPushButton("Start openais Now").mouseClick()
sleep(config.MEDIUM_DELAY)

procedurelogger.expectedResult("Current Status is running")
yFrame.findLabel("Running")

yFrame.findPushButton("Next").mouseClick()
sleep(config.SHORT_DELAY)

# STEP5: set up Configure Csync2 as default
yFrame = app.findFrame(re.compile('^Cluster - Configure Csync2'))

yFrame.findPushButton("Next").mouseClick()
sleep(config.SHORT_DELAY)

# STEP6: set Configure conntrackd as default
yFrame = app.findFrame(re.compile('^Cluster - Configure conntrackd'))

yFrame.findPushButton("Next").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:
# STEP1: /etc/corosync/corosync.conf is created
procedurelogger.expectedResult("%s is created" % conf_path)
if not os.path.exists(conf_path):
    raise Exception, conf_path + " doesn't been created"

# STEP2: communication channel informations are in corosync.conf
procedurelogger.action("Checking communication channel informations")

procedurelogger.expectedResult("communication channel informations are in %s" % conf_path)
for m in channel_info:
    UItest.checkInfo(m, conf_path)

# STEP3: secauth shows in corosync.conf is "off"
procedurelogger.expectedResult("secauth shows off in %s" % conf_path)
UItest.checkInfo("secauth:\toff", conf_path)

# STEP4: use_mgmtd shows in corosync.conf is "yes"; openais process is running; mgmtd process is running
procedurelogger.expectedResult("use_mgmtd shows yes in %s" % conf_path)
UItest.checkInfo("use_mgmtd:\tyes", conf_path)

procedurelogger.expectedResult("openais process is running")
UItest.checkProcess("corosync")

procedurelogger.expectedResult("mgmtd process is running")
UItest.checkProcess("mgmtd")

# STEP5: "group ha_group" is created in /etc/csync2/csync2.cfg
procedurelogger.expectedResult("group ha_group is created in /etc/csync2/csync2.cfg")
UItest.checkInfo("ha_group", "/etc/csync2/csync2.cfg")

