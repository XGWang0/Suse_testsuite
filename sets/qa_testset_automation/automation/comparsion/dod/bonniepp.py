#!/usr/bin/env python3

import sys
import os
import re

from dod import *
from common import *
import pprint
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)
IO_PATTERN=('Sequential Output','Sequential Input','Random','Sequential Create','Random Create')
IO_OPERATION=('Per Chr','Block','Rewrite','Seeks','Create','Read','Delete')
class DODBonniepp(DODLog):
    def __init__(self, stream):
        super(DODBonniepp, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 's'
        for i in IO_PATTERN:
            self._dod[i] = DictOfDict()

    def parser(self):
        for line in self.stream:
            r = line.split(',')
            if len(r) > 24 :
                self._dod[IO_PATTERN[0]]=DictOfDict({IO_OPERATION[0]:int(r[2]),IO_OPERATION[1]:int(r[4]),IO_OPERATION[2]:int(r[6])})
                self._dod[IO_PATTERN[1]]=DictOfDict({IO_OPERATION[0]:int(r[8]),IO_OPERATION[1]:int(r[10])})
                self._dod[IO_PATTERN[2]] = DictOfDict({IO_OPERATION[3]:float(r[12])}) 
                self._dod[IO_PATTERN[3]]=DictOfDict({IO_OPERATION[4]:int(r[15]),IO_OPERATION[5]:int(r[17]),IO_OPERATION[6]:int(r[19])})
                self._dod[IO_PATTERN]=DictOfDict({IO_OPERATION[4]:int(r[21]),IO_OPERATION[5]:int(r[23]),IO_OPERATION[6]:int(r[25])})

    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()


