#!/usr/bin/env python
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
# Date:        06/07/2011
# Description: Gnome Launch seahorse and create a PGP key Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Launch seahorse and create a PGP key===
====Create PGP key====
Step1: Launch "seahorse" 
Step2: Create a PGP key from File -> New, choose "PGP Key" , click "continue" button, input full name "PGP-A" and email address "novellautotest@gmail.com" for PGP key
Step3: In "Passphrase for New PGP Key" dialog, insert password "novell", click "OK"
Step4: "Generating key" dialog appears
Step5: On "My Personal Keys" page, "PGP-A novellautotest@gmail.com" table cell appears
Step6: Export PGP-A from File -> Export... to "~/"

====Encrypt====
Step7: Touch '~/fileA'
Step8: Run "seahorse-tool -e ~/fileA", "Choose Recipients" dialog pops up in seahorse-tool application
Step9: Preform "toggle" action on PGP-A table cell, click "OK" button
Step10: "~/fileA.pgp" is created

====Decrypt====
Step11: Run "seahorse-tool -d ~/fileA.pgp", "Choose Decrypted File Name for 'fileA'" dialog pops up
Step12: insert name "~/fileB", click "Save" button
Step13: "~/fileB" is created, it's the same as fileA
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

file_path = '/home/%s/' % os.getenv('USER')
files = ['fileA', 'fileA.pgp', 'fileB', 'PGP-A.asc']

def deleteKey(tab_name, key_name):
    '''
    Delete password and encryption keys from seahorse
    '''
    shFrame.findPageTab(tab_name).mouseClick()
    sleep(config.MEDIUM_DELAY)

    try:
        shFrame.findTableCell(re.compile('^%s' % key_name)).grabFocus()
        sleep(config.SHORT_DELAY)
    except SearchError:
        pass
    else:    
        shFrame.findMenuBar(None).select(['Edit', 'Delete'])
        sleep(config.SHORT_DELAY)

        sh_app.findAlert(None).findPushButton("Delete").mouseClick()
        sleep(config.SHORT_DELAY)

        sh_app.findAlert(None).findPushButton("Delete").mouseClick()
        sleep(config.SHORT_DELAY)


# Remove the exist pgp key files
for i in files:
    if os.path.exists('%s%s' % (file_path, i)):
        os.remove('%s%s' % (file_path, i))

# ====Create PGP key and Export====
# Step1: Launch "seahorse"
sh_app = launchApp("/usr/bin/seahorse", "seahorse")

# just an alias to make things shorter
shFrame = sh_app.seahorseFrame

sh_menubar = shFrame.findMenuBar(None)

# Delete the exist pgp key
deleteKey(tab_name="My Personal Keys", key_name="PGP-A")

# Step2: Create a PGP key from File -> New, choose "PGP Key" , click "Continue" button, input full name "PGP-A" and email address "novellautotest@gmail.com" for PGP key
sh_menubar.findMenuItem("New...", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

create_dialog = sh_app.findDialog("Create New ...")

create_dialog.findTableCell(re.compile('^PGP Key')).mouseClick()
sleep(config.SHORT_DELAY)
create_dialog.findPushButton("Continue").mouseClick()
sleep(config.SHORT_DELAY)

new_dialog = sh_app.findDialog("New PGP Key")
new_dialog.findText(None, labelledBy="Full Name:").insertText("PGP-A")
sleep(config.SHORT_DELAY)
new_dialog.findText(None, labelledBy="Email Address:").insertText("novellautotest@gmail.com")
sleep(config.SHORT_DELAY)

new_dialog.findPushButton("Create").mouseClick()
sleep(config.SHORT_DELAY)

# Step3: In "Passphrase for New PGP Key" dialog, insert password "novell", click "OK"
key_dialog = sh_app.findDialog("Passphrase for New PGP Key")
procedurelogger.action('In "Passphrase for New PGP Key" dialog, insert password "novell"')
cache._desktop.typeText("novell", log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.typeText("novell", log=False)
sleep(config.SHORT_DELAY)
key_dialog.findPushButton("OK").mouseClick()
sleep(160)

# Step4: "Generating key" dialog appears
gen_dialog = sh_app.findDialog("Generating key")
gen_dialog.mouseClick(log=False)
sleep(config.SHORT_DELAY)

gen_dialog.altF4()
sleep(config.SHORT_DELAY)

sh_app = launchApp("/usr/bin/seahorse", "seahorse")
sleep(60)
# just an alias to make things shorter
shFrame = sh_app.seahorseFrame
shFrame.findPageTab("Other Keys").mouseClick(log=False)
sleep(config.MEDIUM_DELAY)
shFrame.findPageTab("My Personal Keys").mouseClick()
sleep(100)

# Step4: On "My Personal Keys" page, "PGP-A novellautotest@gmail.com" table cell appears
procedurelogger.expectedResult('"PGP-A  novellautotest@gmail.com" table cell appears')
shFrame.findTableCell("PGP-A  novellautotest@gmail.com").grabFocus()
sleep(config.SHORT_DELAY)

# Step6: Export PGP-A from File -> Export... to "~/"
shFrame.findMenuBar(None).select(['File', 'Export...'])
sleep(config.SHORT_DELAY)

export_dialog = sh_app.findDialog("Export public key")
export_dialog.findText(None, labelledBy="Name:").enterText("%sPGP-A.asc" % file_path)
sleep(config.SHORT_DELAY)
export_dialog.findPushButton("Save").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('PGP-A.asc is created in %s' % file_path)
assert os.path.exists('%sPGP-A.asc' % file_path) ==True, "PGP-A.asc doesn't exist"

# ====Encrypt====
# Step7: Touch '~/fileA'
procedurelogger.action('Touch "~/fileA"')
os.system('touch %sfileA' % file_path)
os.system('echo "pgp test file" >%sfileA' % file_path)

# Step8: Run "seahorse-tool -e ~/fileA", "Choose Recipients" dialog pops up in seahorse-tool application
procedurelogger.action('Run "seahorse-tool -e ~/fileA"')
subprocess.Popen('seahorse-tool -e %sfileA' % file_path, shell=True)
sleep(config.MEDIUM_DELAY)

tool_app = cache._desktop.findApplication("seahorse-tool", checkShowing=False)
sleep(config.SHORT_DELAY)
cache.addApplication(tool_app)

tool_dialog = tool_app.findDialog("Choose Recipients")

# Step9: Preform "toggle" action on PGP-A table cell, click "OK" button
tool_dialog.findTableCell(None).toggle(log=True)
sleep(config.SHORT_DELAY)

tool_dialog.findPushButton("OK").click(log=True)
sleep(config.SHORT_DELAY)

# Step10: "~/fileA.pgp" is created
procedurelogger.expectedResult('fileA.pgp is created in %s' % file_path)
assert os.path.exists('%sfileA.pgp' % file_path) ==True, "fileA.pgp doesn't exist"

# ====Decrypt====
# Step11: Run "seahorse-tool -d ~/fileA.pgp", "Choose Decrypted File Name for 'fileA'" dialog pops up
procedurelogger.action('Run "seahorse-tool -d %sfileA.pgp"')
subprocess.Popen('seahorse-tool -d %sfileA.pgp' % file_path, shell=True)
sleep(config.MEDIUM_DELAY)

tool_app = cache._desktop.findApplication("seahorse-tool", checkShowing=False)
sleep(config.SHORT_DELAY)
cache.addApplication(tool_app)

tool_dialog = tool_app.findDialog("Choose Decrypted File Name for 'fileA'")

# Step12: insert name "~/fileB", click "Save" button
tool_dialog.findText(None, labelledBy="Name:").enterText("%sfileB" % file_path)
sleep(config.SHORT_DELAY)
tool_dialog.findPushButton("Save").click(log=True)
sleep(config.MEDIUM_DELAY)

procedurelogger.action('Insert password "novell"')
cache._desktop.typeText("novell", log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('Tab', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)
cache._desktop.keyCombo('enter', grabFocus=False, log=False)
sleep(config.SHORT_DELAY)

# Step13: "~/fileB" is created, it's the same as fileA
procedurelogger.expectedResult('fileB is created in %s' % file_path)
assert os.path.exists('%sfileB' % file_path) ==True, "fileB doesn't exist"

# Delete pgp key
deleteKey(tab_name="My Personal Keys", key_name="PGP-A")

# Close seahorse
shFrame.findMenuBar(None).select(['File', 'Quit'])
sleep(config.SHORT_DELAY)
sh_app.assertClosed()

# remove the created file
for i in files:
    os.remove('%s%s' % (file_path, i))

