#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import timedelta, datetime
import glob
import logging
import os
from optparse import OptionParser
import random
import re
import shutil
import sys
import subprocess
import socket
import xml.etree.ElementTree as ET

HOSTNAME = socket.gethostname()

### Utils functions ###
def similarity(x, y): 
    m = [[0 for i in range(len(y)+1)] for i in range(len(x)+1)]
    for i in range(1, len(x) + 1): 
        for j in range(1, len(y) + 1): 
            if x[i-1] == y[j-1]:
                m[i][j] = m[i-1][j-1] + 1 
            elif m[i-1][j] > m[i][j-1]:
                m[i][j] = m[i-1][j]
            else:
                m[i][j] = m[i][j-1]
    return m[len(x)][len(y)] / ((len(x) + len(y)) / 2.0)

def get_logger(level=logging.INFO):
    logging.basicConfig(format='[%(name)s]%(levelname)s: %(message)s')
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(level)
    return logger

def current_timestamp():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Expand ~ and env vars of a path and return its absolute path
def expand_path(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return path

# Replace ]]> with ]]&gt;
def escape_cdata_text(text):
    return text.replace(']]>', ']]&gt;')

# Detect raw string encoding and convert it to unicode object
# Note: This function uses chardet lib to detect encoding,
#       but should work as well without it
def str_to_unicode(raw_str):
    try:
        # Use chardet to detect encoding
        import chardet
        res = chardet.detect(raw_str)
        return unicode(raw_str, res['encoding'])
    except:
        # Try all possible encodings
        for encoding in ['UTF-8', 'ASCII',                                      # ASCII and unicode
                        'windows-1252', 'latin-1',                              # English
                        'ISO-8859-5', 'windows-1251',                           # Bulgarian
                        'ISO-8859-16',                                          # German
                        'ISO-8859-2', 'windows-1250',                           # Hungarian
                        'ISO-8859-5', 'windows-1251',                           # Cyrillic
                        'Big5', 'GBK',                                          # Chinese
                        'ISO-8859-7', 'windows-1253']:                          # Greek
            try:
                return unicode(raw_str, encoding)
            except:
                continue
    raise ValueError("Unknown encoding: %s" % (raw_str))

def read_last_lines(path, count=50):
    path = expand_path(path)
    lines = []
    with file(path, 'r') as f:
        for line in f:
            if isinstance(count, int) and len(lines) >= count:
                lines.pop(0)
            lines.append(line.strip())
    return os.linesep.join(lines)

###### xml.etree.ElementTree Hack ######
# Hack xml.etree.ElementTree to support CDATA tag
# Generate a CDATA element
def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element

# Hack xml.etree.ElementTree to generate pretty xml
def _serialize_xml(write, elem, encoding, qnames, namespaces, level=0):
    def _indent_gen(i):
        return ' ' * (2 * i)
    tag = elem.tag
    text = elem.text
    if tag == '![CDATA[':
        # CDATA. Do NOT escape special characters except ]]>
        u = str_to_unicode(escape_cdata_text(text))
        write("<%s%s\n]]>\n" % (tag, u.encode(encoding)))
    elif tag is ET.Comment:
        write("%s<!--%s-->\n" % (_indent_gen(level),
                                ET._encode(text, encoding)))
    elif tag is ET.ProcessingInstruction:
        write("%s<?%s?>\n" % (_indent_gen(level),
                                ET._encode(text, encoding)))
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                string = ET._escape_cdata(text, encoding)
                if len(elem) > 0:
                    string = "%s%s\n" % (_indent_gen(level+1), string)
                write(string)
            for e in elem:
                _serialize_xml(write, e, encoding, qnames, None, level+1)
        else:
            write("%s<%s" % (_indent_gen(level), tag))
            items = elem.items()
            if items or namespaces:
                if namespaces:
                    for v, k in sorted(namespaces.items(),
                                       key=lambda x: x[1]):  # sort on prefix
                        if k:
                            k = ":" + k
                        write(" xmlns%s=\"%s\"" % (
                            k.encode(encoding),
                            ET._escape_attrib(v, encoding)
                            ))
                for k, v in sorted(items):  # lexical order
                    if isinstance(k, ET.QName):
                        k = k.text
                    if isinstance(v, ET.QName):
                        v = qnames[v.text]
                    else:
                        v = ET._escape_attrib(v, encoding)
                    write(" %s=\"%s\"" % (qnames[k], v))
            if text or len(elem):
                write(">")
                if len(elem) > 0:
                    write("\n")
                if text:
                    string = ET._escape_cdata(text, encoding)
                    if len(elem) > 0:
                        string = "%s%s\n" % (_indent_gen(level+1), string)
                    write(string)
                for e in elem:
                    _serialize_xml(write, e, encoding, qnames, None, level+1)
                string = "</%s>\n" % tag
                if len(elem) > 0:
                    string = "%s%s" % (_indent_gen(level), string)
                write(string)
            else:
                write(" />\n")
    if elem.tail:
        write("%s%s\n" % (_indent_gen(level),
                            ET._escape_cdata(elem.tail, encoding)))

ET._serialize_xml = ET._serialize['xml'] = _serialize_xml


class BaseElement(object):
    def __init__(self, tag, attrs={}, text=None, tail=None):
        self.data = {
            'tag'   : tag,
            'attrs' : attrs,
            'text'  : text,
            'tail'  : tail,
            'sub'   : [],
        }
        self.sub = []

    def add_sub_element(self, elem):
        self.data['sub'].append(elem.data)
        self.sub.append(elem)

    def set(self, k, v):
        self.data['attrs'][k] = v

    def get(self, k):
        return self.data['attrs'][k]

    def to_xml_element(self, data):
        if data['tag'] == 'CDATA':
            return CDATA(data.get('text', ''))
        elem = ET.Element(data['tag'])
        if data.get('text'):
            elem.text = data['text']
        if data.get('tail'):
            elem.text = data['tail']
        for k, v in data.get('attrs', {}).items():
            elem.set(k, str(v))
        # Convert sub elements
        for child in data.get('sub', []):
            sub_elem = self.to_xml_element(child)
            elem.append(sub_elem)
        return elem

    def to_xml(self, file_like=None, encoding='UTF-8'):
        root = self.to_xml_element(self.data)
        s = ET.tostring(root, encoding=encoding, method='xml')
        if file_like is not None:
            file_like.write(s)
        return s

class TestcaseElement(BaseElement):
    STATES = ('failure', 'success', 'count', 'time', 'error', 'skipped')

    # ts_name   : testsuite name
    # name      : testcase name
    def __init__(self, ts_name, name, states):
        self.states = {}
        for i in range(len(self.STATES)):
            self.states[self.STATES[i]] = states[i]
        self.calc_status()
        attrs = {
            'name'      : name,
            'classname' : '%s.%s' % (ts_name, name),
            'status'    : self.status,
            'time'      : self.states['time'],
        }
        super(self.__class__, self).__init__('testcase', attrs)

    def calc_status(self, states=None):
        if states is None:
            states = self.states
        self.status = 'success'
        for k in ['failure', 'error', 'success', 'skipped']:
            if states[k] > 0:
                self.status = k
                break
        return self.status

    def add_status_tag(self, msg=None):
        if msg is None:
            msg = "%d/%d %s" % (self.states[self.status],
                                self.states['count'],
                                self.status)
        if self.status in ['failure', 'error']:
            attrs = {'message': msg, 'type': self.status}
        elif self.status == 'skipped':
            attrs = {}
        else:
            return
        elem = BaseElement(self.status, attrs=attrs, text=msg)
        self.add_sub_element(elem)

    def add_system_tag(self, tag, msg):
        if tag not in ['system-err', 'system-out']:
            raise ValueError('Invalid tag: %s. Must be "system-err" or "system-out"' % tag)
        elem = BaseElement(tag)
        cdata_elem = BaseElement('CDATA', text=msg)
        elem.add_sub_element(cdata_elem)
        self.add_sub_element(elem)


class TestsuiteElement(BaseElement):
    NEXT_ID = 0

    def __init__(self, name, timestamp=None):
        if timestamp is None:
            timestamp = current_timestamp()
        attrs = {
            'name'      : name,
            'hostname'  : HOSTNAME,
            'id'        : TestsuiteElement.NEXT_ID,
            'package'   : name,
            'tests'     : 0,
            'failures'  : 0,
            'errors'    : 0,
            'skipped'   : 0,
            'time'      : 0,
            'timestamp' : timestamp,
        }
        TestsuiteElement.NEXT_ID += 1
        super(self.__class__, self).__init__('testsuite', attrs)

    def add_testcase(self, tc_elem):
        self.add_sub_element(tc_elem)
        self.data['attrs']['tests'] += 1
        self.data['attrs']['time'] += tc_elem.get('time')
        status = tc_elem.get('status')
        mapping = {
            'failure'   : 'failures',
            'error'     : 'errors',
            'skipped'   : 'skipped',
        }
        for k, v in mapping.items():
            if status == k:
                self.data['attrs'][v] += 1
                break
    
    def add_fake_testcase(self, name, msg):
        tc_elem = TestcaseElement(self.data['attrs']['name'],
                                'fake_testcase',
                                [1, 0, 1, 1, 0, 0])
        tc_elem.add_status_tag(msg)
        self.add_testcase(tc_elem)

class RootElement(BaseElement):
    def __init__(self, name):
        attrs = {
            'name'      : name,
            'tests'     : 0,
            'failures'  : 0,
            'errors'    : 0,
            'skipped'   : 0,
            'time'      : 0,
        }
        super(self.__class__, self).__init__('testsuites', attrs)

    def add_testsuite(self, ts_elem):
        self.add_sub_element(ts_elem)
        for item in ['tests', 'failures', 'errors', 'skipped', 'time']:
            self.data['attrs'][item] += ts_elem.get(item)


class DataCollector(object):
    def __init__(self, name, qaset_dir='/var/log/qaset', logger=None):
        if logger is None:
            self.logger = get_logger()
        else:
            self.logger = logger
        self.qaset_dir = qaset_dir
        assert os.path.isdir(self.qaset_dir), "Not a directory: %s" % (self.qaset_dir)
        self.name = name
        self.log_dir = os.path.join(self.qaset_dir, 'log')
        self.sub_dir = os.path.join(self.qaset_dir, 'submission')
        self.submission = {}
        self.root = RootElement(name)

    def create_tmp_dir(self):
        tmp_dir = '/tmp/junit_generator-%d' % random.randint(0, 100000)
        os.mkdir(tmp_dir, 0755)
        return tmp_dir

    def testsuite_name_fixup(self, name):
        name = name.replace('-', '_')
        name = re.sub(r'^qa_', '', name)    # Remove prefix: qa_
        name = re.sub(r'_testsuite$', '', name) # Remove postfix: _testsuite
        return name

    def extract_testsuite_dir_name(self, basename):
        m = re.search(r'(.*)-(\d+(?:-\d+){5})', basename)
        if not m:
            return basename, current_timestamp()
        # Name
        name = m.group(1).strip()
        name = self.testsuite_name_fixup(name)
        # Timestamp
        lst = m.group(2).split('-')
        date = '-'.join(lst[:3])
        time = ':'.join(lst[-3:])
        timestamp = "%sT%s" % (date, time)
        return name, timestamp

    def collect_submission(self):
        for sub_log in glob.glob(os.path.join(self.sub_dir, "*.log")):
            basename = os.path.basename(sub_log)
            m = re.search(r'(?<=submission-).*(?=.log)', basename)
            if not m:
                self.logger.warning("Not a submission log: %s" % (sub_log))
                break
            ts_name = m.group(0)
            # Submission ID & link
            data = {'id': None, 'link': None, 'dir': None}
            with file(sub_log, 'r') as f:
                content = f.read()
            m = re.search(r'ID (\d+): (.*)$', content, re.IGNORECASE | re.MULTILINE)
            if m:
                data['id'] = m.group(1)
                data['link'] = m.group(2).strip()
            else:
                self.logger.warning("No submission info for testsuite %s" % (ts_name))
            m = re.search(r'Processing:\s+([^\s]+)$', content, re.IGNORECASE | re.MULTILINE)
            if m:
                data['dir'] = m.group(1).strip()
            else:
                self.logger.warning("No log dir inside submission log of testsuite %s" % (ts_name))
            self.submission[ts_name] = data

    def collect_log(self):
        root = RootElement(self.name)
        # Extract tarballs
        tmp_dir = self.create_tmp_dir()
        for tarball in glob.glob(os.path.join(self.log_dir, '*.tar.*')):
            cmd = "tar xf '%s' -C '%s'" % (tarball, tmp_dir)
            ret = subprocess.call(cmd, shell=True)
            if ret != 0:
                self.logger.warning("Extraction failed: %s" % (os.path.basename(tarball)))
        # Create testsuite elements from submission data
        testsuites = {}
        for ts_name, d in self.submission.items():
            ts_elem = TestsuiteElement(ts_name)
            if d.get('dir'):
                ts_dir = os.path.join(tmp_dir, d['dir'])
                self.logger.debug("Parsing testsuite %s: %s" % (ts_name, d['dir']))
                self.parse_testsuite(ts_dir, ts_elem)
                shutil.rmtree(ts_dir)
            testsuites[ts_name] = ts_elem
        # Remaining testsuite dirs
        for ts_dir in glob.glob(os.path.join(tmp_dir, '*')):
            basename = os.path.basename(ts_dir)
            ts_name, timestamp = self.extract_testsuite_dir_name(basename)
            # Find the most similar ts_elem
            rate = 0
            ts_elem = None
            for k, v in testsuites.items():
                tmp = similarity(ts_name, k)
                if tmp > rate:
                    rate = tmp
                    ts_elem = v
            self.logger.debug("Parsing testsuite %s: %s" % (ts_name, basename))
            self.parse_testsuite(ts_dir, ts_elem)
            shutil.rmtree(ts_dir)
        # Create fake testcase for testsuites with no results
        # and add all testsuites to self.root
        for ts_name, ts_elem in testsuites.items():
            if len(ts_elem.sub) == 0:
                msg = "Testsuite %s didn't run at all. Installation failure?" % (ts_elem.get('name'))
                ts_elem.add_fake_testcase('fake_testcase', msg)
            self.root.add_testsuite(ts_elem)
        shutil.rmtree(tmp_dir)

    # path: path of the extracted testsuite log dir
    def parse_testsuite(self, path, ts_elem):
        basename = os.path.basename(path)
        ts_name, timestamp = self.extract_testsuite_dir_name(basename)
        ts_name = ts_elem.data['attrs']['name']
        ts_elem.set('timestamp', timestamp)
        # Read test_results
        try:
            with file(os.path.join(path, 'test_results')) as f:
                lines = f.read().splitlines()
        except IOError, e:
            lines = []
        for i in range(0, len(lines), 2):
            tc_name = lines[i]
            states = lines[i+1]
            if not(tc_name and states):
                break
            states = states.split()
            states = map(int, states)
            tc_elem = TestcaseElement(ts_name, tc_name, states)
            tc_elem.add_status_tag()
            # Read log file
            if self.submission[ts_name]['id'] and self.submission[ts_name]['link']:
                system_err = "Submission ID %s: %s" % (self.submission[ts_name]['id'],
                                                    self.submission[ts_name]['link'])
            else:
                system_err = "No submission info"
            tc_elem.add_system_tag('system-err', system_err)
            try:
                system_out = read_last_lines(os.path.join(path, tc_name))
            except IOError, e:
                system_out = "No test result found: %s" % (e)
            tc_elem.add_system_tag('system-out', system_out)
            # Add to testsuite
            ts_elem.add_testcase(tc_elem)
        if len(ts_elem.sub) == 0:
            # Add a fake testcase to indicate error
            msg = 'No testcases or no test_results file found for testsuite %s' % (ts_elem.get('name'))
            ts_elem.add_fake_testcase('fake_testcase', msg)


if __name__ == '__main__':
    usage = '''Usage: %prog [options] qaset_dir

Arguments:
    qaset_dir       qaset directory. e.g. /var/log/qaset

Options:
    -n|--name       (Required) Test run name, e.g. kernel_regression
    -o|--outfile    Write xml to file instead of stdout
    -d|--debug      Enable debug mode
'''
    op = OptionParser(usage=usage)
    op.add_option('-n', '--name', dest='name', type='string',
                help='Test run name')
    op.add_option('-o', '--outfile', dest='file', type='string',
                help='Write xml to file')
    op.add_option('-d', '--debug', action="store_true", dest="debug",
                help='Enable debug mode')
    (options, args) = op.parse_args()
    # Logger
    logging.basicConfig(format='[%(name)s]%(levelname)s: %(message)s')
    logger = logging.getLogger(__file__)
    level = logging.DEBUG if options.debug else logging.INFO
    logger.setLevel(level)
    # Check options
    try:
        assert len(args) == 1, "qaset_dir must be specified!"
        assert options.name, "Test run name must be specified!"
    except AssertionError, e:
        print e
        op.print_usage()
        exit(255)
    options.file = expand_path(options.file)
    dc = DataCollector(options.name, expand_path(args[0]), logger=logger)
    dc.collect_submission()
    dc.collect_log()
    with file(options.file, 'w') as f:
        dc.root.to_xml(f)
    exit(0)
