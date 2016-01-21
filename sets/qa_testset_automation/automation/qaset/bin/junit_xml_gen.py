#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from datetime import timedelta, datetime
import fnmatch
import glob
import json
import logging
import os
from optparse import OptionParser
import random
import re
import shutil
import sys
import subprocess
import uuid
import socket
import traceback
import xml.dom.minidom as MINIDOM
import xml.etree.ElementTree as ET

### Utils functions ###
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


class BaseParser(object):
    '''
    Base class of parser classes
    '''
    def __init__(self, path, logger=None):
        self.path = expand_path(path)
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
        else:
            self.logger = logger
    
    def get_result(self):
        return self.data


class TestcaseParser(BaseParser):
    # Read and parse testcase log file
    # Status/time info are omitted because they're already in test_results file
    def __init__(self, path, extracted, line_count=50, logger=None):
        super(self.__class__, self).__init__(path, logger)
        self.extracted = extracted
        self.line_count = line_count
        self.data = {'name'         : os.path.basename(path),   # [str] testcase name
                    'time'          : extracted['time'],        # [int] time used(in seconds)
                    'status'        : extracted['status'],      # [str] success/failure/error/skipped
                    'skipped'       : None,                     # [str] Skip message
                    'failure'       : None,                     # [dict] Example: {'type': 'failure',
                                                                #                   'message': '3/5 failure', 'text': '...'}
                    'error'         : None,                     # [dict] Example: {'type': 'error',
                                                                #                   'message': '2/5 error', 'text': '...'}
                    'system-out'    : None}                     # [str] log(50 lines by default)

    def parse_log(self):
        self.data['system-out'] = read_last_lines(self.path, count=self.line_count)

    def parse_skipped(self):
        if self.extracted['status'] == 'skipped':
            self.data['skipped'] = '%s/%s skipped' % (self.extracted['skipped'], self.extracted['count'])

    def parse_failure_error(self):
        for status in ['failure', 'error']:
            if self.extracted[status] > 0:
                self.data[status] = {'type'     : status,
                                    'message'   : '%s/%s %s' % (self.extracted[status],
                                                                self.extracted['count'],
                                                                status)}
                self.data[status]['text'] = self.data[status]['message']

    def parse(self):
        self.parse_log()
        self.parse_skipped()
        self.parse_failure_error()


class TestsuiteParser(BaseParser):
    '''
    Parse one test_results file and return a dict

    Test result file format:
        <testcase_name>                                         # testcase name line
        <failure> <success> <count> <time> <error> <skipped>    # test result line

    '''
    RESULT_ITEMS    = ['failure', 'success', 'count', 'time', 'error', 'skipped']
    TEST_RESULTS    = 'test_results'
    ID              = 0

    # path: Path to the log dir. Example: /usr/share/qa/ctcs2/qa_bzip2-2015-12-18-11-37-53
    def __init__(self, path, logger=None):
        super(self.__class__, self).__init__(path, logger)
        self.data = {'name'     : None,                 # [str] Testsuite name
                    'tests'     : 0,                    # [int] The amount of tests
                    'failures'  : 0,                    # [int] The amount of failed tests
                    'errors'    : 0,                    # [int] The amount of tests with internal errors
                    'time'      : 0,                    # [int] Time consumed by all its testcases(in seconds)
                    'skipped'   : 0,                    # [int] The amount of skipped tests
                    'timestamp' : None,                 # [str] Testsuite start time
                    'hostname'  : socket.gethostname(), # [str] Hostname
                    'id'        : TestsuiteParser.ID,   # [int] Sequence number
                    'package'   : None,                 # [str] Same as testsuite name
                    'testcases' : []}                   # [list] List of testcases
        TestsuiteParser.ID += 1
        self.test_results_file = os.path.join(self.path, TestsuiteParser.TEST_RESULTS)

    # Parse dir name to get testsuite name
    def parse_testsuite_name_timestamp(self):
        basename = os.path.basename(self.path)
        m = re.search(r'(.*)-(\d+(?:-\d+){5})', basename)
        assert m is not None, "Invalid directory name: %s" % (basename)
        # Name & Package
        self.data['name'] = m.group(1).strip()
        self.data['name'] = re.sub(r'^qa[_\-]', '', self.data['name']) # Remove prefix: qa_
        self.data['name'] = self.data['name'].replace('-', '_')         # Replace - with _
        self.data['package'] = self.data['name']
        # Timestamp
        lst = m.group(2).split('-')
        date = '-'.join(lst[:3])
        time = ':'.join(lst[-3:])
        self.data['timestamp'] = "%sT%s" % (date, time)

    # Parse test result line and return a dict.
    # A test result line contains 6 numbers:
    #   <failure> <succeed> <count> <time> <error> <skipped>
    # 
    # Return: {'status': <status>, }
    def extract_result_line(self, line):
        m = re.search(r'\d+(\s+\d+){5}', line) 
        assert m is not None, "Invalid result line: %s" % (line)
        nums = line.split()
        nums = map(int, nums)
        assert nums[2] > 0, "No tests found: %s" % (line)
        status = None
        for i in [0, 4, 1, 5]:
            if nums[i] > 0:
                status = TestsuiteParser.RESULT_ITEMS[i]
        extracted_data = {'status': status}
        for i in range(len(TestsuiteParser.RESULT_ITEMS)):
            extracted_data[TestsuiteParser.RESULT_ITEMS[i]] = nums[i]
        return extracted_data

    # Parse the test_results file
    # and save the result to self.data['testcases']
    #               [{'name'    : <testcase name>,
    #               'failed'    : 0,
    #               'succeeded' : 2,
    #               'count'     : 2,
    #               'time'      : 10,
    #               'error'     : 0,
    #               'skipped'   : 0},
    #               'log'       : <100 lines of the log>}]
    def parse_testcases(self):
        self.data['testcases'] = []
        testcase_name = ''
        line_num = 0
        self.logger.debug("Parsing file %s" % (self.test_results_file))
        with file(self.test_results_file, 'r') as f:
            # Parse test_results file line by line
            for line in f:
                line_num += 1
                line = line.strip()
                # Testcase name line
                if line_num % 2 == 1:
                    testcase_name = line
                    self.logger.debug("Parsing testcase %s" % (testcase_name))
                    assert len(testcase_name) != 0, "[%s:%s]Invalid format" % (self.test_results_file, line_num)
                    continue
                # Test result line
                self.logger.debug("Getting results of testcase %s" % (testcase_name))
                try:
                    extracted = self.extract_result_line(line)
                except Exception, e:
                    self.logger.error("[%s:%s]Invalid format" % (self.test_results_file, line_num))
                    self.logger.debug(traceback.format_exc())
                    raise e
                try:
                    tp = TestcaseParser(os.path.join(self.path, testcase_name), extracted, logger=self.logger)
                    tp.parse()
                except Exception, e:
                    self.logger.error("Failed to parse testcase %s.%s" % (self.data['name'],
                                                                        testcase_name))
                    self.logger.debug(traceback.format_exc())
                testcase_data = tp.get_result()
                testcase_data['classname'] = "%s.%s" % (self.data['name'], testcase_data['name'])
                self.data['testcases'].append(testcase_data)
                # Statistics for testsuite
                self.data['time'] += testcase_data['time']
                self.data['tests'] += 1
                tmp = {'failure'    : 'failures',
                        'error'     : 'errors',
                        'skipped'   : 'skipped'}
                for k, v in tmp.items():
                    if testcase_data['status'] == k:
                        self.data[v] += 1
                # Prepare for next loop
                testcase_name = ''
        assert line_num % 2 == 0, ("No test result of testcase '%s'(%s:%s)" %
                                (testcase_name, self.test_results_file, line_num))

    # Parse all the data.
    def parse(self):
        self.parse_testsuite_name_timestamp()
        self.parse_testcases()


class TestsuiteTarballParser(BaseParser):
    '''
    Extract and parse the logs inside a tarball.
    A tarball may contain multiple testsuite log dirs'''

    TMP_DIR = '/tmp'

    # path: Path to the tarball containing logs. Example:
    #       /usr/share/qaset/log/gzip-ACAP2-20151216-20151216T110220.tar.bz2
    def __init__(self, path, logger=None):
        super(self.__class__, self).__init__(path, logger)
        self.extraction_dir = None
        self.data = []              # A list of testsuites

    # Create extraction dir for extracting tarballs
    def create_extraction_dir(self):
        unique_id = uuid.uuid4()
        dirname = "extracted_logs_%s" % (unique_id)
        extraction_dir = os.path.join(self.TMP_DIR, dirname)
        self.logger.debug("Creating %s" % (extraction_dir))
        os.mkdir(extraction_dir, 0755)
        self.extraction_dir = extraction_dir

    # Remove the extraction dir
    def remove_extraction_dir(self):
        try:
            shutil.rmtree(self.extraction_dir)
        except OSError, e:
            self.logger.warning("Unable to remove extraction dir %s.\nMaybe it's already removed?" % (self.extraction_dir))
            self.logger.debug(traceback.format_exc())
        self.extraction_dir = None

    # Extract a tarball to self.extraction_dir
    # tarball: The path to the log tarball
    def extract(self):
        cmd = "tar xf '%s' -C '%s'" % (self.path, self.extraction_dir)
        ret = subprocess.call(cmd, shell=True)
        assert ret == 0, "Extraction failed: %s" % (cmd)

    # Extract the tarball and parse the files inside it
    def parse(self):
        self.create_extraction_dir()
        self.extract()
        for entry in glob.glob(os.path.join(self.extraction_dir, '*')):
            p = TestsuiteParser(entry, self.logger)
            try:
                p.parse()
                self.data.append(p.get_result())
            except Exception, e:
                self.logger.error("Failed to parse %s: %s" % (entry, e))
                self.logger.debug(traceback.format_exc())
        self.remove_extraction_dir()
        # Check if there's any data
        if len(self.data) == 0:
            self.logger.warning("No log data in %s" % (self.path))


class SubmissionParser(BaseParser):
    '''
    Parse all submission logs to get submission ids and links.
    '''

    def __init__(self, path, logger=None):
        super(self.__class__, self).__init__(path, logger)
        self.data = {}  # A list containing all the submission links and ids

    def get_testsuite_name(self, submission_file_name):
        m = re.search(r'^submission-(.*)\.log$', submission_file_name)
        assert m is not None, "Can't detect testsuite name: %s" % (submission_file_name)
        name = m.group(1).strip().replace('-', '_')
        return m.group(1)

    def parse_submission(self, submission_file_path):
        file_name = os.path.basename(submission_file_path)
        testsuite_name = self.get_testsuite_name(file_name)
        s = read_last_lines(submission_file_path, 10)
        m = re.search(r'ID (\d+): (.*)$', s, re.MULTILINE | re.IGNORECASE)
        assert m is not None, "No submission id/link found: %s" % (file_name)
        self.data[testsuite_name] = {'id': m.group(1), 'link': m.group(2)}

    def parse(self):
        self.data = {}
        for entry in glob.glob(os.path.join(self.path, 'submission-*.log')):
            if os.path.isfile(entry):
                try:
                    self.parse_submission(entry)
                except AssertionError, e:
                    self.logger.warning("%s" % e)


class TestsuitesParser(BaseParser):
    '''
    Parse all the logs under a directory.

    Example:
        /var/log/qaset/log/
    '''

    RESULT_FILE_NAME    = 'test_results'
    TARBALL_PATTERN     = '*.tar.*'
    TMP_DIR             = '/tmp'

    # path: The directory containing log tarballs or log dirs.
    #   Example: /var/log/qaset/log/
    def __init__(self, name, path, logger=None):
        super(self.__class__, self).__init__(path, logger)
        self.data = {'name'     : name,     # [str] Test name(e.g.Kernel, Userspace regression)
                    'time'      : 0,        # [int] time used(in seconds)
                    'tests'     : 0,        # [int] Amount of testsuites
                    'failures'  : 0,        # [int] Amount of failed testsuites
                    'errors'    : 0,        # [int] Amount of testsuites with internal errors
                    'skipped'   : 0,        # [int] Amount of skipped testsuites
                    'testsuites': []}       # [list] List of testsuites

    # Parse all the tarballs or dirs in self.path
    def parse(self):
        for entry in glob.glob(os.path.join(self.path, '*')):
            if fnmatch.fnmatch(os.path.basename(entry), '*.tar.*'):
                p = TestsuiteTarballParser(entry, self.logger)
            elif os.path.isdir(entry):
                p = TestsuiteParser(entry, self.logger)
            else:
                self.logger.warning("Unknown entry '%s'" % (entry))
            try:
                p.parse()
            except Exception, e:
                self.logger.error("Failed to parse %s: %s" % (entry, e))
                self.logger.debug(traceback.format_exc())
            testsuites_data = p.get_result()
            if not isinstance(testsuites_data, list):
                testsuites_data = [testsuites_data]
            # Statistics for testsuites
            for testsuite in testsuites_data:
                self.data['time'] += testsuite['time']
                self.data['tests'] += testsuite['tests']
                self.data['failures'] += testsuite['failures']
                self.data['errors'] += testsuite['errors']
                self.data['skipped'] += testsuite['skipped']
            self.data['testsuites'].extend(testsuites_data)
        return self.data

class BaseElement(object):
    ATTR_BLACKLIST = ['system-out', 'system-err',
                        'submission_id', 'submission_link']

    def __init__(self, data, tag, parent=None):
        self.data = data
        self.elem = ET.Element(tag)
        if parent is not None:
            parent.append(self)

    def append(self, elem):
        if not isinstance(elem, BaseElement):
            raise TypeError("Cannot append %s as sub element. Type be BaseElement" % (elem.__class__.__name__))
        self.elem.append(elem.elem)

    def set_attrs(self):
        for k, v in self.data.items():
            if not(isinstance(v, list) or
                    isinstance(v, dict) or
                    v is None or
                    k in BaseElement.ATTR_BLACKLIST):
                if not isinstance(v, basestring):
                    v = str(v)
                self.elem.set(k, v)

    def to_pretty_xml(self, encoding='UTF-8'):
        return ET.tostring(self.elem, encoding=encoding, method='xml')


class TestcaseElement(BaseElement):
    def __init__(self, testcase_data, parent=None):
        super(self.__class__, self).__init__(testcase_data,
                                            'testcase',
                                            parent)
        self.convert()

    def convert_submission_data(self):
        if not(self.data.get('submission_id', None) and
                self.data.get('submission_link', None)):
            return
        text = "Submission ID %s: %s" % (self.data['submission_id'],
                                        self.data['submission_link'])
        # Write submission data into "system-err"
        err_elem = ET.SubElement(self.elem, 'system-err')
        cdata_elem = CDATA(text)
        err_elem.append(cdata_elem)

    def convert(self):
        self.set_attrs()
        self.convert_submission_data()
        # skipped
        if self.data['skipped'] is not None:
            skip_elem = ET.SubElement(self.elem, 'skipped')
            skip_elem.text = self.data['skipped']
        # failure & error
        for key in ['failure', 'error']:
            if self.data[key] is not None:
                elem = ET.SubElement(self.elem, key)
                for attr in ['type', 'message']:
                    elem.set(attr, self.data[key][attr])
                elem.text = self.data[key]['text']
        # system-out
        out_elem = ET.SubElement(self.elem, 'system-out')
        cdata_elem = CDATA(self.data['system-out'])
        out_elem.append(cdata_elem)


class TestsuiteElement(BaseElement):
    def __init__(self, testsuite_data, parent=None):
        super(self.__class__, self).__init__(testsuite_data,
                                            'testsuite',
                                            parent)
        self.convert()

    def convert(self):
        self.set_attrs()
        for testcase_data in self.data['testcases']:
            TestcaseElement(testcase_data, parent=self)


class TestsuitesElement(BaseElement):
    def __init__(self, testsuite_data, parent=None):
        super(self.__class__, self).__init__(testsuite_data,
                                            'testsuites',
                                            parent)
        self.convert()

    def convert(self):
        self.set_attrs()
        for testsuite_data in self.data['testsuites']:
            TestsuiteElement(testsuite_data, parent=self)


class JunitConverter(object):
    '''
    Convert testsuites data to junit format
    '''
    def __init__(self, name, log_dir, submission_dir=None, encoding='UTF-8', logger=None):
        self.name = name
        self.log_dir = expand_path(log_dir)
        if submission_dir is not None:
            submission_dir = expand_path(submission_dir)
        self.submission_dir = submission_dir
        self.root = None
        self.encoding = encoding
        self.logger = logger

    def __str__(self):
        return self.root.to_pretty_xml(self.encoding)

    def set_encoding(self, encoding):
        self.encoding = encoding

    def run(self):
        # Parse log files
        log_parser = TestsuitesParser(self.name, self.log_dir, self.logger)
        log_parser.parse()
        log_data = log_parser.get_result()
        # Parse submission files
        if self.submission_dir is not None:
            submission_parser = SubmissionParser(self.submission_dir, self.logger)
            submission_parser.parse()
            submission_data = submission_parser.get_result()
            # Add submission id and link to log_data
            for testsuite in log_data['testsuites']:
                d = {}
                for k, v in submission_data.items():
                    if k == testsuite['name']:
                        d = v
                if len(d) == 0:
                    self.logger.warning("No submission data for testsuite %s" % (testsuite['name']))
                    continue
                submission_id = d.get('id', None)
                submission_link = d.get('link', None)
                if submission_id and submission_link:
                    for testcase in testsuite['testcases']:
                        testcase['submission_id'] = submission_id
                        testcase['submission_link'] = submission_link
        # Create xml tree 
        self.root = TestsuitesElement(log_data)

    def dump(self, file_like_or_io):
        file_like_or_io.write(str(self))


if __name__ == '__main__':
    # Parse cmd line options
    usage = '''Usage: %prog [options] log_dir

  Arguments:
    log_dir             QA log dir. Default: /var/log/qaset/log

  Options:
    -n|--name           (Required)Name of this test(e.g.Kernel Regression, Userspace, Acceptance)
    -s|--submission     Log submission dir. Default: /var/log/qaset/submission
    -o|--output         Write xml to file instead of STDOUT
    -d|--debug          Enable debug mode
    -e|--encoding       (TBD)Set xml encoding. Default: UTF-8
'''
    op = OptionParser(usage=usage)
    op.add_option('-n', '--name', dest='name', type='string',
                help='Name of this test')
    op.add_option('-s', '--submission', dest='submission', type='string',
                default="/var/log/qaset/submission",
                help='Log submission dir. Default: /var/log/qaset/submission')
    op.add_option('-o', '--output', dest='file', type='string',
                help='Save xml to file')
    op.add_option('-d', '--debug', action="store_true", dest="debug",
                help='Enable debug mode')
    op.add_option('-e', '--encoding', dest="encoding", default='UTF-8',
                help='(TBD)Set xml encoding')
    (options, args) = op.parse_args()
    # Logger
    logging.basicConfig(format='[%(name)s]%(levelname)s: %(message)s')
    logger = logging.getLogger(__file__)
    level = logging.DEBUG if options.debug else logging.INFO
    logger.setLevel(level)
    # Check options & args
    try:
        assert len(args) == 1
        assert options.name
    except AssertionError, e:
        op.print_usage()
        exit(255)
    # Log dir & Submission dir
    log_dir = expand_path(args[0])
    assert os.path.isdir(log_dir), "Not a directory: %s" % (log_dir)
    submission_dir = expand_path(options.submission)
    if not os.path.isdir(submission_dir):
        logger.warning("No submission data. Not a directory: %s." % (submission_dir))
        submission_dir = None
    # Output file
    if options.file:
        try:
            outfile = file(options.file, 'w')
        except Exception, e:
            logger.error("Failed to create output file %s: %s" % (options.file, e))
            self.logger.debug(traceback.format_exc())
            exit(1)
    else:
        outfile = sys.stdout
    # Convert to xml
    converter = JunitConverter( options.name,
                                log_dir,
                                submission_dir=submission_dir,
                                encoding=options.encoding,
                                logger=logger)
    converter.run()
    converter.dump(outfile)
