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
# Date:        04/05/2012
# Description: remote connection and setup functions, use python expect module
#              to control interaction
##############################################################################

import pexpect
import sys
import re
import os
import subprocess

from pyatspi import Registry
from strongwind import *
from time import sleep

class remoteSetting():
    """This is the class for connection or action on remote machines by pexpect interaction module"""

    def __init__(self, node_ip, node_pwd, user="root"):

        self.node_ip = node_ip
        self.node_pwd = node_pwd
        self.user = user

    def scp_run(self, copy_file=None, copy_path=None):
        """
        scp files to remote server
        """
        connect = pexpect.spawn('scp -r %s %s@%s:%s' % (copy_file, self.user, self.node_ip, copy_path))
        expects = connect.expect([pexpect.EOF, pexpect.TIMEOUT, 'Are you sure(?i)', 'Password:', "#|->"])
        if expects == 2:
            connect.sendline("yes")
            exp = connect.expect([pexpect.TIMEOUT,'Password:', "#|->"])
            if exp == 1:
                connect.sendline(self.node_pwd)
                connect.expect([pexpect.TIMEOUT, "#|->"])
        elif expects == 3:
            connect.sendline(self.node_pwd)
            connect.expect([pexpect.TIMEOUT, "#|->"])
        else:
            pass
        print connect.before
    
    def ssh_connect(self):
        '''
        SSH remote connect to node
        '''
        connect = pexpect.spawn('ssh -X %s@%s' % (self.user, self.node_ip))
        expects = connect.expect([pexpect.EOF, pexpect.TIMEOUT, 'Are you sure(?i)', 'Password:', "#|->"])
        if expects == 0:
            raise Exception, "Network error!"
        elif expects == 2:
            connect.sendline("yes")
            exp = connect.expect([pexpect.TIMEOUT,'Password:', "#|->"])
            if exp == 1:
                connect.sendline(self.node_pwd)
                connect.expect([pexpect.TIMEOUT, "#|->"])
        elif expects == 3:
            connect.sendline(self.node_pwd)
            connect.expect([pexpect.TIMEOUT, "#|->"])
        else:
            pass
        print connect.before
        return connect
    
    # ssh interaction to set up hostname
    def setup_hostname(self, node_hostname):
        '''
        Set up hostname on each node
        '''
        connect = self.ssh_connect()
    
        connect.sendline('sysctl -w kernel.hostname=%s' % node_hostname)
        connect.expect([pexpect.TIMEOUT, "#|->"])
        print connect.before
    
        connect.sendline('hostname')
        connect.expect([pexpect.TIMEOUT, "#|->"])
        print connect.before
    
        connect.sendline('exit')
    
    def setup_hosts(self, node_hostname, EOF_line):
        '''
        Add each node's ip and hostname to hosts
        '''
        connect = self.ssh_connect()
    
        connect.sendline('grep %s /etc/hosts' % self.node_ip)
        connect.expect("#|->")
        grep_info=connect.before
    
        if grep_info.find(self.node_ip + ' ' + node_hostname) == -1:
            connect.sendline('cat >>/etc/hosts %s' % EOF_line)
            connect.expect([pexpect.TIMEOUT, "#|->"])
            print connect.before
    
        connect.sendline('exit')
    
    def ping_test(self, ping_hostname):
        '''
        Ping test in each node
        '''
        connect = self.ssh_connect()
    
        connect.sendline('ping -c 1 %s' % ping_hostname)
        connect.expect([pexpect.TIMEOUT,"#|->"])
    
        compiles = [re.compile('unknown host'), re.compile('unreachable')]
        for i in compiles:
            if i.search(connect.before):
                raise RuntimeError, "Your setting up fails, check your hostname and /etc/hosts"
    
        print connect.before
    
        connect.sendline('exit')
    
    def setup_UItest(self, boolean=True, auto_login=True):
        '''
        Enable Accessibility for UI test, restart gnome session to load at-spi process
        '''
        enable_acc = False
        enable_xhost = False
        enable_login = False
        EOF_line = "<<EOF\n[Desktop Entry]\nType=Application\nExec=xhost +\nHidden=false\nX-Gnome-Autostart-enabled=true\nName=xhost\nComment=xhost + to allow hamsta run UI tests\nEOF"
        xhost_path = "/%s/.config/autostart/xhost.desktop" % self.user
    
        connect = self.ssh_connect()
    
        # enable accessibility
        connect.sendline('gconftool-2 -g /desktop/gnome/interface/accessibility')
        connect.expect([pexpect.TIMEOUT,"#|->"])
        if re.search('false', connect.before):
            connect.sendline('gconftool-2 -s --type=Boolean /desktop/gnome/interface/accessibility %s' % boolean)
            connect.expect([pexpect.TIMEOUT,"#|->"])
            enable_acc = True
        print connect.before
    
        # enable xhost +
        connect.sendline('ls %s' % xhost_path)
        connect.expect([pexpect.TIMEOUT,"#|->"])
        if re.search('cannot access', connect.before):
            connect.sendline('mkdir -p /%s/.config/autostart' % self.user)
            connect.expect([pexpect.TIMEOUT, "#|->"])
            connect.sendline('cat >>%s %s' % (xhost_path, EOF_line))
            connect.expect([pexpect.TIMEOUT, "#|->"])
            enable_xhost = True
            print connect.before
    
        # make user auto login X window
        if auto_login:
            EOF_line = "<<EOF\n\n[daemon]\nTimedLoginEnable=true\nAutomaticLoginEnable=true\nTimedLogin=%s\nAutomaticLogin=%s\nTimeLoginDelay=5\nEOF" % (self.user, self.user)
            gdm_conf_path = "/etc/gdm/custom.conf"
    
            connect.sendline('grep -c "\[daemon\]" %s' % gdm_conf_path)
            connect.expect([pexpect.TIMEOUT,"#|->"])
            print connect.before
            if re.search('0', connect.before):
                connect.sendline('cat >>%s %s' % (gdm_conf_path, EOF_line))
                connect.expect([pexpect.TIMEOUT, "#|->"])
                enable_login = True
                print connect.before
    
        # restart gnome session
        if enable_acc or enable_xhost or enable_login:
            connect.sendline('rcxdm restart')
            connect.expect(pexpect.TIMEOUT)
            print connect.before
    
        connect.sendline('exit')
    
    def install_Patterns(self, patterns=[]):
        '''
        Install require patterns
        '''
        connect = self.ssh_connect()
    
        for p in patterns:
            connect.sendline("zypper search -i -t pattern %s |tail -n 1" % p)
            connect.expect([pexpect.TIMEOUT,"#|->"])
            print connect.before
    
            if re.search('No packages found', connect.before):
                connect.sendline("zypper install -l -t pattern %s" % p)
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
    
    def act_service(self, service=None, status=None, check=False, process=None):
        '''
        To start, stop, restart service
        '''
        connect = self.ssh_connect()
    
        connect.sendline('%s %s' % (service, status))
        connect.expect([pexpect.TIMEOUT,"#|->"])
    
        compiles=[re.compile('.*No such file.*'), re.compile('.*command not found.*')]
        for i in compiles:
            if i.search(connect.before):
    	        raise RuntimeError, "Service doesn't exist"
        print connect.before
    
        if check:
            self.check_process(connect, process)
       
        connect.sendline('exit')
    
    def check_process(self, connect, process):
        '''
        Check process is running or not
        '''
        connect.sendline('pgrep -xl %s' % process)
        connect.expect([pexpect.TIMEOUT,"#|->"])
    
        if not re.search('[1-9].*%s' % process, connect.before):
            raise Exception, "%s process doesn't exist" % process
    
        print connect.before

class autoUITest():
    """This is the class for UI Automation test"""
    def launchYastApp(self, exe, appname):
        '''
        Nautilus always exist in gnome since X window start, just find it from 
        _desktop, otherwise if using strongwind launchApp will get an error in 
        cache findNewApplication with SearchError.
        '''
        # Kill the exist 'nautilus' application
        os.system("sudo killall -9 %s" % appname)
        sleep(config.MEDIUM_DELAY)
    
        # Launch nautilus
        procedurelogger.action('Launch %s.' % exe)
        subproc = subprocess.Popen(exe, shell=True)
        sleep(config.LONG_DELAY)
        app = cache._desktop.findAllApplications(appname.lower(), checkShowing=None)[-1]
        cache.addApplication(app)
        return app
    
    def removeFile(self, path):
        '''
        Clean exists file
        '''
        if os.path.exists(path):
            os.system('rm -fr %s' % path)
    
    def checkInfo(self, info, f_path):
        '''
        Checking informations are expected in the file
        '''
        result = os.system('grep "%s" %s' % (info, f_path))
        if result != 0:
            raise Exception, "%s doesn't exist in %s" % (info, f_path)
    
    def checkProcess(self, p_name, status=True):
        '''
        Checking process: when status is True the process should be running, otherwise it should be stopped"
        '''
        process = os.system('pgrep -xl %s' % p_name)
    
        if status and process != 0:
               raise Exception, "%s is not running" % p_name
        elif status == False and process == 0:
                raise Exception, "%s should be stopped" % p_name       
    
    def press (self, x, y, button=1, log=True):
        """
        Synthesize a mouse button press at (x,y)
        """
        if log:
            procedurelogger.action("Mouse button %s press at (%s,%s)"%(button,x,y))
        Registry.generateMouseEvent(x,y, 'b%sp' % button)
        sleep(config.SHORT_DELAY)
    
    def release (self, x, y, button=1, log=True):
        """
        Synthesize a mouse button release at (x,y)
        """
        if log:
            procedurelogger.action("Mouse button %s release at (%s,%s)"%(button,x,y))
        Registry.generateMouseEvent(x,y, 'b%sr' % button)
        sleep(config.SHORT_DELAY)
    
    def absoluteMotion (self, x, y, log=True):
        """
        Synthesize mouse absolute motion to (x,y)
        """
        if log:
            procedurelogger.action("Mouse absolute motion to (%s,%s)"%(x,y))
        Registry.generateMouseEvent(x,y, 'abs')
        sleep(config.SHORT_DELAY)
    
    def drag(self, fromObject=None, toObject=None, fromXY=0, toXY=0, button = 1, log=True):
        """
        Synthesize a mouse press, drag, and release on the screen.
        """
        if fromObject:
            bbox_l = fromObject.extents
            x_l = bbox_l.x + (bbox_l.width / 2)
            y_l = bbox_l.y + (bbox_l.height / 2)
            fromXY = (x_l, y_l - 10)
        (x,y) = fromXY
        press (x, y, button, log)
    
        if toObject:
            bbox_t = toObject.extents
            x_t = bbox_t.x + (bbox_t.width / 2)
            y_t = bbox_t.y + (bbox_t.height / 2)
            toXY = (x_t + 120, y_t)
     	
        (x,y) = toXY
    
        if log:
            procedurelogger.action("Mouse button %s drag %s from %s to %s%s"% \
                        (button, fromObject.name, fromXY, toObject.roleName, toXY))
        absoluteMotion(x, y, log)
        #sleep(config.SHORT_DELAY)
     	
        release (x, y, button, log)
        sleep(config.SHORT_DELAY)
    
    def doubleClick(self, widget, log=True):
        """
        Synthesize a mouse double click on the screen.
        """
        if log:
            procedurelogger.action('double click %s' % widget)
        x, y = widget._getAccessibleCenter()
        pyatspi.Registry.generateMouseEvent(x, y, 'b1d')
    
