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
# Date:        11/26/2012
# Description: Testing DRBD service
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

# On server1 (primary node):
procedurelogger.action("Create filesystem on top of the DRBD device")
os.system('drbdadm primary r0')
sleep(config.SHORT_DELAY)
os.system('mkfs.ext3 /dev/drbd0')
sleep(config.SHORT_DELAY)

procedurelogger.action("Mount drbd device and create file on server1")
os.system('mount -o rw %s /mnt' % director_device)
sleep(config.SHORT_DELAY)
os.system('touch /mnt/from_server1')
sleep(config.SHORT_DELAY)

procedurelogger.action("Unmount drbd device and downgrade the drbd service to secondary")
os.system('umount /mnt')
sleep(config.SHORT_DELAY)
os.system('drbdadm secondary r0')
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("rcdrbd status should be Secondary/Secondary")
l_1 = os.popen('rcdrbd status |tail -1').read().split(' ')
status = [i for i in l_1 if i != ''] [2]
assert status == "Secondary/Secondary", "status wrong with %s" % status

# On server2:
rs1 = remoteSetting(node_ip=node1_ip, node_pwd=node1_pwd)
rs1_connect = rs1.ssh_connect()

procedurelogger.action("Promote to primary on server2 and mount drbd device")
rs1_connect.sendline('drbdadm primary r0')
rs1_connect.expect([pexpect.TIMEOUT, "#|->"])
rs1_connect.sendline('mount -o rw %s /mnt' % node1_device)
rs1_connect.expect([pexpect.TIMEOUT, "#|->"])

procedurelogger.expectedResult("File from_server1 created on servere1 is viewable")
rs1_connect.sendline('ls /mnt/from_server1')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

compiles=[re.compile('.*No such file or directory')]
for i in compiles:
    if i.search(rs1_connect.before):
        raise IOError, "from_server1 doesn't exist on server2"
print rs1_connect.before

procedurelogger.action("Unmount drbd device and downgrade the drbd service to secondary")
rs1_connect.sendline('umount /mnt')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])
rs1_connect.sendline('drbdadm secondary r0')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

rs1_connect.sendline('exit')

# On server1:
procedurelogger.action("Promote to primary on server1")
os.system('drbdadm primary r0')
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("rcdrbd status should be Primary/Secondary")
l_1 = os.popen('rcdrbd status |tail -1').read().split(' ')
status = [i for i in l_1 if i != ''] [2]
assert status == "Primary/Secondary", "status wrong with %s" % status
