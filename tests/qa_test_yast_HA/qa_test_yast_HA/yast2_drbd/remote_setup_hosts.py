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
# Date:        11/20/2012
# Description: Set up hosts on both nodes, nodes can connection with hostname
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

# Set up director_hostname
ds = remoteSetting(node_ip=director_ip, node_pwd=director_pwd)
procedurelogger.action("SSH connect to director %s, set hostname to %s" % \
                                                    (director_ip, director_name))
ds.setup_hostname(director_name)

# Set up node1_hostname
rs1 = remoteSetting(node_ip=node1_ip, node_pwd=node1_pwd)
procedurelogger.action("SSH connect to node1 %s, set hostname to %s" % \
                                                    (node1_ip, node1_name))
rs1.setup_hostname(node1_name)

# Set up director hosts
EOF_line="<<EOF\n%s %s\n%s %s\nEOF" % (director_ip, director_name, node1_ip, node1_name)
procedurelogger.action("Set up %s /etc/hosts" % director_name)
ds.setup_hosts(director_name, EOF_line)

# Set up node1 hosts
procedurelogger.action("Set up %s /etc/hosts" % node1_name)
rs1.setup_hosts(node1_name, EOF_line)

# Ping node1 hostname to check the settings
procedurelogger.expectedResult("Ping %s successed" % node1_name)
rs1.ping_test(node1_name)

# Ping director hostname to check the settings
procedurelogger.expectedResult("Ping %s successed" % director_name)
ds.ping_test(director_name)
