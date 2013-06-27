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
# Date:        03/28/2012
# Description: Communication Channels: Redundant Channel setup test
##############################################################################

from yast2_cluster_config import *
from yast2_test_frame import *

doc="""
Actions:

STEP1: Launch yast2 cluster
STEP2: Start openais at booting
STEP3: Stop openais Now
STEP4: Disable mgmtd

Expected:

STEP1: openais services is enabled:  #chkconfig -l |grep openais |grep on
STEP2: openais process is not running: #ps -ef |grep openais |grep -v grep
STEP3: use_mgmtd shows in corosync.conf is "no"
"""

print doc

conf_path = "/etc/corosync/corosync.conf"

UItest = autoUITest()

###### Actions:

# STEP1: Launch yast2 cluster
app = UItest.launchYastApp("yast2 -gtk cluster&", "y2base")

yFrame = app.findFrame(re.compile('^Cluster - Communication'))

# STEP2: Start openais at booting
yFrame.findTableCell("Service").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findRadioButton(re.compile('^On')).mouseClick()
sleep(config.SHORT_DELAY)

# STEP3: Stop openais Now
yFrame.findPushButton("Stop openais Now").mouseClick()
sleep(config.MEDIUM_DELAY)

# STEP4: Disable mgmtd
enable_cbox = yFrame.findCheckBox(re.compile('^Enable mgmtd'))
if enable_cbox.checked:
    enable_cbox.mouseClick()
    sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:
# STEP1: openais services is enabled:  #chkconfig -l |grep openais |grep on
procedurelogger.expectedResult("openais services is enabled")
if os.system("chkconfig -l |grep openais |grep on") is None:
    raise Exception, "openais services didn't enabled"

# STEP2: openais process is not running
procedurelogger.expectedResult("openais process is not running")
UItest.checkProcess("corosync", status=False)

# STEP3: use_mgmtd shows in corosync.conf is "no"
procedurelogger.expectedResult("use_mgmtd shows no in %s" % conf_path)
UItest.checkInfo("use_mgmtd:\tno", conf_path)

