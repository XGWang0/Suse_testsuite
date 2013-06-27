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
# Date:        10/25/2010
# Description: Firefox Search Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===Search test===
Search using the embedded search bar in the top right of the browser.
Vary Search Engines between tests

Step1: From Tools -> Web Search focus to the search bar
Step2: Entry of search bar is focused
Step3: Insert 'Novell' and make search
Step4: Make sure to load New Document Frame the name start with 'Novell'
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

# Step1: From Tools -> Web Search focus to the search bar
menubar = fFrame.findMenuBar(None)
menubar.select(['Tools', 'Web Search'])
sleep(config.SHORT_DELAY)

# Step2: Entry of search bar is focused
procedurelogger.expectedResult('Make sure Entry of search bar is focused')
search_entry = fFrame.findEntry("Search using Google")
assert search_entry.focused == True, "Search entry should be focused"

# Step3: Insert 'Novell' and make search
search_entry.insertText("Novell")
sleep(config.SHORT_DELAY)
fFrame.findAllPushButtons("Search")[1].mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Make sure to load New Document Frame the name start with 'Novell'
procedurelogger.expectedResult('Make sure to load New Document Frame')
app.findDocumentFrame(re.compile('^Novell'))

# Close application
fFrame.findMenu("File").click(log=True)
sleep(config.SHORT_DELAY)
fFrame.findMenuItem("Quit", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
app.assertClosed()

