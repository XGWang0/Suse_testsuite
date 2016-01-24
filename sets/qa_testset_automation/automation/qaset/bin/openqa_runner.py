#!/usr/bin/env python
import argparse
import datetime
import glob
import os
from string import Template
import subprocess
import threading
import random
import re
import time
import logging

# Hack logging module to add heartbeat info
_orig_log = logging.Logger._log

def _new_log(self, level, msg, args, exc_info=None, extra=None):
    heart_rate = random.random() * 40 + 60
    msg = "%s (%.7fbpm)" % (msg, heart_rate)
    return _orig_log(self, level, msg, args, exc_info, extra)

logging.Logger._log = _new_log

def run_with_heartbeat(cmd, msg, begin_msg=None, succ_msg=None,
                        fail_msg=None, no_check=False, interval=60):
    def _parse_msg(s, data):
        tmpl = Template(s)
        return tmpl.safe_substitute(data)

    interval /= 3
    start_time = datetime.datetime.now()
    proc = PopenWithName('', cmd)
    if begin_msg is not None:
        parsed_msg = _parse_msg(begin_msg, {'pid': proc.pid})
        logging.info(parsed_msg)
    logging.info("># %s" % (cmd))
    count = 0
    while proc.poll() is None:
        count += 1
        if count >= interval:
            td = datetime.datetime.now() - start_time
            parsed_msg = _parse_msg(msg, {  'pid'       : proc.pid, 
                                            'seconds'   : td.seconds,
                                            'minutes'   : td.seconds/60})
            logging.info(parsed_msg)
            count = 0
        time.sleep(3)
    if no_check or proc.poll() == 0:
        end_msg = succ_msg
    else:
        end_msg = fail_msg
    if end_msg is not None:
        td = datetime.datetime.now() - start_time
        parsed_msg = _parse_msg(end_msg, { 'pid'       : proc.pid,
                                        'exitstatus': proc.poll(),
                                        'seconds'   : td.seconds,
                                        'minutes'   : td.seconds/60})
        logging.info(parsed_msg)
    return proc.poll(), proc.stdout.read()

def upload_log(log_tarball, upload_url_prefix):
    upload_url = "%s/uploadlog/%s"  % (upload_url_prefix,
                                        os.path.basename(log_tarball))
    cmd = "curl --form upload='%s' '%s'" % (log_tarball, upload_url)
    return run_with_heartbeat(cmd, 'Uploading "%s"' % (log_tarball),
                            succ_msg='Upload succeeded',
                            fail_msg='Upload failed with exit code $exitstatus')

def upload_all_logs(log_dir, upload_url_prefix, pattern='*.tar.*'):
    for item in glob.glob(os.path.join(log_dir, pattern)):
        upload_log(item, upload_url_prefix)


class PopenWithName(subprocess.Popen):
    def __init__(self, name, cmd):
        self.name = name
        super(self.__class__, self).__init__(cmd, shell=True, stdin=None,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT)


class OpenqaRunner(object):
    # run_script:   Script to trigger test. e.g. /usr/share/qa/qaset/run/kernel-all-run
    def __init__(self, run_script):
        self.script = run_script
        self.name = re.sub(r'-run$', '', os.path.basename(self.script))
        self.proc = None                # Subprocess of 'screen -r <pid>'
        self.main_proc = None

    def __del__(self):
        pass

    def start_test(self):
        logging.info("Starting %s testing" % (self.name))
        subprocess.check_call(self.script, shell=True, stdin=None,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for i in range(20):
            lst = self.list_proc()
            if len(lst) == 0:
                time.sleep(0.5)
            else:
                return
        raise RuntimeError("Failed to start test: %s" % (self.script))

    def list_proc(self):
        def _filter_proc_list(item):
            blacklist = ['hamsta', ]
            pid, name, status = item
            for item in blacklist:
                if item in name:
                    return False
            return True

        def _pid_to_int(item):
            pid, name, status = item
            pid = int(pid)
            return pid, name, status

        proc = PopenWithName('list-proc', 'screen -list')
        ret = proc.wait()
        output = proc.stdout.read()
        lst = re.findall(r'(\d+)\.([^\s]+)\s*\((\w+)\)', output)
        lst = filter(_filter_proc_list, lst)
        lst = map(_pid_to_int, lst)
        return lst

    def testrun_finished(self, lst=None):
        if lst is None:
            lst = self.list_proc()
        for pid, name, status in lst:
            if name.endswith("-%s" % (self.name)):
                return False
        return True

    def start_main_monitor(self, lst=None):
        if lst is None:
            lst = self.list_proc()
        for pid, name, status in lst:
            if name.endswith("-%s" % (self.name)):
                logging.info("Main process found: %d.%s" % (pid, name))
                self.main_proc = PopenWithName(name, 'screen -r %d' % (pid))
                return
        raise RuntimeError("No main process found")

    def stop_main_monitor(self):
        if self.main_proc is not None:
            # Fetch exitstatus to prevent zombie processes
            ret = self.main_proc.poll()
            if ret is None:
                logging.info("Killing main process...")
                self.main_proc.kill()
            else:
                logging.info("Main process exited")

    def get_test_proc(self, lst=None):
        def _filter_test_proc(item):
            pid, name, status = item
            if name.endswith("-%s" % (self.name)):
                return False
            return True
        if lst is None:
            lst = self.list_proc()
        lst = filter(_filter_test_proc, lst)
        assert len(lst) == 1, "Failed to find test proc: %s" % (lst)
        return lst[0]

    def main_loop(self, interval=60):
        lst = self.list_proc()
        while self.testrun_finished(lst) == False:
            try:
                pid, name, status = self.get_test_proc(lst)
            except AssertionError, e:
                logging.warning("No test process found")
                time.sleep(3)
                lst = self.list_proc()
                continue
            cmd = 'screen -r %d' % (pid)
            run_with_heartbeat( cmd, '${pid}.%s running for ${seconds}s' % (name),
                                begin_msg='Test process found: ${pid}.%s' % (name),
                                succ_msg='${pid}.%s succeeded in ${minutes}m' % (name),
                                fail_msg='${pid}.%s failed with code ${exitstatus} in ${minutes}m' % (name),
                                interval=interval,
                                no_check=False)
            lst = self.list_proc()

    def reset(self):
        logging.info("Resetting testset")
        subprocess.check_call('/usr/share/qa/qaset/qaset reset',
                                shell=True, stdin=None,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

    def run(self):
        self.reset()
        self.start_test()
        self.start_main_monitor()
        self.main_loop()
        self.stop_main_monitor()


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser(description='OpenQA test runner')
    parser.add_argument('script', type=str,
                        help='Script to start testing')
    parser.add_argument('-u', '--upload-url-prefix', metavar='URL', dest='upload_url',
                        type=str, required=True, help='Upload url prefix')
    parser.add_argument('-l', '--log-dir', metavar='DIR', dest='log_dir',
                        type=str, required=True, default='/var/log/qaset/log',
                        help='Log dir. Default: /var/log/qaset/log')
    parser.add_argument('-s', '--submission-dir', metavar='DIR', dest='submission_dir',
                        type=str, required=True, default='/var/log/qaset/submission',
                        help='Submission dir. Default: /var/log/qaset/submission')
    parser.add_argument('--junit-type', metavar='TYPE', dest='junit_type',
                        type=str, required=True,
                        help='Junit type')
    parser.add_argument('--junit-file', metavar='FILE', dest='junit_file',
                        type=str, required=True,
                        help='Junit type')
    args = parser.parse_args()
    # Init
    random.seed()
    logging.basicConfig(format='\r<%(asctime)s> [%(levelname)s] %(message)s\r',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    # Running test
    runner = OpenqaRunner(args.script)
    runner.run()
    # Upload logs
    upload_all_logs(args.log_dir, args.upload_url)
    # Generate junit report
    cmd = "/usr/share/qa/qaset/bin/junit_xml_gen.py %s -s %s -o %s -n '%s'" % (args.log_dir,
                                                                            args.submission_dir,
                                                                            args.junit_file,
                                                                            args.junit_type)
    subprocess.call(cmd, shell=True)
    exit(0)
