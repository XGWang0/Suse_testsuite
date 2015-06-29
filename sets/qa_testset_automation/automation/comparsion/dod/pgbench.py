#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pdb
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)
IO_PATTERN = ('arg', 'tps')

class DODPgbench(DODLog):
    def __init__(self, stream):
        super(DODPgbench, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'

    def parser(self):
        if self.ST == PST_NULL:
            arg =""
            for line in self.stream:
                m = re.match(r'transaction\s*type', line)
                if m:
                    arg =""
                    arg +=(line.split(':'))[1].strip()+'-'
                    line = next(self.stream)
                    arg +=(line.split())[1]+(line.split())[2]+'-'
                    line = next(self.stream)
                    arg +=(line.split())[1]+(line.split())[2]+'-'
                    line = next(self.stream)
                    arg +=(line.split())[2]+(line.split())[3]+'-'
                    line = next(self.stream)
                    arg +=(line.split())[2]+(line.split())[3]+'-'
                    line = next(self.stream)
                    arg +=(line.split())[4]+(line.split())[5]+'-'
                    line = next(self.stream)
                    arg +=(line.split())[4]+(line.split())[5]
                else:
                    s = re.match(r'^tps = (\d+\.?\d*).*including', line)
                    if s:
                        tps = float(s.group(1))
                        self._dod[arg]=tps


    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()

