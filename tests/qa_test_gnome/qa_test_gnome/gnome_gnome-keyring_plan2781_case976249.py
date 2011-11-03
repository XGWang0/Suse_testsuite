#!/usr/bin/env python
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
# Written by: Calen Chen <cachen@novell.com>
# Date:        06/01/2011
# Description: Gnome Keyring be called by application Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Gnome Keyring===
====Pidgin====
Step1: Launch "seahorse" 
Step2: Delete "Passwords: ***" table cell from Passwords page
Step3: Launch pidgin for the first time, create autotest MSN account, select "Remember password"
Step4: Windows of "Create Default Keyring" pops up, insert password "novell", click "Create"
Step5: "Passwords: default" table cell appears, "gaim.local  prpl-msn://novellautotest" table cell appears in seahorse

====Evolution====
Step1: Launch evolution for the first time
Step2: Create novellautotest@gmail.com with POP type and SSL encryption type
Step3: Send / Receive mail.(save password for account)
Step4: Windows of "Create Default Keyring" pops up, insert password "novell", click "Create"
Step5: "Passwords: default" table cell appears, "pop://novellautotest@pop.gmail.com/" table cell appears in seahorse

====Wireless Network====
Step1: Launch NetworkManager again
Step2: From gnome panel click nm-applet, select wireless "SLEDQATEAM-DLINK"
Step3: Enter password "aaaaaaaaaa" and click "Connect"
Step4: Windows of "Create Default Keyring" pops up, insert password "novell", click "Create"
Step5: "Passwords: default" table cell appears, "Network secret" table cell appears in seahorse
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

def deletePwd():
    '''
    Delete "Passwords: ***" table cell in Passowrds page tab from seahorse
    '''
    try:
        shFrame.findTableCell(re.compile('^Passwords:')).grabFocus()
        sleep(config.SHORT_DELAY)
    except SearchError:
        pass
    else:    
        shFrame.findMenuBar(None).select(['Edit', 'Delete'])
        sleep(config.SHORT_DELAY)

        sh_app.findAlert(None).findPushButton("Delete").mouseClick()
        sleep(config.SHORT_DELAY)

        procedurelogger.expectedResult("Passwords page tab is empty")
        pwd_cells = shFrame.findPageTab("Passwords").findAllTableCells(None)
        # BUG697847: Delete password keyring doesn't empty the list 
        assert len(pwd_cells) == 0, "%s shouldn't exist, it should be empty" % pwd_cells

    # Close seahorse
    shFrame.findMenuBar(None).select(['File', 'Quit'])
    sleep(config.SHORT_DELAY)
    sh_app.assertClosed()

def keyringPwd(pwd):
    '''
    Insert password as keyring when Create Default Keyring window pops up
    '''
    procedurelogger.action("Insert %s in Create Default Keyring" % pwd)
    cache._desktop.typeText(pwd, log=False)
    sleep(config.SHORT_DELAY)
    cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
    sleep(config.SHORT_DELAY)
    cache._desktop.typeText(pwd, log=False)
    cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
    sleep(config.SHORT_DELAY)
    cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
    sleep(config.SHORT_DELAY)
    cache._desktop.keyCombo('Enter', grabFocus=False, log=False)
    sleep(config.SHORT_DELAY)

# ====Pidgin====
# Step1: Launch "seahorse" 
sh_app = launchApp("/usr/bin/seahorse", "seahorse")

# just an alias to make things shorter
shFrame = sh_app.seahorseFrame

# Step2: Delete "Passwords: ***" tabel cell from Passwords page
deletePwd()

# Step3: Launch pidgin for the first time, create autotest MSN account, select "Remember password"
os.system('killall -9 %s' % "pidgin")
sleep(config.SHORT_DELAY)

subprocess.Popen("/usr/bin/pidgin")
sleep(config.MEDIUM_DELAY)
pg_app = cache._desktop.findApplication("Pidgin", checkShowing=False)
cache.addApplication(pg_app)

try:
    a_dialog = pg_app.findDialog("Accounts")
except SearchError:
    pg_dialog = pg_app.findDialog(None)

    pg_dialog.findPasswordText(None).insertText("autotest")
    sleep(config.SHORT_DELAY)
    pg_dialog.findCheckBox("Save password").mouseClick()
    sleep(config.SHORT_DELAY)
    pg_dialog.findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)
    pg_dialog.assertClosed()
else:
    # Create autotest MSN account
    #a_dialog = pg_app.findDialog("Accounts")
    a_dialog.findPushButton(re.compile('^Add')).mouseClick()
    sleep(config.SHORT_DELAY)
    add_dialog = pg_app.findDialog("Add Account")
    add_dialog.findMenuItem("MSN", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    add_dialog.findText("Username:").insertText("novellautotest@hotmail.com")
    sleep(config.SHORT_DELAY)
    add_dialog.findPasswordText("Password:").insertText("autotest")
    sleep(config.SHORT_DELAY)
    add_dialog.findCheckBox("Remember password").mouseClick()
    sleep(config.SHORT_DELAY)
    add_dialog.findPushButton("Add").mouseClick()
    sleep(config.SHORT_DELAY)
    add_dialog.assertClosed()

sleep(config.LONG_DELAY)

# Step4: Windows of "Create Default Keyring" pops up
procedurelogger.expectedResult('Windows of "Create Default Keyring" pops up')
pyatspi.findDescendant(cache._desktop, lambda x: x.name == "Create Default Keyring")

# Insert password "novell", click "Create". Create Default Keyring window 
# doesn't accessible, use key press event to perform each action step
keyringPwd(pwd="novell")

# Delete novellautotest account from Accounts list
bl_frame = pg_app.findFrame("Buddy List")
bl_frame.findMenuBar(None).select(['Accounts', 'Manage Accounts'])
sleep(config.SHORT_DELAY)

accounts_dialog = pg_app.findDialog("Accounts")
accounts_dialog.findTableCell(re.compile('^novellautotest@hotmail.com')).mouseClick()
sleep(config.SHORT_DELAY)

accounts_dialog.findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)
pg_app.findDialog('').findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

accounts_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
accounts_dialog.assertClosed()

# Quit Pidgin
bl_frame.findMenuBar(None).select(['Buddies', 'Quit'])
pg_app.assertClosed()

# Step5: Launch seahorse again, "Passwords: default" table cell appears, "gaim.local  prpl-msn://novellautotest" table cell appears
sh_app = launchApp("/usr/bin/seahorse", "seahorse")
shFrame = sh_app.seahorseFrame

procedurelogger.expectedResult('"Passwords: default" table cell appears')
shFrame.findTableCell("Passwords: default")

procedurelogger.expectedResult('"gaim.local  prpl-msn://" table cell appears')
shFrame.findTableCell(re.compile('^gaim.local  prpl-msn://novellautotest'), checkShowing=False)

# Delete keyring and quit
deletePwd()

# ====Evolution====
# Step1: Launch evolution for the first time
el_apps = cache._desktop.findAllApplications("evolution", checkShowing=False)
if len(el_apps) != 0:
    for i in el_apps:
        quitApp(app=i)

el_app = launchApp("/usr/bin/evolution", "evolution")

# just an alias to make things shorter
elFrame = el_app.evolutionFrame

# Step2: Create novellautotest@gmail.com with POP type and SSL encryption type
if elFrame.name == 'Evolution Setup Assistant':
    elFrame.findPushButton("Forward").click(log=True)
    sleep(config.SHORT_DELAY)
    elFrame.findPushButton("Forward").click(log=True)
    sleep(config.SHORT_DELAY)

    elFrame.findText(None, labelledBy="Email Address:").insertText("novellautotest@gmail.com")
    sleep(config.SHORT_DELAY)
    elFrame.findPushButton("Forward").click(log=True)
    sleep(config.SHORT_DELAY)

    elFrame.findMenuItem("POP", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    elFrame.findText(None, labelledBy="Server:").enterText("pop.gmail.com")
    sleep(config.SHORT_DELAY)
    elFrame.findMenuItem("SSL encryption", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    elFrame.findCheckBox("Remember password").mouseClick()
    sleep(config.SHORT_DELAY)
    elFrame.findPushButton("Forward").click(log=True)
    sleep(config.SHORT_DELAY)

    elFrame.findPushButton("Forward").click(log=True)
    sleep(config.SHORT_DELAY)
    elFrame.findPushButton("Forward").click(log=True)
    sleep(config.SHORT_DELAY)
    elFrame.findPushButton("Forward").click(log=True)
    sleep(config.SHORT_DELAY)

    elFrame.findPushButton("Apply").click(log=True)
    sleep(config.SHORT_DELAY)

# Step3: Send / Receive mail.(save password for account)
elFrame = el_app.findFrame("Mail - Evolution")

elFrame.findPushButton("Send / Receive").mouseClick()
sleep(config.SHORT_DELAY)

pwd_dialog = el_app.findDialog("Enter Password for novellautotest@gmail.com")
pwd_dialog.findPasswordText(None).insertText("autotest")
sleep(config.SHORT_DELAY)
pwd_dialog.findPushButton("OK").mouseClick()
sleep(config.MEDIUM_DELAY)

# Step4: Windows of "Create Default Keyring" pops up
procedurelogger.expectedResult('Windows of "Create Default Keyring" pops up')
pyatspi.findDescendant(cache._desktop, lambda x: x.name == "Create Default Keyring")

# Insert password "novell", click "Create"
keyringPwd(pwd="novell")

# Quit evolution
elFrame.findMenuBar(None).select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
el_app.assertClosed()

# Step5: "Passwords: default" table cell appears, "pop://novellautotest@pop.gmail.com/" table cell appears in seahorse
sh_app = launchApp("/usr/bin/seahorse", "seahorse")
shFrame = sh_app.seahorseFrame

procedurelogger.expectedResult('"Passwords: default" table cell appears')
shFrame.findTableCell("Passwords: default")

procedurelogger.expectedResult('"pop://novellautotest@pop.gmail.com/" table cell appears')
shFrame.findTableCell(re.compile('^pop://novellautotest@pop.gmail.com/'), checkShowing=False)

# Delete keyring and quit
deletePwd()

# ====Wireless Network====
wireless_name = "SLEDQATEAM-DLINK"
wireless_pwd = "aaaaaaaaaa"

# Step1: Launch NetworkManager again
os.system('sudo killall -9 nm-applet')
subprocess.Popen('/usr/bin/nm-applet&', shell=True)

nm_applet_app = cache._desktop.findApplication("nm-applet", checkShowing=False)
cache.addApplication(nm_applet_app)

gnome_panel = cache._desktop.findApplication("gnome-panel", checkShowing=False)
notification_area = pyatspi.findDescendant(gnome_panel, lambda x: x.name == 'Panel Notification Area')
filler = notification_area.findFiller(None)
nm_panel = filler.findAllPanels(None)[0]

# Step2: From gnome panel click nm-applet, select wireless "SLEDQATEAM-DLINK"
nm_panel.mouseClick()
sleep(config.SHORT_DELAY)

nm_applet_app.findWindow(None).findCheckMenuItem(wireless_name).mouseClick()
sleep(20)

authen_dialog = nm_applet_app.findDialog("Wireless Network Authentication Required")

# Step3: Enter password "aaaaaaaaaa" and click "Connect"
authen_dialog.findPasswordText(None).enterText("aaaaaaaaaa")
sleep(config.SHORT_DELAY)

authen_dialog.findPushButton("Connect").mouseClick()
sleep(20)

# Step4: Windows of "Create Default Keyring" pops up
procedurelogger.expectedResult('Windows of "Create Default Keyring" pops up')
pyatspi.findDescendant(cache._desktop, lambda x: x.name == "Create Default Keyring")

# Insert password "novell", click "Create"
keyringPwd(pwd="novell")


# Step5: "Passwords: default" table cell appears, "Network secret" table cell appears in seahorse
sh_app = launchApp("/usr/bin/seahorse", "seahorse")
shFrame = sh_app.seahorseFrame

procedurelogger.expectedResult('"Passwords: default" table cell appears')
shFrame.findTableCell("Passwords: default")

procedurelogger.expectedResult('"Network secret" table cell appears')
shFrame.findTableCell(re.compile('^Network secret'), checkShowing=False)

# Delete keyring and quit
deletePwd()

