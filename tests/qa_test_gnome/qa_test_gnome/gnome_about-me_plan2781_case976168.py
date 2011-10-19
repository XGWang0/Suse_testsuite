#!/usr/bin/env python
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# Date:        07/22/2011
# Description: Gnome about me test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Gnome About Me===
Step1: Launch "gnome-about-me" 
Step2: Change password for the user
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

user_name = os.getenv("USER")
pwd_path = "/usr/share/qa/data/passwords/%s" % user_name
user_pwd = ""

if os.path.exists(pwd_path):
    f = open(pwd_path)
    user_pwd = f.read().strip()
    f.close()
elif user_pwd != "":
    user_pwd = user_pwd
else:
    print "WARNING: This test need user password authentication, but user_pwd is None, please set the user password first and run test again"
    exit(22)

# Step1: Launch "gnome-about-me" 
try:
    app = launchApp("/usr/bin/gnome-about-me", "gnome-about-me", window="Dialog")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# just an alias to make things shorter
aDialog = app.findDialog(re.compile('^About'))

# Step2: Change password for the user
aDialog.findPushButton(re.compile('^Change Password')).mouseClick()
sleep(config.SHORT_DELAY)

pwd_dialog = app.findDialog("Change password")

pwd_dialog.findPasswordText(None, labelledBy="Current password:").typeText(user_pwd)
sleep(config.SHORT_DELAY)

pwd_dialog.findPushButton("Authenticate").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Make sure current password is authenticated")
pwd_dialog.findLabel("Authenticated!")

# Not equal test
pwd_dialog.findPasswordText(None, labelledBy="New password:").insertText("newpwd1")
sleep(config.SHORT_DELAY)
pwd_dialog.findPasswordText(None, labelledBy="Retype new password:").insertText("newpwd2")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Make sure two password are not equal")
pwd_dialog.findLabel("The two passwords are not equal.")

# Equal test
pwd_dialog.findPasswordText(None, labelledBy="New password:").enterText("newpwd")
sleep(config.SHORT_DELAY)
pwd_dialog.findPasswordText(None, labelledBy="Retype new password:").enterText("newpwd")
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Make sure two password are equal")
change_button = pwd_dialog.findPushButton("Change password")
assert change_button.sensitive == True, "Two password are not equal"

# Change password
change_button.mouseClick()
sleep(config.SHORT_DELAY)

# Authenticate an error current password
pwd_dialog.findPasswordText(None, labelledBy="Current password:").typeText("wrongpwd")
sleep(config.SHORT_DELAY)

pwd_dialog.findPushButton("Authenticate").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult("Make sure current password is not authenticated")
try:
    pwd_dialog.findLabel("Authenticated!")
except SearchError:
    pass
else:
    raise Exception, "ERROR: the current password should be %s, but not %s" % \
                                         ("newpwd", "wrongpwd")

# Authenticate current password and revert the password
pwd_dialog.findPasswordText(None, labelledBy="Current password:").typeText("newpwd")
sleep(config.SHORT_DELAY)

pwd_dialog.findPushButton("Authenticate").mouseClick()
sleep(config.SHORT_DELAY)

pwd_dialog.findPasswordText(None, labelledBy="New password:").enterText(user_pwd)
sleep(config.SHORT_DELAY)
pwd_dialog.findPasswordText(None, labelledBy="Retype new password:").enterText(user_pwd)
sleep(config.SHORT_DELAY)

# Close dialog
pwd_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
pwd_dialog.assertClosed()

# Quit app
aDialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
app.assertClosed()

