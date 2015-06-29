#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pprint
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

class DODSysbencholtp(DODLog):
    def __init__(self, stream):
        super(DODSysbencholtp, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'

    def parser(self):
        if self.ST == PST_NULL :
            thread = []
            value = []
            for line in self.stream:
                tmatch = re.match(r'Number of threads:\s*(\d)',line)
                vmatch = re.match(r'\s*total\s*time\:\s*(\d*\.?\d*)',line)
                if tmatch:
                    thread.append('thread num '+tmatch.group(1))
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

