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
# Date:        05/03/2012
# Description: iplb global configuration setup test
##############################################################################

from yast2_iplb_config import *
from yast2_iplb_frame import *

doc="""
Actions:

STEP1: Add Virtual Server
STEP2: Set up Virtual Server: IP + Port (support IPv4)
STEP3: Set up other configurations
STEP4: Add Real Servers: IP + Port + forwarding method (support IPv4)

Expected:

STEP1: Settings is saved to /etc/ha.d/ldirectord.cf


========================Start Running========================
"""

print doc

conf_path = "/etc/ha.d/ldirectord.cf"

UItest = autoUITest()

###### Actions:
# Launch yast2 iplb
app = UItest.launchYastApp("yast2 -gtk iplb&", "y2base")

yFrame = app.findFrame(re.compile('^IPLB - Global'))

# STEP1: Add Virtual Server
yFrame.findPageTab("Virtual Server Configuration").mouseClick()
sleep(config.SHORT_DELAY)

if yFrame.findPushButton("Delete").sensitive:
    yFrame.findPushButton("Delete").mouseClick()
    sleep(config.SHORT_DELAY)

yFrame.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

yFrame = app.findFrame(re.compile('^IPLB - Virtual'))

# STEP2: Set up Virtual Server: IP + Port (support IPv4)
# STEP3: Set up other configurations
text_settings = os.popen("grep vt yast2_iplb_config.py |awk '{print $3}'").read().strip().replace('"','').split('\n')
texts = yFrame.findAllTexts(None)
for k, v in zip(texts, text_settings):
    k.insertText(v)

combobox_settings = os.popen("grep vc yast2_iplb_config.py |awk '{print $3}'").read().strip().replace('"','').split('\n')
comboboxs = yFrame.findAllComboBoxs(None)
for k, v in zip(comboboxs, combobox_settings):
    k.findMenuItem(v, checkShowing=False).click(log=True)

# STEP4: Add Real Servers: IP + Port + forwarding method (support IPv4)

yFrame.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPushButton("OK").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:
# STEP1: Settings is saved to /etc/ha.d/ldirectord.cf
procedurelogger.expectedResult("%s is created" % conf_path)
if not os.path.exists(conf_path):
    raise Exception, conf_path + " doesn't been created"

for i in set(text_settings + combobox_settings):
    UItest.checkInfo(i, conf_path)
