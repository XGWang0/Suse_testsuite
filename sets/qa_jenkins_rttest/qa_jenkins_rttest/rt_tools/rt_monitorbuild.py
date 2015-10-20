#!/usr/bin/python
"""
****************************************************************************
Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.

THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
LIABILITY.

SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
****************************************************************************

Tool Brief:
  Description: This script is used to monitor repo change and trigger remote jenkins job to do test
"""
from  pylib.constantvars import *
from  pylib import StringColor as StringClor
from  pylib import CMDParamParser as ParseParam
from  pylib import RegConfigParser as ParseConfig
from  pylib import URLParser, HostContorller
from  pylib import JenkinsAPI

class RTBuildChange(object):
    def __init__(self, options):
        
        pc = ParseConfig()
        
        # Get project project name, host list, archs repo and so on
        self.prj_name = options.mbuild_prj.upper()
        self.hosts = pc.convertItem(pc.getItem(RT_REF_TEST_CFG_FILE, self.prj_name, 'host'))

        self.lrepo = options.mbuild_lrepo
        self.larch = pc.convertItem(pc.getItem(RT_REF_TEST_CFG_FILE, self.prj_name, 'larch'))

        self.rrepo = options.mbuild_mrepo
        self.rarch = pc.convertItem(pc.getItem(RT_REF_TEST_CFG_FILE, self.prj_name, 'rarch'))

        # Get folder contains all relevant files
        self.prj_cfg_path = RT_PRJ_CONFIG_PATH

        self.repo_store_path = PrjPath().createFolder(
                                os.path.join(self.prj_cfg_path, 'rt_repo', self.prj_name))
        self.host_status_file = HOST_STATUS_FILE
        self.rdy_tirgger_job_file = os.path.join(self.prj_cfg_path, RT_RDY_TRIGGER_JOB_FILE)

        self.jenkins_job = "curl -X POST --user admin:susetesting \"" + os.path.dirname(PrjPath().getJobURL()[:-1])  + "/%(arch)s/buildWithParameters?ARCH=%(arch)s&BUILD_VER=%(build_ver)s&REPORT_FILE=%(report_file)s&MACHINE="

        
        self.triggered_arch = ""
        self.return_code = 1
        
        # Instance for url operation and host controller
        self.urlpaser = URLParser()
        self.flowctrller = HostContorller()

        LOGGER.info("Initial")

        self.loopCheckBuildChange(self.larch)
        self.loopCheckBuildChange(self.rarch)

    def loopCheckBuildChange(self, arch_list):
        '''Traverse needed arches and mode for build change
        '''
        repo = arch_list == self.larch and self.lrepo or self.rrepo

        for arch in arch_list:
            LOGGER.info("Current arch is  %s" %(arch))
            
            # Get build change information
            bc = self.getBuildChange(repo, arch)
            LOGGER.info(bc)

            if bc[2] == "":
                LOGGER.warn("Can not get build infomation, skip !!")
                continue
            build_version = bc[2]
            for arch in [i for i in arch_list if i in self.hosts]:
                trigger_job_cmd = ''

                # Get stored data from local file
                cmd_triggerjob_map = CommonOpt().loadData(self.rdy_tirgger_job_file) or {}

                # Check jenkins job if is enable
                key_name_tirgger_job = '%s_%s' %(self.prj_name, arch)
                # If build change is existent, followint operation will be done
                if bc[0] is True:
                    report_file = CommonOpt.generateRandomStr()
                    trigger_job_cmd = self.jenkins_job %dict(arch=arch,
                                                             build_ver=build_version,
                                                             report_file=report_file)
                    LOGGER.info("BC:Detect build change")

                # BUild change is non-existent
                elif bc[0] is False:
                    if key_name_tirgger_job in cmd_triggerjob_map and cmd_triggerjob_map[key_name_tirgger_job]:
                        trigger_job_cmd = cmd_triggerjob_map[key_name_tirgger_job]
                        LOGGER.info(StringClor().printColorString(
                                    "No build change, Try to tirgger last build change with job cmd : %s" %trigger_job_cmd,
                                    StringClor.F_GRE))

                        cmd_triggerjob_map[key_name_tirgger_job]=""
                        CommonOpt().dumpData(self.rdy_tirgger_job_file, cmd_triggerjob_map)
                    else:
                        LOGGER.info(StringClor().printColorString(
                                    "No build change or last build change needs to be triggered",
                                    StringClor.F_GRE))

                self.triggerJob(arch, trigger_job_cmd, key_name_tirgger_job, cmd_triggerjob_map)
                LOGGER.info("-"*50)

    def getBuildChange(self, repo, arch):
        url = os.path.join(repo, arch, 'dvd1/media.1/build')
        abs_last_file = os.path.join(self.repo_store_path, "last_repo_file_on_%s" %arch)
        return self.checkBuildChange(abs_last_file, url)

    def triggerJob(self, arch, cmd, cmd_key, cmd_map):
        if cmd:
            report_file = re.search('REPORT_FILE=(\S+)&', cmd, re.I).groups()[0]
            
            fh = self.flowctrller.chooseHost(self.hosts[arch], self.host_status_file, report_file, chkssh=True)

            if fh:   
                self.return_code = 0
                cmd = cmd + fh + "\""
                LOGGER.debug("Trigger job %s" %cmd)

                # Remove old build change info from trigger job file
                cmd_map[cmd_key]=""
                os.system(cmd)
            else:
                LOGGER.info("NO available host %s for triggering, dump data to file" %str(self.hosts[arch]))
                cmd_map[cmd_key]=cmd
            CommonOpt().dumpData(self.rdy_tirgger_job_file, cmd_map)
        else:
            LOGGER.info("No trigger build")


    def checkBuildChange(self, last_file, url):

        last_content = CommonOpt().loadData(last_file)
        curr_content = self.urlpaser.getFileContent(url).strip()

        if ''.join(curr_content.strip()) == "":
            return (False, last_content, "")
        else:
            if ''.join(last_content).strip() == curr_content.strip():
                return (False, last_content, curr_content)
            else:
                LOGGER.info("Save newest build info to last repo file")
                CommonOpt().dumpData(last_file, curr_content)
                return (True, last_content, curr_content)


def main():

    # Get parameters from cmd
    ins_parseparam = ParseParam().parseMonitorParam()
    options, _args = ins_parseparam.parse_args()
    
    # Get config file of kotd project
    if os.path.exists(RT_REF_TEST_CFG_FILE):
        rtbc = RTBuildChange(options)
        sys.exit(rtbc.return_code)
    else:
        LOGGER.error("Config file does not exist.")
        sys.exit(-1)


if __name__ == '__main__':
    main()

