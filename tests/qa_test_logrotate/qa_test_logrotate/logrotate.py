#!/usr/bin/python
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


import os, shutil, gzip, subprocess

TEST_DIR = '/tmp/qa_logrotate_test'
TEST_LOG = os.path.join(TEST_DIR, 'test_log')
TEST_CONF = os.path.join(TEST_DIR, 'test_log.conf')
TEST_MISSING = os.path.join(os.path.join(TEST_DIR, 'missing_dir'), 'test_log')

def setup(fill=True, copy=False, compress=False, weekly=True, addextension=False, rotate=5, dateformat=False, notifempty=False, ifempty=False, size=False, missingok=False, nomissingok=False):
	if os.path.exists(TEST_DIR):
		cleanup()
	os.mkdir(TEST_DIR)
	if fill:
		fill_log()
	conf = open(TEST_CONF, "wt")
	conf.write('create\n')
	if compress:
		conf.write('compress\n')
	log_location = TEST_LOG
	if missingok or nomissingok:
		log_location = TEST_MISSING
	conf.write('%s {\n' % log_location)
	if copy:
		conf.write('\tcopy\n')
        if addextension:
		conf.write('\taddextension .log\n')
	if dateformat:
		conf.write('\tdateext\n')
		conf.write('\t' + r'dateformat -%Y%m%d%s' + '\n')
	if notifempty:
		conf.write('\tnotifempty\n')
	if ifempty:
		conf.write('\tifempty\n')
	if size:
		conf.write('\tsize %s\n' % size)
	if weekly:
		conf.write('\tweekly\n')
	if missingok:
		conf.write('\tmissingok\n')
	if nomissingok:
		conf.write('\tnomissingok\n')
	conf.write('\trotate %d\n}' % rotate)
	conf.close()

def fill_log(text='First rotation.', lines=100):
	log = open(TEST_LOG, "a+")
	for x in range(lines):
		log.write('%d %s\n' % (x, text))
	log.close()

def rotate_log(force=True, missingok=False, nomissingok=False):
	arg = '-fv'
	if not force:
		arg = '-v'
	command = ['logrotate', arg, TEST_CONF]
	code = subprocess.Popen(command).wait()
	if missingok and code != 0:
		close (1)
	if nomissingok and code == 0:
		close (1)

def log_contains(text, filename=TEST_LOG):
	log = open(filename, "r")
	for line in log.readlines():
		if text in line:
			log.close()
			return True;
	log.close()
	return False;

def assert_contains(text, file_name=TEST_LOG):
	if not log_contains(text, filename=file_name):
		close(1)

def assert_not_contains(text, file_name=TEST_LOG):
	if log_contains(text, filename=file_name):
		close(1)

def assert_exists(file_name):
	if not os.path.exists(file_name):
		close(1)

def assert_not_exists(file_name):
	if os.path.exists(file_name):
		close(1)

def assert_rotated(count, text):
	log = os.path.join(TEST_DIR, TEST_LOG + '.' + str(count))
	assert_exists(log)
	if not log_contains(text, filename=log):
		close(1)

def unzip(file_name):
	zipped_file = gzip.GzipFile(file_name, 'rb')
	unzipped_file = file(file_name.replace('.gz', ''), 'wb')
	for line in zipped_file.readlines():
		unzipped_file.write(line)
	zipped_file.close()
	unzipped_file.close()

def cleanup():
	shutil.rmtree(TEST_DIR)

def close(code):
	cleanup()
	exit (code)


