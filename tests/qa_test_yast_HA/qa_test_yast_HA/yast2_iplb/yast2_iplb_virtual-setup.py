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
# Date:        05/08/2012
# Description: iplb global configuration setup test
##############################################################################

import sys
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
iplb_conf = "/usr/share/qa/qa_test_yast_HA/yast2_iplb/yast2_iplb_config.py"

try:
    ip_type = sys.argv[1]
except IndexError:
    print "Usage: yast2_iplb_virtual-setup.py <ipv4|ipv6>"
    sys.exit(0)

if ip_type == "ipv4":
    text_settings = os.popen("grep vt %s |grep -v ipv6 |awk '{print $3}'" % iplb_conf).read().strip().replace('"','').split('\n')
elif ip_type == "ipv6":
    text_settings = os.popen("grep vt %s |grep -v ipv4 |awk '{print $3}'" % iplb_conf).read().strip().replace('"','').split('\n')
else:
    print "ERROR: IP type should be ipv4 or ipv6"
    exit(2)

combobox_settings = os.popen("grep vc %s |awk '{print $3}'" % iplb_conf).read().strip().replace('"','').split('\n')
real_server_settings = os.popen("grep \"real_server_\" %s |grep %s |awk '{print $3}'" % (iplb_conf, ip_type)).read().strip().replace('"','').split('\n')

if text_settings[0] == '':
    print "ERROR: Please give server settings on yast2_iplb_config.py"
    exit(2)

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

# STEP2: Set up Virtual Server: IP + Port (support IPv4 and IPv6)
# STEP3: Set up other configurations
texts = yFrame.findAllTexts(None)
texts[0].insertText(text_settings[0])
for k, v in zip(texts[1:], text_settings):
    k.insertText(v)

comboboxs = yFrame.findAllComboBoxs(None)
for k, v in zip(comboboxs, combobox_settings):
    k.findMenuItem(v, checkShowing=False).click(log=True)

# STEP4: Add Real Servers: IP + Port + forwarding method (support IPv4 and IPv6)
for i in real_server_settings:
    yFrame.findPushButton("Add").mouseClick()
    sleep(config.SHORT_DELAY)

    dialog = app.findDialog(None)
    dialog.findText(None).insertText(i)
    sleep(config.SHORT_DELAY)
    dialog.findMenuItem(real_forward_method, checkShowing=False).click()
    sleep(config.SHORT_DELAY)
    dialog.findSpinButton(None).text = real_weight

    dialog.findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)

yFrame.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

yFrame.findPushButton("OK").mouseClick()
sleep(config.MEDIUM_DELAY)

###### Expected:
# STEP1: Settings is saved to /etc/ha.d/ldirectord.cf
procedurelogger.expectedResult("%s is created" % conf_path)
if not os.path.exists(conf_path):
    raise Exception, conf_path + " doesn't been created"

for i in set(text_settings + combobox_settings + real_server_settings):
    UItest.checkInfo(i, conf_path)
