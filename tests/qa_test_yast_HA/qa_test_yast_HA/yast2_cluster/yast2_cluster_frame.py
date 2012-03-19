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
# Date:        03/06/2012
# Description: Define functions for reused in yast tools UI Automation tests
##############################################################################

import os
import subprocess

from pyatspi import Registry
from strongwind import *

def launchYastApp(exe, appname):
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

def removeFile(path):
    '''
    Clean exists file
    '''
    if os.path.exists(path):
        os.system('rm -fr %s' % path)

def checkInfo(info, f_path):
    '''
    Checking informations are expected in the file
    '''
    result = os.system('grep "%s" %s' % (info, f_path))
    if result != 0:
        raise Exception, "%s doesn't exist in %s" % (info, f_path)

def checkProcess(p_name, status=True):
    '''
    Checking process: when status is True the process should be running, otherwise it should be stopped"
    '''
    process = os.system('pgrep -xl %s' % p_name)

    if status and process != 0:
           raise Exception, "%s is not running" % p_name
    elif status == False and process == 0:
            raise Exception, "%s should be stopped" % p_name       

def press (x, y, button=1, log=True):
    """
    Synthesize a mouse button press at (x,y)
    """
    if log:
        procedurelogger.action("Mouse button %s press at (%s,%s)"%(button,x,y))
    Registry.generateMouseEvent(x,y, 'b%sp' % button)
    sleep(config.SHORT_DELAY)

def release (x, y, button=1, log=True):
    """
    Synthesize a mouse button release at (x,y)
    """
    if log:
        procedurelogger.action("Mouse button %s release at (%s,%s)"%(button,x,y))
    Registry.generateMouseEvent(x,y, 'b%sr' % button)
    sleep(config.SHORT_DELAY)

def absoluteMotion (x, y, log=True):
    """
    Synthesize mouse absolute motion to (x,y)
    """
    if log:
        procedurelogger.action("Mouse absolute motion to (%s,%s)"%(x,y))
    Registry.generateMouseEvent(x,y, 'abs')
    sleep(config.SHORT_DELAY)

def drag(fromObject=None, toObject=None, fromXY=0, toXY=0, button = 1, log=True):
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

def doubleClick(widget, log=True):
    """
    Synthesize a mouse double click on the screen.
    """
    if log:
        procedurelogger.action('double click %s' % widget)
    x, y = widget._getAccessibleCenter()
    pyatspi.Registry.generateMouseEvent(x, y, 'b1d')

