#!/usr/bin/env python3

import sys
import os
import re
from dod import *
from common import *
import parserManager
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)

IO_PATTERN = ('Elapsed_Time', 'User_Time','System_Time','Percent_CPU','Context_Switches','Sleeps')
class DODKernbench(DODLog):
    def __init__(self, stream):
        super(DODKernbench, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'

    def parser(self):
        if self.ST == PST_NULL:
            for line in self.stream:
                match = re.match(r'Average\s.*\sload\s-j\s*(\d*)',line)
                if match:
                   nrun = match.group(1)
                   self._dod[nrun] = self.getvalue(nrun)

    def getvalue(self,nrun):
        v_tree = DictOfDict()
        for i in range(5):
            line = next(self.stream)
            vs =(line.strip().split())[2]
            v_tree[IO_PATTERN[i]] =float(vs)
        line = next(self.stream)
        vs =(line.strip().split())[1]
        v_tree[IO_PATTERN[5]] =float(vs)
        return v_tree


    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()

parserManager.add_parser("sample",
                         "kernbench",
                         "kernbench",
                         DODKernbench)

parserManager.add_parser("sample",
                         "kernbench_fast",
                         "kernbench",
                         DODKernbench)
