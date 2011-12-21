#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
# Written by:  Felicia Mu <fxmu@novell.com>
#              Cachen Chen <cachen@novell.com>
# Description: Add more functions
##############################################################################

import urllib
from pyatspi import Registry
from strongwind import *

def launchDialog(exe, appname):
    """
    Launch Dialog and return object. Log an error and return None if 
    something goes wrong (Because the launchApp() method in strongwind only
    can find frame not dialog, so this method is used to find dialog.)
    """
    if exe=="" or appname=="":
        print "You need to give both executable file (include path) and appilcation name (show in accerciser)"
        raise NotImplementedError
    args = [exe]
    (app, subproc) = cache.launchApplication(args=args, name=appname, wait=config.LONG_DELAY) #set wait smaller if your network is good.
    return app

def nmAppletApp():
    """
    Return nm_applet_app object
    """
    nm_applet_app = cache._desktop.findApplication("nm-applet", checkShowing=False)
    return nm_applet_app

def nmPanel():
    """
    Return NetworkManager panel object on Panel Notification Area
    """
    gnome_panel = cache._desktop.findApplication("gnome-panel", checkShowing=False)
    notification_area = pyatspi.findDescendant(gnome_panel, lambda x: x.name == 'Panel Notification Area')
    filler = notification_area.findFiller(None)
    nm_panel = filler.findAllPanels(None)[0]
    return nm_panel

def cleanConnection(name, tab="Wireless"):
    """
    Clean up wireless from Network Connections editor
    """
    nm_panel = nmPanel()
    nm_applet_app = nmAppletApp()

    nm_panel.mouseClick(button=3)
    sleep(config.SHORT_DELAY)

    nm_applet_app.findWindow(None).findMenuItem(re.compile('^Edit Connections')).click(log=True)
    sleep(config.SHORT_DELAY)

    nm_editor_app = cache._desktop.findApplication("nm-connection-editor", checkShowing=False)
    connection_dialog = nm_editor_app.findDialog("Network Connections")

    # Select tab, select the network name and click the Delete button
    connection_dialog.findPageTab(tab).mouseClick()
    sleep(config.SHORT_DELAY)

    try:
        wireless = connection_dialog.findTableCell(re.compile('%s$' % name))
    except SearchError:
        connection_dialog.findPushButton("Close").mouseClick()
        sleep(config.SHORT_DELAY)
    else:
        wireless.mouseClick()
        sleep(config.SHORT_DELAY)

        connection_dialog.findPushButton("Delete").mouseClick()
        sleep(config.SHORT_DELAY)

        nm_editor_app.findAlert(None).findPushButton("Delete").mouseClick()
        sleep(config.SHORT_DELAY)

        connection_dialog.findPushButton("Close").mouseClick()
        sleep(config.SHORT_DELAY)

        nm_editor_app.assertClosed()

def checkConnection(acc_name, status=True):
    """
    Make sure wired or wireless network connection check menu item is checked
    """
    nm_panel = nmPanel()
    nm_applet_app = nmAppletApp()

    nm_panel.mouseClick()
    sleep(config.SHORT_DELAY)

    acc_item = nm_applet_app.findWindow(None).findCheckMenuItem(acc_name)

    if status:
        connection = "checked"
    else:
        connection = "unchecked"

    procedurelogger.expectedResult("Make sure %s is %s" % (acc_name, connection))
    assert acc_item.checked == status, "Network %s should be %s" % \
                                                       (acc_name, connection)

    nm_panel.mouseClick(log=False)
    sleep(config.SHORT_DELAY)

def checkInfo(acc_name=[]):
    """
    From Connection Information to make sure wired or wireless connected
    """
    nm_panel = nmPanel()
    nm_applet_app = nmAppletApp()

    # Right click on the NetworkManager icon, select Connection Information
    nm_panel.mouseClick(button=3)
    sleep(config.SHORT_DELAY)

    nm_applet_app.findWindow(None).findMenuItem(re.compile('^Connection Information')).click(log=True)
    sleep(config.SHORT_DELAY)

    info_dialog = nm_applet_app.findDialog("Connection Information")

    #  Find the connection network name
    for i in acc_name:
        procedurelogger.expectedResult("Successful Connection to %s" % i) 
        info_dialog.findPageTab(i)
        sleep(config.SHORT_DELAY)

    info_dialog.findPushButton("Close").mouseClick()
    sleep(config.SHORT_DELAY)
    info_dialog.assertClosed()

def loadURL(url):
    """
    Make sure Network connection to load url
    """
    procedurelogger.expectedResult("Load %s successful" %url)
    try:
        urllib.urlopen(url)
    except:
        raise IOError, "False to load %s, errors on the Network connection" % url

def setDLink(dlink_url, admin_pwd, item_name, item_role, set_info=None):
    """
    Load Firefox to D-Link SYSTEMS to set wireless network settings according to 
    some test cases request
    @url: D-LINK SYSTEMS web link, i.e. http://192.168.0.1
    @item_name: The name of the item you want to set
    @item_role: The role of the item, i.e. MenuItem
    @set_info: provide setting informations for some item, i.e. Text and 
     PasswordText details
    """
    # Launch Firefox and load D-Link SYSTEMS web page with url giving
    firefox_app = launchApp('/usr/bin/firefox', "Firefox")
    fFrame = firefox_app.firefoxFrame
    entry = fFrame.findEntry("Search Bookmarks and History")
    entry.mouseClick(log=False)
    sleep(config.SHORT_DELAY)
    entry.text = dlink_url
    sleep(config.SHORT_DELAY)
    fFrame.keyCombo("Enter", grabFocus=False)
    sleep(config.MEDIUM_DELAY)

    # Give Admin password to D-Link settings page
    dlink_frame = firefox_app.findDocumentFrame(re.compile('^D-LINK SYSTEMS'))
    dlink_frame.findMenuItem("English", checkShowing=False).select(log=True)
    sleep(config.SHORT_DELAY)
    dlink_frame.findPasswordText(None).enterText(admin_pwd)
    sleep(config.SHORT_DELAY)
    dlink_frame.findPushButton("Log In").mouseClick()
    sleep(config.MEDIUM_DELAY)

    # Link to SETUP->WIRELESS SETTINGS->Manual Wireless Network Setup
    fFrame.findLink("SETUP").mouseClick()
    sleep(config.SHORT_DELAY)
    fFrame.findLink("WIRELESS SETTINGS").mouseClick()
    sleep(config.SHORT_DELAY)
    fFrame.findPushButton("Manual Wireless Network Setup", checkShowing=False).press(log=True)
    sleep(config.MEDIUM_DELAY)

    # Settings
    function = getattr(fFrame, "find" + item_role)

    if item_role == 'Text' or item_role == "PasswordText":
        function(item_name).enterText(set_info)
        sleep(config.SHORT_DELAY)
    elif item_role == "MenuItem":
        function(item_name, checkShowing=False).select(log=True)
        sleep(config.SHORT_DELAY)

    # Save settings
    fFrame.findPushButton("Save Settings").mouseClick()
    sleep(config.MEDIUM_DELAY)

    # Close Firefox
    menubar = fFrame.findMenuBar(None)
    menubar.select(['File', 'Quit'])
    sleep(config.SHORT_DELAY)
    firefox_app.assertClosed()

def authenWireless(pwd, name=None, security=None):
    """
    Enter password to authen the wireless
    """
    nm_applet_app = nmAppletApp()
    running = True
    count = 0
    while running:
        try:
            authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")
        except SearchError:
            running = False
        else:
            count += 1
            if count == 4:
                authen_dialog.findPushButton("Cancel").mouseClick(log=False)
                sleep(config.SHORT_DELAY)
                raise Exception, "ERROR: Fails to connect wireless, Please make sure it works"
                exit(22)
            else:
                # Enter password wireless1_pwd, click Connect
                authen_dialog.findPasswordText(None).enterText(pwd)
                sleep(config.SHORT_DELAY)

                authen_dialog.findPushButton("Connect").mouseClick()
                sleep(30)

