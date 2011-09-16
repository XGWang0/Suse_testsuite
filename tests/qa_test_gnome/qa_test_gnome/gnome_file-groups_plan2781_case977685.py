#!/usr/bin/env python

##############################################################################
# Written by:  Calen Chen <cachen@novell.com>
# Date:        07/11/2011
# Description: File Groups Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===File Groups===
Set up:
Step1: Make sure nautilus-group package is installed
Step2: Create "test1" folder in ~/
Step3: Create an empty folder "test2" in ~/
Step4: Touch "a.txt", "b.txt" in "test1"

Copy file by group:
Step1: Launch Nautilus, navigate to ~/test1, multiple select a.txt b.txt
Step2: From Edit, choose "Add to a new Group", input group name "group test"
Step3: Navigate to ~/test2, From "File" choose "Copy Group here"
Step4: Make sure a.txt b.txt appear in ~/test2
Step5: Make sure a.txt b.txt still in ~/test1
Step6: Clear ~/test2

Move file by group
Step1: Navigate to ~/test2, right-clicked and choose "move group here"
Step2: Make sure a.txt b.txt appear in ~/test2
Step3: Make sure a.txt b.txt not in ~/test1

Add or delete group:
Step1: In ~/test1, multiple select a.txt b.txt
Step2: From Edit, choose "Edit the Group list"
Step3: Add a new goup named "group add"
Step4: Delete "group add" group

Add or delete file from group:
Step1: In ~/test1, multiple select a.txt b.txt
Step2: From Edit, choose "Add to a new Group", input group name "group test1"
Step3: From Edit, choose "Edit the Group list"
Step4: In group list, right-mouse click a file, choose "Remove this item"
Step5: Make sure a.txt item is removed from group
Step6: In group list, right-mouse click, choose "Add new item", select file a.txt from ~/test1
Step7: Make sure file a.txt  is added

Send group to:
Step1: Right-mouse click at nautilus anywhere, choose "Edit group list", click "Send this group to"
Step2: send as "evolution"
Step3: compressed with zip/tar.gz/bar.bz2
"""

# imports
from strongwind import *
from gnome_frame import *
import os
import subprocess

print doc

test1_path = os.getenv("HOME") + "/test1/"
test2_path = os.getenv("HOME") + "/test2/"

def createFile(path_name, file_name):
    """
    Create test file in file_path
    """
    procedurelogger.action("Create %s in %s" % (file_name, path_name))    
    f = open(os.path.join(path_name, file_name), 'w')
    f.close()
    sleep(config.SHORT_DELAY)

def changePath(acc, path_name):
    """
    Navigate folder from Location text
    """
    location_text = acc.findText(None, labelledBy="Location:", checkShowing=False)
    if not location_text.showing:
        edit_toggle = acc.findToggleButton("Edit").mouseClick()
        sleep(config.SHORT_DELAY)

    procedurelogger.action('Enter %s' % path_name)
    location_text.enterText(path_name)

    location_text.mouseClick()
    sleep(config.SHORT_DELAY)
    location_text.keyCombo('enter')
    sleep(config.MEDIUM_DELAY)

def sendGroup(compre_type):
    """
    Send group in expected compression type
    """
    sendto_app = cache._desktop.findApplication("nautilus-sendto", checkShowing=False)
    cache.addApplication(sendto_app)
    sendto_dialog = sendto_app.findDialog(None)

    sendto_dialog.findMenuItem("Email", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)

    sendto_dialog.findText(None, labelledBy="Send to:").enterText("novellautotest@gmail.com")
    sleep(config.SHORT_DELAY)

    checkbox = sendto_dialog.findCheckBox("Send packed in:")
    if not checkbox.checked:
        checkbox.mouseClick()
        sleep(config.SHORT_DELAY)
    # compressed with zip/tar.gz/bar.bz2
    sendto_dialog.findMenuItem(compre_type, checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)

    sendto_dialog.findPushButton("Send").mouseClick()
    sleep(config.MEDIUM_DELAY)

    evolution_app = cache._desktop.findApplication("evolution", checkShowing=False)
    cache.addApplication(evolution_app)

    evolution_frame = evolution_app.findFrame(None)
    evolution_frame.findIcon(re.compile('^Files%s' % compre_type))

    evolution_frame.findMenuItem("Close", checkShowing=False).click(log=True)
    sleep(config.SHORT_DELAY)
    evolution_frame.mouseClick(log=False)
    evolution_app.findDialog("Warning: Modified Message").findPushButton("Discard Changes").mouseClick()
    sleep(config.SHORT_DELAY)  
    evolution_app.assertClosed()

## Set up:
# Step1: Make sure nautilus-group package is installed
if os.system('rpm -q nautilus-group') == 256:
    print "ERROR: Please install nautilus-group package and run test again"
    exit(22)

# Step2: Create "test1" folder in ~/
if not os.path.exists(test1_path):
    os.mkdir(test1_path)
    sleep(config.SHORT_DELAY)

# Step3: Create an empty folder "test2" in ~/
if not os.path.exists(test2_path):
    os.mkdir(test2_path)
    sleep(config.SHORT_DELAY)

# Step4: Touch "a.txt", "b.txt" in "test1"
createFile(test1_path, "a.txt")
createFile(test1_path, "b.txt")

procedurelogger.expectedResult("a.txt b.txt exist in %s" % test1_path)
for i in ["a.txt", "b.txt"]:
    assert os.path.exists(os.path.join(test1_path + i))

## Copy file by group:
# Step1: Launch Nautilus
try:
    app = launchNautilus("/usr/bin/nautilus", "nautilus")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# Just an alias to make things shorter.
nFrame = app.findFrame(re.compile('^%s' % os.getenv('USER')))
menubar = nFrame.findMenuBar(None)
content_view = nFrame.findScrollPane("Content View")
icon_view = content_view.findLayeredPane("Icon View")
test1_icon = icon_view.findIcon("test1")
test2_icon = icon_view.findIcon("test2")

# Navigate to ~/test1, multiple select a.txt b.txt
openAction(test1_icon)
sleep(5)

procedurelogger.action("multiple select a.txt b.txt")
icon_view.selectAll()
sleep(config.SHORT_DELAY)

# Step2: From Edit, choose "Add to a new Group", input group name "group test"
edit_menu = menubar.findMenu("Edit")

add_group = edit_menu.findMenuItem("Add to a new Group", checkShowing=False)
sleep(config.SHORT_DELAY)

try:
    edit_menu.findMenuItem(re.compile('group test'), checkShowing=False)
except:
    add_group.click(log=True)
    sleep(config.SHORT_DELAY)

    new_dialog = app.findDialog("New group:")

    new_dialog.findText(None).typeText("group test")
    sleep(config.SHORT_DELAY)

    new_dialog.findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)

# Create a new window
menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
menubar.findMenuItem("New Window", checkShowing=False).mouseClick()
sleep(config.SHORT_DELAY)

new_frame = app.findFrame(re.compile('^%s' % os.getenv('USER')))
new_menubar = new_frame.findMenuBar(None)
new_icon_view = new_frame.findLayeredPane("Icon View")
new_test2_icon = new_icon_view.findIcon("test2")

# Remove the exist files
subprocess.Popen('rm %s*.txt' % test2_path, shell=True)

# Step3: Navigate to ~/test2, From "File" choose "Copy Group here"
openAction(new_test2_icon)
sleep(config.SHORT_DELAY)

new_menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)

new_menubar.findMenu("Copy Group here").mouseClick()
sleep(config.SHORT_DELAY)

new_menubar.findMenuItem(re.compile('^group test')).mouseClick()
sleep(config.MEDIUM_DELAY)

# Step4: Make sure a.txt b.txt appear in ~/test2
procedurelogger.expectedResult("a.txt b.txt exist in %s" % test2_path)
for i in ["a.txt", "b.txt"]:
    assert os.path.exists(os.path.join(test2_path + i))

# Step5: Make sure a.txt b.txt still in ~/test1
procedurelogger.expectedResult("a.txt b.txt exist in %s" % test1_path)
for i in ["a.txt", "b.txt"]:
    assert os.path.exists(os.path.join(test1_path + i))

# Step6: Clear ~/test2
subprocess.Popen('rm %s*.txt' % test2_path, shell=True)

# Close test2 window
new_menubar.findMenuItem("Close", checkShowing=False).click(log=True)

new_frame.assertClosed()
sleep(config.SHORT_DELAY)

## Move file by group
# Create a new window
menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)
menubar.findMenuItem("New Window", checkShowing=False).mouseClick()
sleep(config.SHORT_DELAY)

new_frame = app.findFrame(re.compile('^%s' % os.getenv('USER')))
new_menubar = new_frame.findMenuBar(None)
new_icon_view = new_frame.findLayeredPane("Icon View")
new_test2_icon = new_icon_view.findIcon("test2")

# Step1: Navigate to ~/test2, right-clicked and choose "move group here"
openAction(new_test2_icon)
sleep(5)

new_menubar.findMenu("File").mouseClick()
sleep(config.SHORT_DELAY)

new_menubar.findMenu("Move Group here").mouseClick()
sleep(config.SHORT_DELAY)

new_menubar.findMenuItem(re.compile('^group test')).mouseClick()
sleep(config.MEDIUM_DELAY)

# Step2: Make sure a.txt b.txt appear in ~/test2
procedurelogger.expectedResult("a.txt b.txt exist in %s" % test2_path)
for i in ["a.txt", "b.txt"]:
    assert os.path.exists(os.path.join(test2_path + i))

# Step3: Make sure a.txt b.txt not in ~/test1
procedurelogger.expectedResult("a.txt b.txt exist in %s" % test1_path)
for i in ["a.txt", "b.txt"]:
    assert not os.path.exists(os.path.join(test1_path + i))

# Step4: Clear ~/test2
subprocess.Popen('rm %s*.txt' % test2_path, shell=True)

# Touch "a.txt", "b.txt" in "test1"
createFile(test1_path, "a.txt")
createFile(test1_path, "b.txt")
sleep(config.SHORT_DELAY)

# Close test2 window
new_menubar.findMenuItem("Close", checkShowing=False).click(log=True)

new_frame.assertClosed()

## Add or delete group:
# Step1: In ~/test1, multiple select a.txt b.txt
procedurelogger.action("multiple select a.txt b.txt")
icon_view.selectAll()
sleep(config.SHORT_DELAY)

# Step2: From Edit, choose "Edit the Group list"
menubar.findMenuItem(re.compile('^Edit the Group List'), checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)

group_frame = app.findFrame("Nautilus file group")

# Step3: Add a new goup named "group add"
group_frame.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

new_dialog = app.findDialog("New group:")

new_dialog.findText(None).typeText("group add")
sleep(config.SHORT_DELAY)
new_dialog.findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('"group add" menu iteam appears')
group_add_item = group_frame.findMenuItem("group add", checkShowing=False)

# Step4: Delete "group add" group
group_add_item.click(log=True)
sleep(config.SHORT_DELAY)

group_frame.findAllPushButtons(None)[0].mouseClick()
sleep(config.SHORT_DELAY)

procedurelogger.expectedResult('"group add" menu iteam disappears')
menuitems = group_frame.findComboBox(None).findAllMenuItems(None)
if "group add" in [i.name for i in menuitems]:
    raise Exception, "ERROR: group add shouldn't exist, Delete group test fails"
    exit(2)

group_frame.altF4()

# Quit nautilus
menubar.findMenuItem("Close", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
nFrame.assertClosed()

## Add or delete file from group:
# Launch nautilus again
app = launchNautilus("/usr/bin/nautilus", "nautilus")

nFrame = app.findFrame(re.compile('^%s' % os.getenv('USER')))
menubar = nFrame.findMenuBar(None)
content_view = nFrame.findScrollPane("Content View")
icon_view = content_view.findLayeredPane("Icon View")
test1_icon = icon_view.findIcon("test1")

# Navigate to ~/test1, multiple select a.txt b.txt
openAction(test1_icon)
sleep(5)

procedurelogger.action("multiple select a.txt b.txt")
icon_view.selectAll()
sleep(config.SHORT_DELAY)

# Step1: From Edit, choose "Add to a new Group", input group name "group test1"
edit_menu = menubar.findMenu("Edit")
add_group = edit_menu.findMenuItem("Add to a new Group", checkShowing=False)
sleep(config.SHORT_DELAY)

try:
    edit_menu.findMenuItem(re.compile('group test1'), checkShowing=False)
except:
    add_group.click(log=True)
    sleep(config.MEDIUM_DELAY)

    new_dialog = app.findDialog("New group:")

    new_dialog.findText(None).typeText("group test1")
    sleep(config.SHORT_DELAY)

    new_dialog.findPushButton("OK").mouseClick()
    sleep(config.SHORT_DELAY)

# Step2: From Edit, choose "Edit the Group list"
edit_menu.mouseClick()
sleep(config.SHORT_DELAY)
edit_menu.findMenu("Add to Group.").mouseClick()
sleep(config.SHORT_DELAY)
edit_menu.findMenuItem(re.compile('^Edit the Group List')).mouseClick()
sleep(config.SHORT_DELAY)

group_frame = app.findFrame("Nautilus file group")

group_frame.findComboBox(None).mouseClick()
sleep(config.SHORT_DELAY)
group_frame.findMenuItem("group test1").mouseClick()
sleep(config.SHORT_DELAY)

# Step3: In group list, right-mouse click a file, choose "Remove this Item"
a_name = test1_path + 'a.txt'
a_cell = group_frame.findTreeTable(None).findTableCell(a_name)
sleep(config.SHORT_DELAY)

a_cell.mouseClick(button=3)
sleep(config.SHORT_DELAY)

app.findWindow(None).findMenuItem("Remove this Item").mouseClick()
sleep(config.SHORT_DELAY)

# Step4: Make sure a.txt item is removed from group
procedurelogger.expectedResult('Make sure a.txt item is removed from group')
cells = group_frame.findTreeTable(None).findAllTableCells(None)
if a_name in [i.name for i in cells]:
    raise Exception, "ERROR: a.txt shouldn't exist, Delete file from group test fails"
    exit(2)

# Step5: In group list, right-mouse click, choose "Add New Item", select file a.txt from ~/test1
group_frame.findTreeTable(None).mouseClick(button=3)
sleep(config.SHORT_DELAY)

app.findWindow(None).findMenuItem("Add New Item").mouseClick()
sleep(config.SHORT_DELAY)

select_dialog = app.findDialog("Select file")

toggle = select_dialog.findToggleButton("Type a file name")

if not toggle.checked:
    toggle.mouseClick()
    sleep(config.SHORT_DELAY)

location_text = select_dialog.findText(None, labelledBy="Location:")
location_text.insertText(test1_path)
location_text.mouseClick()
location_text.keyCombo('enter')
sleep(config.SHORT_DELAY)

select_dialog.findTableCell("a.txt").mouseClick()
sleep(config.SHORT_DELAY)

select_dialog.findPushButton("Open").mouseClick()
sleep(config.SHORT_DELAY)

# Step6: Make sure file a.txt  is added to group
procedurelogger.expectedResult('Make sure a.txt item is added to group')
cells = group_frame.findTreeTable(None).findAllTableCells(None)
if a_name not in [i.name for i in cells]:
    raise Exception, "ERROR: a.txt should exist, Add file to group test fails"
    exit(2)

## Send group to:
# Step1: Click "Send this group to"
group_frame.findAllPushButtons(None)[2].mouseClick()
sleep(config.SHORT_DELAY)

# Step2: send as "evolution" with zip
sendGroup(".zip")

# with tar.gz
group_frame.findAllPushButtons(None)[2].mouseClick()
sleep(config.SHORT_DELAY)

sendGroup(".tar.gz")

# with tar.bz2
group_frame.findAllPushButtons(None)[2].mouseClick()
sleep(config.SHORT_DELAY)

sendGroup(".tar.bz2")

# Remove group test and quit
group_frame.findAllPushButtons(None)[0].mouseClick()
sleep(config.SHORT_DELAY)

group_frame.altF4()

# Quit nautilus
menubar.findMenuItem("Close", checkShowing=False).click(log=True)
sleep(config.SHORT_DELAY)
nFrame.assertClosed()
