#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        08/03/2011
# Description: Change Gnome Keyring Password Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Change Gnome Keyring Password===
Step1: Launch "seahorse" 
Step2: Delete the exist Passwords

Step3: Launch evolution for the first time
Step4: Create novellautotest@gmail.com with POP type and SSL encryption type
Step5: Send / Receive mail.(save password for account)
Step6: Create keyring password "gnome",

Step7: On seahorse, Select the keyring and the right click options, choose "change password" item.
Step8: "Change Keyring Password" Window pops up
Step9: Input Old password and set new password "novell" for keyring, then touch "change" button

Step10: Delete evolution account and launch evolution again
Step11: Create novellautotest@gmail.com with POP type and SSL encryption type
Step12: Send / Receive mail.(save password for account)
Step13: Insert old keyring password "gnome", keyring dialog pops up again
Step14: Insert new keyring password "novell", it works
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

def launchEvolution():
    # Remove exist evolution account
    home_path = os.getenv('HOME')
    os.system('rm -fr %s/.evolution %s/.gconf/apps/evolution/ %s/.gnome2_private/*' % (home_path, home_path, home_path))
    os.system('killall gconfd-2')
    os.system('killall gnome-keyring-daemon')

    # Launch evolution for the first time
    el_apps = cache._desktop.findAllApplications("evolution", checkShowing=False)
    if len(el_apps) != 0:
        for i in el_apps:
            quitApp(app=i)

    el_app = launchApp("/usr/bin/evolution", "evolution")

    # just an alias to make things shorter
    el_frame = el_app.evolutionFrame
    return el_app, el_frame

def createAccount(el_frame):
    # Create novellautotest@gmail.com with POP type and SSL encryption type
    if el_frame.name == 'Evolution Setup Assistant':
        el_frame.findPushButton("Forward").click(log=True)
        sleep(config.SHORT_DELAY)
        el_frame.findPushButton("Forward").click(log=True)
        sleep(config.SHORT_DELAY)

        el_frame.findText(None, labelledBy="Email Address:").insertText("novellautotest@gmail.com")
        sleep(config.SHORT_DELAY)
        el_frame.findPushButton("Forward").click(log=True)
        sleep(config.SHORT_DELAY)

        el_frame.findMenuItem("POP", checkShowing=False).click(log=True)
        sleep(config.SHORT_DELAY)
        el_frame.findText(None, labelledBy="Server:").enterText("pop.gmail.com")
        sleep(config.SHORT_DELAY)
        el_frame.findMenuItem("SSL encryption", checkShowing=False).click(log=True)
        sleep(config.SHORT_DELAY)
        el_frame.findCheckBox("Remember password").mouseClick()
        sleep(config.SHORT_DELAY)
        el_frame.findPushButton("Forward").click(log=True)
        sleep(config.SHORT_DELAY)

        el_frame.findPushButton("Forward").click(log=True)
        sleep(config.SHORT_DELAY)
        el_frame.findPushButton("Forward").click(log=True)
        sleep(config.SHORT_DELAY)
        el_frame.findPushButton("Forward").click(log=True)
        sleep(config.SHORT_DELAY)

        el_frame.findPushButton("Apply").click(log=True)
        sleep(config.SHORT_DELAY)

# Step1: Launch "seahorse" 
sh_app = launchApp("/usr/bin/seahorse", "seahorse")

# just an alias to make things shorter
shFrame = sh_app.seahorseFrame

# Step2: Delete "Passwords: ***" tabel cell from Passwords page
deletePwd()

# Step3: Launch evolution for the first time
(el_app, el_frame) = launchEvolution()

# Step4: Create novellautotest@gmail.com with POP type and SSL encryption type
createAccount(el_frame)

# Step5: Send / Receive mail.(save password for account)
elFrame = el_app.findFrame("Mail - Evolution")

elFrame.findPushButton("Send / Receive").mouseClick()
sleep(config.SHORT_DELAY)

try:
    el_app.findDialog("Evolution Warning").findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)
except SearchError:
    pass

pwd_dialog = el_app.findDialog("Enter Password for novellautotest@gmail.com")
pwd_dialog.findPasswordText(None).insertText("autotest")
sleep(config.SHORT_DELAY)
pwd_checkbox = pwd_dialog.findCheckBox("Remember this password")
if pwd_checkbox.checked:
    pass
else:
    pwd_checkbox.mouseClick()
    sleep(config.SHORT_DELAY)
pwd_dialog.findPushButton("OK").mouseClick()
sleep(config.MEDIUM_DELAY)

# Step6: Create keyring password "gnome",
keyringPwd("gnome")

# Quit evolution
elFrame.findMenuBar(None).select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
el_app.assertClosed()

# Step7: On seahorse, Select the keyring and the right click options, choose "Change Password" item.
sh_app = launchApp("/usr/bin/seahorse", "seahorse")

# just an alias to make things shorter
shFrame = sh_app.seahorseFrame

shFrame.findTableCell(re.compile('^Passwords:')).mouseClick(button=3)
sleep(config.SHORT_DELAY)

# Step8: "Change Keyring Password" Window pops up
sh_app.findAllWindows(None)[-1].findMenuItem("Change Password").mouseClick()
sleep(config.SHORT_DELAY)

# Step9: Input Old password and set new password "novell" for keyring, then touch "change" button
procedurelogger.action("Insert old password and new password to change Keyring")
cache._desktop.typeText("gnome", log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.typeText("novell", log=False)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.typeText("novell", log=False)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Enter', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)

# Step10: Delete evolution account and launch evolution again
(el_app, el_frame) = launchEvolution()

# Step11: Create novellautotest@gmail.com with POP type and SSL encryption type
createAccount(el_frame)

# Step12: Send / Receive mail.(save password for account)
elFrame = el_app.findFrame("Mail - Evolution")

elFrame.findPushButton("Send / Receive").mouseClick()
sleep(config.MEDIUM_DELAY)

# Step13: Insert old keyring password "gnome", keyring dialog pops up again
procedurelogger.action("Insert %s Keyring password" % "gnome")
cache._desktop.typeText("gnome", log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Enter', grabFocus=False, log=False)
sleep(config.MEDIUM_DELAY)

# Step14: Insert new keyring password "novell", it works
procedurelogger.action("Insert %s Keyring password" % "novell")
cache._desktop.typeText("novell", log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Enter', grabFocus=False, log=False)
sleep(config.MEDIUM_DELAY)

procedurelogger.expectedResult('password is right')
assert el_app.childCount == 1, "send/receive dialog shouldn closed"

# Quit evolution
elFrame.findMenuBar(None).select(['File', 'Quit'])
sleep(config.MEDIUM_DELAY)
el_app.assertClosed()

# Close seahorse
shFrame.findMenuBar(None).select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
shFrame.assertClosed()
