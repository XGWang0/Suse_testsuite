#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from collections import defaultdict
import contextlib
import glob
import sys
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom
import mmap
import optparse
import os

#from six import u, iteritems, PY2

try:
    # Python 2
    unichr
except NameError:  # pragma: nocover
    # Python 3
    unichr = chr

"""
Based on the understanding of what Jenkins can parse for JUnit XML files.

<?xml version="1.0" encoding="utf-8"?>
<testsuites errors="1" failures="1" tests="4" time="45">
    <testsuite errors="1" failures="1" hostname="localhost" id="0" name="test1"
               package="testdb" tests="4" timestamp="2012-11-15T01:02:29">
        <properties>
            <property name="assert-passed" value="1"/>
        </properties>
        <testcase classname="testdb.directory" name="1-passed-test" time="10"/>
        <testcase classname="testdb.directory" name="2-failed-test" time="20">
            <failure message="Assertion FAILED: failed assert" type="failure">
                the output of the testcase
            </failure>
        </testcase>
        <testcase classname="package.directory" name="3-errord-test" time="15">
            <error message="Assertion ERROR: error assert" type="error">
                the output of the testcase
            </error>
        </testcase>
        <testcase classname="package.directory" name="3-skipped-test" time="0">
            <skipped message="SKIPPED Test" type="skipped">
                the output of the testcase
            </skipped>
        </testcase>
        <testcase classname="testdb.directory" name="3-passed-test" time="10">
            <system-out>
                I am system output
            </system-out>
            <system-err>
                I am the error output
            </system-err>
        </testcase>
    </testsuite>
</testsuites>
"""


def decode(var, encoding):
    '''
    If not already unicode, decode it.
    '''

    #if PY2:
    if isinstance(var, unicode):
        ret = var
    elif isinstance(var, str):
        if encoding:
            ret = var.decode(encoding)
        else:
            ret = unicode(var)
    else:
        ret = unicode(var)
    '''
    else:
        ret = str(var)

    '''
    return ret

class TestSuite(object):
    '''Suite of test cases.
    Can handle unicode strings or binary strings if their encoding is provided.
    '''

    def __init__(self, name, test_cases=None, hostname=None, id=None,
                 package=None, timestamp=None, properties=None):
        self.name = name
        if not test_cases:
            test_cases = []
        try:
            iter(test_cases)
        except TypeError:
            raise Exception('test_cases must be a list of test cases')
        self.test_cases = test_cases
        self.hostname = hostname
        self.id = id
        self.package = package
        self.timestamp = timestamp
        self.properties = properties


    def build_xml_doc(self, encoding=None):
        '''
        Builds the XML document for the JUnit test suite.
        Produces clean unicode strings and decodes non-unicode with the help of encoding.
        @param encoding: Used to decode encoded strings.
        @return: XML document with unicode string elements
        '''

        # build the test suite element
        test_suite_attributes = dict()
        test_suite_attributes['name'] = decode(self.name, encoding)
        test_suite_attributes['failures'] = \
            str(len([c for c in self.test_cases if c.is_failure()]))
        test_suite_attributes['errors'] = \
            str(len([c for c in self.test_cases if c.is_error()]))
        test_suite_attributes['skipped'] = \
            str(len([c for c in self.test_cases if c.is_skipped()]))
        test_suite_attributes['time'] = \
            str(sum(c.elapsed_sec for c in self.test_cases if c.elapsed_sec))
        test_suite_attributes['tests'] = str(len(self.test_cases))

        if self.hostname:
            test_suite_attributes['hostname'] = decode(self.hostname, encoding)
        if self.id:
            test_suite_attributes['id'] = decode(self.id, encoding)
        if self.package:
            test_suite_attributes['package'] = decode(self.package, encoding)
        if self.timestamp:
            test_suite_attributes['timestamp'] = decode(self.timestamp, encoding)

        xml_element = ET.Element("testsuite", test_suite_attributes)

        # add any properties
        if self.properties:
            props_element = ET.SubElement(xml_element, "properties")
            for k, v in self.properties.items():
                attrs = {'name': decode(k, encoding), 'value': decode(v, encoding)}
                ET.SubElement(props_element, "property", attrs)

        # test cases
        for case in self.test_cases:
            test_case_attributes = dict()
            test_case_attributes['name'] = decode(case.name, encoding)
            if case.elapsed_sec is not None:
                test_case_attributes['time'] = "%f" % case.elapsed_sec
            if case.classname:
                test_case_attributes['classname'] = decode(case.classname, encoding)
            if case.status:
                test_case_attributes['status'] = decode(case.status, encoding)

            test_case_element = ET.SubElement(
                xml_element, "testcase", test_case_attributes)

            # failures
            if case.is_failure():
                attrs = {'type': 'failure'}
                if case.failure_message:
                    attrs['message'] = decode("RandomFailure", encoding)
                    #attrs['message'] = decode(case.failure_message, encoding)
                failure_element = ET.Element("failure", attrs)
                if case.failure_output:
                    failure_element.text = decode(case.failure_output, encoding)
                test_case_element.append(failure_element)

            # errors
            if case.is_error():
                attrs = {'type': 'error'}
                if case.error_message:
                    attrs['message'] = decode(case.error_message, encoding)
                error_element = ET.Element("error", attrs)
                if case.error_output:
                    error_element.text = decode(case.error_output, encoding)
                test_case_element.append(error_element)

            # skippeds
            if case.is_skipped():
                attrs = {'type': 'skipped'}
                if case.skipped_message:
                    attrs['message'] = decode(case.skipped_message, encoding)
                skipped_element = ET.Element("skipped", attrs)
                if case.skipped_output:
                    skipped_element.text = decode(case.skipped_output, encoding)
                test_case_element.append(skipped_element)

            # test stdout
            if case.stdout is not None:
                stdout_element = ET.Element("system-out")
                stdout_element.text = decode(case.stdout, encoding)
                test_case_element.append(stdout_element)

            # test stderr
            if case.stderr:
                stderr_element = ET.Element("system-err")
                stderr_element.text = decode(case.stderr, encoding)
                test_case_element.append(stderr_element)

        return xml_element

    @staticmethod
    def to_xml_string(test_suites, test_suites_name, prettyprint=True, encoding=None):
        '''Returns the string representation of the JUnit XML document.
        @param encoding: The encoding of the input.
        @return: unicode string
        '''

        try:
            iter(test_suites)
        except TypeError:
            raise Exception('test_suites must be a list of test suites')

        xml_element = ET.Element("testsuites")
        attributes = defaultdict(int)
        for ts in test_suites:
            ts_xml = ts.build_xml_doc(encoding=encoding)
            for key in ['failures', 'errors', 'skipped', 'tests']:
                attributes[key] += int(ts_xml.get(key, 0))
            for key in ['time']:
                attributes[key] += float(ts_xml.get(key, 0))
            for key in ['package']:
                attributes[key] = test_suites_name
            xml_element.append(ts_xml)
        #for key, value in iteritems(attributes):
        for key, value in attributes.iteritems():
            xml_element.set(key, str(value))

        xml_string = ET.tostring(xml_element, encoding=encoding)
        # is encoded now
        xml_string = TestSuite._clean_illegal_xml_chars(
            xml_string.decode(encoding or 'utf-8'))
        # is unicode now

        if prettyprint:
            # minidom.parseString() works just on correctly encoded binary strings
            xml_string = xml_string.encode(encoding or 'utf-8')
            xml_string = xml.dom.minidom.parseString(xml_string)
            # toprettyxml() produces unicode if no encoding is being passed or binary string with an encoding
            xml_string = xml_string.toprettyxml(encoding=encoding)
            if encoding:
                xml_string = xml_string.decode(encoding)
            # is unicode now
        return xml_string

    @staticmethod
    def to_file(file_descriptor, test_suites, testsuite_name, prettyprint=True, encoding=None):
        '''
        Writes the JUnit XML document to a file.
        '''
        xml_string = TestSuite.to_xml_string(
            test_suites, testsuite_name, prettyprint=prettyprint, encoding=encoding)
        # has problems with encoded str with non-ASCII (non-default-encoding) characters!
        file_descriptor.write(xml_string)


    @staticmethod
    def _clean_illegal_xml_chars(string_to_clean):
        '''
        Removes any illegal unicode characters from the given XML string.
        
        @see: http://stackoverflow.com/questions/1707890/fast-way-to-filter-illegal-xml-unicode-chars-in-python
        '''

        illegal_unichrs = [
            (0x00, 0x08), (0x0B, 0x1F), (0x7F, 0x84), (0x86, 0x9F),
            (0xD800, 0xDFFF), (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF),
            (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), (0x3FFFE, 0x3FFFF),
            (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
            (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), (0x9FFFE, 0x9FFFF),
            (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
            (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF), (0xFFFFE, 0xFFFFF),
            (0x10FFFE, 0x10FFFF)]

        illegal_ranges = ["%s-%s" % (unichr(low), unichr(high))
                          for (low, high) in illegal_unichrs
                          if low < sys.maxunicode]

        illegal_xml_re = re.compile(u'[%s]' % u''.join(illegal_ranges))
        return illegal_xml_re.sub('', string_to_clean)


class TestCase(object):
    """A JUnit test case with a result and possibly some stdout or stderr"""

    def __init__(self, name, classname=None, elapsed_sec=None, stdout=None,
                 stderr=None, status='success'):
        self.name = name
        self.elapsed_sec = elapsed_sec
        self.stdout = stdout
        self.stderr = stderr
        self.classname = classname
        self.error_message = None
        self.error_output = None
        self.failure_message = None
        self.failure_output = None
        self.skipped_message = None
        self.skipped_output = None
        self.status = status in ['passed', 'success'] and "success" or "failure"

    def add_error_info(self, message=None, output=None):
        """Adds an error message, output, or both to the test case"""
        if message:
            self.error_message = message
        if output:
            self.error_output = output

    def add_failure_info(self, message=None, output=None):
        """Adds a failure message, output, or both to the test case"""
        if message:
            self.failure_message = message
        if output:
            self.failure_output = output

    def add_skipped_info(self, message=None, output=None):
        """Adds a skipped message, output, or both to the test case"""
        if message:
            self.skipped_message = message
        if output:
            self.skipped_output = output

    def is_failure(self):
        """returns true if this test case is a failure"""
        if self.status in ['failure', 'failed']:
            self.failure_message = self.failure_output = self.stdout
            return True
        #return self.failure_output or self.failure_message

    def is_error(self):
        """returns true if this test case is an error"""
        if self.status in ['error']:
            self.error_message = self.error_output = self.stdout
            return True
        #return self.error_output or self.error_message

    def is_skipped(self):
        """returns true if this test case has been skipped"""
        return self.skipped_output or self.skipped_message

    
class CollectData(object):

    CASE_STATUS = {'PASS':'passed',
                   'FAIL':'failed',
                   'SKIP':'skipped'}

    CASE_TYPE = {'stress_validation':'SV',
                 'kernel_regression':'KR',
                 'user_regression':'UR'}

    CASE_DESC = {'stress_validation':('Stress Validation Test:\n'
                                        'This test is only for Stress validation test, '
                                        'the test will execute test cases (fs_stress, process_stress,  sched_stress) on specific arch machine'
                                        ' then upload output data, verify and analyze result automatically \n'
                                        'Test may be last several hours to finish, Once test pass, '
                                        'a mail notification will be send to test owner'),
                 'kernel_regression':('Kernel Regression Test:\n'
                                        'This test is only for Kernel regression test, '
                                        'the test will execute test cases on specific arch machine'
                                        ' then upload output data, verify and analyze result automatically \n'
                                        'Test may be last several hours to finish, Once test pass, '
                                        'a mail notification will be send to test owner'),
                 'user_regression':('User Space APP Test:\n'
                                      'This test is only for user space app test, '
                                      'the test will execute test cases () on specific arch machine'
                                      ' then upload output data, verify and analyze result automatically \n'
                                      'Test may be last several hours to finish, Once test pass, '
                                      'a mail notification will be send to test owner')}

    CTCS2_LOG_PATH = '/var/log/qa/oldlogs/'

    def __init__(self, options):
        self.options = options
        self.test_type = self.options.test_type
        self.log_folder = self.options.log_path
        self.submission_folder = self.options.submission_path

    def _convertTime(self, str_time="0h0m0s"):
        hour_num = min_num = sec_num = 0
        if 'h' in str_time:
            hour_num = re.search("(\d+)h", str_time).groups()[0]
        if 'm' in str_time:
            min_num = re.search("(\d+)m", str_time).groups()[0]
        if 's' in str_time:
            sec_num = re.search("(\d+)s", str_time).groups()[0]
        total_sec = int(hour_num) * 3600 + int(min_num) * 60 + int(sec_num)
        return total_sec


    def combineTCData(self, tc_name='tc', step_desc='', tc_status='passed',
                      tc_output=None, tc_url=None, tc_duration=0,):
        tmp_data_map = {}

        tmp_data_map['tc_name'] = tc_name
        tmp_data_map['step_desc'] = step_desc
        tmp_data_map['tc_status'] = tc_status == "timeout" and "failed" or tc_status
        tmp_data_map['tc_output'] = tc_output
        tmp_data_map['tc_url'] = tc_url
        tmp_data_map['tc_duration'] = tc_duration
        
        return [tmp_data_map]

    def combineTSData(self, ts_name='ts', ts_tc_list=[], ts_tags=None, ts_url=None):

        tmp_data_map = {}
        passed_tc_num = failed_tc_num = skipped_tc_num = 0
        tmp_data_map['ts_name'] = ts_name
        tmp_data_map['ts_tc_list'] = ts_tc_list
        tmp_data_map['ts_tags'] = ts_tags
        tmp_data_map['ts_url'] = ts_url

        if ts_tc_list:
            passed_tc_num = len(filter(lambda x: re.search('passed',x['tc_status'], re.I), ts_tc_list)) / float(len(ts_tc_list))
            failed_tc_num = len(filter(lambda x:re.search('(failed|timeout)',x['tc_status'],re.I), ts_tc_list)) / float(len(ts_tc_list))
            skipped_tc_num = len(filter(lambda x:re.search('skipped', x['tc_status'], re.I), ts_tc_list)) / float(len(ts_tc_list))

        tmp_data_map['ts_rate'] = ('Passed:%0.2f%%,' %(100 * passed_tc_num) + 
                                   'Failed:%0.2f%%,' %(100 * failed_tc_num) +
                                   'Skillped:%0.2f%%,' %(100 * skipped_tc_num))

        return [tmp_data_map]

    def getTestCaseOutput(self, ts_name, tc_name):
        folder = '/var/log/qa/oldlogs/'
        if os.path.exists(folder):
            all_folders = os.listdir(folder)
            folder_list = filter(lambda x : re.search("[qa_]*%s(_testsuite)*-\d+" %ts_name, x), all_folders)
            if folder_list:
                tc_file = os.path.join(folder, folder_list[-1], tc_name)
                if os.path.exists(tc_file):
                    with open(tc_file, "r") as f:
                        return f.read()
        return "Not found output file !"

    def getTestCaseInfo(self, file_name, submission_url):
        if not os.path.exists(file_name):
            tc_reason = 'Can not found file %s' %file_name
            return self.combineTCData(tc_name=os.path.basename(file_name),
                                      tc_status=CollectData.CASE_STATUS['FAIL'],
                                      tc_duration=0, tc_output=tc_reason)
        else:
            tc_info_list = []
            pattern = re.compile(r"(\[\s*\d+/\d+\]\s+)(\S+).*(passed|failed|skipped|timeout).*\((\S*)\)", re.DOTALL | re.IGNORECASE | re.MULTILINE)
            with open(file_name, 'r') as f:
                with contextlib.closing(mmap.mmap(f.fileno(), 0,
                                      access=mmap.ACCESS_READ)) as m:
                    line = m.readline()
                    while line:
                        re_s =  pattern.search(line)
                        if re_s:
                            tc = re_s.groups()
                            tc_duration = self._convertTime(tc[3])
                            
                            base_name = os.path.basename(file_name)
                            ts_name = '-' in base_name and base_name.split("-")[0] or base_name
                            tc_output = self.getTestCaseOutput(ts_name, tc[1])
                            #tc_output= ""
                            tc_info_list.extend(self.combineTCData(tc_name=tc[1],
                                                                   tc_status=tc[2].lower(),
                                                                   tc_duration=tc_duration,
                                                                   tc_output=tc_output,
                                                                   tc_url=submission_url))
                        line = m.readline()
            return tc_info_list


    def getSubmissionUrl(self, file_name, folder='/tmp/submission'):
        submission_file_list = glob.glob(os.path.join(folder, 'submission*-%s.log' %file_name))
        if submission_file_list:
            submission_file = submission_file_list[-1]
            with open(submission_file, 'r') as f:
                file_content = f.read()
                re_s = re.search("ID\s+\d+:\s+(http://\S+submission.php\?submission_id=\d+)", file_content, re.I)
                if re_s:
                    return re_s.groups()[0]
        else:
            return "Not found submission url"
                        
    def getTestSuiteInfo(self, run_folder='/var/log/qaset/runs/', runlog_postfix='screenlog',
                         submission_folder='/var/log/qaset/submission'):

        ts_info = []

        folder = run_folder
        file_list = glob.glob(os.path.join(folder, '*.%s' %runlog_postfix))
        for f in file_list:
            base_name = os.path.basename(f)
            ts_name = '-' in base_name and base_name.split("-")[0] or base_name
            ts_submission_url = self.getSubmissionUrl(file_name=ts_name, folder=submission_folder)
    
            tc_info = self.getTestCaseInfo(f, ts_submission_url)
            if tc_info:
                ts_info.extend(self.combineTSData(ts_name=ts_name, ts_tc_list=tc_info, ts_url=ts_submission_url))

        return ts_info

class CMDParamParser(optparse.OptionParser):
    """Class which parses command parameters
    """

    def __init__(self):
        
        pass

    def Param(self):
        optparse.OptionParser.__init__(
            self, 
            usage='Usage: %prog [options]',
            epilog="Generate HTML report ...")

        
        self.add_option("-t", "--testtype", action="store", type="choice",
                        dest="test_type", choices=["stress_validation","kernel_regression","user_regression","all"],
                        help=("Input test type \"stress_validation|kernel_regression|user_regression|all\"."))

        self.add_option("-l", "--logpath", action="store", type="string",
                        dest="log_path",
                        help=("Input a log path"))
    
        self.add_option("-s", "--submissionpath", action="store", type="string",
                        dest="submission_path",
                        help=("Input a submission path."))

        self.add_option("-o", "--output", action="store", type="string",
                        dest="outputfile",
                        help=("Input path which json and html file will be generated to there"))


        return self

class LOGGER(object):

    @staticmethod
    def info(msg):
        print '[INFO ] : %s' %msg
    
    @staticmethod
    def debug(msg):
        print '[DEBUG] : %s' %msg

    @staticmethod
    def error(msg):
        print '[ERROR] : %s' %msg

    @staticmethod
    def warn(msg):
        print '[WARN ] : %s' %msg    

def generateJunitXML(ts_list, testsuites_name, outputfile):
    try:
        iter(ts_list)
    except TypeError:
        raise Exception('test_suites must be a list of test suites')

    junit_ts_info = []
    for i, ts in enumerate(ts_list):
        tc_list = ts['ts_tc_list']
        ts_name = ts['ts_name']
        ts_package = ts['ts_name']
        ts_id = i
        
        junit_tc_info = []
        for tc in tc_list:
            tc_name = tc['tc_name']
            tc_classname = '%s.%s' %(ts_name, tc_name)
            tc_duration = tc['tc_duration']
            tc_status = tc['tc_status']
            if re.search('passed', tc_status, re.I):
                tc_output = tc['tc_url']
            else:
                tc_output = tc['tc_output'] and tc['tc_output'] + '\nQADB URL : %s' %tc['tc_url'] or tc['tc_url']
            
            junit_tc_info.append(TestCase(tc_name, tc_classname, tc_duration, tc_output, status=tc_status))
        
        junit_ts_info.append(TestSuite("my test suite", junit_tc_info, package=ts_package, id=str(ts_id)))
    
    with open(outputfile, 'w+') as f:
        TestSuite.to_file(f, junit_ts_info, testsuites_name)

def main():
    LOGGER.info("Start to generate junit xml file")
    ins_parseparam = CMDParamParser().Param()
    options, _args = ins_parseparam.parse_args()

    LOGGER.info("Collect all test case data")
    cd = CollectData(options)

    ts_info = cd.getTestSuiteInfo(run_folder=options.log_path,
                                  submission_folder=options.submission_path)
    '''
    import pprint
    pprint.pprint(ts_info)
    '''
    LOGGER.info("Generate Junit formated xml file")        
    generateJunitXML(ts_info, options.test_type, options.outputfile)

    LOGGER.info("Test result file is %s" %options.outputfile)
    LOGGER.info("End")
if __name__ == '__main__':
    main()

