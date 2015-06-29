#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pprint
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

IO_PATTERN = ('Thread', 'Throughput')
class DODDbench(DODLog):
    def __init__(self, stream):
        super(DODDbench, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'        
        for i in IO_PATTERN:
            self._dod[i]=DictOfDict()

    def parser(self):
        thread = []
        value = [] 
        if self.ST == PST_NULL or self.ST== PST_START:
            for line in self.stream:
                tmatch = re.match(r'^dbench\s*\-[a-z]\s*\d*\s*\-[A-Z]\s*\/[a-z]*\s*(\d*)',line)
                vmatch = re.match(r'^Throughput+\s*(\d*\.?\d*)',line)
                if tmatch:
                    thread.append(tmatch.group(1))
                    continue
                elif vmatch:
                    value.append(vmatch.group(1))
                else:
                    pass
        if len(thread) ==len(value):
            for i in range(len(thread)):
                self._dod[thread[i]]=float(value[i])

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()


