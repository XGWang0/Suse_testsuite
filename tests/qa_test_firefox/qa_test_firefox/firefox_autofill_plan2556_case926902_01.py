#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        10/29/2010
# Description: Firefox Autofill Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Autofill test===

Step1: Launch http://live.gnome.org/action/login/Bugzilla?action=login
Step2: Enter username/password of qatest/qapassword, then click the Login button
Step3: Make sure Confirm alert appears to asking whether you wish to save the 
username and password
Step4: Click "Remember" button
Step5: Log out the site and refresh the login page again
Step6: Restart firefox and redo step1
Step7: Autofill should still work
Step8: Remove the saved password from Edit -> Preference
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

web_url = "http://live.gnome.org/action/login/Bugzilla?action=login"
master_pwd = "masterpwd"
user = "qatest"
password = "qapassword"

# Step8: Remove the exist password from Edit -> Preference
menubar = fFrame.findMenuBar(None)
menubar.select(["Edit", "Preferences"])

preferences_frame = app.findFrame("Firefox Preferences")

preferences_frame.findListItem("Security").mouseClick()
sleep(config.SHORT_DELAY)

preferences_frame.findPushButton(re.compile('^Saved Passwords')).mouseClick()
sleep(config.SHORT_DELAY)

save_frame = app.findFrame("Saved Passwords")

sleep(config.SHORT_DELAY)

save_frame.findPushButton("Remove All").mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog("Remove all passwords").findPushButton("Yes").mouseClick()
sleep(config.SHORT_DELAY)

# Step1: Launch http://live.gnome.org/action/login/Bugzilla?action=login
openURL(fFrame, web_url)

fFrame.findLink("Login").mouseClick()
sleep(config.MEDIUM_DELAY)

doc_frame = fFrame.findDocumentFrame("Login - GNOME Live!")

# Step2: Enter username/password of qatest/qatest, then click the Login button
doc_frame.findEntry("").insertText(user)

doc_frame.findPasswordText(None).insertText(password)

doc_frame.findPushButton("Login").mouseClick()
sleep(config.SHORT_DELAY)

# Step3: Make sure Confirm alert appears to asking whether you wish to save the 
# username and password
procedurelogger.expectedResult('Make sure confirm alert appears')
pwd_alert = fFrame.findAlert(None)

# Step4: Click "Remember" button
pwd_alert.findPushButton("Remember").mouseClick()
sleep(config.SHORT_DELAY)

# Step5: Log out the site and refresh the login page again
doc_frame = fFrame.findDocumentFrame("Bugzilla - GNOME Live!")

doc_frame.findLink("Logout").mouseClick()
sleep(config.MEDIUM_DELAY)

fFrame.findLink("Login").mouseClick()
sleep(config.SHORT_DELAY)

doc_frame = fFrame.findDocumentFrame("Login - GNOME Live!")

# Step6: username and password are auto filled in
procedurelogger.expectedResult('The username and password should be filled in')
name_entry = doc_frame.findAllEntrys(None)[1]
assert name_entry.text == user, "username shouldn't be %s" % entry.text

assert doc_frame.findPasswordText(None).text == "******", "error password"

# Step7: Close Firefox 
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
app.assertClosed()
sleep(config.SHORT_DELAY)

# Restart Firefox 
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

# Redo step1
openURL(fFrame, web_url)

doc_frame = fFrame.findDocumentFrame("Login - GNOME Live!")

# Step7: Autofill should still work
procedurelogger.expectedResult('The username and password should be filled in')
name_entry = doc_frame.findAllEntrys(None)[1]
assert name_entry.text == user, "username shouldn't be %s" % entry.text

assert doc_frame.findPasswordText(None).text == "******", "error password"

# Step8: Remove the saved password from Edit -> Preference
menubar = fFrame.findMenuBar(None)
menubar.select(["Edit", "Preferences"])

preferences_frame = app.findFrame("Firefox Preferences")

preferences_frame.findListItem("Security").mouseClick()
sleep(config.SHORT_DELAY)

preferences_frame.findPushButton(re.compile('^Saved Passwords')).mouseClick()
sleep(config.SHORT_DELAY)

save_frame = app.findFrame("Saved Passwords")

site = "http://live.gnome.org"
save_frame.findTableCell(site).mouseClick()
sleep(config.SHORT_DELAY)

save_frame.findPushButton("Remove").mouseClick()
sleep(config.SHORT_DELAY)

# Close application
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
