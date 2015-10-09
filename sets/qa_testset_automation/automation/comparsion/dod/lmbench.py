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


PROCESSOR_T = ['Mhz','null call','null I/O','stat','open clos','slct TCP','sig inst','sig hndl','fork proc','exec proc','sh proc']
INTEGER_T = ['intgr bit','intgr add','intgr mul','intgr div','intgr mod']
UINT64_T = ['int64 bit','int64 add','int64 mul','int64 div','int64 mod']
FLOAT_T = ['float add','float mul','float div','float mod']
DOUBLE_T = ['double add','double mul','double div','double mod']
CTXSW_T = ['2p/0K ctxsw','2p/16K ctxsw','2p/64K ctxsw','8p/16K ctxsw','8p/64K ctxsw','16p/16K ctxsw','16p/64K ctxsw']
LOCAL_L = ['LOCAL_2p/0K ctxsw','Pipe','AF UNIX','UDP','RPC/UDP','TCP','RPC/TCP','TCP conn']
REMOTE_L = ['REMOTE_UDP', 'REMOTE_RPC/UDP','REMOTE_TCP','REMOTE_RPC/TCP','REMOTE_TCP conn']
FILE_VM_L = ['0K File Create','0K File Delete','10K File Create','10K File Delete','Mmap Latency','Prot Fault','Page Fault','100fd selct']
LOCAL_B = ['Pipe','AF UNIX','TCP ','File reread','Mmap reread','Bcopy (libc)','Bcopy (hand)','Mem read','Mem write']
MEMORY_L = ['L1$','L2$','Rand mem','Rand mem']

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
                print(line)
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
        print(conf)
        print(value)
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
