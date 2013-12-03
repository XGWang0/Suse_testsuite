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
# Date:        11/26/2012
# Description: Clean up on director server
##############################################################################

from yast2_drbd_config import *
from yast2_test_frame import *

procedurelogger.action("Clean up %s" % director_ip)

os.system('killall -9 zenity 2>/dev/null')

# umount /mnt
os.system('umount /mnt 2>/dev/null')

# stop rcdrbd
os.system('rcdrbd stop')
sleep(config.SHORT_DELAY)

# wipe r0
child = pexpect.spawn('drbdadm -- --ignore-sanity-checks wipe-md r0')
exp = child.expect([pexpect.TIMEOUT, ".*[need to type 'yes' to confirm]", "#|->"])
if exp == 1:
    child.sendline("yes")
    print child.before

# losetup loop0
os.system('losetup -d %s 2>/dev/null' % director_disk)

# rm drbd.img
os.system('rm -fr /opt/drbd.img')

# mv drbd configuration files
os.system('mv /etc/drbd.conf /etc/drbd.conf.bak')
os.system('mv /etc/drbd.d /etc/drbd.d.bak')
