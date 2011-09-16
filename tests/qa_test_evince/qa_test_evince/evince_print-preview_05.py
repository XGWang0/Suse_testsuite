#!/usr/bin/env python

##############################################################################
# Written by:  Cachen Chen <cachen@novell.com>
# Date:        07/22/2010
# Description: Evince test for "Print" and "Print Preview" MenuItem
##############################################################################

# The docstring below  is used in the generated log file
doc = """

==Evince Menu Functions test==
==="Print and Print Preview" MenuItem test===
Step1: From <File> menu select <Print...> menu item to invoke Print dialog
Step2: Select Print to File, Updage Name to 'test.svg' and Save in folder to Document, Output as SVG, choose Current Page In General tab page
Step3: Change Pages per side, change Page ordering, change Only print and Scale in Page Setup tab page
Step4: Click Print Preview push button to invoke a new application
Step5: Click Print push button in the new application window
Step6: From <File> menu select <Open...> menu item to invoke dialog, assert 'test.svg' item is in Document folder
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

# remove the exist file first
import os

who = os.popen('whoami').read().replace('\n', '')

if os.path.isfile('/%s/Desktop/test.pdf' % who):
    os.remove('/%s/Desktop/test.pdf' % who)

# Step1: Open an exited pdf
menubar = eFrame.findMenuBar(None)
try:
    menubar.select(['File', '1.  rtstat.pdf'])
except SearchError:
    from evince_frame import *
    openFile(eFrame, app)

# Step2: From <File> menu select <Print...> menu item to invoke Print dialog
menubar.select(['File', 'Print...'])
sleep(config.SHORT_DELAY)
print_dialog = app.findDialog("Print")

# Step3: Select Print to File, Updage Name to 'test.svg' and Save in folder to 
# Document, Output as SVG, choose Current Page In General tab page
general_tab = print_dialog.findPageTab("General")
print_to_file_tablecell = general_tab.findTableCell("Print to File")
print_to_file_tablecell.mouseClick()
sleep(config.SHORT_DELAY)
general_tab.findText(None, labelledBy="Name:").text = "test.pdf"
sleep(config.SHORT_DELAY)
general_tab.findMenuItem("Desktop", checkShowing=False).click()
sleep(config.SHORT_DELAY)
# Make sure Desktop is selected
if not general_tab.findComboBox(None).name == "Desktop":
    raise Exception, "ERROR: Desktop menu doesn't selected for save in folder, when remote connect to the normal user login system with doing 'ssh -X root@host, export DISPLAY=:0.0, evince', then run evince will get this bug"
    exit(1)             

general_tab.findRadioButton("PDF").mouseClick()
sleep(config.SHORT_DELAY)
general_tab.findRadioButton("Current Page").mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Change Pages per side, change Only print and Scale in Page Setup tab page
page_setup_tab = print_dialog.findPageTab("Page Setup")
page_setup_tab.mouseClick()
sleep(config.SHORT_DELAY)
page_setup_tab.findMenuItem("2", checkShowing=False).click()
sleep(config.SHORT_DELAY)
page_setup_tab.findMenuItem("All sheets", checkShowing=False).click()
sleep(config.SHORT_DELAY)
page_setup_tab.findSpinButton(None, labelledBy="Scale:").value = 110
sleep(config.SHORT_DELAY)

# Step5: Click Print Preview push button to invoke a new application
print_dialog.findPushButton("Print Preview").click(log=True)
sleep(config.SHORT_DELAY)

app_sub_version = os.popen('rpm -q evince').read().split('-')[1].split('.')[1]
if app_sub_version == '24':
    preview_app = app.findFrame(re.compile('^evince_print'))
else:
    preview_app = cache._desktop.findApplication("evince-previewer", checkShowing=False)

# Step6: Click Print push button in the new application window
preview_app.findPushButton("Print", checkShowing=False).click()
sleep(config.SHORT_DELAY)
preview_app.assertClosed()

# Step7: From <File> menu select <Open...> menu item to invoke dialog, 
# assert 'test.svg' item is in Document folder 
menubar.select(['File', 'Open...'])
sleep(config.SHORT_DELAY)
open_dialog = app.findDialog("Open Document")
open_dialog.findTableCell("Desktop").mouseClick()
sleep(config.SHORT_DELAY)
procedurelogger.expectedResult("%s should be in the file list" % "test.pdf")
assert open_dialog.findTableCell("test.pdf").showing == True, \
                                             "doesn't find test.pdf file"

# Step8 Close the application
menubar.select(['File', 'Close'])
sleep(config.SHORT_DELAY)
eFrame.assertClosed()
