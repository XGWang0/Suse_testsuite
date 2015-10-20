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

import pexpect
import datetime
import re
import random
import time
import os

from constantvars import *
from stringcolor import StringColor

class ConnSlave(object):

    def __init__(self, slave_addr, slave_name, slave_passwd):
        self.slave_addr = slave_addr
        self.slave_name = slave_name
        self.slave_passwd = slave_passwd
        self.color_ins = StringColor()
        
        self.prompt = "#" + ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',10)) + "#"

        self.ssh = None
    
    def sshSlave(self, timeout=30, try_times=3, interval_time=600):

        cmd_sshslave = "ssh -o ConnectTimeout=%s %s@%s" %(timeout,
                                                       self.slave_name,
                                                       self.slave_addr)
        LOGGER.info(cmd_sshslave)
        timeout_times = 1
        incorrect_passwd_time = 1
        respawn_flag = False
        ssh_newkey = 'Are you sure you want to continue connecting'

        self.ssh = pexpect.spawn(cmd_sshslave, timeout=timeout)
        while try_times > 0:
            try:
                i = self.ssh.expect([pexpect.EOF, pexpect.TIMEOUT,
                                  ssh_newkey, '[Pp]assword: ', 'Last login:.*', 'Host key verification failed'],)
    
                if i == 0:
                    LOGGER.info(self.color_ins.printColorString(self.ssh.before, StringColor.F_YEL))
                    respawn_flag = True
                    try_times = try_times - 1

                    output_str = "Connection refused, delay %ds, try it again ..." %interval_time
                    LOGGER.info(self.color_ins.printColorString(output_str, StringColor.F_YEL))
                elif i == 1:
                    respawn_flag = True
                    timeout_times = timeout_times + 1
                    try_times = try_times - 1

                    output_str = "Connect slave timeout, delay %s  try it again ..." %interval_time
                    LOGGER.info(self.color_ins.printColorString(output_str, StringColor.F_YEL))
                    LOGGER.info(self.color_ins.printColorString(self.ssh.before, StringColor.F_YEL))
                elif i == 2:
                    self.ssh.sendline("yes")
                    continue
                elif i == 3:
                    self.ssh.sendline(self.slave_passwd)
                    try_times = try_times - 1
                    incorrect_passwd_time = incorrect_passwd_time + 1

                    output_str = "Send password"
                    LOGGER.info(self.color_ins.printColorString(output_str, StringColor.F_BLU))
                    if incorrect_passwd_time > 3:
                        output_str = "Incorrect password [%s] to ssh" %self.slave_passwd
                        LOGGER.error(self.color_ins.printColorString(output_str, StringColor.F_RED))
                        return False
                    else:
                        continue
                elif i == 4:
                    output_str = "Successful connect to slave [%s]" %self.slave_addr
                    LOGGER.info(self.color_ins.printColorString(output_str, StringColor.F_GRE))
                    break

                elif i == 5:
                    os.system('sed -i "/%s/d" /var/lib/jenkins/.ssh/known_hosts' %self.slave_addr)
                    LOGGER.info(os.system('id'))
                    respawn_flag = True
                    try_times = try_times - 1
                    

            except pexpect.ExceptionPexpect as e:
                LOGGER.info(self.color_ins.printColorString(e, StringColor.F_BLU))
                LOGGER.error(self.color_ins.printColorString("SSH failed on login.", StringColor.F_RED))
                return False

            if try_times == 0:
                LOGGER.error(self.color_ins.printColorString("SSH Connection Operation TIMEOUT.",
                                                             StringColor.F_RED))
                return False

            time.sleep(interval_time)

            if  respawn_flag:
                self.closeSSH()
                self.ssh = pexpect.spawn(cmd_sshslave, timeout=timeout)

        self.ssh.sendline("PS1=%s" %self.prompt)
        self.ssh.expect(["%s.+%s" % (self.prompt, self.prompt)], timeout=100)

        return True


    def scpFiles2(self, org_files, desc_files):
        
        expectations = ['[Pp]assword',
                        'continue (yes/no)?',
                        pexpect.EOF,
                        pexpect.TIMEOUT,
                        'Name or service not known',
                        'Permission denied',
                        'No such file or directory',
                        'No route to host',
                        'Network is unreachable',
                        'failure in name resolution',
                        'No space left on device'
                        ]

        try:
            child = pexpect.spawn( 'scp -r %(orgfolder)s %(user)s@%(passwd)s:%(destfolder)s'%dict(orgfolder=org_files,
                                                                                                  user=self.slave_name,
                                                                                                  passwd=self.slave_addr,
                                                                                                  destfolder=desc_files))
            res = child.expect( expectations )
            print "Child Exit Status :",child.exitstatus
            print  res,"::",child.before," :After:",child.after
            if res == 0:
                child.sendline(self.slave_passwd)
                return self.scpFiles2(org_files, desc_files, try_times=3, timeout=5)
            if res == 1:
                child.sendline('yes')
                return self.scpFiles2(org_files, desc_files, try_times=3, timeout=5)
            if res == 2:
                line = child.before
                print "Line:",line
                print "Now check the result and return status."
            if res == 3:
                print "TIMEOUT Occurred."
                child.kill(0)
                return False
            if res >= 4:
                child.kill(0)
                print "ERROR:",expectations[res]
                return False
            return True
        except:
            import traceback; traceback.print_exc()
            print "Did file finish?",child.exitstatus

    def closeSSH(self):
        if self.ssh.isalive():
            self.ssh.close(force=True)

    def getSSHHandler(self):
        return self.ssh

    def getResultFromCMD(self, cmd, priority='P', w_timeout=100, s_timeout=10,
                         handlespecialchar=False, chk_reltime=True ):
        '''(1, msg) : get expected result
           (3, msg) : get unexpected result
           (5, msg) : whole operation timeout
           (0, msg) : ssh handler is not alive 
        '''
        rlt = ()
        for i in range(3):
            if rlt:
                if rlt[0] == 0:
                    if self.sshSlave() is True:
                        rlt=()
                    else:
                        continue
                else:
                    break
            else:
                pass

            if self.ssh.isalive():
                self.ssh.setwinsize(65535, 200)
                self.ssh.sendline(cmd)
        
                LOGGER.info(self.color_ins.printColorString("Execute cmd :%s"%cmd,
                                                            StringColor.F_BLU))
                rel = ""
                start_time = time.time()
                try:
                    while time.time() - start_time < w_timeout:
                        #TODO: SSH Connection is broken , maybe cause some issues
                        rel = rel + self.ssh.read_nonblocking(1, timeout=s_timeout)
                        if chk_reltime is True:
                            if re.search(r'%s\s*(.*)%s' %(re.escape(cmd), self.prompt), rel, re.S|re.I):
                                break
                except pexpect.TIMEOUT as e:
                    LOGGER.warn(self.color_ins.printColorString("Read 1 character from console timeout:%d" % s_timeout,
                                                                StringColor.F_YEL))
                    time.sleep(30)
                    if i == 1:
                        LOGGER.warn(self.color_ins.printColorString("Failed to get console info, reconnect slave",
                                                                    StringColor.F_YEL))
                        self.closeSSH()
                        ret = (0, "Reconnect slave")
                        continue
    
                except pexpect.EOF as e1:
                    LOGGER.warn(self.color_ins.printColorString(e1,
                                                                 StringColor.F_RED))
                    rlt =  (0, "Connection is broken")
    
                finally:
                    if rlt:
                        pass
                    else:
                        re_ins = re.search(r'%s\s*(.*)%s' %(re.escape(cmd), self.prompt), rel, re.S|re.I)
                        if re_ins:
                            rlt =  (1, re_ins.groups()[0].strip())
                        else:
                            rlt = (3, rel)
            else:
                LOGGER.warn(self.color_ins.printColorString("Lost connection with slave",
                                                            StringColor.F_RED))
                rlt = (0, "SSH handler is not alive")
        
        return rlt

    def getReturnCode(self, cmd=r"echo $?", times=3):
        #TODO: 1.loop may be not necessary
        for i in range(times):
            rel = self.getResultFromCMD(cmd, w_timeout=100, s_timeout=60)
            if rel[0] == 1:
                if rel[1] == "0":
                    return (True, rel[1])
                else:
                    LOGGER.info(self.color_ins.printColorString("rel = [%s]" %rel[1], 
                                                                StringColor.F_BLU))
                    return (False, rel[1])
            elif rel[0] == "1":
                LOGGER.error(self.color_ins.printColorString("rel = [%s]" %rel[1], 
                                                            StringColor.F_BLU))
                return (None, 'Lost connection')
            else:
                continue
        LOGGER.warn(self.color_ins.printColorString("Failed to get return code! rel = [%s]" %rel[1], 
                                                     StringColor.F_RED))

        return ('', 'Failed to get return code')
        
if __name__ == '__main__':

    cs = ConnSlave("147.2.207.54", "root", "susetesting")
    
    cs.scpFiles2('/tmp/test', '/tmp/')
    
    '''
    if cs.sshSlave(interval_time=10,try_times=30):
        rel = cs.getResultFromCMD("/tmp/test.sh")
        print rel
        cs.closeSSH()
    '''