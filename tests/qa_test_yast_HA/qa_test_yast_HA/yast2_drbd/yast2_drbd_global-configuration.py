#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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
# Date:        11/22/2012
# Description: drbd global configuration setup test
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

doc="""
Action:

 STEP1: Set up Minor Count to default
 STEP2: Set up Dialog Refresh to default
 STEP3: Enable IP Verification

Expect:

 STEP1: Global settings writed in /etc/drbd.conf
 STEP2: minor-count is 5
 STEP3: dialog-refresh is 1
 STEP4: disable-ip-verification if disabled
"""

print doc

conf_path = "/etc/drbd.d/global_common.conf"

UItest = autoUITest()

# Action: 
# Launch yast2 cluster
app = UItest.launchYastApp("yast2 -gtk drbd&", "y2base")

if app._accessible.childCount > 1:
    app.findDialog(None).findPushButton("Install").mouseClick()
    sleep(90)

yFrame = app.findFrame(re.compile('^DRBD - Start-up Configuration'))

yFrame.findTableCell("Global Configuration").mouseClick()
sleep(config.SHORT_DELAY)

dv_checkbox = yFrame.findCheckBox("Disable IP Verification")

if not dv_checkbox.checked:
    dv_checkbox.mouseClick()
    sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.LONG_DELAY)

# Expect:
ui = autoUITest()
procedurelogger.expectedResult("Global settings writed in %s" % conf_path)
ui.checkInfo("minor-count\t5", conf_path)
ui.checkInfo("dialog-refresh\t1", conf_path)
ui.checkInfo("disable-ip-verification", conf_path)
