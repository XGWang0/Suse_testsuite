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
# Date:        05/21/2012
# Description: Set up Apache server on both real servers for IPLB test
##############################################################################

import urllib2
from yast2_iplb_config import *
from yast2_iplb_frame import *

doc="""
Actions:

STEP1: Visite Virtual Server
STEP2: Sleep time(Check Interval setting) and visite Virtual Server again

Expected:

STEP1: The page of index.html changed once every "Check Interval" setting time and request <real_server1 ip>:80/index.html or <real_server2 ip>:80/index.html

========================Start Running========================
"""

print doc

def web_test():
    while True:
        try:
            web_info = urllib2.urlopen("http://%s" % virtual_server_ip).read()
        except urllib2.URLError:
            print "continue connection"
            continue
        else:
            return web_info

# index.html can be visited by virtual server ip on director server

os.system("ifconfig eth0:0 down")

procedurelogger.expectedResult("index.html can be visited by virtual server ip %s" % virtual_server_ip)

web_info = web_test() 
print web_info

# Stop web service on real server1
procedurelogger.action("Stop web service on real server1")
rs1 = remoteSetting(node_ip=real_server1_ip, node_pwd=real_server1_pwd)
rs1.act_service(service="/etc/init.d/apache2", status="stop")
sleep(5)

# index.html on real server2 can be visited by virtual server ip
procedurelogger.expectedResult("Apache on real server 2 %s works" % real_server2_ip)
web_info = web_test()
print web_info

if web_info.find("real_server2") == -1:
    raise Exception, "http://%s doesn't works!" % virtual_server_ip

# Start web service on real server1
procedurelogger.action("Start web service on real server1")
rs1 = remoteSetting(node_ip=real_server1_ip, node_pwd=real_server1_pwd)

rs1.act_service(service="/etc/init.d/apache2", status="start", check=True, process="httpd2-prefork")

# Stop web service on real server2
procedurelogger.action("Stop web service on real server2")
rs1 = remoteSetting(node_ip=real_server2_ip, node_pwd=real_server2_pwd)
rs1.act_service(service="/etc/init.d/apache2", status="stop")
sleep(5)

# index.html on real server1 can be visited by virtual server ip
procedurelogger.expectedResult("Apache on real server 1 %s works" % real_server1_ip)
web_info = web_test()
print web_info

if web_info.find("real_server1") == -1:
    raise Exception, "http://%s doesn't works!" % virtual_server_ip

# Start web service on real server2
procedurelogger.action("Start web service on real server1")
rs2 = remoteSetting(node_ip=real_server2_ip, node_pwd=real_server2_pwd)
rs2.act_service(service="/etc/init.d/apache2", status="start", check=True, process="httpd2-prefork")

