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
  Description: Execute stree validation test on host machine
"""

from  pylib.constantvars import *
from  pylib import CMDParamParser as ParseParam
from  pylib import StringColor as StringClor
from  pylib import ConnSlave as ConnSlave
from  pylib import QA_TESTSET
from  pylib import HostContorller
#REINSTALL_CMD = '/usr/share/qa/tools/install.pl  -p http://147.2.207.1/dist/install/SLP/SLES-11-SP3-GM/x86_64/DVD1/ -t base -B'

def main():

    start_time = datetime.datetime.now()
    
    ts_result = []
    
    # Instance parameters parse function
    ins_parseparam = ParseParam().parseRegTestParam()
    options, _args = ins_parseparam.parse_args()

    if options.regre_type == 'stress_validation':
        feat_name = 'SV'
        feat_desc = ('Stress Validation Test:\n'
                     'This test is only for Stress validation test, '
                     'the test will execute test cases (fs_stress, process_stress,  sched_stress) on specific arch machine'
                     ' then upload output data, verify and analyze result automatically \n'
                     'Test may be last several hours to finish, Once test pass, '
                     'a mail notification will be send to test owner')

        ts_run = '/usr/share/qa/qaset/run/acceptance-run'
    elif options.regre_type == 'kernel_regression':
        feat_name = 'KR'
        feat_desc = ('Kernel Regression Test:\n'
                     'This test is only for Kernel regression test, '
                     'the test will execute test cases on specific arch machine'
                     ' then upload output data, verify and analyze result automatically \n'
                     'Test may be last several hours to finish, Once test pass, '
                     'a mail notification will be send to test owner')

        ts_run = '/usr/share/qa/qaset/run/kernel-run'
    elif options.regre_type == 'userspace_app':
        feat_name = 'US'
        feat_desc = ('User Space APP Test:\n'
                     'This test is only for user space app test, '
                     'the test will execute test cases () on specific arch machine'
                     ' then upload output data, verify and analyze result automatically \n'
                     'Test may be last several hours to finish, Once test pass, '
                     'a mail notification will be send to test owner')
        ts_run = '/usr/share/qa/qaset/run/regression-run'

    LOGGER.info(StringClor().printColorString("---------Test Start -----------",
                                             StringClor.HIGLIG))
    # Initial environment
    CommonOpt().cleanFile(subfix="pkl")
    CommonOpt().cleanFile(subfix="json")

    #Update available host status
    ins_qaset = QA_TESTSET(options.regre_productv, options.regre_arch, options.regre_mach, options.regre_report, (feat_name, feat_desc))

    if HostContorller().reserveHost(options.regre_mach, HOST_STATUS_FILE, ins_qaset.report_file):
        pass
    else:
        rel_msg = "Host %s is busy now, test exit." %options.regre_mach
        LOGGER.error(rel_msg)
        exec_duration = CommonOpt().getDiffTime(start_time, datetime.datetime.now())
        tc_data = ins_qaset.combineTCData(tc_name='Lock host', tc_status='failed', 
                                 tc_duration=exec_duration, tc_output=rel_msg)
        ts_data = ins_qaset.combineTSData(ts_name="Reserve Host", ts_tc_list=tc_data)
        ts_result.extend(ts_data)
        ins_qaset._exit(ts_result, flg='1vn')

    rl = ins_qaset.sshSlave(try_times=60, interval_time=5)


    rel = ins_qaset.installPackage(qa_repo=options.regre_qarepo)
    LOGGER.info(options.regre_ts)
    rel = ins_qaset.genRTConfig(options.regre_ts)

    rel = ins_qaset.executeTS(ts_run=ts_run, timeout=60)

    ins_qaset.checkFile(ts_run=ts_run, timeout=345600, interval_time=120)

    ts_data = ins_qaset.getTestSuiteInfo()
    ts_result.extend(ts_data)

    
    ins_qaset.executeCMD("mkdir -p /var/log/qaset/bak", title="Create bak folder")
    ins_qaset.executeCMD("cp -r /var/log/qaset/runs /var/log/qaset/bak/runs_`date +\"%Y-%m-%d-%H-%M-%S\"`", title="Backup runs folder")
    ins_qaset.executeCMD("cp -r /var/log/qaset/submission /var/log/qaset/bak/submission_`date +\"%Y-%m-%d-%H-%M-%S\"`", title="Backup runs folder")


    '''
    exec_duration = CommonOpt().getDiffTime(start_time, datetime.datetime.now())
    tc_data = ins_qaset.combineTCData(tc_name='Get os version', tc_status='passed', 
                                 tc_duration=exec_duration, tc_output=rel[1])
    ts_data = ins_qaset.combineTSData(ts_name="OS version", ts_tc_list=tc_data)

    #ins_qaset.rebootSlave()
    '''
    ins_qaset._exit(ts_result, flg='1v1')

if __name__ == '__main__':
    LOGGER.info("------------START---------------")
    main()
