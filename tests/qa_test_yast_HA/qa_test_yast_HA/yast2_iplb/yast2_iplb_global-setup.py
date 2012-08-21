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

STEP1: Set up global configuration

Expected:

STEP1: Settings is saved to /etc/ha.d/ldirectord.cf

========================Start Running========================
"""

print doc

conf_path = "/etc/ha.d/ldirectord.cf"
iplb_conf = "/usr/share/qa/qa_test_yast_HA/yast2_iplb/yast2_iplb_config.py"

UItest = autoUITest()

###### Actions:
# STEP1: backup the old /etc/ha.d/ldirectord.cf to initialize the set up
os.system("mv %s %s.bak 2>/dev/null" % (conf_path, conf_path))

# Launch yast2 iplb
app = UItest.launchYastApp("yast2 -gtk iplb&", "y2base")

yFrame = app.findFrame(re.compile('^IPLB - Global'))

# STEP1: Set up global configuration
text_settings = os.popen("grep gt %s |awk '{print $3}'" % iplb_conf).read().strip().replace('"','').split('\n')
texts = yFrame.findPageTab("Global Configuration").findAllTexts(None)
for k, v in zip(texts, text_settings):
    k.insertText(v)

combobox_settings = os.popen("grep gc %s |awk '{print $3}'" % iplb_conf).read().strip().replace('"','').split('\n')
comboboxs = yFrame.findPageTab("Global Configuration").findAllComboBoxs(None)
for k, v in zip(comboboxs, combobox_settings):
    k.findMenuItem(v, checkShowing=False).click(log=True)
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
