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
  Description: Reintall host machine by hamsta cmd
"""

from  pylib.constantvars import *
from  pylib import CMDParamParser as ParseParam
from  pylib import StringColor as StringClor
from  pylib import ConnSlave as ConnSlave
from  pylib import QA_TESTSET
from  pylib import HostContorller


#REINSTALL_CMD = '/usr/share/qa/tools/install.pl  -p http://147.2.207.1/dist/install/SLP/SLES-11-SP3-GM/x86_64/DVD1/ -t base -B'

def main():

    ts_data_list = []
    feat_name = 'RH'
    feat_desc = ('Re-installation Host:\n'
                 'This test is only for reinstalling host, '
                 'the test will verify if the product can be installed on specific arch machine successfully\n'
                 'The project uses install.pl tool to remotely install OS on host thru ssh connection.\n'
                 'Test may be last 20 minutes to finish, Once installation pass, '
                 'a mail notification will be send to test owner')

    LOGGER.info(StringClor().printColorString("---------Reinstall Host Start -----------",
                                              StringClor.HIGLIG))
    start_time = datetime.datetime.now()
    # Instance parameters parse function
    ins_parseparam = ParseParam().parseReInstParam()
    options, _args = ins_parseparam.parse_args()

    # Initial environment
    CommonOpt().cleanFile(subfix="pkl")
    CommonOpt().cleanFile(subfix="json")
    
    ins_qaset = QA_TESTSET(options.rinst_productv, options.rinst_arch,
                           options.rinst_mach,options.rinst_report, (feat_name, feat_desc))

    ins_qaset.getRepoLocation(options.rinst_project)
    #Update available host status
    if HostContorller().reserveHost(options.rinst_mach, HOST_STATUS_FILE, ins_qaset.report_file):
        pass
    else:
        rel_msg = "Host %s is busy now, test exit." %options.rinst_mach
        LOGGER.error(rel_msg)
        exec_duration = CommonOpt().getDiffTime(start_time, datetime.datetime.now())
        tc_data = ins_qaset.combineTCData(tc_name='Lock host', tc_status='failed', 
                                 tc_duration=exec_duration, tc_output=rel_msg)
        ts_data = ins_qaset.combineTSData(ts_name="Reserve Host", ts_tc_list=tc_data)
        ts_data_list.extend(ts_data)
        ins_qaset._exit(ts_data_list, flg='1vn')

    ts_data_list.extend(ins_qaset.sshSlave())

    ts_data_list.extend(ins_qaset.installRITools())

    ts_data_list.extend(ins_qaset.installSlave(repo=options.rinst_repo, s_timeout=600))

    rel = ins_qaset.rebootSlave()
    rel = ins_qaset.sshSlave(try_times=120, interval_time=60)

    rel = ins_qaset.executeCMD("uname -a")

    rel = ins_qaset.executeCMD("cat /etc/issue")

    exec_duration = CommonOpt().getDiffTime(start_time, datetime.datetime.now())
    tc_data = ins_qaset.combineTCData(tc_name='Get os version', tc_status='passed', 
                                 tc_duration=exec_duration, tc_output=rel[1])
    ts_data = ins_qaset.combineTSData(ts_name="OS version", ts_tc_list=tc_data)
    ts_data_list.extend(ts_data)

    ins_qaset._exit(ts_data_list, flg='1vn')

if __name__ == '__main__':
    main()
