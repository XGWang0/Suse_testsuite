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
# Date:        11/22/2012
# Description: Create drbd disk on both nodes
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

# scp drbd configuration files to node1
rs1 = remoteSetting(node_ip=node1_ip, node_pwd=node1_pwd)

procedurelogger.action("scp drbd configuration files to %s" % node1_ip)
rs1.scp_run(copy_file="/etc/drbd.conf", copy_path="/etc")
rs1.scp_run(copy_file="/etc/drbd.d", copy_path="/etc")

# Initialize and start drbd on director
ds = remoteSetting(node_ip=director_ip, node_pwd=director_pwd)

ds_connect = ds.ssh_connect()
ds_connect.sendline('drbdadm -- --ignore-sanity-checks create-md r0')
exp = ds_connect.expect([pexpect.TIMEOUT, "[need to type 'yes' to confirm]", "#|->"])
if exp == 1:
    ds_connect.sendline("yes")
    print ds_connect.before
if ds_connect.expect(".*RETURN]"):
    ds_connect.sendline("")
ds_connect.expect([pexpect.TIMEOUT,"#|->"])
print ds_connect.before

ds_connect.sendline('rcdrbd start')
ds_connect.expect([pexpect.TIMEOUT, "#|->"])
print ds_connect.before

# Initialize and start drbd on node1
rs1_connect = rs1.ssh_connect()
rs1_connect.sendline('drbdadm -- --ignore-sanity-checks create-md r0')
exp = rs1_connect.expect([pexpect.TIMEOUT, "[need to type 'yes' to confirm]", "#|->"])
if exp == 1:
    rs1_connect.sendline("yes")
    print ds_connect.before
if rs1_connect.expect(".*RETURN]"):
    rs1_connect.sendline("")
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])
print rs1_connect.before

rs1_connect.sendline('rcdrbd start')
rs1_connect.expect([pexpect.TIMEOUT, "#|->"])
print rs1_connect.before

ds_connect.sendline('exit')
rs1_connect.sendline('exit')

sleep(config.MEDIUM_DELAY)

# Monitor drbd status
procedurelogger.expectedResult("rcdrbd status should be Secondary/Secondary")
l_1 = os.popen('rcdrbd status |tail -1').read().split(' ')
status = [i for i in l_1 if i != ''] [2]
assert status == "Secondary/Secondary", "status wrong with %s" % status

# Start the resync process and primary node on director
os.system('drbdadm -- --overwrite-data-of-peer primary r0')
os.system('drbdadm primary r0')

sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("rcdrbd status should be Primary/Secondary")
l_1 = os.popen('rcdrbd status |tail -1').read().split(' ')
status = [i for i in l_1 if i != ''] [2]
assert status == "Primary/Secondary", "status wrong with %s" % status
