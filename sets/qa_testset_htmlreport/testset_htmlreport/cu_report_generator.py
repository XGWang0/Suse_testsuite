#!/usr/bin/env python

import contextlib
import glob
import json
import warnings
import mmap
import os
import pickle
import random
import re
import sys
import optparse
import shutil

class JsonGenerator(object):
    
    def __init__(self, file_name):

        self.step_data = []
        self.scen_data = []
        self.feat_data = []
        self.file_name = file_name
        
    def addStep(self, step_name, step_status='passed', step_duration=0, step_keyword="TestCase:",
                     step_err_msg="", step_desc=None, step_output=None, step_doc=None, step_url=None):

        if step_desc:
            if type(step_desc) == type({}):
                if 'description' in step_desc:
                    step_desc_data = step_desc
                else:
                    step_desc_data = {}
                    warnings.warn("Error : Please pass correct data. eg:{\'description':\"Description for step\"}")
            elif type(step_desc) == type(''):
                step_desc_data = {'description':"%s" %step_desc}
            else:
                step_desc_data = {}
                warnings.warn("Error : Please pass correct data. eg:{\'description':\"Description for step\"},"
                              " \"This is description info\"")
        else:
            step_desc_data = {}

        # Add qadb url to step name
        if step_url:
            step_name = (step_name + " -  <a href=%s>QADB URL</a>" %step_url)
            
        if step_output:
            if type(step_output) == type({}):
                step_output_data = step_output
            elif type(step_output) == type([]):
                step_output_data = {'output':step_output}
            elif type(step_output) == type(''):
                step_output_data = {'output':[step_output]}
            else:
                step_output_data = {}
                warnings.warn("Error : Please pass correct data. eg:[\"This is step output info\"],"
                              " \"This is step output info\"")
        else:
            step_output_data = {}

        if step_doc:
            if type(step_doc) == type({}):
                if 'doc_string' in step_doc:
                    step_doc_data = step_doc
                else:
                    step_doc_data = {}
                    warnings.warn("Error : Please pass correct data. eg:{\'value':\"Doc string info for step\"}")
            elif type(step_doc) == type(''):
                step_doc_data = {'doc_string':{'value':"%s" %step_doc}}
            else:
                step_doc_data = {}
                warnings.warn("Error : Please pass correct data. eg:{\'value':\"Doc string info for step\"},"
                              " \"This is doc string info\"")
        else:
            step_doc_data = {}


        b_step_map = {'keyword':step_keyword,
                       'name':step_name,
                       'result':{'status':step_status,
                                 'error_message':(step_err_msg or "Test Case %s is failed, refer to qadb "
                                                  "for more details." %step_name),
                                 'duration':step_duration * pow(10,9)}}
        b_step_map.update(step_desc_data)
        b_step_map.update(step_output_data)
        b_step_map.update(step_doc_data)

        self.step_data.append(b_step_map)

    def addScenario(self, scen_name, scen_step=[], scen_keyword="TestSuite", scen_tags=None, scen_url=None):
        
        if scen_tags:
            if type(scen_tags) == type({}):
                scen_tags_data = scen_tags
            elif type(scen_tags) == type(''):
                scen_tags_data = {'tags':[{'name':scen_tags}]}
            else:
                scen_tags_data = {}
                warnings.warn("Error : Please pass correct data. eg:[{\'name':\"tags name\"}] or "
                              " \"This is tags name\"")
        else:
            scen_tags_data = {}

        scen_name = (scen_name + (scen_url and " |  <a href=%s>QADB URL</a>" %(scen_url) or ''))
        b_sen_map = {'keyword':scen_keyword,
                      'name':scen_name,
                      'steps':scen_step}
        self.step_data = []
        b_sen_map.update(scen_tags_data)
        
        self.scen_data.append(b_sen_map)

    def addFeature(self, feat_name, feat_desc, feat_keyword="Features", feat_elements=[], feat_tags=None):

        if feat_tags:
            if type(feat_tags) == type({}):
                feat_tags_data = feat_tags
            elif type(feat_tags) == type(''):
                feat_tags_data = {'tags':[{'name':feat_tags}]}
            else:
                feat_tags_data = {}
                warnings.warn("Error : Please pass correct data. eg:[{\'name':\"tags name\"}] or "
                              " \"This is tags name\"")
        else:
            feat_tags_data = {}
       
        b_fea_map = {'description':feat_desc,
                      'keyword':feat_keyword,
                      'name':feat_name,
                      'elements':feat_elements,
                      'uri':"%s-%d" %(feat_name, random.randint(10000,999999))}
        
        b_fea_map.update(feat_tags_data)
        
        self.feat_data.append(b_fea_map)
    
    def setEmpty2StepData(self):
        self.step_data = []

    def setEmpty2ScenData(self):
        self.scen_data = []

    def setEmpty2FeatData(self):
        self.feat_data = []
        
    def generateJsonFile(self, file, data=[]):
        feat_data = data or self.feat_data
        json_data = json.dumps(feat_data, sort_keys = True, indent = 4, )
        with open(file, "w+") as f:
            f.truncate()
            f.write(json_data)

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

    def __init__(self, options):
        self.options = options
        self.test_type = self.options.test_type
        self.log_folder = self.options.log_path
        self.submission_folder = self.options.submission_path
        self.output = self.options.output

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


    def getTestCaseInfo(self, file_name):
        if not os.path.exists(file_name):
            tc_reason = 'Can not found file %s' %file_name
            return self.combineTCData(tc_name=os.path.basename(file_name),
                                      tc_status=CollectData.CASE_STATUS['FAIL'],
                                      tc_duration=0, tc_output=tc_reason)
        else:
            tc_info_list = []
            pattern = re.compile(r"(\[\s*\d+/\d+\]\s+\S+).*(passed|failed|skipped|timeout).*\((\S*)\)", re.DOTALL | re.IGNORECASE | re.MULTILINE)
            with open(file_name, 'r') as f:
                with contextlib.closing(mmap.mmap(f.fileno(), 0,
                                      access=mmap.ACCESS_READ)) as m:
                    line = m.readline()
                    while line:
                        re_s =  pattern.search(line)
                        if re_s:
                            tc = re_s.groups()
                            tc_duration = self._convertTime(tc[2])
                            tc_info_list.extend(self.combineTCData(tc_name=tc[0],
                                                                   tc_status=tc[1].lower(),
                                                                   tc_duration=tc_duration))
                        line = m.readline()
            return tc_info_list


    def getSubmissionUrl(self, file_name, folder='/tmp/submission'):
        submission_file = os.path.join(folder, 'submission-%s.log' %file_name)
        if os.path.exists(submission_file):
            with open(submission_file, 'r') as f:
                file_content = f.read()
                re_s = re.search("ID\s+\d+:\s+(http://\S+submission.php\?submission_id=\d+)", file_content, re.I)
                if re_s:
                    return re_s.groups()[0]
        else:
            return ""
                        
    def getTestSuiteInfo(self, folder='/var/log/qaset/runs/', postfix='screenlog'):

        ts_info = []

        folder = folder
        file_list = glob.glob(os.path.join(folder, '*.%s' %postfix))

        for f in file_list:          
            tc_info = self.getTestCaseInfo(f)
            if tc_info:
                base_name = os.path.basename(f)
                ts_name = '-' in base_name and base_name.split("-")[0] or base_name
                ts_submission_url = self.getSubmissionUrl(file_name=ts_name)
    
                ts_info.extend(self.combineTSData(ts_name=ts_name, ts_tc_list=tc_info, ts_url=ts_submission_url))

        return ts_info

    def getOSversion(self):
        with open('/etc/issue', 'r') as f:
            file_content = f.read()
            re_s = re.search('Welcome to (.*)?- Kernel', file_content, re.I)
            if re_s:
                w_v =  re_s.groups()[0]
                if 'openSUSE' in w_v:
                    return re.search('(openSUSE \d+\.*\d*)', w_v, re.I).groups()[0]
                elif 'SUSE Linux Enterprise Server' in w_v:
                    return re.search('SUSE Linux Enterprise Server (\d+ [SP]*\d*)', w_v).groups()[0]
            else:
                return ""

    def createJsonFile(self, ts_info, folder, test_type='SV', flg='1v1'):

        #scen_data = []
        lastscen_data = []
        # Generate json file for cucumber report
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        json_file = os.path.join(folder, "%s_result.json" %test_type)
        ins_jg = JsonGenerator(json_file)

        for i in ts_info:
            scen_name = i['ts_name']
            scen_step = i['ts_tc_list']
            scen_url = i['ts_url']
            scen_tags = i['ts_tags']
            scen_rate = i['ts_rate']

            for j in scen_step:
                step_name = j['tc_name']
                step_url = j['tc_url']
                step_status = j['tc_status']
                step_duration = j['tc_duration']
                step_desc = j['step_desc']

                if step_status == 'passed':
                    step_err_msg = None
                    step_output = j['tc_output']
                else:
                    step_err_msg = j['tc_output']
                    step_output = None

                ins_jg.addStep(step_keyword="Test case: ", step_name=step_name, step_url=step_url,
                               step_status=step_status, step_duration=step_duration, step_desc=step_desc,
                               step_err_msg=step_err_msg, step_output=step_output)
            #ins_jg.addScenario(scen_name=scen_name, scen_url=scen_url,
            ins_jg.addScenario(scen_name=scen_name, scen_url="", 
                               scen_tags=scen_tags, scen_step=ins_jg.step_data)
            if flg == '1vn':
                pass
            elif flg == '1v1':
                format_str = '[{0}] - [TSuite: {1:<15}] - Arch:{2} for {3}'
                feat_name = format_str.format(test_type,
                                              scen_name,
                                              sys.arch.upper(),
                                              self.getOSversion())
                qadb_url = scen_url and "QADB Line: <a href=%s>QADB URL</a>" %scen_url or ""
                feat_desc = '%s\n\nStatus Rate: %s\n%s' %(CollectData.CASE_DESC[test_type],
                                                          scen_rate, qadb_url)
                ins_jg.addFeature(feat_name=feat_name, 
                                  feat_desc=feat_desc,
                                  feat_elements=ins_jg.scen_data)
                ins_jg.setEmpty2StepData()
                ins_jg.setEmpty2ScenData()

        #scen_data.extend(ins_jg.scen_data)
        if flg == '1vn':
            format_str = '[{0}] - Arch:{1} for {2}'
            feat_name = format_str.format(test_type,
                                          sys.arch.upper(),
                                          self.getOSversion())
                                          #PrjPath().getProductVersion())

            ins_jg.addFeature(feat_name=feat_name, 
                              feat_desc=self.feat_desc, feat_elements=ins_jg.scen_data)
        lastscen_data.extend(ins_jg.feat_data)

        ins_jg.generateJsonFile(json_file, lastscen_data)

    def generateHTML(self, json_folder, output_folder):
        cucmber_generator = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),
                                         'cucumber_generator.jar')
        cmd = 'java -jar %s -n -f %s -o %s' %(cucmber_generator, json_folder, output_folder)
        cucumber_html_path = os.path.join(output_folder, 'cucumber-html-reports')
        os.path.exists(cucumber_html_path) and shutil.rmtree(cucumber_html_path)
        os.system(cmd)
        html_list = glob.glob(os.path.join(cucumber_html_path,'*.html'))
        
        if html_list:
            LOGGER.info("-"*50 + 'HTML report' + "-"*50)
            map(LOGGER.info, html_list)
            LOGGER.info("-"*50 + 'HTML report' + "-"*50)
        else:
            LOGGER.error("No html report is generated")

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
                        dest="test_type", choices=["stress_validation","kernel_regression","user_regression"],
                        help=("Input test type \"stress_validation|kernel_regression|user_regression\"."))

        self.add_option("-l", "--logpath", action="store", type="string",
                        dest="log_path",
                        help=("Input a log path"))
    
        self.add_option("-s", "--submissionpath", action="store", type="string",
                        dest="submission_path",
                        help=("Input a submission path."))

        self.add_option("-o", "--output", action="store", type="string",
                        dest="output",
                        help=("Input path which json and html file will be generated to there"))


        return self

def main():
    ins_parseparam = CMDParamParser().Param()
    options, _args = ins_parseparam.parse_args()
    cd = CollectData(options)
    ts_info = cd.getTestSuiteInfo(options.log_path)
    cd.createJsonFile(ts_info, options.output, test_type=options.test_type, flg='1v1')
    cd.generateHTML(options.output, options.output)

if __name__ == '__main__':
    main()