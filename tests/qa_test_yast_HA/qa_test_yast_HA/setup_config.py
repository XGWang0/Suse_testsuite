#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        05/30/2012
# Description: Use for setting up arguments in configuration files for each 
#              HA Yast2 tools UI testsuit include yast2_cluster yast2_iplb 
#              yast2_drbd
##############################################################################

import os
import sys

config_path = ""
suit = ""
v_name = "node"
args = sys.argv[1:]

# Setting test suit argument
try:
    if args[0] == "cluster":
        config_path="/usr/share/qa/qa_test_yast_HA/yast2_cluster/yast2_cluster_config.py"
        suit = "cluster"
    elif args[0] == "iplb":
        config_path = "/usr/share/qa/qa_test_yast_HA/yast2_iplb/yast2_iplb_config.py"
        suit = "iplb"
        v_name = "real_server"
    elif args[0] == "drbd":
        config_path = "/usr/share/qa/qa_test_yast_HA/yast2_drbd/yast2_drbd_config.py"
        suit = "drbd"
    else:
        raise Exception, "There is no %s test suit" % args[0]
except IndexError:
    print """Warning: Please give argument which test suit you want to run:
    %s [cluster|iplb|drbd] <node_ip> <node_ip>""" % sys.argv[0]
    exit(1)

# Check OS version
os_release = os.popen("cat /etc/SuSE-release |awk 'NR==1'").read().strip()
gui_server_ip = os.popen("ifconfig |grep 'inet addr' |awk '{print $2}' |head -n 1 |cut -d ':' -f2").read().strip()

exec(os.popen("cat /etc/SuSE-release |grep -v SUSE").read().split('\n')[0])
exec(os.popen("cat /etc/SuSE-release |grep -v SUSE").read().split('\n')[1])

if PATCHLEVEL < 2:
    print """###############################################################
Warning: This test was created in SLES-SP2, but you are running \non %s %s, that might got some test \nfailed due to difference UI design!"
###############################################################""" % (os_release, PATCHLEVEL)

# Update configuration files
exec(os.popen("grep ip %s" % config_path).read())

if not director_ip or director_ip != gui_server_ip:
    os.system("sed -i '/director_ip/s/director_ip.*/director_ip = \"%s\"/g' %s" % (gui_server_ip, config_path))

for i in range(len(args[1:])):
    vname = v_name + str(i+1)

    if os.system("grep %s_ip %s >/dev/null" % (vname, config_path)) == 0:
        os.system("sed -i '/%s_ip/s/%s_ip.*/%s_ip = \"%s\"/g' %s" % (vname,vname,vname,args[i+1],config_path))
    else:
        os.system("echo '\n%s_ip = \"%s\"\n%s_pwd = \"susetesting\"' >> %s" % (vname, args[i+1], vname, config_path))

    if suit == "iplb":
        os.system("sed -i '/real_server_%s_ipv4/s/real_server_%s.*/real_server_%s_ipv4 = \"%s:80\"/g' %s" % (i+1, i+1, i+1, args[i+1], config_path))

print "Run %s test on %s, node servers are %s" % (suit, director_ip, args[1:])
