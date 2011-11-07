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
# Date:        10/25/2010
# Description: Define some common functions for reused in other tests
##############################################################################
import os

from pyatspi import Registry
from strongwind import *

def launchApp(exe, appname):
    """
    Launch Firefox and return object. Log an error and return None if 
    something goes wrong
    """
    if exe=="" or appname=="":
	print "You need to give both executable file (include path) and appilcation name (show in accerciser)"
	raise NotImplementedError
    # First to kill the exist application.
    # In some cases, if the application has been opend before doing launchApplication, then the second invoked application window would not been found. That will be useful when running a branch of tests in one process
    #if appname in [i.name for i in cache._desktop]:
    for i in cache._desktop:
        if i.name == appname:
            app = i
            try:
                fFrame = app.findFrame(None)
            except SearchError:
                pass
            else:
                quitFirefox(fFrame, quit=False)
                quitMultipleTabs(app, quit=False)
                app.assertClosed()        

    args = [exe]
    
    #set wait smaller if your network is good.
    (app, subproc) = cache.launchApplication(args=args, name=appname, wait=config.LONG_DELAY)
    cache.addApplication(app)
    app.findFrame(name=None, logName=appname)
    return app

def checkVersion(package_name="MozillaFirefox", expected_version="3.5.11"):
    """
    Check MozillaFirefox's version
    """
    version = os.popen('rpm -q MozillaFirefox').read().strip().split('-')[1]
    main_actual = version.split('.')[0]
    m_actual = version.split('.')[1]
    s_actual = version.split('.')[2]

    main_expected = expected_version.split('.')[1]
    m_expected = expected_version.split('.')[1]
    s_expected = expected_version.split('.')[2]

    if int(main_actual) <= int(main_expected) and int(m_actual) < int(m_expected) and int(s_actual) < int(s_expected):
        print "MozillaFirefox-%s is too old to be automation, please update to MozillaFirefox-%s+" % (version, expected_version)

        exit(22)
    else:
        pass

def openURL(test_frame, url):
    procedurelogger.action("Launch %s" % url)
    test_frame.findMenu("File").mouseClick()
    sleep(config.SHORT_DELAY)
    test_frame.findMenuItem(re.compile('^Open Location')).mouseClick()
    sleep(config.SHORT_DELAY)

    url_entry = test_frame.findEntry("Search Bookmarks and History")
    url_entry.text = url
    sleep(config.SHORT_DELAY)
    url_entry.keyCombo("enter")
    sleep(config.LONG_DELAY)

def quitMultipleTabs(app, quit=True):
    """
    Close the pop up dialog When "Warn me when closing multiple tabs" 
    is setting enabled
    """
    try:
        quit_dialog = app.findDialog("Quit Firefox")
    except LookupError:
        pass
    else:
        quit_dialog.findPushButton("Quit").mouseClick()
        sleep(config.SHORT_DELAY)
        if quit:
            app.assertClosed()

def quitFirefox(application, quit=True):
    """
    Close Firefox application from File -> Close
    """
    application.findMenu("File", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    application.findMenuItem("Quit", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)

    if quit:
        application.assertClosed()
        sleep(config.SHORT_DELAY)

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

