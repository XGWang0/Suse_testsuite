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
# Description: drbd resource configuration setup test
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

doc="""
Action:

 STEP1: Click Add button to create drbd resource
 STEP2: Set up Resource Name: r0
 STEP3: Set up Node1: Name(server1), Address:Port(192.168.0.23:7789), Device(/dev/drbd0), Disk(/dev/loop0), Meta-disk(internal)
 STEP4: Set up Node2: Name(server2), Address:Port(192.168.0.24:7789), Device(/dev/drbd0), Disk(/dev/loop0), Meta-disk(internal)
 STEP5: Click Advance Config
 STEP6: Set up Syncer Rate to 2M

Expect:

 STEP1: Resource settings writed in /etc/drbd.d/r0.res
 STEP2: resouce r0 exist in configuration file
 STEP3: on server1 exist in configuration file
 STEP4: on server2 exist in configuration file 
 STEP5: syncer settings writed in /etc/drbd.d/r0.res, rate is 2M
"""

print doc

conf_path = "/etc/drbd.d/r0.res"

UItest = autoUITest()

# Action: 
# Launch yast2 cluster
app = UItest.launchYastApp("yast2 -gtk drbd&", "y2base")

if app._accessible.childCount > 1:
    app.findDialog(None).findPushButton("Install").mouseClick()
    sleep(90)

yFrame = app.findFrame(re.compile('^DRBD - Start-up Configuration'))

yFrame.findTableCell("Resource Configuration").mouseClick()
sleep(config.SHORT_DELAY)

# insert configurations into text boxs
yFrame.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

infos = [resource_name, director_name, director_addr_port, director_device, director_disk, director_meta, node1_name, node1_addr_port, node1_device, node1_disk, node1_meta]
textboxs = yFrame.findAllTexts(None)

def insert(x, y):
    x.text = y
map(insert, textboxs, infos)
sleep(config.SHORT_DELAY)

# Advanced config
yFrame.findPushButton("Advanced Config").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findAllTexts(None)[-2].text = "2M"
sleep(config.SHORT_DELAY)

yFrame.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.LONG_DELAY)

# Expect:
ui = autoUITest()
procedurelogger.expectedResult("resource settings writed in %s" % conf_path)
ui.checkInfo("resource r0", conf_path)
ui.checkInfo("on server1", conf_path)
ui.checkInfo("on director", conf_path)
ui.checkInfo("rate\t2M;", conf_path)
