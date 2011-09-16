#!/usr/bin/env python

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
Step3: Visit https://147.2.207.207/repo
"""
# imports
import os
from strongwind import *
from sys import path
from firefox_frame import *

source_path = '/usr/share/qa/qa_test_firefox/test_source'
download_web = "https://bugzilla.novell.com/tr_show_case.cgi?case_id=1014760"
test_web = "https://147.2.207.207/repo/"

# Make sure MozillaFirefox version is expected for the test
checkVersion()

# Step1: Make sure SMTSERVER.site exists
procedurelogger.expectedResult('Make sure SMTSERVER.site exists')
if not os.path.exists("%s/SMTSERVER.site" % source_path):
    raise IOError, "Could not find file %s in %s, please download from %s " % \
                                    ("SMTSERVER.site", source_path, download_web)
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

preferences_frame = app.findFrame("Firefox Preferences")
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
sleep(config.SHORT_DELAY)

select_dialog = app.findDialog(re.compile('^Select File'))
toggle = select_dialog.findToggleButton(None)
if not toggle.checked:
    toggle.click(log=True)

location_text = select_dialog.findText(None, labelledBy="Location:", \
                                checkShowing=False).text = "%s/SMTSERVER.site" % source_path
select_dialog.findPushButton("Open").mouseClick()
sleep(config.SHORT_DELAY)
select_dialog.assertClosed()

procedurelogger.expectedResult('Make sure SMTSERVER.site is imported')
pdb_cell = certificate_dialog.findTableCell("SMTSERVER.site")

# Click "Edit" button and make "Trust the authenticity of this certificate."
pdb_cell.mouseClick()
sleep(config.SHORT_DELAY)
certificate_dialog.findPushButton(re.compile('^Edit')).mouseClick()
sleep(config.SHORT_DELAY)
edit_dialog = app.findDialog(re.compile('^Edit web site'))

edit_dialog.findRadioButton(re.compile('^Trust ')).mouseClick()
sleep(config.SHORT_DELAY)
edit_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)
edit_dialog.assertClosed()

preferences_frame.findPushButton("Close").press()
sleep(config.SHORT_DELAY)

# Step3: Visit https://147.2.207.207/repo/
openURL(fFrame, test_web)

procedurelogger.expectedResult('%s frame appears' % test_web)
fFrame.findDocumentFrame(re.compile('^Index of /repo'))

# Clear SMTSERVER.site certificate
certificate_dialog.findPushButton(re.compile('^Delete')).press(log=True)
sleep(config.SHORT_DELAY)
delete_dialog = app.findDialog("Delete Server Certificate Exceptions")
delete_dialog.findPushButton("OK").press(log=True)
sleep(config.SHORT_DELAY)
delete_dialog.assertClosed()

# Close application
menubar = fFrame.findMenuBar(None)
menubar.select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
fFrame.assertClosed()
