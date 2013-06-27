#!/usr/bin/env python
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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
# Date:        07/20/2011
# Description: Set preference from gnome power managerment preferences test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Power Management Preferences===
Step1: Launch "gnome-power-manager" 
Step2: In tab "On AC Power", change Actions and Display settings
Step3: In tab "On Battery Power", change Actions and Display settings
Step4: In tab "Genaral", change Actions and Notification Area settings
Step5: In tab "Scheduling", change Automatic Wakeup settings
Step6: Revert the settings by click Make Default button

NOTES: All settings take effect should be checked manually!
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

root_pwd_path = "/usr/share/qa/data/passwords/root"
root_pwd = ""

if os.path.exists(root_pwd_path):
    f = open(root_pwd_path)
    root_pwd = f.read().strip()
    f.close()
elif root_pwd != "":
    root_pwd = root_pwd
else:
    print "WARNING: This test need root password authentication, but root_pwd is None, please set the root password first and run test again"
    exit(22)

# Step1: Launch "gnome-power-preferences" 
try:
    app = launchApp("/usr/bin/gnome-power-preferences", "gnome-power-preferences")
except IOError, msg:
    print "ERROR:  %s" % msg
    exit(2)

# just an alias to make things shorter
pFrame = app.gnomePowerPreferencesFrame

# Make default
pFrame.findPushButton("Make Default").mouseClick(log=False)
sleep(config.SHORT_DELAY)

# Authenticate, root_pwd will be the default root password
cache._desktop.typeText(root_pwd, log=False)
sleep(config.SHORT_DELAY)
pFrame.keyCombo("enter", grabFocus=False)
sleep(config.SHORT_DELAY)

# Step2: In tab "On AC Power", change Actions and Display settings
ac_tab = pFrame.findPageTab("On AC Power")

ac_tab.mouseClick()
sleep(config.SHORT_DELAY)

# get old value
ac_values_old = []
ac_sliders = ac_tab.findAllSliders(None)
for i in ac_sliders:
    ac_values_old.append(i.value)

try:
    ac_tab.findLabel(re.compile('^When laptop'))
except SearchError:
    is_laptop = False
else:
    is_laptop = True

if is_laptop:
    ac_combobox = ac_tab.findComboBox(None)
    ac_values_old.append(ac_combobox.name)

    ac_checkbox = ac_tab.findCheckBox("Dim display when idle")
    if ac_checkbox.checked:
        ac_values_old.append("%s checked" % i.name)

# set value
procedurelogger.action("Put computer to sleep when inactive for: 20 minutes")
ac_sliders[0].value = 20
sleep(config.SHORT_DELAY)

if is_laptop:
    procedurelogger.action("Put display to sleep when inactive for: 50 minutes")
    ac_sliders[1].value = 50
    sleep(config.SHORT_DELAY)

    procedurelogger.action("When laptop lid is closed: Hibernate")
    ac_combobox.findMenuItem("Hibernate", checkShowing=False).click()
    sleep(config.SHORT_DELAY)

    procedurelogger.action("Set display brightness to: 50")
    ac_sliders[2].value = 50
    sleep(config.SHORT_DELAY)

    if not ac_checkbox.checked:
        ac_checkbox.mouseClick()
        sleep(config.SHORT_DELAY)

# Make sure the settings are saved
ac_values_new = []
for i in ac_sliders:
    ac_values_new.append(i.value)

if is_laptop:
    ac_values_new.append(ac_combobox.name)

    if ac_checkbox.checked:
        ac_values_new.append("%s checked" % i.name)

procedurelogger.expectedResult("Make sure the settings are saved")
assert ac_values_new != ac_values_old, \
                         "On AC Power expect settings: %s, actual settings: %" % \
                                        (ac_values_new, ac_values_old)

if is_laptop:
    # Step3: In tab "On Battery Power", change Actions and Display settings
    bp_tab = pFrame.findPageTab("On Battery Power")
    bp_tab.mouseClick()
    sleep(config.SHORT_DELAY)

    # get old value
    bp_values_old = []
    bp_sliders = bp_tab.findAllSliders(None)
    for i in bp_sliders:
        bp_values_old.append(i.value)

    bp_comboboxs = bp_tab.findAllComboBoxs(None)
    for i in bp_comboboxs:
        bp_values_old.append(i.name)

    bp_checkboxs = bp_tab.findAllCheckBoxs(None)
    for i in bp_checkboxs:
        if i.checked:
            bp_values_old.append("%s checked" % i.name)

    # set value
    procedurelogger.action("Put computer to sleep when inactive for: 20 minutes")
    bp_sliders[0].value = 20
    sleep(config.SHORT_DELAY)

    procedurelogger.action("Put display to sleep when inactive for: 60 minutes")
    bp_sliders[1].value = 60
    sleep(config.SHORT_DELAY)

    procedurelogger.action("When laptop lid is closed: Blank screen")
    bp_comboboxs[0].findMenuItem("Blank screen", checkShowing=False).click()
    sleep(config.SHORT_DELAY)

    procedurelogger.action("When battery power is critically low: Do nothing")
    bp_comboboxs[1].findMenuItem("Do nothing", checkShowing=False).click()
    sleep(config.SHORT_DELAY)

    for i in bp_checkboxs:
        i.mouseClick()
        sleep(config.SHORT_DELAY)

    # Make sure the settings are saved
    bp_values_new = []
    for i in bp_sliders:
        bp_values_new.append(i.value)

    for i in bp_comboboxs:
        bp_values_new.append(i.name)

    for i in bp_checkboxs:
        if i.checked:
            bp_values_new.append("%s checked" % i.name)

    procedurelogger.expectedResult("Make sure the settings are saved")
    assert bp_values_new != bp_values_old, \
                        "On Battery Power expect settings: %s, actual settings: %" % \
                                           (bp_valuses_new, bp_values_old)

# Step4: In tab "Genaral", change Actions and Notification Area settings
general_tab = pFrame.findPageTab("General")
general_tab.mouseClick()
sleep(config.SHORT_DELAY)

# get old value
general_values_old = []
general_comboboxs = general_tab.findAllComboBoxs(None)
for i in general_comboboxs:
    general_values_old.append(i.name)

general_radios = general_tab.findAllRadioButtons(None)
for i in general_radios:
    if i.checked:
        general_values_old.append(i.name)

try:
    general_tab.findLabel("Extras")
except SearchError:
    pass
else:
    is_extras = True

if is_extras:
    general_checkboxs = general_tab.findAllCheckBoxs(None)
    for i in general_checkboxs:
        if i.checked:
            general_values_old.append("%s checked" % i.name)

# set value
procedurelogger.action("When the power button is pressed: Shutdown")
general_comboboxs[0].findMenuItem("Shutdown", checkShowing=False).click()
sleep(config.SHORT_DELAY)

procedurelogger.action("When the suspend button is pressed: Hibernate")
general_comboboxs[1].findMenuItem("Hibernate", checkShowing=False).click()
sleep(config.SHORT_DELAY)

general_radios[1].mouseClick()
sleep(config.SHORT_DELAY)

if is_extras:
    general_checkboxs[0].mouseClick()
    sleep(config.SHORT_DELAY)

# Make sure the settings are saved
general_values_new = []
if is_extras:
    for i in general_comboboxs:
        general_values_new.append(i.name)

for i in general_checkboxs:
    if i.checked:
        general_values_new.append("%s checked" % i.name)

for i in general_radios:
    if i.checked:
        general_values_new.append(i.name)

procedurelogger.expectedResult("Make sure the settings are saved")
assert general_values_new != general_values_old, \
                        "General expect settings: %s, actual settings: %" % \
                                           (general_valuses_new, general_values_old)

# Step5: In tab "Scheduling", change Automatic Wakeup settings
scheduling_tab = pFrame.findPageTab("Scheduling")
scheduling_tab.mouseClick()
sleep(config.SHORT_DELAY)

# get old value
scheduling_values_old = []
scheduling_checkboxs = scheduling_tab.findAllCheckBoxs(None)
for i in scheduling_checkboxs:
    if i.checked:
        scheduling_values_old.append("%s checked" % i.name)

scheduling_spins = scheduling_tab.findAllSpinButtons(None)
for i in scheduling_spins:
    scheduling_values_old.append(i.value)

# set value
if not scheduling_checkboxs[0].checked:
    scheduling_checkboxs[0].mouseClick()
    sleep(config.SHORT_DELAY)

procedurelogger.action("Set Wake up at: 12:30")
scheduling_spins[0].value = 12
scheduling_spins[1].value = 30
sleep(config.SHORT_DELAY)

scheduling_checkboxs[5].mouseClick()
sleep(config.SHORT_DELAY)

# Make sure the settings are saved
scheduling_values_new = []
for i in scheduling_checkboxs:
    if i.checked:
        scheduling_values_new.append("%s checked" % i.name)

for i in scheduling_spins:
    scheduling_values_new.append(i.value)

procedurelogger.expectedResult("Make sure the settings are saved")
assert scheduling_values_new != scheduling_values_old, \
                        "Scheduling expect settings: %s, actual settings: %" % \
                                           (scheduling_valuses_new, scheduling_values_old)

# Step6: Revert the settings by click Make Default button
pFrame.findPushButton("Make Default").mouseClick(log=False)
sleep(config.SHORT_DELAY)

cache._desktop.typeText(root_pwd, log=False)
sleep(config.SHORT_DELAY)
pFrame.keyCombo("enter", grabFocus=False, log=False)
sleep(config.SHORT_DELAY)

# Quit app
pFrame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
app.assertClosed()

