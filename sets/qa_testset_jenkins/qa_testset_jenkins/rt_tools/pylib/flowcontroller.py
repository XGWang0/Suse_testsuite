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

import re
import fcntl

from constantvars import *
from conslaves import ConnSlave


class HostContorller(object):

    HOST_READY = 'READY'
    HOST_FREE = 'FREE'
    HOST_RUNNING = 'RUNNING'
    HOST_RUNNING_RH = 'RUNNING RH'
    HOST_RUNNING_SK = 'RUNNING SK'
    HOST_RUNNING_SV = 'RUNNING SV'
    HOST_RUNNING_US = 'RUNNING US'

    def __init__(self):
        pass

    def reserveFile(self, fp, timeout=100):
        curr_time = time.time()
        while time.time() - curr_time < 100:
            try:
                fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
                LOGGER.debug("Successfully lock usable host config file")
                return True
            except IOError, e:
                LOGGER.warn(e)
                continue
        
        LOGGER.error("Failed to get file lock of file %s" %fp.filename)
        return False
    
    def releaseFile(self, fp):
        try:
            fcntl.flock(fp, fcntl.LOCK_UN)
            LOGGER.debug("Successfully unlock usable host config file")
            return True
        except Exception,e:
            print e
            LOGGER.debug("Failed to unlock usable host config file")
            return False

    #TODO Maybe exist blocking issue
    def getAvailableHost(self, host, host_status_file,
                       org_status=HOST_FREE, cur_status=HOST_READY):

        acquired_host_flag = False
        
        avaliable_host = ""

        try:
            fp = open(host_status_file, "a+")
        except IOError,e:
            LOGGER.debug("Failed to open file because of %s" %e)
            return ""

        if self.reserveFile(fp) is False:
            return ""
        fp.seek(0)
        lines = fp.readlines()
        LOGGER.debug('Host is %s' %host)
        LOGGER.debug('org_status is  %s' %org_status)
        for i, line in enumerate(lines):
            if host in line:
                LOGGER.debug("Host status : %s" %line)      
                if re.search("%s\s+%s" %(host,org_status), line, re.I):
                    LOGGER.debug("Get available host")
                    lines[i] = "%s %s\n" %(host, cur_status)
                    acquired_host_flag = True
                    avaliable_host = host
                    break
                else:
                    LOGGER.debug("Host is busy")
                    acquired_host_flag= False
                    avaliable_host = ""
                    break
            else:
                pass
        else:
            acquired_host_flag = True
            avaliable_host = host
            lines.append("%s %s\n" %(host, cur_status))

        if acquired_host_flag is True:
            self.modifyHostStatus(fp, lines)

        self.releaseFile(fp)
        fp.close()
        
        return avaliable_host

    def modifyHostStatus(self, fp, file_lines):
        
        #LOGGER.info(("ALL LINES is ", file_lines))
        fp.seek(0)
        fp.truncate()
        fp.writelines(file_lines)

    def chooseHost(self, host_list, host_status_file, uuid_seed_file, chkssh=False):

        reserve_uuid = CommonOpt.generateUUID(uuid_seed_file)
        for host in host_list:
            tmp_aval_host = ''

            avail_host = self.getAvailableHost(host.strip(), host_status_file,
                                               HostContorller.HOST_FREE + ' ' + reserve_uuid,
                                               HostContorller.HOST_FREE + ' ' + reserve_uuid)
            
            if avail_host:
                LOGGER.info("Get available host %s" %avail_host)
                tmp_aval_host = avail_host
            else:
                avail_host = self.getAvailableHost(host.strip(), host_status_file,
                                                   HostContorller.HOST_FREE + ' ALL',
                                                   HostContorller.HOST_FREE + ' ' + reserve_uuid)
                if avail_host:
                    tmp_aval_host =  avail_host
            
            if tmp_aval_host:
                if chkssh is False:
                    return tmp_aval_host
                else:
                    conslave = ConnSlave(host,
                                         REINSTALL_MACHINE_USER,
                                         REINSTALL_MACHINE_PASSWD)
                    if conslave.sshSlave(try_times=5, interval_time=5) is True:
                        return tmp_aval_host
                    else:
                        self.getAvailableHost(host.strip(), host_status_file,
                                              HostContorller.HOST_FREE,
                                              HostContorller.HOST_FREE + ' ALL')
                        conslave.closeSSH()
        LOGGER.warn("There is no any available host")
        return ""     

    def freeHost(self, host, host_status_file, uuid_seed_file):
        LOGGER.info("Free host %s" %host)
        reserve_uuid = CommonOpt.generateUUID(uuid_seed_file)
        fh = self.getAvailableHost(host, host_status_file,
                                   HostContorller.HOST_RUNNING + ' ' + reserve_uuid, 
                                   HostContorller.HOST_FREE + ' ALL')
        
        if fh:
            return fh
        else:
            return ""

    def reserveHost(self, host, host_status_file, uuid_seed_file):
        LOGGER.info("Reserve host %s" %host)
        reserve_uuid = CommonOpt.generateUUID(uuid_seed_file)
        fh = self.getAvailableHost(host, host_status_file,
                                   HostContorller.HOST_FREE + ' ' + reserve_uuid,
                                   HostContorller.HOST_RUNNING + ' ' + reserve_uuid)
        
        if fh:
            return fh
        else:
            fh = self.getAvailableHost(host, host_status_file,
                                       HostContorller.HOST_FREE + ' ALL',
                                       HostContorller.HOST_RUNNING + ' ' + reserve_uuid)
            if fh:
                return fh
            else:
                return ""
    
    def releaseHost(self,host, host_status_file, uuid_seed_file):
        LOGGER.info("Release host %s" %host)
        reserve_uuid = CommonOpt.generateUUID(uuid_seed_file)
        fh = self.getAvailableHost(host, host_status_file,
                                   HostContorller.HOST_RUNNING + ' ' + reserve_uuid,
                                   HostContorller.HOST_FREE + ' ' + reserve_uuid)
        
        if fh:
            return fh
        else:
            return ""
        