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
# Date:        04/05/2012
# Description: Set up hosts on both nodes, nodes can connection with hostname
##############################################################################

from yast2_test_frame import *
from yast2_cluster_config import *

doc="""
Action:

STEP1: On both nodes start openais: # rcopenais start

Excepted:

STEP1: /usr/lib/heartbeat/crmd process started
STEP2: # crmadmin -S server1
       Status of crmd@server1: S_IDLE (ok)
STEP3: # crmadmin -S server2
       Status of crmd@server2: S_IDLE (ok)
=================================================
"""

print doc

###### Actions:

# STEP1: On nodes start openais: # rcopenais start
# /usr/lib/heartbeat/crmd process started
service = "/usr/sbin/rcopenais"
status = "restart \&"

rs = remoteSetting(node_ip=director_ip, node_pwd=director_pwd)
rs.act_service(service=service, status=status,check=True, process="crmd")

rs = remoteSetting(node_ip=node2_ip, node_pwd=node2_pwd)
rs.act_service(service=service, status=status,check=True, process="crmd")

rs = remoteSetting(node_ip=node1_ip, node_pwd=node1_pwd)
rs.act_service(service=service, status=status,check=True, process="crmd")

###### Expected:
procedurelogger.action("Check %s crmd status" % director_hostname)
if os.system('crmadmin -S %s |grep ok' % director_hostname) != 0:
    raise Exception, "crmd@%s status is failed" % director_hostname

# STEP2: # crmadmin -S server1
#       Status of crmd@server1: S_IDLE (ok)
procedurelogger.action("Check %s crmd status" % node1_hostname)
if os.system('crmadmin -S %s |grep ok' % node1_hostname) != 0:
    raise Exception, "crmd@%s status is failed" % node1_hostname

# STEP3: # crmadmin -S server2
#       Status of crmd@server2: S_IDLE (ok)
procedurelogger.action("Check %s crmd status" % node2_hostname)
if os.system('crmadmin -S %s |grep ok' % node2_hostname) != 0:
    raise Exception, "crmd@%s status is failed" % node2_hostname
