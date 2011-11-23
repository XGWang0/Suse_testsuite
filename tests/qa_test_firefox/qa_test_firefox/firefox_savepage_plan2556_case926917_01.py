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
# Date:        10/15/2010
# Description: Firefox Save Page Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Firefox test==
===Save Page test===
Step1: Open browser to http://www.mozilla.org
Step2: From the toplevel menu, select File | Save Page As
Step3: In the resulting file picker, make sure "Web Page, complete" is selected.
Step4: Choose a target directory (e.g., your desktop or home directory).
Step5: Click the Save button.
Step6: Make sure mozorg.html is saved to /home
"""

# imports
from strongwind import *
from firefox_frame import *

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Launch browser
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# clean existed mozorg.html
who = os.popen('whoami').read().replace('\n', '')
if who == "root":
    file_path = '/root/Desktop/mozorg.html'
else:
    file_path = '/home/%s/Desktop/mozorg.html' % who

if os.path.exists(file_path):
    os.remove(file_path)

# Step1: Open browser to http://www.mozilla.org
openURL(fFrame, "http://www.mozilla.org")

procedurelogger.expectedResult("make sure mozilla.org is opened")
assert fFrame.name == "Home of the Mozilla Project - Mozilla Firefox", \
                                       "Mozilla.org frame doesn't appears"

# Step2: From the top level menu, select File | Save Page As
menubar = fFrame.findMenuBar(None)
fFrame.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)

# Unidentified encode key of "..." in the name, use click to instead select
#menubar.select(['File', 'Save Page As...'])
sa_menuitem = fFrame.findMenuItem(re.compile('^Save Page As'))
sa_menuitem.mouseClick()
sleep(config.SHORT_DELAY)

# Step3: In the resulting file picker, make sure "Web Page, complete" is selected
save_dialog = app.findDialog("Save As")
comboboxs = save_dialog.findAllComboBoxs(None, checkShowing=False)
if comboboxs[-1].showing is False:
    save_dialog.findToggleButton(re.compile('Browse for other folders$')).activate()

procedurelogger.expectedResult("make sure \"Web Page, complete\" is selected")
assert comboboxs[-1].name == "Web Page, complete", \
                                     "\"Web Page, complete\" isn't selected"

# Step4: Choose a target directory (e.g., your desktop or home directory)
procedurelogger.action("choose Desktop as target directory")
save_dialog.findText(None, labelledBy='Name:').text = file_path
sleep(config.SHORT_DELAY)

# Step5: Click the Save button
save_dialog.findPushButton("Save").mouseClick()
sleep(config.LONG_DELAY)

# Step6: Make sure mozorg.html is saved to Desktop
import os
procedurelogger.expectedResult("make sure mozorg.html is saved to home")
assert os.path.exists(file_path) == True, \
                               "mozorg.html doesn't saved to home"

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

