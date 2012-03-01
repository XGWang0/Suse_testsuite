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
# Date:        03/01/2012
# Description: Set up hosts on both nodes, nodes can connection with hostname
##############################################################################

import pexpect
import sys
import re

from time import sleep
from yast2_cluster_config import *

def ssh_connect(node_ip, node_pwd):
    '''
    SSH remote connect to node
    '''
    connect = pexpect.spawn('ssh -X %s' % node_ip)
    expects = connect.expect([pexpect.TIMEOUT, 'Password:', "#|->"])
    if expects == 1:
        connect.sendline(node_pwd)
        connect.expect([pexpect.TIMEOUT, "#|->"])
    else:
        pass
    print connect.before
    return connect


# ssh interaction to set up hostname
def setup_hostname(node_ip, node_pwd, node_hostname):
    '''
    Set up hostname on each node
    '''
    connect = ssh_connect(node_ip, node_pwd)

    connect.sendline('sysctl -w kernel.hostname=%s' % node_hostname)
    connect.expect([pexpect.TIMEOUT, "#|->"])
    print connect.before

    connect.sendline('hostname')
    connect.expect([pexpect.TIMEOUT, "#|->"])
    print connect.before

    connect.sendline('exit')

def setup_hosts(node_ip, node_pwd, node_hostname, EOF_line):
    '''
    Add each node's ip and hostname to hosts
    '''
    connect = ssh_connect(node_ip, node_pwd)

    connect.sendline('grep %s /etc/hosts' % node_ip)
    connect.expect("#|->")
    grep_info=connect.before

    if grep_info.find(node_ip + ' ' + node_hostname) == -1:
        connect.sendline('cat >>/etc/hosts %s' % EOF_line)
        connect.expect([pexpect.TIMEOUT, "#|->"])
        print connect.before

    connect.sendline('exit')

def ping_test(node_ip, node_pwd, ping_hostname):
    '''
    Ping test in each node
    '''
    connect = ssh_connect(node_ip, node_pwd)

    connect.sendline('ping -c 1 %s' % ping_hostname)
    connect.expect([pexpect.TIMEOUT,"#|->"])

    if re.search('unknown host', connect.before):
        raise RuntimeError, "Your setting up fails, check your hostname and /etc/hosts"

    print connect.before

    connect.sendline('exit')


