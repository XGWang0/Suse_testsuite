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

from yast2_cluster_config import *
from yast2_test_frame import *

doc="""
Actions:

STEP1: Launch yast2 cluster
STEP2: Enable Security Auth
STEP3: Generate Auth Key File

Expected:

STEP1: /etc/corosync/authkey is created
"""

print doc

key_path = "/etc/corosync/authkey"

UItest = autoUITest()

###### Actions:

# Remove the exist authkey
UItest.removeFile(key_path)

# STEP1: Launch yast2 cluster
app = UItest.launchYastApp("yast2 -gtk cluster&", "y2base")

yFrame = app.findFrame(re.compile('^Cluster - Communication'))

# STEP2: Enable Security Auth
yFrame.findTableCell("Security").mouseClick()
sleep(config.SHORT_DELAY)

enable_cbox = yFrame.findCheckBox("Enable Security Auth")
if not enable_cbox.checked:
    enable_cbox.mouseClick()
    sleep(config.SHORT_DELAY)

# STEP3: Generate Auth Key File
yFrame.findPushButton("Generate Auth Key File").mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog(None).findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:

# STEP1: /etc/corosync/authkey is created
procedurelogger.expectedResult("%s is created" % key_path)
if not os.path.exists(key_path):
    raise Exception, key_path + " doesn't been created"

