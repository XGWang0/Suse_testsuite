from urllib2 import urlopen, HTTPError
import json
import re

from constantvars import *
from stringcolor import StringColor
from  urloperation import URLParser

class JenkinsAPI(object):
    
    def __init__(self):
        self.jenkins_url = ''

    def getJobsData(self, url):
        url = 'http://147.2.207.67:8080/job/REGRESSIONTEST/job/SLES-11-SP4/job/x86_64/'
        url = os.path.join(url, 'api', 'json?pretty=true', '&tree=jobs[name,color]')
        
        jobs_list = []
        
        try:
            req = urlopen(url)
            res = req.read()
            data = json.loads(res)
            
            return data['jobs']

        except HTTPError, e:
            LOGGER.warn(StringColor().printColorString(
                                    "Failed to access website ,cause [%s]" %e,
                                    StringColor.F_RED))
            return []
    
    def getJobStatus(self, url, job_name):
        jobs_data = self.getJobsData(url)
        
        for job in jobs_data:
            if job['name'] == job_name:
                if job['color'] == 'blue':
                    return 'pending'
                elif job['color'] == 'blue':
                    pass

    
    @staticmethod
    def checkBuildable(url):
        #url = 'http://127.0.0.1:8080/job/test'
        url = os.path.join(url, 'api', 'json?pretty=true', '&tree=buildable')
        job_status = ""
        
        if URLParser().checkURLPath(url):
            req = urlopen(url)
            data = json.loads(req.read())
            if 'buildable' in data:
                job_status = data['buildable']
            else:
                job_status =  False
        LOGGER.info("Job %s is %s" %(url, job_status) )
        return job_status

    @staticmethod
    def checkDownStreamProject(url):
        #url = 'http://127.0.0.1:8080/job/test'
        url = os.path.join(url, 'api', 'json?pretty=true', '&tree=downstreamProjects[name,url,color]')
        downstream_prj = ""
        
        if URLParser().checkURLPath(url):
            req = urlopen(url)
            data = json.loads(req.read())
            down_stream_data =  data['downstreamProjects']
            if down_stream_data:
                if down_stream_data[0]["color"] == "disabled":
                    downstream_prj = False
                else:
                    downstream_prj = True
            else:
                downstream_prj =  False
        LOGGER.info("Job %s is %s" %(url, downstream_prj) )
        return downstream_prj

    @staticmethod
    def checkCauseType(url):
        #url = 'http://127.0.0.1:8080/job/test'
        url = os.path.join(url, 'api', 'json?pretty=true', '&tree=actions[causes[shortDescription]]')

        if URLParser().checkURLPath(url):
            req = urlopen(url)
            data = json.loads(req.read())
            
            for act1 in data['actions']:
                if 'causes' in act1:
                    for cau1 in act1['causes']:
                        if 'shortDescription' in cau1:
                            if re.search('Started by upstream project', cau1['shortDescription'], re.I):
                                return True
    
            return False
        else:
            LOGGER.warn("url %s is invalid" %url)
            return False

    '''
    def chkCurrBuildCause(self):
        build_api_json = PrjPath().getBuildURL() + '/api/json'
        
        try:
            req = urlopen(build_api_json)
            res = req.read()
            data = json.loads(res)
            
            for act in data['actions']:
                if 'causes' in act:
                    for cau in act['causes']:
                        if 'shortDescription' in cau:
                            if re.search('Started by user', cau['shortDescription'], re.I):
                                return True
                            else:
                                return False
        except HTTPError, e:
            LOGGER.warn(StringColor().printColorString(
                                    "Failed to access website ,cause [%s]" %e,
                                    StringColor.F_RED))
            return False
        return False
    '''


if __name__ == '__main__':
    api = JenkinsAPI()
    
    print api.checkCauseType('http://127.0.0.1:8080/job/group/job/t4/7/')