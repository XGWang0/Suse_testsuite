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
# Description: launch basic drbd setup test
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

doc="""
Actions:

STEP1: Set up Booting to On
STEP2: Start DRBD Server Now

Expected:

STEP1: drbd services is enabled
STEP2: drbd process is running
"""

print doc

conf_path = "/etc/drbd.conf"

UItest = autoUITest()

# Action:
# Launch yast2 cluster
app = UItest.launchYastApp("yast2 -gtk drbd&", "y2base")

if app._accessible.childCount > 1:
    app.findDialog(None).findPushButton("Install").mouseClick()
    sleep(90)

yFrame = app.findFrame(re.compile('^DRBD - Start-up Configuration'))

yFrame.findTableCell("Start-up Configuration").mouseClick()
sleep(config.SHORT_DELAY)

# STEP2: Set up Booting to On
on_radiobutton = yFrame.findRadioButton(re.compile('^On'))

if not on_radiobutton.checked:
    on_radiobutton.mouseClick()
    sleep(config.SHORT_DELAY)

# STEP3: start DRBD Server Now
yFrame.findPushButton("Start DRBD Server Now").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.LONG_DELAY)

# Expect:
# STEP1: drbd services is enabled
procedurelogger.expectedResult("drbd services is enabled")
status = set(os.popen('chkconfig -l |grep drbd').read().split(' '))

if "2:on" not in status:
    raise Exception, "drbd services is not enabled"

# STEP2: drbd process is running
procedurelogger.expectedResult("drbd process is running")
status =  os.system('ps -ef |grep drbd |grep -v grep')

if status != 0:
    raise Exception, "drbd process is not running"
