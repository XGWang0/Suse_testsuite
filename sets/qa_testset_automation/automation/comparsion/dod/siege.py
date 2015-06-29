#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pprint
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

IO_PATTERN = ('Transaction rate', 'Throughput')
class DODSiege(DODLog):
    def __init__(self, stream):
        super(DODSiege, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'

        for i in IO_PATTERN:
            self._dod[i]=DictOfDict()

    def parser(self):
        rate = []
        throughput = [] 
        if self.ST == PST_NULL or self.ST== PST_START:
            for line in self.stream:
                tmatch = re.match(r'Transaction rate:\s*(\d*.\d*)',line)
                vmatch = re.match(r'Throughput:\s*(\d*\.\d*)',line)
                if tmatch:
                    rate.append(float(tmatch.group(1)))
                    continue
                elif vmatch:
                    throughput.append(float(vmatch.group(1)))
                else:
                    pass
        if len(rate) !=0 and len(throughput) !=0:
           rsum = sum(rate)/len(rate)
           vsum = sum (throughput)/len(throughput)
           self._dod[IO_PATTERN[0]]=float(rsum)
           self._dod[IO_PATTERN[1]]=float(vsum)

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()


