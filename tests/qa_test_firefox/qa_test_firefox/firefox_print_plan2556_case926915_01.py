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
# Description: Firefox Print Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Print test===

Step1: Launch http://www.novell.com
Step2: Select File | Print or click the toolbar Print icon
Step3: Print the page and check the hard copy output
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

# remove the exist file first
import os

who = os.popen('whoami').read().replace('\n', '')

if os.path.isfile('/%s/Desktop/mozilla.ps' % who):
    os.remove('/%s/Desktop/mozilla.ps' % who)

web_url = "http://www.novell.com"

# Step1: Launch http://www.novell.com
openURL(fFrame, web_url)

doc_frame = fFrame.findDocumentFrame(re.compile('^NOVELL'))

# Step2: Select File | Print or click the toolbar Print icon
menubar = fFrame.findMenuBar(None)
menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
menubar.findAllMenuItems(re.compile('^Print'))[1].mouseClick()
sleep(config.SHORT_DELAY)

print_dialog = app.findDialog("Print")

# Step3: Print the page and check the hard copy output
print_dialog.findTableCell("Print to File").mouseClick()
sleep(config.SHORT_DELAY)
print_dialog.findMenuItem("Desktop", checkShowing=False).click(log=True)

print_dialog.findPushButton("Print").mouseClick()
sleep(config.SHORT_DELAY)
print_dialog.assertClosed()

# Close application
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

