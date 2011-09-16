#!/usr/bin/env python

##############################################################################
# Written by: Calen Chen <cachen@novell.com>
# Date:        06/22/2011
# Description: Switch between compiz and metacity Test
##############################################################################

# The docstring below is used in the generated log file
doc = """
==Gnome test==
===Switch between compiz and metacity===
Switch metacity to compiz:
Step1: If compiz is not in used, run "/usr/bin/compiz --replace"
Step2: Make sure metacity process is done, and compiz process is up
Step3: Launch "Desktop Effects" by runing simple-ccsm
Step4: Makse sure 'Enable desktop effects' in 'Desktop Effects' is checked

Switch compiz to metaciry:
Step1: run "/usr/bin/metacity --replace"
Step2: Make sure compiz process is done, and metacity process is up
Step3: Launch "Desktop Effects" by runing simple-ccsm
Step4: Makse sure 'Enable desktop effects' in 'Desktop Effects' is unchecked
"""

# imports
from strongwind import *
from gnome_frame import *
import os

print doc

def getPid(process_name):
    '''
    Get pid of the expected process
    '''
    cmd = "ps -C %s |grep -v CMD |awk '{print $1'}" % process_name
    pid = os.popen(cmd).read().strip()
    return pid

## Switch metacity to compiz:
# Step1: If compiz is not in used, run "/usr/bin/compiz --replace"
compiz_pid = getPid("compiz")

procedurelogger.action('Run "/usr/bin/compiz --replace"')
if compiz_pid == '':
    subproc = subprocess.Popen("/usr/bin/compiz --replace &", shell=True)
    sleep(config.LONG_DELAY)

# Step2: Make sure metacity process is done, and compiz process is up
procedurelogger.expectedResult('metacity process should done, compiz process pid should up')
if getPid("metacity") != '':
    raise Exception, "metacity process pid should removed, but still exist, BUG574248 still happens"
    exit(1)

if getPid("compiz") == '':
    raise Exception, "compiz process pid doesn't exist, BUG574248 still happens"
    exit(1)

# Step3: Launch "Desktop Effects" by runing simple-ccsm
sh_app = launchApp("/usr/bin/simple-ccsm", "simple-ccsm")

scFrame = sh_app.findFrame("Simple CompizConfig Settings Manager")

# Step4: Makse sure 'Enable desktop effects' in 'Desktop Effects' is checked
enable_check = scFrame.findCheckBox("Enable desktop effects")

procedurelogger.expectedResult('Makse sure "Enable desktop effects" is checked')
if not enable_check.checked:
    subprocess.Popen('killall -9 simple-ccsm', shell=True)
    raise Exception, "'Enable desktop effects should checked, but now is unchecked"
    exit(1)

## Switch compiz to metaciry:
# Step1: run "/usr/bin/metacity --replace"
metacity_pid = getPid("metacity")

procedurelogger.action('Run "/usr/bin/metacity --replace"')
if metacity_pid == '':
    subproc = subprocess.Popen("/usr/bin/metacity --replace &", shell=True)
    sleep(config.LONG_DELAY)

# Step2: Make sure compiz process is done, and metacity process is up
procedurelogger.expectedResult('compiz process should done, metacity process pid should up')
if getPid("compiz") != '':
    raise Exception, "compiz process pid should removed, but still exist, BUG574248 still happens"
    exit(1)

if getPid("metacity") == '':
    raise Exception, "metacity process pid doesn't exist, BUG574248 still happens"
    exit(1)

# Step3: Launch "Desktop Effects" by runing simple-ccsm
sh_app = launchApp("/usr/bin/simple-ccsm", "simple-ccsm")

scFrame = sh_app.findFrame("Simple CompizConfig Settings Manager")

# Step4: Makse sure 'Enable desktop effects' in 'Desktop Effects' is unchecked
enable_check = scFrame.findCheckBox("Enable desktop effects")

procedurelogger.expectedResult('Makse sure "Enable desktop effects" is unchecked')
if enable_check.checked:
    subprocess.Popen('killall -9 simple-ccsm', shell=True)
    raise Exception, "'Enable desktop effects should unchecked, but now is checked"
    exit(1)

# Close simple-ccsm
scFrame.findPushButton("Close").mouseClick()
sleep(config.SHORT_DELAY)
sh_app.assertClosed()
