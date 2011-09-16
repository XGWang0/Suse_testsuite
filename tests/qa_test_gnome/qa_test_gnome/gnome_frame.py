#!/usr/bin/env python

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        10/25/2010
# Description: Define some common functions for reused in other tests
##############################################################################
import os
import re
import subprocess

from pyatspi import Registry
from strongwind import *

def launchNautilus(exe, appname):
    '''
    Nautilus always exist in gnome since X window start, just find it from 
    _desktop, otherwise if using strongwind launchApp will get an error in 
    cache findNewApplication with SearchError.
    '''
    # Kill the exist 'nautilus' application
    os.system("sudo killall -9 nautilus")
    sleep(config.MEDIUM_DELAY)

    # Launch nautilus
    procedurelogger.action('Launch %s.' % appname)
    subproc = subprocess.Popen(exe, shell=True)
    sleep(config.MEDIUM_DELAY)
    app = cache._desktop.findAllApplications(appname.lower(), checkShowing=None)[-1]
    cache.addApplication(app)
    return app

def quitApp(app=None, acc=None):
    '''
    Close application's all dialog, alert, frame windows before raise error
    '''
    if acc != None:
        app = acc.getApplication()
    child_count = app.childCount

    for i in range(child_count-1, -1, -1):
        x,y = app.getChildAtIndex(i)._accessible.queryComponent().getPosition(0)
        pyatspi.Registry.generateMouseEvent(x + 300, y + 10, 'b1c')

        app.getChildAtIndex(i).keyCombo('<Alt>F4', grabFocus=False, log=False)
        sleep(config.SHORT_DELAY)

def openAction(acc):
    '''
    Perform 'open' action for view icons in Nautilus
    '''
    # View icons doesn't perform sensitive status, so fails to use doActionMethod of strongwind, define it along
    iaction = acc._accessible.queryAction()
    procedurelogger.action('Perform "%s" action for %s.' % (iaction.getName(0), acc))
    iaction.doAction(0)

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

    if log and fromObject and toObject:
        procedurelogger.action("Mouse button %s drag %s from %s to %s%s"% \
                    (button, fromObject.name, fromXY, toObject.roleName, toXY))
    else:
        procedurelogger.action("Mouse button %s drag %s from %s to %s%s"% \
                    (button, fromObject, fromXY, toObject, toXY))

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

def screenDimensions():
    """
    Return the dimensions (resolution) of the screen as a tuple.
    """
    p = subprocess.Popen('xrandr', stdout=subprocess.PIPE)
    (stdout, stdin) = p.communicate()
    match = re.search(r'(\d+)x(\d+)\s+\d*\.\d*\*', stdout)
    return (int(match.group(1)), int(match.group(2)))

def getPid(process_name):
    '''
    Get pid of the expected process
    '''
    cmd = "ps -C %s |grep -v CMD |awk '{print $1'}" % process_name
    pid = os.popen(cmd).read().strip()
    return pid

