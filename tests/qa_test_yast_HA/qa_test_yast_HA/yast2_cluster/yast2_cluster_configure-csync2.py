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
# Date:        03/29/2012
# Description: Configure Csync2 test
##############################################################################

from strongwind import *
from yast2_cluster_config import *
from yast2_cluster_frame import *
from remote_setup_frame import *

doc="""

TestCase1 Actions:

STEP1: Launch yast2 cluster
STEP2: Generate Pre-Shared-keys to create /etc/csync2/key_hagroup
STEP3: Add Suggested Files that /etc/csync2/key_hagroup will be added to the list
STEP4: Add server1 and server2 to Sync Host list 
STEP5: Turn csync2 ON

Expected:

STEP1: host server1 server2 shows in /etc/csync2/csync2.cfg
STEP2: "chkconfig -l |grep csync2" shows "on"

TestCase2 Actions:

STEP1: copy /etc/csync2/csync2.cfg to server2
STEP2: copy /etc/csync2/key_hagroup to server2
STEP3: chkconfig csync2 on; chkconfig xinetd on
STEP4: start xinetd process: #rcxineted start
STEP5: start csync2: #csync2 -xv 2>&1 |grep "Finished with 0 errors"

Expected:

STEP1: csync finished with 0 errors
"""

print doc

cfg_path = "/etc/csync2/csync2.cfg"
key_path = "/etc/csync2/key_hagroup"

######TestCase1 Actions:

# Clean the exist file
removeFile(key_path)

# STEP1: Launch yast2 cluster
app = launchYastApp("yast2 -gtk cluster&", "y2base")

yFrame = app.findFrame(re.compile('^Cluster - Communication'))

# STEP2: Generate Pre-Shared-keys to create /etc/csync2/key_hagroup
yFrame.findTableCell("Configure Csync2").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPushButton("Generate Pre-Shared-Keys").mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog(None).findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("%s is created" % key_path)
if not os.path.exists(key_path):
    raise Exception, key_path + " doesn't been created"

# STEP3: Add Suggested Files that /etc/csync2/key_hagroup will be added to the list
yFrame.findPushButton("Add Suggested Files").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("%s be added to the list" % key_path)
yFrame.findPanel("Sync File").findTableCell(key_path)

# STEP4: Add server1 and server2 to Sync Host list 
yFrame.findPanel("Sync Host").findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)
app.findDialog(None).findText(None).insertText(node1_hostname)
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPanel("Sync Host").findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)
app.findDialog(None).findText(None).insertText(node2_hostname)
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

# STEP5: Turn csync2 ON
if os.system("chkconfig -l |grep csync2 |grep on") is None:
    yFrame.findPushButton("Turn csync2 ON").mouseClick()
    sleep(config.SHORT_DELAY)

yFrame.findPushButton("Finish").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:

# STEP1: host server1 server2 shows in /etc/csync2/csync2.cfg
procedurelogger.expectedResult("%s shows in %s" % (node1_hostname, cfg_path))
checkInfo(node1_hostname, cfg_path)

procedurelogger.expectedResult("%s shows in %s" % (node2_hostname, cfg_path))
checkInfo(node2_hostname, cfg_path)

# STEP2: "chkconfig -l |grep csync2" shows "on"
procedurelogger.expectedResult("csync2 services is enabled")
if os.system("chkconfig -l |grep csync2 |grep on") is None:
    raise Exception, "csync2 services didn't enabled"

######TestCase2 Actions:

# STEP1: copy /etc/csync2/csync2.cfg to server2
# STEP2: copy /etc/csync2/key_hagroup to server2
copy_file = "/etc/csync2/csync2.cfg /etc/csync2/key_hagroup"
copy_path = "/etc/csync2/"
procedurelogger.action("copy %s to %s" % (copy_file, node2_ip))
scp_run(node2_ip, node2_pwd, user="root", copy_file=copy_file, copy_path=copy_path)

# STEP3: chkconfig csync2 on; chkconfig xinetd on
procedurelogger.action("chkconfig to make csync2 and xinetd on")
os.system("chkconfig csync2 on")
os.system("chkconfig xinetd on")

status=os.popen("chkconfig -l |grep -E \"csync2|xinetd\" |grep -c on").read().strip()
if status != '2':
    raise Exception, "csync2 or xinetd services didn't enabled"

# STEP4: start xinetd process: #rcxinetd start
procedurelogger.action("start xinetd process")
if os.system("rcxinetd start") != 0:
    raise Exception, "xinetd process doesn't start"

# STEP5: start csync2: #csync2 -xv 2>&1 |grep "Finished with 0 errors"
procedurelogger.action("start csync2")

######Expected:

# STEP1: csync finished with 0 errors
procedurelogger.expectedResult("csync finished with 0 errors")
if os.system("csync2 -xv 2>&1 |grep \"Finished with 0 errors\"") != 0:
    raise Exception, "csync nodes with error"