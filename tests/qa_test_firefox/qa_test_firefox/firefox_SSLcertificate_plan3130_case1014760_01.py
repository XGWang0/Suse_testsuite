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
# Date:        10/21/2010
# Description: Firefox SSL Certificate Test
##############################################################################

class PluginError(Exception):
    "Raised when plugin doesn't exist"
    pass

# The docstring below  is used in the generated log file
doc = """
==Firefox test==
===SSL Certificate test===
Step1: Make sure SMTSERVER.site exists
Step2: Edit-Preference-Advanced-Encryption-View Certificates, import this file in Servers label, then click "Edit" button and make "Trust the authenticity of this certificate"
Step3: Visit https web page
"""
# imports
import os
from strongwind import *
from sys import path
from firefox_frame import *
from firefox_config import *

source_path = '/usr/share/qa/qa_test_firefox/test_source'
ca_name = ca_name
download_web = ssl_ca_download_web
test_web = https_test_server

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Step1: Make sure SMTSERVER.site exists
procedurelogger.expectedResult('Make sure %s exists' % ca_name)
if not os.path.exists("%s/%s" % (source_path, ca_name)):
    raise IOError, "Could not find file %s in %s, please download from %s " % \
                                    (ca_name, source_path, download_web)
    exit(11)

# Launch Firefox.
try:
  app = launchApp('/usr/bin/firefox', "Firefox")
except IOError, msg:
  print "ERROR:  %s" % msg
  exit(2)
# just an alias to make things shorter
fFrame = app.firefoxFrame

print doc

# Step2: Edit-Preference-Advanced-Encryption-View Certificates
menubar = fFrame.findMenuBar(None)
menubar.select(['Edit', 'Preferences'])
sleep(config.SHORT_DELAY)

preferences_frame = pyatspi.findDescendant(app, lambda x: x.name == "Firefox Preferences")
preferences_frame.findListItem("Advanced").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPageTab("Encryption").mouseClick()
sleep(config.SHORT_DELAY)
preferences_frame.findPushButton("View Certificates").press(log=True)
sleep(config.SHORT_DELAY)
certificate_dialog = app.findDialog("Certificate Manager")

# Import pdb.suse.de file in Servers label
pdb_cell = certificate_dialog.findPageTab("Servers").switch(log=True)
sleep(config.SHORT_DELAY)
certificate_dialog.findPushButton(re.compile('^Import')).mouseClick()
sleep(config.MEDIUM_DELAY)

select_dialog = app.findDialog(re.compile('^Select File'))
toggle = select_dialog.findToggleButton(None)
if not toggle.checked:
    toggle.click(log=True)

location_text = select_dialog.findText(None, labelledBy="Location:", \
                                checkShowing=False).text = "%s/%s" % (source_path, ca_name)
select_dialog.findPushButton("Open").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('Make sure %s is imported' % ca_name)
pdb_cell = certificate_dialog.findTableCell(ca_name)

if pdb_cell._accessible.parent.name.startswith(ca_name):
    pdb_cell = certificate_dialog.findListItem(re.compile('^%s' % ca_name))

# Click "Edit" button and make "Trust the authenticity of this certificate."
pdb_cell.grabFocus()
sleep(config.SHORT_DELAY)
pdb_cell.activate()
sleep(config.SHORT_DELAY)
certificate_dialog.findPushButton(re.compile('^Edit')).mouseClick()
sleep(config.MEDIUM_DELAY)
edit_dialog = app.findDialog(re.compile('^Edit web site'))

edit_dialog.findRadioButton(re.compile('^Trust ')).mouseClick()
sleep(config.SHORT_DELAY)
edit_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

preferences_frame.findPushButton("Close").press()
sleep(config.SHORT_DELAY)

# Step3: Visit https test web
openURL(fFrame, test_web)

procedurelogger.expectedResult('%s frame appears' % test_web)
fFrame.findDocumentFrame(re.compile('^Index of /repo'))

# Clear SMTSERVER.site certificate
certificate_dialog.findPushButton(re.compile('^Delete')).press(log=True)
sleep(config.MEDIUM_DELAY)
delete_dialog = app.findDialog("Delete Server Certificate Exceptions")
delete_dialog.findPushButton("OK").press(log=True)
sleep(config.SHORT_DELAY)

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()

