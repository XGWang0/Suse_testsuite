#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

IO_PATTERN = ('Num Forked', 'Jobs per Minute')
class DODReaim(DODLog):
    def __init__(self, stream):
        super(DODReaim, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'
        
    def parser(self):
        if self.ST == PST_NULL:
            for line in self.stream:
                match = re.match(r'(\d+)\s*(\d+\.?\d*\s*){8}',line)
                if match:
                    result = line.strip().split()
                    self._dod[result[0]] = float(result[4])

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()


