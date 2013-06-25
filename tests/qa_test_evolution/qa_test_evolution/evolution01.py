#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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
# Description: Test logic of Evlution, inclue registry, compose and send mail, input password, receive and check mail.
# Written by Leon
##############################################################################
# The docstring below  is used in the generated log file
"""
       ===Evolution test demo===
Step1: Click Forward button on Welcome window1
Step2: Click Forward button on Welcome window2
Step3: Input account information and click Forward button on Welcome window3
Step4: Choose server type, security type, input server name, click Forward button on Welcome window4
Step5: Click Forward button on Welcome window5
Step6: Input smtp sever name and choose authentication type as login, in some version this step is not needed
Step7: Click Forward button on Welcome window6
Step8: Click Forward button on Welcome window7
Step9: Click Apply button on Welcome window8
Step10: Get evolution new frame and click inbox table cell
Step11: Click New button on Frame window
Step12: Input receiver and subject then click Send button on Compose Message window
Step13: Click Send / Receive to make sure mail is sent out
Step14: Accept SSL and input password for sending mail
Step15: Accept SSL and input password for receiving mail
Step16: Click Send / Receive to receive the mail
Step17: Check mail received. And quit evolution
"""
from strongwind import *

# Cleanup the test
os.system('sh cleanup.sh')

# open the label sample application
try:
  app = launchApp("/usr/bin/evolution", "evolution")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)

# make sure we got the app back
if app is None:
  exit(4)

# just an alias to make things shorter
lFrame = app.evolutionFrame

# Step1: Click Forward button on Welcome window1
lFrame.clickItem("PushButton", "Forward")
sleep(config.SHORT_DELAY)

# Step2: Click Forward button on Welcome window2
lFrame.clickItem("PushButton", "Forward")
sleep(config.SHORT_DELAY)

# Step3: Input account information and click Forward button on Welcome window3
textdata={"0":"automation", "1":"novellautotest@gmail.com"}
lFrame.inputItem("Texts", textdata)
lFrame.clickItem("PushButton", "Forward")
sleep(config.SHORT_DELAY)

# Step4: Choose server type, security type, input server namem, click Forward button on Welcome window4
lFrame.findComboBox(None).select("POP")
sleep(config.MEDIUM_DELAY)
lFrame.findComboBox("No encryption").select("SSL encryption")
sleep(config.SHORT_DELAY)

lFrame.findText(None, labelledBy="Server:").enterText("pop.gmail.com")
sleep(config.SHORT_DELAY)

lFrame.clickItem("PushButton", "Forward")
sleep(config.SHORT_DELAY)

# Step5: Click Forward button on Welcome window5
lFrame.clickItem("PushButton", "Forward")
sleep(config.SHORT_DELAY)

# Step6: Input smtp sever name and choose authentication type as login, in some version this step is not needed
lFrame.clickItem("CheckBox", "Server requires authentication")
textdata={"6":"smtp.gmail.com"}
lFrame.inputItem("Texts", textdata)
sleep(config.SHORT_DELAY)

# Step7: Click Forward button on Welcome window6
lFrame.clickItem("PushButton", "Forward")
sleep(config.SHORT_DELAY)

# Step8: Click Forward button on Welcome window7
lFrame.clickItem("PushButton", "Forward")
sleep(config.SHORT_DELAY)

# Step9: Click Apply button on Welcome window8
try:
    lFrame.findPushButton("Apply")
except SearchError:
    lFrame.clickItem("PushButton", "Forward")
    sleep(config.SHORT_DELAY)

lFrame.clickItem("PushButton", "Apply")
sleep(config.SHORT_DELAY)

# Step10: Get evolution new frame and click inbox table cell
lFrame = lFrame.findNewItem("Frame", "Mail - Evolution")
lFrame.clickItem("TableCell", "Inbox (1)")

# Step11: Click New button on Frame window
lFrame.clickItem("PushButton", "New")
sleep(config.SHORT_DELAY)

# Step12: Input receiver and subject then click Send button on Compose Message window
newframe = lFrame.findNewItem("Frame", "Compose Message")
textdata={"0":"this is a test", "2":"novellautotest@gmail.com", "3":"test body"}
newframe.inputItem("Texts", textdata)
newframe.clickItem("PushButton", "Send")
sleep(config.SHORT_DELAY)

# Step13: Click Send / Receive to make sure mail is sent out
lFrame.clickItem("PushButton", "Send / Receive")
sleep(config.SHORT_DELAY)

# Step14: Accept SSL and input password for sending mail
try:
    app.findDialog("Evolution Warning").findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)
except SearchError:
    pass

textdata={"0":"autotest"}
newdialog = lFrame.findNewItem("Dialog", "Enter Password for novellautotest@gmail.com")
newdialog.inputItem("PasswordTexts", textdata)
newdialog.findPushButton("OK", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

# Step15: Accept SSL and input password for receiving mail
try:
    app.findDialog("Evolution Warning").findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)
except SearchError:
    pass

newdialog = lFrame.findNewItem("Dialog", "Enter Password for novellautotest@gmail.com")
newdialog.inputItem("PasswordTexts", textdata)
newdialog.findPushButton("OK", checkShowing=False).click(log=True)
sleep(config.LONG_DELAY)

# Step16: Click Send / Receive to receive the mail
lFrame.clickItem("PushButton", "Send / Receive")
sleep(config.SHORT_DELAY)

# Step17: Check mail received. And quit evolution
lFrame.assertobject("TableCell", "this is a test")
sleep(config.SHORT_DELAY)
lFrame.altF4()

