#!/usr/bin/python
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

import os, shutil, gzip, subprocess
from subprocess import Popen, call

TEST_DIR = '/tmp/qa_test_logwatch'

def setup():
	if os.path.exists(TEST_DIR):
		cleanup()
	os.mkdir(TEST_DIR)

def remove_text_from_file(filename, text):
	file_read = open(filename)
	file_write = open(filename + '.new', 'w')
	for line in file_read:
		if not text in line:
			file_write.write(line)
	os.remove(filename)
	shutil.move(filename + '.new', filename)

def assert_log_report_diff(first, second):
	diff = call(['diff', first, second], stdout=open('/dev/null', 'w'))
	if not diff:
		close(1)

def make_report(filename=None, detail=10, logfile=None, service=None):
	command = ['/usr/sbin/logwatch']
	command.append("--detail=" + str(detail))
	outputfile = None
	if filename:
		outputfile = open(filename, "wb")
	if logfile:
		command.append("--logfile=" + logfile)
	if service:
		command.append("--service=" + service)
	code = call(command, stdout=outputfile)
	if code != 0:
		close(1)

def cleanup():
	shutil.rmtree(TEST_DIR)

def close(code):
	cleanup()
	exit (code)


