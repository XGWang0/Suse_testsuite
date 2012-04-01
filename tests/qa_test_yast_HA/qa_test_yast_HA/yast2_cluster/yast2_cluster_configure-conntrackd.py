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
# Date:        04/01/2012
# Description: Communication Channels: Redundant Channel setup test
##############################################################################

from strongwind import *
from yast2_cluster_config import *
from yast2_cluster_frame import *

doc="""
Actions:

STEP1: Set up Multicast Address and Group Number (226.94.1.2, 1)
STEP2: Generate /etc/conntrackd/conntrackd.conf

Expected:

STEP1: /etc/conntrackd/conntrackd.conf is created
"""

print doc

conf_path = "/etc/corosync/corosync.conf"
multicast_addr = multicast_addr_1
group_num = "1"

###### Actions:

# Remove exists conntrackd.conf
removeFile("/etc/conntrackd/conntrackd.conf")

# Launch yast2 cluster
app = launchYastApp("yast2 -gtk cluster&", "y2base")

yFrame = app.findFrame(re.compile('^Cluster - Communication'))

# STEP1: Set up Multicast Address and Group Number (226.94.1.2, 1)
yFrame.findTableCell("Configure conntrackd").mouseClick()
sleep(config.SHORT_DELAY)

texts = yFrame.findAllTexts(None)
texts[0].insertText(multicast_addr)
texts[1].insertText(group_num)
sleep(config.SHORT_DELAY)

# STEP2: Generate /etc/conntrackd/conntrackd.conf
yFrame.findPushButton(re.compile('^Generate')).mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog(None).findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:
# STEP1: /etc/conntrackd/conntrackd.conf is created
procedurelogger.expectedResult("/etc/conntrackd/conntrackd.conf is created")
if not os.path.exists("/etc/conntrackd/conntrackd.conf"):
    raise Exception, "Missing /etc/conntrackd/conntrackd.conf"
