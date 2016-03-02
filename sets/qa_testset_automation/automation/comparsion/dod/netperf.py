#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import parserManager
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

class DODNetperf(DODLog):
    def __init__(self, stream):
        super(DODNetperf, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 'b'

    def parser(self):
        if self.ST == PST_NULL:
            for line in self.stream:
                vmatch = re.match(r'Size\s*Size\s*Size\s*Time\s*Throughput ',line)
                if vmatch:
                    line =next(self.stream)
                    line =next(self.stream)
                    line =next(self.stream)
                    sendt =line.strip().split()
                    self._dod['TCP']['Throughput']= float(sendt[4])
                tmatch = re.match(r'Size\s*Size\s*Time\s*Okay\s*Errors\s*Throughput',line)
                if tmatch:
                    line =next(self.stream)
                    line =next(self.stream)
                    line =next(self.stream)
                    uset = line.strip().split()
                    line =next(self.stream)
                    ret = line.strip().split()
                    self._dod['UDP']['Send_Throughput']= float(uset[5])
                    self._dod['UDP']['Recieve_Throughput']= float(ret[3])
                    break
                else:
                    pass

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()

tl= ['netperf-peer-loop','netperf-peer-loop6']
ll=['netperf-loop-udp','netperf-loop-tcp']

for i in tl:
    for j in ll:
        parserManager.add_parser("sample",i,j,DODNetperf)

fl=['netperf-peer-fiber','netperf-peer-fiber6']

parserManager.add_parser("sample",'netperf-peer-fiber','netperf-fiber-tcp',DODNetperf)

parserManager.add_parser("sample",'netperf-peer-fiber','netperf-fiber-udp',DODNetperf)

parserManager.add_parser("sample",'netperf-peer-fiber6','netperf-fiber-udp6',DODNetperf)

parserManager.add_parser("sample",'netperf-peer-fiber6','netperf-fiber-tcp6',DODNetperf)

for i in ['netperf-peer-loop-tcp','netperf-peer-loop6-tcp']:
    parserManager.add_parser("sample",i,'netperf-loop-tcp',DODNetperf)
for i in ['netperf-peer-loop-udp','netperf-peer-loop6-udp']:
    parserManager.add_parser("sample",i,'netperf-loop-udp',DODNetperf)
