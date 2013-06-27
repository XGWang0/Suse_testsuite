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
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        09/26/2010
# Description: Evince test for "Find..." MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Find..." MenuItem test===
Step1: From <Edit> menu select <Find...> menu item
Step2: Make sure 'Find' text box, 'Find Previous' and 'Find Next' push button appear
Step3: type "command" in Find text box on bottom
Step4: Make sure '1found on this page' label appear
Step5: type "novell" in Find text box on botton
Step6: Make sure '0 found on this page' label appear
"""

# imports
from os import system
from strongwind import *

# open the label sample application
try:
  app = launchApp("/usr/bin/evince", "evince")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter

eFrame = app.evinceFrame

print doc

# Step1: Open an exited pdf
menubar = eFrame.findMenuBar(None)
try:
    menubar.select(['File', '1.  rtstat.pdf'])
except SearchError:
    from evince_frame import *
    openFile(eFrame, app)

# Step2: From <Edit> menu select <Find...> menu item
menubar.select(['Edit', 'Find...'])
sleep(config.SHORT_DELAY)

# Step3: Make sure 'Find' text box, 'Find Previous' and 'Find Next' 
# push button appear
procedurelogger.expectedResult("'Find' text box, 'Find Previous' and \
                                  'Find Next' push button should appear")
eFrame.findPushButton("Find Previous")
eFrame.findPushButton("Find Next")
find_textbox = eFrame.findText(None, labelledBy="Find:")

# Step4: type "command" in Find text box on bottom
find_textbox.insertText("command")
sleep(config.SHORT_DELAY)

# Step5: Make sure '1 found on this page' label appear
procedurelogger.expectedResult("%s found on this page" % "1")
eFrame.findLabel("1 found on this page")

# Step6: type "novell" in Find text box on botton
find_textbox.insertText("novell")
sleep(config.SHORT_DELAY)

# Step7: Make sure '0 found on this page' label appear
procedurelogger.expectedResult("%s found on this page" % "0")
eFrame.findLabel("0 found on this page")

# Step8 Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()

