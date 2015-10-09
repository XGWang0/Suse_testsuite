#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pprint
import logging
import parserManager
PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)


PROCESSOR_T = ['Mhz','null_call','null_I/O','stat','open_clos','slct_TCP','sig_inst','sig_hndl','fork_proc','exec_proc','sh_proc']
INTEGER_T = ['intgr_bit','intgr_add','intgr_mul','intgr_div','intgr_mod']
UINT64_T = ['int64_bit','int64_add','int64_mul','int64_div','int64_mod']
FLOAT_T = ['float_add','float_mul','float_div','float_mod']
DOUBLE_T = ['double_add','double_mul','double_div','double_mod']
CTXSW_T = ['2p/0K_ctxsw','2p/16K_ctxsw','2p/64K_ctxsw','8p/16K_ctxsw','8p/64K_ctxsw','16p/16K_ctxsw','16p/64K_ctxsw']
LOCAL_L = ['LOCAL_2p/0K_ctxsw','Pipe','AF_UNIX','UDP','RPC/UDP','TCP','RPC/TCP','TCP_conn']
REMOTE_L = ['REMOTE_UDP','REMOTE_RPC/UDP','REMOTE_TCP','REMOTE_RPC/TCP','REMOTE_TCP_conn']
FILE_VM_L = ['0K_File_Create','0K_File_Delete','10K_File_Create','10K_File_Delete','Mmap_Latency','Prot_Fault','Page_Fault','100fd_selct']
LOCAL_B = ['Pipe','AF_UNIX','TCP','File_reread','Mmap_reread','Bcopy_(libc)','Bcopy_(hand)','Mem_read','Mem_write']
MEMORY_L = ['L1$','L2$','Rand_mem','Rand_mem']

class DODLmbench(DODLog):
    def __init__(self, stream):
        super(DODLmbench, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'
        self._dod = DictOfDict()

    def parser(self):
        for line in self.stream:
            vmatch = re.search(r'(\s*\d*\.?\d*\|){4}',line)
            if re.match(r'Processor',line):
                while not vmatch:
                    line =next(self.stream)
                    vmatch = re.search(r'(\s*\d*\.?\d*\|){4}',line)
                self.getvalue(PROCESSOR_T,line)
            elif re.search(r'Context\s*switch',line):
                while not vmatch:
                    line =next(self.stream)
                    vmatch = re.search(r'(\s*\d*\.?\d*\|){4}',line)
                self.getvalue(CTXSW_T,line)
            elif re.match(r'File & VM system',line):
                while not vmatch:
                    line =next(self.stream)
                    vmatch = re.search(r'(\s*\d*\.?\d*\|){4}',line)
                self.getvalue(FILE_VM_L,line)
            elif re.match(r'\*Local\*\s*Communication\s*latencies',line):
                while not vmatch:
                    line =next(self.stream)
                    vmatch = re.search(r'(\s*\d*\.?\d*\|){4}',line)
                self.getvalue(LOCAL_L,line)
            elif re.match(r'Memory latencies',line):
                while not vmatch:
                    line =next(self.stream)
                    vmatch = re.search(r'(\s*\d*\.?\d*\|){3}',line)
                self.getvalue(MEMORY_L,line)
            else:
                pass

    def getvalue(self,conf,line):
        value = []
        value = (''.join(line.strip().split()[3:])).split('|')
        for i in range(len(value)-1):
            if value[i].find('K'):
               value[i]=value[i].replace('K','')
        if len(conf) ==len(value):
            for i in range(len(value)-1):
                if not value[i]:
                    self._dod[conf[i]]=0.1
                else:
                    self._dod[conf[i]]=float(value[i])


    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()

class DODLmbenchBand(DODLog):
    def __init__(self, stream):
        super(DODLmbenchBand, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 'b'

    def parser(self):
        for line in self.stream:
            vmatch = re.search(r'(\d*\.?\d*\|){4}',line)
            if re.match(r'\*Local\* Communication bandwidths',line):
                while not vmatch:
                    line =next(self.stream)
                    vmatch = re.search(r'(\d*\.?\d*\|){4}',line)
                else:
                    self.getvalue(LOCAL_B,line)
                    break

    def getvalue(self,conf,line):
        value = []
        value = (''.join(line.strip().split()[3:])).split('|')
        if len(conf) ==len(value):
            for i in range(len(value)-1):
                if not value[i]:
                    self._dod[conf[i]]=0.1
                else:
                    self._dod[conf[i]]=float(value[i])

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()

parserManager.add_parser("sample","lmbench","lmbench",DODLmbench)

#parserManager.add_parser("sample","lmbench","lmbench",DODLmbenchBand)
