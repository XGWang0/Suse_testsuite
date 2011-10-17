#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/28/2010
# Description: Firefox Remember Password Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Remember Password test===

Step1: Precondition:The master password be enabled(Edit-> Preferences-> Security)
Step2: Launch http://www-archive.mozilla.org/quality/browser/front-end/testcases/wallet/login.html
Step3: Enter username/password of squiddy/calamari, then click the Login button
Step4: Make sure Confirm alert appears to asking whether you wish to save the 
username and password
Step5: Click "Remember" button
Step6: Make sure The dialog called "Password Required" appears
Step7: Enter master password, then click OK
Step8: Select Edit-> Preferences-> Security-> Saved Passwords
Step9: The Saved Passwords dialog should appear, listing the site and the Username 
you have just saved
Step10: Click "Close" to dismiss the dialog
Step11: The Saved Passwords dialog should be closed
Step12: Quit and relaunch the browser
Step13: Launch http://www-archive.mozilla.org/quality/browser/front-end/testcases/wallet/login.html again, Enter your master password, then click OK
Step14: The username and password should be filled in for you
Step15: Redo step1 to step 8 with The master password be disabled(Edit-> Preferences-> Security)
"""
# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch Firefox.
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

web_url = "http://www-archive.mozilla.org/quality/browser/front-end/testcases/wallet/login.html"
master_pwd = "masterpwd"
user = "qatest"
password = "qatest"

# Step1: Precondition:The master password be enabled(Edit-> Preferences-> Security)
menubar = fFrame.findMenuBar(None)
menubar.select(["Edit", "Preferences"])

preferences_frame = app.findFrame("Firefox Preferences")

preferences_frame.findListItem("Security").mouseClick()
sleep(config.SHORT_DELAY)

master_check = preferences_frame.findCheckBox("Use a master password")
# Remove the exist master password
if master_check.checked:
    master_check.mouseClick()
    sleep(config.SHORT_DELAY)
    remove_dialog = app.findDialog(re.compile('^Remove Master'))
    remove_dialog.findPasswordText(None).insertText(master_pwd)
    sleep(config.SHORT_DELAY)
    remove_dialog.findPushButton("Remove").mouseClick()
    sleep(config.SHORT_DELAY)
    app.findDialog("Password Change Succeeded").findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)
    preferences_frame.findPushButton(re.compile('^Saved Passwords')).mouseClick()
    sleep(config.SHORT_DELAY)
    save_dialog = app.findDialog("Saved Passwords")
    save_dialog.findPushButton("Remove All").mouseClick()
    sleep(config.SHORT_DELAY)
    app.findDialog("Remove all passwords").findPushButton("Yes").mouseClick()
    sleep(config.SHORT_DELAY)
   
    quitFirefox(fFrame)

    app = launchApp('/usr/bin/firefox', "Firefox")
    fFrame = app.firefoxFrame
    menubar = fFrame.findMenuBar(None)
    menubar.select(["Edit", "Preferences"])

    preferences_frame = app.findFrame("Firefox Preferences")

    preferences_frame.findListItem("Security").mouseClick()
    sleep(config.SHORT_DELAY)

    master_check = preferences_frame.findCheckBox("Use a master password")

master_check.mouseClick()
sleep(config.SHORT_DELAY)

change_dialog = app.findDialog("Change Master Password")
change_dialog.findPasswordText("Enter new password:").mouseClick()
sleep(config.SHORT_DELAY)
change_dialog.findPasswordText("Enter new password:").typeText(master_pwd)
sleep(config.SHORT_DELAY)
change_dialog.findPasswordText("Re-enter password:").mouseClick()
sleep(config.SHORT_DELAY)
change_dialog.findPasswordText("Re-enter password:").typeText(master_pwd)
sleep(config.SHORT_DELAY)
change_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)
app.findDialog("Password Change Succeeded").findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)
change_dialog.assertClosed()

preferences_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.assertClosed()

# Step2: Launch http://www-archive.mozilla.org/quality/browser/front-end/testcases/wallet/login.html
openURL(fFrame, web_url)

doc_frame = fFrame.findDocumentFrame("password")

# Step3: Enter username/password of squiddy/calamari, then click the Login button
entrys = doc_frame.findAllEntrys(None)
for entry in entrys:
    if entry.name == "":
        entry.insertText(user)

doc_frame.findPasswordText(None).insertText(password)

doc_frame.findPushButton("Login", checkShowing=False).press(log=True)
sleep(config.SHORT_DELAY)

# Step4: Make sure Confirm alert appears to asking whether you wish to save the 
# username and password
procedurelogger.expectedResult('Make sure confirm alert appears')
pwd_alert = fFrame.findAlert(None)

# Step5: Click "Remember" button
pwd_alert.findPushButton("Remember").mouseClick()
sleep(config.SHORT_DELAY)

# Step6: Make sure The dialog called "Password Required" appears
required_dialog = app.findDialog("Password Required")

# Step7: Enter master password, then click OK
required_dialog.findPasswordText(None).insertText(master_pwd)

required_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

if app._accessible.childCount == 2:
    raise Exception, "confirm alert shouldn't appears"

# Step8: Select Edit-> Preferences-> Security-> Saved Passwords
menubar.select(["Edit", "Preferences"])

preferences_frame = app.findFrame("Firefox Preferences")

preferences_frame.findPushButton(re.compile('^Saved Passwords')).mouseClick()
sleep(config.SHORT_DELAY)

# Step9: The Saved Passwords dialog should appear, listing the Site and the Username 
# you have just saved
save_frame = app.findFrame("Saved Passwords")

site = "http://www-archive.mozilla.org"
procedurelogger.expectedResult('Make sure %s %s appears in the list' % (site, user))
save_frame.findTableCell(site)
save_frame.findTableCell(user)

# Step10: Click "Close" to dismiss the dialog
save_frame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

# Step11: The Saved Passwords dialog should be closed
save_frame.assertClosed()

# Step12: Quit and relaunch the browser
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

sleep(config.MEDIUM_DELAY)

# Launch Firefox again
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

# Step13: Launch http://www-archive.mozilla.org/quality/browser/front-end/testcases/wallet/login.html again, Enter your master password, then click OK
openURL(fFrame, web_url)

required_dialog = app.findDialog("Password Required")

# Enter master password, then click OK
required_dialog.findPasswordText(None).insertText(master_pwd)

required_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

doc_frame = fFrame.findDocumentFrame("password")

# Step14: The username and password should be filled in for you
procedurelogger.expectedResult('The username and password should be filled in')
entrys = doc_frame.findAllEntrys(None)
for entry in entrys:
    if entry.name is None:
        assert entry.text == user, "username shouldn't be %s" % entry.text

assert doc_frame.findPasswordText(None).text == "******", "error password"

# Step15: Redo step1 to step 8 with The master password be disabled(Edit-> Preferences-> Security)
menubar = fFrame.findMenuBar(None)
menubar.select(["Edit", "Preferences"])

preferences_frame = app.findFrame("Firefox Preferences")

preferences_frame.findCheckBox("Use a master password").mouseClick()
sleep(config.SHORT_DELAY)

# Remove master password
remove_dialog = app.findDialog("Remove Master Password")
remove_dialog.findPasswordText("Current password:").typeText(master_pwd)

remove_dialog.findPushButton("Remove").mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog("Password Change Succeeded").findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

remove_dialog.assertClosed()

# Remove saved password
preferences_frame.findPushButton(re.compile('^Saved Passwords')).mouseClick()
sleep(config.SHORT_DELAY)

save_frame = app.findFrame("Saved Passwords")

site = "http://www-archive.mozilla.org"
save_frame.findTableCell(site).mouseClick()
sleep(config.SHORT_DELAY)

save_frame.findPushButton("Remove").mouseClick()
sleep(config.SHORT_DELAY)

# Close application
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
app.assertClosed()

sleep(config.MEDIUM_DELAY)

# Launch Firefox again
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

# Launch the login page again
openURL(fFrame, web_url)

# Master password required doesn't appears
procedurelogger.expectedResult('Make sure master password required doesn\'t appears')
try:
    app.findDialog("Password Required")
except SearchError:
    pass # expected
else:
    assert False, "Master Password Required shouldn't appears"

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
