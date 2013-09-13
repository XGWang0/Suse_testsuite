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
# Date:        03/05/2012
# Description: Enable accessibility, enable xhost, restart gdm
##############################################################################

import os
import getopt

frame_path = "/usr/share/qa/qa_test_yast_HA/yast2_cluster/yast2_test_frame.py"
os.system("sed -i '/^from strongwind/s/from strongwind/#from strongwind/' %s" % frame_path)

from yast2_test_frame import *

node_ip = None
node_pwd = None

opts = []
args = []
opts, args = getopt.getopt(sys.argv[1:],"hi:p:",["help","ip=","password="])

for o, a in opts:
    if o in ("-h", "--help"):
        print "Usage: remote_setup_UI-test.py -i <machine ip> -p <machine password>"
        sys.exit(0)
    if o in ("-i", "--ip"):
        node_ip = a
    if o in ("-p", "--pwd"):
        node_pwd = a

if node_ip == None or node_pwd == None:
    from yast2_cluster_config import *
    if node1_ip and node1_pwd:
        node_ip = node1_ip
        node_pwd = node1_pwd
    else:
        print "Usage: remote_setup_UI-test.py -i <machine ip> -p <machine password>"
        sys.exit(1)

# Install UI related patterns
rs = remoteSetting(node_ip=director_ip, node_pwd=director_pwd)

rs.install_Patterns(patterns=["X11", "gnome"])

# Enable accessibility technology which the machine you want to run UI tool
rs.setup_UItest()
sleep(30)

os.system("sed -i '/^#from strongwind/s/#from strongwind/from strongwind/' %s" % frame_path)

