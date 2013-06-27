#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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


##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        12/24/2010
# Description: Tomboy Modified Note Of The Day Test
##############################################################################

# The docstring below  is used in the generated log file
doc = """
==Tomboy test==
===Modified Note Of The Day test===
Step1: From Preferences -> Add-ins -> Tools to enable "Note of the Day"
Step2: Make sure that a new note of the day for the new date is available
Step3: Insert some texts in the note
Step4: Update the system's date time to the next day
Step5: Restart Tomboy by logging out and back in
Step6: Make sure that a new note of the day for the next day is available, the old saved note from the previous day is available
Step7: Delete the new note
Step8: Restore the date time to the current day
Step9: Restore "Note of the Day" to disable

NOTE:
Some problems in accessibility:
(1) context menu of Tomboy on notification area doesn't accessible
"""
# imports
import os
from strongwind import *
from tomboy_frame import *

print doc

def setAddIns(action="Enable"):
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

    note_cell = tomboy_dialog.findTableCell("Note of the Day")
    note_cell.mouseClick()
    sleep(config.SHORT_DELAY)

    tomboy_dialog.findPushButton(action).mouseClick()
    sleep(config.SHORT_DELAY)

    tomboy_dialog.findPushButton("Close").mouseClick()
    sleep(config.SHORT_DELAY)
    tomboy_dialog.assertClosed()
    sleep(config.MEDIUM_DELAY)

def dayTime():
    time = os.popen('date "+%A, %B %d %Y"').read().replace('\n','').split(',')
    week = time[0]
    month = time[1].split(' ')[1]
    day = time[1].split(' ')[2]
    year = time[1].split(' ')[3]
    if day.startswith('0'):
        day = day.replace('0','')
    currentTime = '%s, %s %s %s' % (week, month, day, year)
    return currentTime

# Check version
app_name = checkVersion()

# Kill the exist Tomboy process
killRunning()

# Load Tomboy for the first time
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel
tomboy_panel = tomboyPanel()

# Step1: From Preferences -> Add-ins -> Tools to enable "Note of the Day"
setAddIns(action="Enable")

# Step2: Make sure that a new note of the day for the new date is available
tomboy_panel.mouseClick()
sleep(config.SHORT_DELAY)

current_time = dayTime()
today_item = app.findWindow(None).findMenuItem(re.compile('^Today: %s' % current_time))
today_item.mouseClick()
sleep(config.SHORT_DELAY)

today_note = app.findFrame('Today: %s' % current_time)

# Step3: Insert some texts in the note and save
today_text = today_note.findText(None)
note_name = today_note.name

today_text.insertText("Test Note for case1014771", offset=60)
sleep(config.SHORT_DELAY)

today_note.altF4()

killRunning()

# Step4: Update the system's date time to the next day
days = os.popen('date "+%m %d %Y %H %M"').read().replace('\n','').split(' ')

month = days[0]
day = days[1]
year = days[2]
hour = days[3]
minute = days[4]

if int(month) == 12 and int(day) == 31:
    month = '01'
    day = 0
    year = int(days[2]) + 1

if int(month) != 12 and int(day) in [28, 30, 31] :
    month = '0' + str(int(month) + 1)
    day = 0

if day == 0:
    next_day = '0' + str(int(day) + 1)
elif day.startswith('0') and day != '09':
    next_day = '0' + str(int(day) + 1)
else:
    next_day = int(day) + 1

procedurelogger.action("Update the system's date time to the next day")
os.system('date %s%s%s%s%s' %(month,next_day,hour,minute,year))
sleep(config.SHORT_DELAY)

# Step5: Restart Tomboy by logging out and back in
(app, subproc) = cache.launchApplication('/usr/bin/tomboy', app_name, wait=config.MEDIUM_DELAY)

# Find tomboy on panel

tomboy_panel = tomboyPanel()

# Step6: Make sure that a new note of the day for the next day is available
tomboy_panel.mouseClick()
sleep(config.MEDIUM_DELAY)

tomboy_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)

tomboy_panel.mouseClick(log=False)
sleep(config.SHORT_DELAY)

new_current_time = dayTime()
today_item = app.findWindow(None).findMenuItem(re.compile('^Today: %s' % new_current_time))
today_item.mouseClick()
sleep(config.SHORT_DELAY)

today_note_new = app.findFrame('Today: %s' % new_current_time)

if os.getenv("USER") != "root":
    deleteNote(app, today_note_new)
    setAddIns(action="Disable")
else:
    # The old saved note from the previous day is available
    tomboy_panel.mouseClick()
    sleep(config.SHORT_DELAY)

    today_item = app.findWindow(None).findMenuItem(re.compile('^Today: %s' %     current_time))
    today_item.mouseClick()
    sleep(config.SHORT_DELAY)

    today_note_old = app.findFrame('Today: %s' % current_time)

    # Step7: Delete the new note
    deleteNote(app, today_note_old)
    deleteNote(app, today_note_new)

    # Step8: Restore the date time to the current day
    procedurelogger.action("Restore the date time to the current day")
    os.system('date %s%s%s%s%s' %(days[0],days[1],days[3],days[4],days[2]))

    # Step9: Restore "Note of the Day" to disable
    setAddIns(action="Disable")

# Quit Tomboy
quitTomboy(tomboy_panel)

