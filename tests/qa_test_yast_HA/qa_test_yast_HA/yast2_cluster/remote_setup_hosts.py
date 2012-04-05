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
# Date:        03/02/2012
# Description: Set up hosts on both nodes, nodes can connection with hostname
##############################################################################

from yast2_cluster_config import *
from yast2_test_frame import *

# Set up node1_hostname
rs1 = remoteSetting(node_ip=node1_ip, node_pwd=node1_pwd)
procedurelogger.action("SSH connect to node1 %s, set hostname to %s" % \
                                                    (node1_ip, node1_hostname))
rs1.setup_hostname(node1_hostname)

# Set up node2_hostname
rs2 = remoteSetting(node_ip=node2_ip, node_pwd=node2_pwd)
procedurelogger.action("SSH connect to node1 %s, set hostname to %s" % \
                                                    (node2_ip, node2_hostname))
rs2.setup_hostname(node2_hostname)

# Set up node1 hosts
EOF_line="<<EOF\n%s %s\n%s %s\nEOF" % (node1_ip, node1_hostname, node2_ip, node2_hostname)

procedurelogger.action("Set up %s /etc/hosts" % node1_hostname)
rs1.setup_hosts(node1_hostname, EOF_line)

# Set up node2 hosts
procedurelogger.action("Set up %s /etc/hosts" % node2_hostname)
rs2.setup_hosts(node2_hostname, EOF_line)

# Ping node2 hostname to check the settings
procedurelogger.expectedResult("Ping %s successed" % node2_hostname)
rs2.ping_test(node2_hostname)

# Ping node1 hostname to check the settings
procedurelogger.expectedResult("Ping %s successed" % node1_hostname)
rs1.ping_test(node1_hostname)
