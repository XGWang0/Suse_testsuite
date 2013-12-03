#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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

##############################################################################
# Written by:  Felicia Mu <fxmu@novell.com>, David Mulder <dmulder@novell.com>
# Date:        12/13/2010
# Description: Define some common functions for reused in other tests
##############################################################################
import os

from pyatspi import Registry
from strongwind import *

def killRunning():
    """
    Kill the exist Banshee process
    """
    process = os.popen("ps ax |grep banshee-1 | grep -v grep | awk '{print $5 \"=\" $1}'").read().split('\n')
    process_lists = [p.split('=', 1) for p in process]
    process_lists.pop()
    process_dict = dict(process_lists)

    for k, v in process_dict.iteritems():
        if k == 'mono':
            os.system('kill %s' % int(v))
        if k == 'bash':
            os.system('kill %s' % int(v))

def keyPress(accessible, key_name, num):
    """
    Doing key press action for-loop
    """
    while num > 0:
        accessible.keyCombo(key_name, grabFocus=False)
        sleep(config.SHORT_DELAY)
        num -= 1
    
def typeText(accessible, text):
	"""
	Type the text while the accessible object has focus.
	"""
	for i in range(0, len(text)):
		accessible.keyCombo(text[i], grabFocus=False)

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


