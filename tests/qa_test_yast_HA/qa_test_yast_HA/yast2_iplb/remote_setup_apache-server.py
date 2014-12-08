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
# Date:        05/10/2012
# Description: Set up Apache server on both real servers for IPLB test
##############################################################################

import urllib
from yast2_iplb_config import *
from yast2_iplb_frame import *

doc="""
Actions:

STEP1: Install Apache and start up http process on both real server nodes: service apache2 start
STEP2: Create index.html to real_server1
STEP3: Create index.html to real_server2 (page different from real_server1) 

Expected:

STEP1: Both index.html can be visited

========================Start Running========================
"""

print doc

http_file = "/srv/www/htdocs/index.html"

##### On real_server1
# Install lamp_server pattern
rs1 = remoteSetting(node_ip=real_server1_ip, node_pwd=real_server1_pwd)

procedurelogger.action("SSH connect to real server 1 %s, install lamp_server pattern" % real_server1_ip)
rs1.install_Patterns(patterns=["lamp_server"], setup_x=False)

# Start up http process: service apache2 start
rs1.act_service(service="service apache2", status="start", check=True, process="httpd2")

# Create index.html
connect = rs1.ssh_connect()
http_EOF = "<<EOF\n<html><body><h1>real_server1 works!</h1></body></html>\nEOF"
connect.sendline('cat >%s %s' % (http_file, http_EOF))
connect.expect([pexpect.TIMEOUT,"#|->"])
print connect.before
connect.sendline('exit')

# index.html can be visited
procedurelogger.expectedResult("Apache on real server 1 %s works" % real_server1_ip)
status = urllib.urlopen("http://%s/index.html" % real_server1_ip).read().find("real_server1")
if status == -1:
    raise Exception, "http://%s/index.html doesn't works!" % real_server1_ip

##### On real_server2
# Install lamp_server pattern
rs1 = remoteSetting(node_ip=real_server2_ip, node_pwd=real_server2_pwd)

procedurelogger.action("SSH connect to real server 2 %s, install lamp_server pattern" % real_server2_ip)
rs1.install_Patterns(patterns=["lamp_server"], setup_x=False)

# Start up http process: service apache2 start
rs1.act_service(service="service apache2", status="start", check=True, process="httpd2")

# Create index.html
connect = rs1.ssh_connect()
http_EOF = "<<EOF\n<html><body><h1>real_server2 works!</h1></body></html>\nEOF"
connect.sendline('cat >%s %s' % (http_file, http_EOF))
connect.expect([pexpect.TIMEOUT,"#|->"])
print connect.before
connect.sendline('exit')

# index.html can be visited
procedurelogger.expectedResult("Apache on real server 2 %s works" % real_server2_ip)
status = urllib.urlopen("http://%s/index.html" % real_server2_ip).read().find("real_server2")
if status == -1:
    raise Exception, "http://%s/index.html doesn't works!" % real_server2_ip
