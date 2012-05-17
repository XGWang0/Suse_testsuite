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
# Date:        05/17/2012
# Description: Set up Apache server on both real servers for IPLB test
##############################################################################

from yast2_iplb_config import *
from yast2_iplb_frame import *

doc="""
Actions:

STEP1: On servers, set up Virtual network IP (#ifconfig eth0:0 192.168.2.33 netmask 255.255.255.0 up) 

Expected:

STEP1: Each server can ping Virtual IP successful

========================Start Running========================
"""

print doc

# Variables
machines = {
        director_server_ip:director_server_pwd, 
        real_server1_ip:real_server1_pwd, 
        real_server2_ip:real_server2_pwd
}

try:
    eth_interface = sys.argv[1:][0]
except IndexError:
    print "Usage: remote_setup_network.py <interface> [ip] [netmask]"
    sys.exit(1)

try:
    set_ip = sys.argv[1:][1]
except IndexError:
    set_ip = virtual_server_ip

try:
    netmask = sys.argv[1:][2]
except IndexError:
    netmask = "255.255.255.0"

# Actions
for k, v in machines.iteritems():
    ms = remoteSetting(node_ip=k, node_pwd=v)
    connect = ms.ssh_connect()

    print "Action: Set up network IP on %s" % k
    connect.sendline("ifconfig %s %s netmask %s up" % (eth_interface, set_ip, netmask))
    connect.expect([pexpect.TIMEOUT,"#|->"])
    print connect.before
    connect.sendline('exit')

    print "Expected result: Ping Virtual IP %s successful" % set_ip
    ms.ping_test(ping_host=set_ip)
