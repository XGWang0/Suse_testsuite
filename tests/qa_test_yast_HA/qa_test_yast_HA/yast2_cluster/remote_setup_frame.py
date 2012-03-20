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
# Description: remote connection and setup functions, use python expect module
#              to control interaction
##############################################################################

import pexpect
import sys
import re

from time import sleep

def ssh_connect(node_ip, node_pwd, user="root"):
    '''
    SSH remote connect to node
    '''
    connect = pexpect.spawn('ssh -X %s@%s' % (user, node_ip))
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

def setup_UItest(node_ip, node_pwd, user="root", boolean=True, auto_login=True):
    '''
    Enable Accessibility for UI test, restart gnome session to load at-spi process
    '''
    EOF_line = "<<EOF\n[Desktop Entry]\nType=Application\nExec=xhost +\nHidden=false\nX-Gnome-Autostart-enabled=true\nName=xhost\nComment=xhost + to allow hamsta run UI tests\nEOF"
    xhost_path = "/%s/.config/autostart/xhost.desktop" % user

    connect = ssh_connect(node_ip, node_pwd)

    # enable accessibility
    connect.sendline('gconftool-2  -s --type=Boolean /desktop/gnome/interface/accessibility %s' % boolean)
    connect.expect([pexpect.TIMEOUT,"#|->"])
    print connect.before

    # enable xhost +
    connect.sendline('ls %s' % xhost_path)
    connect.expect([pexpect.TIMEOUT,"#|->"])
    if re.search('cannot access', connect.before):
        connect.sendline('mkdir -p /%s/.config/autostart' % user)
        connect.expect([pexpect.TIMEOUT, "#|->"])
        connect.sendline('cat >>%s %s' % (xhost_path, EOF_line))
        connect.expect([pexpect.TIMEOUT, "#|->"])
        print connect.before

    # make user auto login X window
    if auto_login:
        EOF_line = "<<EOF\n\n[daemon]\nTimedLoginEnable=true\nAutomaticLoginEnable=true\nTimedLogin=%s\nAutomaticLogin=%s\nTimeLoginDelay=5\nEOF" % (user, user)
        gdm_conf_path = "/etc/gdm/custom.conf"

        connect.sendline('grep -c "\[daemon\]" %s' % gdm_conf_path)
        connect.expect([pexpect.TIMEOUT,"#|->"])
        print connect.before
        if re.search('0', connect.before):
            connect.sendline('cat >>%s %s' % (gdm_conf_path, EOF_line))
            connect.expect([pexpect.TIMEOUT, "#|->"])
            print connect.before

    # restart gnome session
    connect.sendline('rcxdm restart')
    connect.expect(pexpect.TIMEOUT)
    print connect.before

    connect.sendline('exit')

def install_Patterns(node_ip, node_pwd, user="root", patterns=[]):
    '''
    Install require patterns
    '''
    connect = ssh_connect(node_ip, node_pwd)

    for p in patterns:
        connect.sendline("zypper search -i -t pattern %s |tail -n 1" % p)
        connect.expect([pexpect.TIMEOUT,"#|->"])
        print connect.before

        if re.search('No packages found', connect.before):
            connect.sendline("zypper install -t pattern %s" % p)
            exp = connect.expect([pexpect.TIMEOUT,"Continue(?i)","#|->"])
            if exp == 1:
                print connect.before
                sleep(10)
                connect.sendline("y")
                while True:
                    index = connect.expect([pexpect.TIMEOUT,"#|->"])
                    print connect.before
                    if index == 0:
                        pass
                    elif index == 1:
                        break

    connect.sendline('exit')
