#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pprint
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

class DODNetperf(DODLog):
    def __init__(self, stream):
        super(DODNetperf, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'

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


