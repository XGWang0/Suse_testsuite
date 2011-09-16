#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/10/2010
# Description: Tomboy Import From Sticky Notes Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Import From Sticky Notes test===
Step1: Right click gnome panel, launch Add to Panel dialog
Step2: Add Sticky Notes to gnome panel
Step3: Double click Sticky Notes on panel to open a new note
Step4: Insert some texts into the Sticky note
Step5: Re-launch Tomboy
Step6: Open an exist note, from tools click Import from Sticky Notes
Step7: Make sure Sticky Note is imported in Tomboy note list
"""
# imports
from strongwind import *
from tomboy_frame import *

print doc

# Check version
app_name = checkVersion()

# Kill the exist Tomboy process
killRunning()

# Step1: Right click gnome panel, launch Add to Panel dialog
gnome_panel = cache._desktop.findApplication("gnome-panel", checkShowing=False)
gnome_panel.findPanel("Bottom Expanded Edge Panel").mouseClick(button=3)
sleep(config.SHORT_DELAY)

gnome_panel.findWindow(None).findMenuItem(re.compile('^Add to Panel')).mouseClick()
sleep(config.SHORT_DELAY)

add_dialog = gnome_panel.findDialog("Add to Panel")

# Step2: Add Sticky Notes to gnome panel
add_table = add_dialog.findTable(None)
sticky_cell = add_dialog.findTableCell(re.compile('^Sticky Notes'), checkShowing=False)

sticky_cell.select()
sleep(config.SHORT_DELAY)

add_dialog.findPushButton("Add").mouseClick()
sleep(config.SHORT_DELAY)

add_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)

add_dialog.assertClosed()

# Step3: Double click Sticky Notes to open a new note
bottom_panel = gnome_panel.findPanel("Bottom Expanded Edge Panel")

sticky_panel = bottom_panel.findAllPanels(None)[-1]

doubleClick(sticky_panel)
sleep(config.SHORT_DELAY)

sticky_app = cache._desktop.findApplication("stickynotes_applet", checkShowing=False)

# Step4: Insert some texts into the Sticky note
sticky_text = sticky_app.findFrame(None).findText(None)
sticky_text.insertText("test note for case1014770")
sleep(config.SHORT_DELAY)

# Step5: launch Tomboy
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()
sticky_text.mouseClick()
sleep(config.SHORT_DELAY)

# Make sure "Sticky Notes importer" is enabled
tomboy_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 4)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)

tomboy_dialog = app.findDialog("Tomboy Preferences")
tomboy_dialog.findPageTab("Add-ins").mouseClick()

# Expand Tools
tools = tomboy_dialog.findTableCell("Tools")
bbox = tools._accessible.queryComponent().getExtents(pyatspi.DESKTOP_COORDS)
x = bbox.x
y = bbox.y

procedurelogger.action('Expand Tools tree')
pyatspi.Registry.generateMouseEvent(x-30, y+10, 'b1c')
sleep(config.SHORT_DELAY)

note_cell = tomboy_dialog.findTableCell("Sticky Notes Importer")
note_cell.mouseClick()
sleep(config.SHORT_DELAY)

tomboy_dialog.findPushButton("Enable").mouseClick()
sleep(config.SHORT_DELAY)

tomboy_dialog.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
tomboy_dialog.assertClosed()
sleep(config.MEDIUM_DELAY)


# Step6: Open an exist note, from tools click Import from Sticky Notes
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
keyPress(tomboy_panel, "Up", 4)
tomboy_panel.keyCombo('enter', grabFocus=False)
sleep(30)

start_frame = app.findFrame("Start Here")
start_frame.findAllToggleButtons(None)[1].mouseClick()
sleep(config.SHORT_DELAY)

app.findWindow(None).findMenuItem("Import from Sticky Notes").mouseClick()
sleep(config.SHORT_DELAY)

app.findDialog(None).findPushButton("OK").mouseClick()
sleep(config.SHORT_DELAY)

start_frame.altF4()

# Step7: Make sure Sticky Note is imported in Tomboy note list
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)
try:
    app.findWindow(None).findMenuItem(re.compile('Sticky Note'))
except SearchError:
    raise SearchError, "Fails to import Sticky Notes"
else:
    keyPress(tomboy_panel, "Up", 6)
    tomboy_panel.keyCombo('enter', grabFocus=False)
    sleep(config.SHORT_DELAY)

    sticky_frame = app.findFrame(re.compile('^Sticky Note'))

# Delete the note
procedurelogger.action('Click Delete button')
sticky_frame.findPushButton("Delete").__getattr__('click')()
sleep(config.SHORT_DELAY)
app.findDialog(None).findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

sticky_frame.assertClosed()

# Quit Tomboy
quitTomboy(tomboy_panel)

# Delete Sticky Note
sticky_text.grabFocus()
sleep(config.SHORT_DELAY)
sticky_app.findFrame(None).keyCombo('<Alt>F4', grabFocus=False)

sticky_app.findDialog(None).findPushButton("Delete").mouseClick()
sleep(config.SHORT_DELAY)

sticky_app.assertClosed()

# Remove Sticky panel
sticky_panel.mouseClick(button=3)
sleep(config.SHORT_DELAY)
sticky_panel

keyPress(sticky_panel, "Up", 3)
sticky_panel.keyCombo('enter', grabFocus=False)
sleep(config.SHORT_DELAY)
