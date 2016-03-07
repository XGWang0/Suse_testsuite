#!/usr/bin/env python3

import sys
import os
import re
import parserManager
from dod import *
from common import *
import logging

PST_NULL, PST_START, PST_DONE, PST_FAILED = range(0, 4)
IO_PATTERN = ('arg', 'tps')

class DODPgbench(DODLog):
    def __init__(self, stream):
        super(DODPgbench, self).__init__(stream)
        self.ST = PST_NULL
        self._dod.standard = 'b'

    def parser(self):
        if self.ST == PST_NULL:
            arg =""
            for line in self.stream:
                m = re.match(r'transaction\s*type', line)
                if m:
                    arg =""
                    arg +=(line.split(':'))[1].strip()+'-'
                    line = next(self.stream)
                    #arg +=(line.split())[1]+(line.split())[2]+'-'
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
                    if s :
                        t=s.group(1)
                        if not t:
                            tps = 0
                        else:
                            tps = float(t)
                        self._dod[arg]=tps


    def __getattr__(self, name):
        if name == 'dod':
            if self.ST == PST_NULL:
                self.parser()
            return self._dod
        raise AttributeError()

tl = ['pgbench_small_ro_ext3','pgbench_small_ro_xfs','pgbench_small_ro_btrfs','pgbench_small_ro_ext4']

for i in tl:
    parserManager.add_parser("sample",i,"pgbench-small-ro",DODPgbench)

rl = ['pgbench_small_rw_ext3','pgbench_small_rw_xfs','pgbench_small_rw_btrfs','pgbench_small_rw_ext4']

for i in rl:
    parserManager.add_parser("sample",i,"pgbench-small-rw",DODPgbench)

otl = ['pgbench_small_ro_osync_ext3','pgbench_small_ro_osync_xfs','pgbench_small_ro_osync_btrfs','pgbench_small_ro_osync_ext4']

for i in otl:
    parserManager.add_parser("sample",i,"pgbench-small-ro-osync",DODPgbench)

orl = ['pgbench_small_rw_osync_ext3','pgbench_small_rw_osync_xfs','pgbench_small_rw_osync_btrfs','pgbench_small_rw_osync_ext4']

for i in orl:
    parserManager.add_parser("sample",i,"pgbench-small-rw_osync",DODPgbench)
