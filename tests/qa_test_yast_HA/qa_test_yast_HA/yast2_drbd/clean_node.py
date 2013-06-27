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
# Description: Clean up on director server
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

procedurelogger.action("Clean up %s" % node1_ip)

# umount /mnt
rs1 = remoteSetting(node_ip=node1_ip, node_pwd=node1_pwd)
rs1_connect = rs1.ssh_connect()
rs1_connect.sendline('umount /mnt')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

# stop rcdrbd
rs1_connect.sendline('rcdrbd stop')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

# wipe r0
rs1_connect.sendline('drbdadm -- --ignore-sanity-checks wipe-md r0')
exp = rs1_connect.expect([pexpect.TIMEOUT, ".*[need to type 'yes' to confirm]", "#|->"])
if exp == 1:
    rs1_connect.sendline("yes")
    print rs1_connect.before
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

# losetup loop0
rs1_connect.sendline('losetup -d %s' % node1_disk)
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

# rm drbd.img
rs1_connect.sendline('rm -fr /opt/drbd.img')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

# mv drbd configuration files
rs1_connect.sendline('mv /etc/drbd.conf /etc/drbd.conf.bak')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])
rs1_connect.sendline('mv /etc/drbd.d /etc/drbd.d.bak')
rs1_connect.expect([pexpect.TIMEOUT,"#|->"])

rs1_connect.sendline('exit')
