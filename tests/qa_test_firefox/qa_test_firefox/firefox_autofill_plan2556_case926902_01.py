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
sleep(config.MEDIUM_DELAY)

preferences_frame = pyatspi.findDescendant(app, lambda x: x.name == "Firefox Preferences")

preferences_frame.findListItem("Security").mouseClick()
sleep(config.SHORT_DELAY)

preferences_frame.findPushButton(re.compile('^Saved Passwords')).mouseClick()
sleep(config.MEDIUM_DELAY)

save_frame = app.findFrame("Saved Passwords")

sleep(config.SHORT_DELAY)

if save_frame.findPushButton("Remove All").sensitive:
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
doc_frame.findAllEntrys("")[1].insertText(user)

doc_frame.findPasswordText(None).mouseClick()
sleep(config.SHORT_DELAY)
doc_frame.findPasswordText(None).typeText(password)

doc_frame.findPushButton("Login").mouseClick()
sleep(config.MEDIUM_DELAY)

# Step3: Make sure Confirm alert appears to asking whether you wish to save the 
# username and password
procedurelogger.expectedResult('Make sure confirm alert appears')
pwd_alert = fFrame.findAlert(None)

# Step4: Click "Remember" button
pwd_alert.findPushButton(re.compile('^Remember')).mouseClick()
sleep(config.SHORT_DELAY)

# Step5: Log out the site and refresh the login page again
doc_frame = fFrame.findDocumentFrame("Bugzilla - GNOME Live!")

doc_frame.findLink("Logout").mouseClick()
sleep(config.SHORT_DELAY)

fFrame.findLink("Login").mouseClick()
sleep(config.SHORT_DELAY)

doc_frame = fFrame.findDocumentFrame("Login - GNOME Live!")

# Step6: username and password are auto filled in
procedurelogger.expectedResult('The username and password should be filled in')
name_entry = doc_frame.findAllEntrys(None)[1]
assert name_entry.text == user, "username shouldn't be %s" % entry.text

assert doc_frame.findPasswordText(None).text != "qapassword", "error password"

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

assert doc_frame.findPasswordText(None).text != "qapassword", "error password"

# Step8: Remove the saved password from Edit -> Preference
menubar = fFrame.findMenuBar(None)
menubar.select(["Edit", "Preferences"])
sleep(config.MEDIUM_DELAY)

preferences_frame = pyatspi.findDescendant(app, lambda x: x.name == "Firefox Preferences")

preferences_frame.findListItem("Security").mouseClick()
sleep(config.SHORT_DELAY)

preferences_frame.findPushButton(re.compile('^Saved Passwords')).mouseClick()
sleep(config.MEDIUM_DELAY)

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

