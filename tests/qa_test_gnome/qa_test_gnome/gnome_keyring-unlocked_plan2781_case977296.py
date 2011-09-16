#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        06/14/2011
# Description: Login keyring is unlocked via pam on login Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Login keyring is unlocked via pam on login===
Step1: Launch "seahorse" 
Step2: Delete "Passwords: ***" table cell from Passwords page
Step3: Launch pidgin for the first time, create novellautotest@hotmail.com MSN account, select "Remember password"
Step4: When Windows of "Create Default Keyring" pops up, insert password "novell", click "Create"
Step5: MSN account is online
Step6: Logout, then login again
Step7: Login keyring is unlocked via pam on login
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
        #assert len(pwd_cells) == 0, "%s shouldn't exist, it should be empty" % pwd_cells

    # Close seahorse
    shFrame.findMenuBar(None).select(['File', 'Quit'])
    sleep(config.SHORT_DELAY)
    shFrame.assertClosed()

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

# Step1: Launch "seahorse" 
sh_app = launchApp("/usr/bin/seahorse", "seahorse")

# just an alias to make things shorter
shFrame = sh_app.seahorseFrame

# Step2: Delete "Passwords: ***" tabel cell from Passwords page
deletePwd()

# Step3: Launch pidgin for the first time, create novellautotest@hotmail.com MSN account, select "Remember password"
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
    # Create novellautotest MSN account
    a_dialog.findPushButton(re.compile('^Add')).mouseClick()
    sleep(config.SHORT_DELAY)
    add_dialog = pg_app.findDialog("Add Account")
    add_dialog.findMenuItem("MSN", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    add_dialog.findText("Username:").enterText("novellautotest@hotmail.com")
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

# Step5: MSN account is online
bl_frame = pg_app.findFrame("Buddy List")
sleep(config.MEDIUM_DELAY)

procedurelogger.expectedResult('novellautotest@hotmail.com MSN account is online')
bl_frame.findMenu("novellautotest@hotmail.com (MSN)", checkShowing=False)

# Step6: Logout, then login again
pg_app = launchApp("/usr/bin/pidgin", "Pidgin")
sleep(config.MEDIUM_DELAY)

# just an alias to make things shorter
bl_frame = pg_app.pidginFrame

# Step7: Login keyring is unlocked via pam on login
procedurelogger.expectedResult('novellautotest@hotmail.com MSN account is online')
bl_frame.findMenu("novellautotest@hotmail.com (MSN)", checkShowing=False)

# Delete novellautotest account from Accounts list
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

# Delete keyring and quit
sh_app = launchApp("/usr/bin/seahorse", "seahorse")
shFrame = sh_app.seahorseFrame
deletePwd()
